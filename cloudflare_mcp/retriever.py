import asyncio
import dspy

from mcp import ClientSession
from mcp.client.sse import sse_client

from .formatter import MCPResultFormatter


class MCPRetriever(dspy.Module):
    """DSPy module that handles MCP-based retrieval"""

    def __init__(self, server_url="https://docs.mcp.cloudflare.com/sse"):
        super().__init__()
        self.server_url = server_url
        self.formatter = MCPResultFormatter()

    def forward(self, question):
        """Retrieve documentation passages using MCP"""
        try:
            # Run async retrieval in sync context
            raw_results = asyncio.run(self._async_retrieve(question))
            # Parse and clean the results
            cleaned_results = self._parse_results(raw_results)
            return dspy.Prediction(passages=cleaned_results)
        except Exception as e:
            error_msg = f"MCP retrieval failed: {str(e)}"
            return dspy.Prediction(passages=error_msg)

    async def _async_retrieve(self, question):
        """Async MCP retrieval implementation"""
        async with sse_client(url=self.server_url) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()

                # Get available tools
                response = await session.list_tools()
                tools = response.tools

                if not tools:
                    return "No tools available from MCP server"

                # Use the first available tool
                tool = tools[0]
                tool_name = tool.name

                # Prepare arguments
                arguments = self._prepare_arguments(tool, question)

                # Call the MCP tool
                result = await session.call_tool(tool_name, arguments)

                # Extract content
                return self._extract_content(result)

    def _prepare_arguments(self, tool, question):
        """Prepare arguments for MCP tool call"""
        arguments = {}
        if hasattr(tool, "inputSchema") and tool.inputSchema:
            properties = tool.inputSchema.get("properties", {})
            for prop_name in properties:
                if prop_name in ["query", "question", "search", "q"]:
                    arguments[prop_name] = question
                    break
            else:
                required = tool.inputSchema.get("required", [])
                if required:
                    arguments[required[0]] = question
                else:
                    arguments["query"] = question
        else:
            arguments["query"] = question
        return arguments

    def _extract_content(self, result):
        """Extract content from MCP result"""
        if hasattr(result, "content"):
            if isinstance(result.content, list):
                content_parts = []
                for item in result.content:
                    if hasattr(item, "text"):
                        content_parts.append(item.text)
                    elif hasattr(item, "content"):
                        content_parts.append(item.content)
                    else:
                        content_parts.append(str(item))
                return "\n".join(content_parts)
            elif hasattr(result.content, "text"):
                return result.content.text
            else:
                return str(result.content)
        else:
            return str(result)

    def _parse_results(self, raw_result):
        """Parse and clean MCP results"""
        results = self.formatter.parse_results(raw_result)

        if not results:
            return "No results found."

        parsed_content = []
        for i, result in enumerate(results, 1):
            url = result["url"]
            text = result["text"]
            cleaned_text = self.formatter._clean_markdown_text(text)
            parsed_content.append(f"Source {i}: {url}\n{cleaned_text}\n")

        return "\n---\n".join(parsed_content)
