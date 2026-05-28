import json
from app.core.prompt import get_system_prompt
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
        self,
        session_id: str,
        user_input: str,
        cart_state: list,
        chat_history: list = None,
    ) -> str:
        """
        Main execution loop for a single conversation turn.
        """
        if chat_history is None:
            chat_history = []

        # Early payment intent detection – bypass LLM if user explicitly wants to pay
        payment_phrases = [
            "please proceed to payment",
            "please proceed",
            "pay now",
            "checkout",
            "proceed to payment",
            "no please please proceed",
            "pay",
            "that's it",
            "that is it",
            "that's all",
            "that is all",
            "nothing else",
            "i am done",
            "i'm done",
            "done ordering",
        ]
        lowered = user_input.lower()
        if any(p in lowered for p in payment_phrases):
            # Directly invoke checkout tool and return a friendly confirmation
            result = await self.tools.execute(
                {"name": "checkout", "arguments": "{}"}, cart_state
            )
            if result.get("success"):
                return f"Order complete. Your total is ₹{result.get('total')}. Please drive to the next window!"
            else:
                return result.get("message", "Unable to process payment at this time.")

        # 1. Calculate time of day for Lisa's greeting
        from datetime import datetime

        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "morning"
        elif 12 <= hour < 17:
            greeting = "afternoon"
        else:
            greeting = "evening"

        # 2. Prepare conversation history with the Master System Prompt
        messages = [{"role": "system", "content": get_system_prompt(greeting)}]

        # Append recent chat history (last 10 messages to save context limit, format the transcript markers)
        for msg in chat_history[-10:]:
            clean_content = msg["content"].replace("🗣️ [Transcribed]: ", "")
            messages.append({"role": msg["role"], "content": clean_content})

        # If the latest user_input isn't already the last message in the history, append it
        if (
            not messages
            or messages[-1]["role"] != "user"
            or messages[-1]["content"] != user_input
        ):
            messages.append({"role": "user", "content": user_input})

        # 2. First Pass: Get intent from Llama-3 (check for tool calls)
        response_data = await self.llm_client.generate(messages, tools=TOOLS)
        if not response_data:
            return (
                "I'm having a bit of trouble with my connection. Could you repeat that?"
            )

        message = response_data["choices"][0]["message"]

        # Guard: if LLM returns neither text nor tool calls, fallback gracefully
        if not message.get("content") and not message.get("tool_calls"):
            return (
                "I'm having a bit of trouble with my connection. Could you repeat that?"
            )

        if "tool_calls" in message and message["tool_calls"]:
            messages.append(message)  # Append the assistant message once

            for tool_call in message["tool_calls"]:
                tool_data = tool_call["function"]
                name = tool_data["name"]
                print(f"DEBUG: Tool called -> {name}")
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

                # Append the tool result back to the LLM to confirm to the user
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": name,
                        "content": json.dumps(result),
                    }
                )

            # --- SECOND PASS: Final Response Generation ---
            final_response = await self.llm_client.generate(messages)
            if final_response:
                return final_response["choices"][0]["message"]["content"]
            return "Got it!"

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
