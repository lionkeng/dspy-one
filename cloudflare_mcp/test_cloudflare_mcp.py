#!/usr/bin/env python3
"""Test script for the overhauled CloudflareModule with rich formatting"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from cloudflare_mcp.module import CloudflareMCPModule


def test_cloudflare_module():
    """Test the CloudflareModule functionality with rich formatting"""
    module = CloudflareMCPModule()

    try:
        # Test simple queries using the idiomatic DSPy forward method
        test_queries = [
            "What is Cloudflare Workers?",
            "How do I deploy a Worker?",
            "What programming languages are supported?",
        ]

        module.formatter.format_info(
            "Testing CloudflareMCP module with idiomatic DSPy approach...",
            "🧪 Test Started",
        )

        for i, query in enumerate(test_queries, 1):
            module.formatter.format_info(
                f"Test {i}/{len(test_queries)}: {query}", "🔍 Testing Query"
            )

            # Test the DSPy forward method
            prediction = module(query)

            # Display the result
            module.formatter.console.print()
            module.formatter.console.print(
                f"[bold cyan]Q:[/bold cyan] {query}\n"
                f"[bold green]A:[/bold green] {prediction.answer}"
            )
            module.formatter.console.print()

            module.formatter.format_success("Query completed successfully!")

            if i < len(test_queries):
                print()  # Add spacing between tests

        # Test another DSPy query
        module.formatter.format_info(
            "Testing additional DSPy query...", "🎯 DSPy Integration Test"
        )
        prediction = module("What are the Workers runtime limits?")

        # Display the result
        module.formatter.console.print()
        module.formatter.console.print(
            f"[bold cyan]Q:[/bold cyan] What are the Workers runtime limits?\n"
            f"[bold green]A:[/bold green] {prediction.answer}"
        )
        module.formatter.console.print()

        module.formatter.format_success("All tests completed successfully!")

    except Exception as e:
        module.formatter.format_error(f"Error during testing: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Run the test with rich formatting"""
    test_cloudflare_module()


if __name__ == "__main__":
    main()
