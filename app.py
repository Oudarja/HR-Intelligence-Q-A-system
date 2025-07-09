import streamlit as st
from mcp_client import Chat
import traceback

chat_agent = Chat()
st.set_page_config(page_title="MySQL LLM Agent")
st.title("MySQL Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask your database something:")
    submitted = st.form_submit_button("Ask")
    if submitted and user_input.strip():
        try:
            with st.spinner("Thinking..."):
                response = chat_agent.process_query_sync(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Agent", response))
        except Exception:
            st.error("Something went wrong.")
            st.code(traceback.format_exc(), language="python")

st.markdown("### Chat History")
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
