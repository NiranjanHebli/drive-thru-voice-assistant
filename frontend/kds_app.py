import streamlit as st
import time

st.set_page_config(page_title="Kitchen Display System", page_icon="🍳", layout="wide")

st.title("🍳 Kitchen Display System (KDS)")
st.markdown("Live orders processed by the AI Drive-Thru Agent.")

# Mock data for demonstration purposes since active state is ephemeral in this demo
if "orders" not in st.session_state:
    st.session_state.orders = [
        {
            "id": 101,
            "items": ["Maharaja Mac", "Medium Fries", "Coke"],
            "status": "Pending",
            "time": "2 mins ago",
        },
        {
            "id": 102,
            "items": ["McAloo Tikki", "Cold Coffee"],
            "status": "Preparing",
            "time": "5 mins ago",
        },
    ]


def complete_order(order_id):
    for order in st.session_state.orders:
        if order["id"] == order_id:
            order["status"] = "Ready"


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔴 Pending")
    for order in st.session_state.orders:
        if order["status"] == "Pending":
            with st.container(border=True):
                st.write(f"**Order #{order['id']}** ({order['time']})")
                for item in order["items"]:
                    st.write(f"- {item}")
                if st.button("Start Preparing", key=f"prep_{order['id']}"):
                    order["status"] = "Preparing"
                    st.rerun()

with col2:
    st.subheader("🟡 Preparing")
    for order in st.session_state.orders:
        if order["status"] == "Preparing":
            with st.container(border=True):
                st.write(f"**Order #{order['id']}** ({order['time']})")
                for item in order["items"]:
                    st.write(f"- {item}")
                if st.button("Mark Ready", key=f"ready_{order['id']}"):
                    complete_order(order["id"])
                    st.rerun()

with col3:
    st.subheader("🟢 Ready for Pickup")
    for order in st.session_state.orders:
        if order["status"] == "Ready":
            with st.container(border=True):
                st.write(f"**Order #{order['id']}**")
                st.success("Ready to hand to customer")
                if st.button("Clear Order", key=f"clear_{order['id']}"):
                    st.session_state.orders.remove(order)
                    st.rerun()
