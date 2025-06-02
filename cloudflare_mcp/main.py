from qa_common.main import initialize_dspy, run_qa_loop
from .module import CloudflareMCPModule


def main():
    """Main function to run the QA loop"""
    try:
        console = initialize_dspy()
    except ValueError as e:
        print(f"Error initializing DSPy: {e}")
        return

    # Create the module
    module = CloudflareMCPModule()

    # Welcome message with rich formatting
    module.formatter.format_info(
        "This system searches Cloudflare documentation and provides AI-powered summaries.\nType 'exit' to quit.",
        "🚀 Cloudflare MCP QA System",
    )

    # Run the QA loop - let it handle display naturally
    run_qa_loop(module, None, console, app_name="Cloudflare MCP QA")


if __name__ == "__main__":
    main()
