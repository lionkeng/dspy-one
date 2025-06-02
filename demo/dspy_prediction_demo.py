#!/usr/bin/env python3
"""Expanded demo showing all aspects of CloudflareMCPModule predictions"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from cloudflare_mcp.main import CloudflareMCPModule

import dspy


def demo_dspy_prediction():
    """Demonstrate dspy.Prediction usage and structure"""

    print("=== DSPy Prediction Demo ===\n")

    # 1. Basic Prediction with single field
    print("1. Basic Prediction:")
    basic_pred = dspy.Prediction(answer="Cloudflare Workers is a serverless platform")
    print(f"   Type: {type(basic_pred)}")
    print(f"   Answer: {basic_pred.answer}")
    print(f"   String representation: {basic_pred}")
    print()

    # 2. Prediction with multiple fields
    print("2. Multi-field Prediction:")
    multi_pred = dspy.Prediction(
        answer="Cloudflare Workers is a serverless platform",
        confidence=0.95,
        source="MCP Documentation",
        reasoning="Based on official Cloudflare documentation",
    )
    print(f"   Answer: {multi_pred.answer}")
    print(f"   Confidence: {multi_pred.confidence}")
    print(f"   Source: {multi_pred.source}")
    print(f"   Reasoning: {multi_pred.reasoning}")
    print()

    # 3. Accessing fields
    print("3. Field Access:")
    print(f"   Direct access: {multi_pred.answer}")
    print(f"   Has 'answer' field: {hasattr(multi_pred, 'answer')}")
    print(f"   Has 'nonexistent' field: {hasattr(multi_pred, 'nonexistent')}")
    print()

    # 4. Converting to dictionary
    print("4. Dictionary representation:")
    pred_dict = dict(multi_pred)
    print(f"   As dict: {pred_dict}")
    print()

    # 5. What happens in our CloudflareModule
    print("5. In CloudflareModule context:")
    mcp_result = (
        "<result><url>https://example.com</url><text>Workers info...</text></result>"
    )
    cloudflare_pred = dspy.Prediction(answer=mcp_result)
    print(f"   Raw MCP result stored in 'answer' field")
    print(f"   Prediction type: {type(cloudflare_pred)}")
    print(f"   Can be used by DSPy optimizers: Yes")
    print(f"   Can be chained with other modules: Yes")
    print()

    # 6. Why use Prediction instead of plain strings?
    print("6. Why dspy.Prediction vs plain strings?")
    print("   ✅ Structured: Named fields for different types of output")
    print("   ✅ DSPy Integration: Works with DSPy's optimization framework")
    print("   ✅ Extensible: Can add metadata, confidence scores, reasoning")
    print("   ✅ Type Safety: Clear interface for module outputs")
    print("   ✅ Composability: Easy to chain multiple modules together")


if __name__ == "__main__":
    demo_dspy_prediction()
