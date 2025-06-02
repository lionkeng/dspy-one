from fastmcp import FastMCP
import traceback

server = FastMCP("Echo Server")


@server.tool()
def echo(query: str) -> dict:
    """Echoes the input query as a dict with a 'content' key."""
    return {"content": query}


def main():
    """Main entry point for the echo server."""
    # Run the server with SSE enabled
    try:
        server.run(transport="sse", port=8000)
    except Exception as exc:
        print(f"DEBUG: Exception in forward: {exc!r}")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
