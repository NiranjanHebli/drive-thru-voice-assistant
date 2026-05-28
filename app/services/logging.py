import sqlite3
from datetime import datetime
import json


class InteractionLogger:
    def __init__(self, db_path="app/data/training_logs.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    session_id TEXT,
                    user_input TEXT,
                    tool_call TEXT,
                    tool_result TEXT,
                    ai_response TEXT,
                    is_correction BOOLEAN DEFAULT 0
                )
            """
            )

    def log_turn(
        self, session_id, user_input, tool_call=None, tool_result=None, ai_response=None
    ):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO logs (timestamp, session_id, user_input, tool_call, tool_result, ai_response)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    session_id,
                    user_input,
                    json.dumps(tool_call) if tool_call else None,
                    json.dumps(tool_result) if tool_result else None,
                    ai_response,
                ),
            )
