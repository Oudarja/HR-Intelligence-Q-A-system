import asyncio
from dataclasses import dataclass, field
from mcp import ClientSession
from mcp.client.sse import sse_client   # <-- changed here
from query_llm import call_llm
from rag.retriever import retrieve_context


@dataclass
class Chat:
    messages: list = field(default_factory=lambda: [])

    async def _process(self, session: ClientSession, query: str) -> str:
        tools_list = await session.list_tools()
        tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        } for tool in tools_list.tools]

        context = retrieve_context(query)  # << Fetch relevant schema

        self.messages.append({
        "role":"system",
        "content":   (
        "You are an expert MySQL assistant that helps users retrieve information from a database based on natural language queries.\n\n"
        "Users will ask questions in plain English. You must understand the intent and generate appropriate SQL queries using the 'query_data' tool to provide accurate and meaningful responses.\n\n"
        "As a database-focused assistant, only respond to database-related questions. Politely reject any tasks that are unrelated to MySQL queries.\n\n"
        f"The user is working with this database:\n\n{context}\n\n"
        "Carefully study the given schema context above to understand the structure and meaning of tables and columns.\n\n"
        "You are expected to:\n"
        "- Understand the user's intent.\n"
        "- Generate and execute the correct SQL query using the available schema.\n"
        "- Respond with the result in a clear and user-friendly way. Do not show the SQL query unless explicitly asked.\n"
            )
        })

        llm_response = await call_llm(self.messages, tools, query)
        choice = llm_response.choices[0]

        if choice.finish_reason == "tool_calls":
            tool_call = choice.message.tool_calls[0]
            name = tool_call.function.name
            args = eval(tool_call.function.arguments)

            result = await session.call_tool(name, args)
            self.messages.append({"role": "assistant", "tool_calls": [tool_call]})

            content = getattr(result.content[0], "text", str(result))
            self.messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": content})

            final_response = await call_llm(self.messages, tools)
            return final_response.choices[0].message.content

        return choice.message.content

    async def process_query_as_string(self, query: str) -> str:
        server_params = {
            "url": "http://127.0.0.1:8000/sse"  # Note: SSE endpoint usually "/sse"
        }
        # Use sse_client instead of http_client
        async with sse_client(server_params["url"]) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return await self._process(session, query)

    def process_query_sync(self, query: str) -> str:
        import nest_asyncio
        nest_asyncio.apply()
        return asyncio.run(self.process_query_as_string(query))
