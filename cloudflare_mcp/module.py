import dspy

from qa_common.main import initialize_dspy
from .formatter import MCPResultFormatter
from .retriever import MCPRetriever
from .summarization import SummarizeDocumentation


class CloudflareMCPModule(dspy.Module):
    """Main DSPy module for Cloudflare documentation Q&A with MCP"""

    def __init__(self):
        super().__init__()
        self.formatter = MCPResultFormatter()

        # Configure DSPy using qa_common's initialize_dspy
        try:
            initialize_dspy()
            self.formatter.format_success("✅ Configured DSPy with OpenAI")
        except ValueError as e:
            self.formatter.format_error(f"❌ {e}")
            self.formatter.format_info("Continuing with fallback summarization mode.")

        # DSPy modules - idiomatic composition
        self.retrieve = MCPRetriever()
        self.summarize = dspy.ChainOfThought(SummarizeDocumentation)

    def forward(self, question):
        """DSPy forward method - clean and idiomatic"""
        # Step 1: Retrieve relevant passages
        retrieval_result = self.retrieve(question)

        # Step 2: Summarize using DSPy
        try:
            summary_result = self.summarize(
                question=question, search_results=retrieval_result.passages
            )
            return summary_result
        except Exception:
            # Fallback to simple summarization
            fallback_answer = self._fallback_summary(
                question, retrieval_result.passages
            )
            return dspy.Prediction(answer=fallback_answer)

    def _fallback_summary(self, question, passages):
        """Simple fallback when DSPy summarization fails"""
        if "No results found" in passages or "MCP retrieval failed" in passages:
            return f"No specific information found about '{question}' in the documentation."

        # Extract first few lines as simple summary
        lines = passages.split("\n")[:10]  # First 10 lines
        summary_lines = [
            line for line in lines if line.strip() and not line.startswith("Source")
        ]

        if summary_lines:
            summary = " ".join(summary_lines[:3])  # First 3 meaningful lines
            if len(summary) > 200:
                summary = summary[:200] + "..."
            return f"Based on the documentation: {summary}"
        else:
            return f"Found documentation about '{question}' but unable to summarize."

    def summarize_document(self, index: int):
        """Placeholder for document summarization - required by QA loop"""
        return dspy.Prediction(
            summary="Document summarization not supported by this MCP server"
        )
