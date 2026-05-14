import json
from app.core.prompt import SYSTEM_PROMPT
from app.models.tool_definition import TOOLS
from app.core.tool_registry import ToolRegistry
from app.core.local_llm_client import LocalLLMClient
from app.core.validator import OrderValidator
from app.services.logging import InteractionLogger


class DialogueManager:
    def __init__(self):
        # Initialize modular components
        self.llm_client = LocalLLMClient()
        self.tools = ToolRegistry()
        self.validator = OrderValidator()
        self.logger = InteractionLogger()

    async def process_turn(
        self, session_id: str, user_input: str, cart_state: list
    ) -> str:
        """
        Main execution loop for a single conversation turn.
        """
        # 1. Prepare conversation history with the Master System Prompt
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]

        # 2. First Pass: Get intent from Llama-3 (check for tool calls)
        response_data = await self.llm_client.generate(messages, tools=TOOLS)
        if not response_data:
            return (
                "I'm having a bit of trouble with my connection. Could you repeat that?"
            )

        message = response_data["choices"][0]["message"]

        # 3. Check for Tool Calls (e.g., adding to cart)
        if "tool_calls" in message and message["tool_calls"]:
            for tool_call in message["tool_calls"]:
                tool_data = tool_call["function"]
                name = tool_data["name"]
                args = json.loads(tool_data.get("arguments", "{}"))

                # --- VALIDATION LAYER ---
                if name == "add_to_cart":
                    # Cross-reference with order_details.json before execution
                    validation = self.validator.validate_add_to_cart(
                        args.get("item_id"), args.get("modifiers")
                    )

                    if not validation["valid"]:
                        # If invalid, inform the LLM of the specific menu error
                        return await self._handle_logic_error(
                            messages, message, tool_call["id"], validation["message"]
                        )

                # --- EXECUTION LAYER ---
                # Execute valid tool and update Valkey state
                result = await self.tools.execute(tool_data, cart_state)

                # Log the interaction for future fine-tuning[cite: 1]
                self.logger.log_turn(
                    session_id, user_input, tool_call=tool_data, tool_result=result
                )

                # --- SECOND PASS: Final Response Generation ---
                # Provide the tool result back to the LLM to confirm to the user
                messages.append(message)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": name,
                        "content": json.dumps(result),
                    }
                )

                final_response = await self.llm_client.generate(messages)
                return final_response["choices"][0]["message"]["content"]

        # 4. Fallback: If no tool was called, log the text-only interaction
        ai_text = message.get("content", "I'm sorry, could you say that again?")
        self.logger.log_turn(session_id, user_input, ai_response=ai_text)
        return ai_text

    async def _handle_logic_error(self, messages, original_msg, call_id, error_msg):
        """
        Internal helper to feed a validation error back to the AI
        so it can explain the issue to the customer[cite: 1].
        """
        messages.append(original_msg)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": call_id,
                "content": json.dumps({"success": False, "error": error_msg}),
            }
        )

        # Ask the LLM to generate a helpful apology/explanation
        correction_res = await self.llm_client.generate(messages)
        return correction_res["choices"][0]["message"]["content"]
