#!/bin/bash

# run_all_demos.sh - Run all Cloudflare MCP demos and tests

set -e  # Exit on any error

echo "🚀 Running All Cloudflare MCP Demos and Tests"
echo "=============================================="
echo

# Function to run a demo with nice formatting
run_demo() {
    local script_path="$1"
    local demo_name="$2"
    
    echo "📋 Running: $demo_name"
    echo "   Script: $script_path"
    echo "   Command: uv run python $script_path"
    echo "----------------------------------------"
    
    if uv run python "$script_path"; then
        echo "✅ $demo_name completed successfully"
    else
        echo "❌ $demo_name failed"
        exit 1
    fi
    
    echo
    echo "=========================================="
    echo
}

# Run all demos
run_demo "demo/demo_rich_formatting.py" "Rich Formatting Demo"
run_demo "demo/demo_dspy_summarization.py" "DSPy Summarization Demo"
run_demo "demo/demo_clean_summary.py" "Clean Summary Demo"
run_demo "demo/dspy_prediction_demo.py" "DSPy Prediction Demo"

# Run test script
run_demo "cloudflare_mcp/test_cloudflare_mcp.py" "Cloudflare MCP Test Suite"

echo "🎉 All demos and tests completed successfully!"
echo "==============================================" 