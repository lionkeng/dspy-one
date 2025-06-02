#!/usr/bin/env python3
"""Demo script to test DSPy-powered summarization of Cloudflare documentation"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from cloudflare_mcp.module import CloudflareMCPModule


def demo_dspy_summarization():
    """Demo the DSPy summarization with real MCP results"""
    module = CloudflareMCPModule()

    try:
        # Test questions that should benefit from summarization
        test_questions = [
            "What is Cloudflare Workers and how does it work?",
            "How do I deploy and manage Workers?",
            "What are the security features of Workers?",
        ]

        for i, question in enumerate(test_questions, 1):
            module.formatter.format_info(
                f"Demo {i}/{len(test_questions)}: {question}",
                "🧪 DSPy Summarization Test",
            )

            # Use idiomatic DSPy forward method
            prediction = module(question)

            # Display the result
            module.formatter.console.print()
            module.formatter.console.print(
                f"[bold cyan]Q:[/bold cyan] {question}\n"
                f"[bold green]A:[/bold green] {prediction.answer}"
            )
            module.formatter.console.print()

            module.formatter.format_success(f"Test {i} completed!")

            if i < len(test_questions):
                print("\n" + "=" * 80 + "\n")  # Separator between tests

        module.formatter.format_success("All DSPy summarization tests completed! 🎉")

    except Exception as e:
        module.formatter.format_error(f"Demo failed: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Run the DSPy summarization demo"""
    demo_dspy_summarization()


if __name__ == "__main__":
    main()
