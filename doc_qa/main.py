import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import dspy


class AnswerQuestion(dspy.Signature):
    """Answer warranty questions using provided context."""

    question = dspy.InputField()
    context = dspy.InputField()
    answer = dspy.OutputField()


class SummarizeDoc(dspy.Signature):
    """Summarize a document."""

    document = dspy.InputField()
    summary = dspy.OutputField(desc="one paragraph")


class DocQAModule(dspy.Module):
    def __init__(self, dataset):
        super().__init__()
        self.dataset = dataset
        self.answer = dspy.ChainOfThought(AnswerQuestion)
        self.summarize = dspy.Predict(SummarizeDoc)

    def forward(self, question):
        context = "\n".join(simple_retrieve(question, self.dataset))
        return self.answer(question=question, context=context)

    def summarize_document(self, index: int):
        text = self.dataset[index]
        return self.summarize(document=text)


def simple_retrieve(query: str, dataset, k: int = 3):
    words = set(query.lower().split())
    scored = []
    for i, text in enumerate(dataset):
        doc_words = set(text.lower().split())
        score = len(words & doc_words)
        scored.append((score, i))
    top = sorted(scored, key=lambda x: x[0], reverse=True)[:k]
    return [dataset[i] for _, i in top]


def load_documents():
    docs_dir = Path(__file__).resolve().parent / "docs"
    texts = []
    for path in sorted(docs_dir.glob("*.txt")):
        texts.append(path.read_text())
    return texts


def main():
    load_dotenv()
    console = Console()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold red]OPENAI_API_KEY not found in .env file.[/bold red]")
        return

    lm = dspy.LM("openai/gpt-4o-mini", api_key=api_key)
    dspy.settings.configure(lm=lm)

    dataset = load_documents()
    module = DocQAModule(dataset)

    console.print("[bold green]Acme Homes Warranty Assistant[/bold green]")
    docs_list = "\n".join(
        f"{i+1}. {Path(p).name}"
        for i, p in enumerate(sorted((Path(__file__).parent / "docs").glob("*.txt")))
    )

    while True:
        prompt_text = Text("Choose [qa] question, [sum] summarize, or [exit]")
        action = Prompt.ask(prompt_text)
        if action.lower() == "exit":
            break
        if action.lower() == "qa":
            q = Prompt.ask("Enter your question")
            if not q.strip():
                continue
            pred = module(q)
            console.print(f"[bold blue]A:[/bold blue] {pred.answer}")
        elif action.lower() == "sum":
            console.print("Documents:")
            console.print(docs_list)
            choice = Prompt.ask("Enter document number to summarize")
            if not choice.isdigit() or not 1 <= int(choice) <= len(dataset):
                console.print("Invalid choice")
                continue
            summary = module.summarize_document(int(choice) - 1)
            console.print(f"[bold blue]Summary:[/bold blue] {summary.summary}")


if __name__ == "__main__":
    main()
