#!/usr/bin/env python3
"""Demo script to showcase rich formatting with a simple query"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from cloudflare_mcp.module import CloudflareMCPModule


def demo_rich_formatting():
    """Demo the rich formatting with a single comprehensive query"""
    module = CloudflareMCPModule()

    try:
        # Demo query using idiomatic DSPy approach
        query = "What is Cloudflare Workers?"
        module.formatter.format_info(f"Demo Query: {query}", "🌟 Rich Formatting Demo")

        # Use DSPy forward method
        prediction = module(query)

        # Display the result with formatting
        module.formatter.console.print()
        module.formatter.console.print(
            f"[bold cyan]Q:[/bold cyan] {query}\n"
            f"[bold green]A:[/bold green] {prediction.answer}"
        )
        module.formatter.console.print()

        module.formatter.format_success("Demo completed! 🎉")

    except Exception as e:
        module.formatter.format_error(f"Demo failed: {e}")


def main():
    """Run the demo"""
    demo_rich_formatting()


if __name__ == "__main__":
    main()
