import sqlite3
import json
import os


def export_to_jsonl(
    db_path="app/data/training_logs.db", output_path="app/data/finetune_dataset.jsonl"
):
    """
    Exports SQLite interaction logs to a JSONL format suitable for LoRA/QLoRA fine-tuning.
    """
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Select successful/corrected interactions to build a high-quality dataset
        cursor.execute("SELECT user_input, tool_call, ai_response FROM logs")
        rows = cursor.fetchall()

    with open(output_path, "w", encoding="utf-8") as f:
        for row in rows:
            # Create a conversation format for Llama-3 instruction tuning
            messages = [
                {
                    "role": "system",
                    "content": "You are an elite Drive-Thru Agent for an Indian QSR.",
                },
                {"role": "user", "content": row["user_input"]},
            ]

            # If there was a tool call, include it in the assistant's response format
            if row["tool_call"]:
                messages.append(
                    {"role": "assistant", "tool_calls": [json.loads(row["tool_call"])]}
                )
            else:
                messages.append(
                    {
                        "role": "assistant",
                        "content": row["ai_response"] if row["ai_response"] else "",
                    }
                )

            # Write JSON object per line
            f.write(json.dumps({"messages": messages}) + "\n")

    print(f"Exported {len(rows)} interactions to {output_path}")


if __name__ == "__main__":
    export_to_jsonl()
