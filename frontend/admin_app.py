import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(page_title="Drive-Thru Admin", page_icon="🍔", layout="wide")

st.title("🍔 Drive-Thru AI Admin Dashboard")
st.markdown("Monitor AI interactions and collect data for model fine-tuning.")

DB_PATH = "app/data/training_logs.db"


def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT id, timestamp, session_id, user_input, tool_call, ai_response FROM logs ORDER BY timestamp DESC LIMIT 100",
            conn,
        )
        conn.close()
        return df
    except sqlite3.OperationalError:
        return pd.DataFrame()


st.subheader("Recent Voice Interactions")
df = load_data()

if df.empty:
    st.info(
        "No interaction logs found. Try interacting with the Drive-Thru agent first."
    )
else:
    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logged Interactions", len(df))
    col2.metric("Tool Calls Made", df["tool_call"].notna().sum())
    col3.metric("Fine-Tuning Ready", "Yes")

    # Display Dataframe
    st.dataframe(
        df,
        column_config={
            "id": st.column_config.NumberColumn("ID", width="small"),
            "timestamp": st.column_config.DatetimeColumn(
                "Time", format="D MMM YYYY, h:mm a"
            ),
            "user_input": st.column_config.TextColumn("Customer Said", width="medium"),
            "tool_call": st.column_config.TextColumn("AI Tool Action", width="medium"),
            "ai_response": st.column_config.TextColumn("AI Spoke", width="medium"),
        },
        hide_index=True,
    )

st.sidebar.header("Export Data")
st.sidebar.markdown(
    "Export the logs to JSONL for LoRA/QLoRA Fine-tuning via `export_finetune_data.py`"
)
if st.sidebar.button("Run Export Script"):
    import subprocess

    result = subprocess.run(
        ["python", "app/scripts/export_finetune_data.py"],
        capture_output=True,
        text=True,
    )
    st.sidebar.success("Export successful!")
    st.sidebar.code(result.stdout)
