import os
from dotenv import load_dotenv
import dspy
from rich.console import Console
from rich.prompt import Prompt


class DocQASignature(dspy.Signature):
    """Answer a question given a context passage."""

    question = dspy.InputField()
    context = dspy.InputField()
    answer = dspy.OutputField()


class ValidateAnswer(dspy.Signature):
    """Validate an answer with yes/no."""

    question = dspy.InputField()
    context = dspy.InputField()
    answer = dspy.InputField()
    valid = dspy.OutputField(desc="yes or no")


class DocQAModule(dspy.Module):
    def __init__(self, num_steps: int = 3):
        super().__init__()
        self.answer = dspy.ChainOfThought(DocQASignature)
        if hasattr(dspy, "GatedChainOfThought"):
            self.validate = dspy.GatedChainOfThought(ValidateAnswer)
        else:
            self.validate = dspy.Predict(ValidateAnswer)
        self.num_steps = num_steps

    def forward(self, question: str, context: str):
        last_prediction = None
        for _ in range(self.num_steps):
            prediction = self.answer(question=question, context=context)
            last_prediction = prediction
            check = self.validate(
                question=question, context=context, answer=prediction.answer
            )
            valid_flag = str(getattr(check, "valid", "")).strip().lower()
            if valid_flag in {"yes", "true", "1"}:
                return prediction
        return last_prediction


def main():
    load_dotenv()
    console = Console()
    console.print("[bold green]Doc QA Bot Initialized[/bold green]")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        console.print("[bold red]Error: OPENAI_API_KEY not found in .env file.[/bold red]")
        return

    turbo = dspy.LM("openai/gpt-4o-mini", api_key=openai_api_key)
    dspy.settings.configure(lm=turbo)

    qa = DocQAModule()

    context = Prompt.ask("Provide a context passage")
    while True:
        question = Prompt.ask("Ask a question about the context (or 'exit')")
        if question.lower() == "exit":
            break
        prediction = qa(question=question, context=context)
        console.print(f"[bold blue]Q:[/bold blue] {question}")
        console.print(f"[bold green]A:[/bold green] {prediction.answer}")


if __name__ == "__main__":
    main()
