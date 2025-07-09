# query_llm.py
import os
from typing import Any
from groq import AsyncGroq
from dotenv import load_dotenv

from rag.retriever import retrieve_context

load_dotenv()
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def call_llm(messages: list[dict], tools: list[dict], query: str = "") -> dict[str, Any]:

    """
        This module serves as the interface between the user's natural language queries and the LLM (Large Language Model)
        used for generating SQL commands. It integrates with Retrieval-Augmented Generation (RAG) to provide schema-aware
        query generation for MySQL databases.
        Key Responsibilities:
        ---------------------
        1. Accepts conversational context and the latest user query.
        2. Optionally retrieves relevant MySQL schema context using a vector store (FAISS) via the RAG mechanism.
        3. Builds a well-structured prompt including system instructions, schema context, and user intent.
        4. Sends the prompt to the underlying LLM (e.g., via Groq API).
        5. Returns the LLM's structured response, which may include:
        - SQL queries to be executed by the MCP tool
        - Natural language answers if appropriate
        Functions:
        ----------
        - `call_llm(messages: List[dict], tools: List[dict], query: Optional[str] = None) -> OpenAIResponse`
        Builds the prompt and sends it to the LLM, returning the model's response object.
        Dependencies:
        -------------
        - `retriever.py` (RAG component): Used to fetch relevant database schema context.
        - LLM client (e.g., Groq) for actual language model interaction.
        - Messages and tools format conform to OpenAI's function calling (tool calling) specification.
    """
    if query:
        messages.append({"role": "user", "content": query})

    response = await groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response
