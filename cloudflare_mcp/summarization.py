import dspy


class SummarizeDocumentation(dspy.Signature):
    """Summarize technical documentation search results into a clear, helpful answer."""

    question = dspy.InputField(desc="The user's question")
    search_results = dspy.InputField(desc="Search results from documentation")
    answer = dspy.OutputField(
        desc="A clear, comprehensive answer based on the search results"
    )
