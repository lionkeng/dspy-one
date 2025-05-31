import dspy

# Import common components
from qa_common.main import (
    AnswerQuestion,
    SummarizeDoc,
    load_documents,
    base_simple_retrieve,
    initialize_dspy,
    run_qa_loop,
)


class DocQAModule(dspy.Module):
    def __init__(self, dataset):
        super().__init__()
        self.dataset = dataset
        # Use imported signatures
        self.answer = dspy.ChainOfThought(AnswerQuestion)
        self.summarize = dspy.Predict(SummarizeDoc)

    def forward(self, question):
        # Use imported base_simple_retrieve
        context = "\n".join(base_simple_retrieve(question, self.dataset))
        return self.answer(question=question, context=context)

    def summarize_document(self, index: int):
        # This method remains specific to this module if its logic is unique
        # or could be part of a base class if also common
        text = self.dataset[index]
        return self.summarize(document=text)


def main():
    try:
        console = initialize_dspy()
    except ValueError as e:
        # initialize_dspy now raises ValueError if OPENAI_API_KEY is not found
        # The function itself prints a message, so we can just return or re-raise
        return

    dataset = load_documents()
    module = DocQAModule(dataset)

    # Pass the app_name to the common loop
    run_qa_loop(
        module, dataset, console, app_name="Acme Homes Warranty Assistant (Basic QA)"
    )


if __name__ == "__main__":
    main()
