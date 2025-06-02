#!/usr/bin/env python3
"""Demo script to test clean DSPy summarization (no intermediate results)"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from cloudflare_mcp.module import CloudflareMCPModule


def demo_clean_summary():
    """Demo the clean summarization - only final answers"""
    module = CloudflareMCPModule()

    try:
        # Simple test question
        question = "What is Cloudflare Workers?"

        module.formatter.format_info(
            f"Testing clean summary for: {question}", "🧪 Clean Summary Demo"
        )

        # Use the idiomatic DSPy forward method
        prediction = module(question)

        # Display the result
        module.formatter.console.print()
        module.formatter.console.print(
            f"[bold cyan]Q:[/bold cyan] {question}\n"
            f"[bold green]A:[/bold green] {prediction.answer}"
        )
        module.formatter.console.print()

        module.formatter.format_success("Demo completed! 🎉")

    except Exception as e:
        module.formatter.format_error(f"Demo failed: {e}")


def main():
    """Run the clean summary demo"""
    demo_clean_summary()


if __name__ == "__main__":
    main()
