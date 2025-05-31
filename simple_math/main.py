import dspy
from rich.console import Console
from rich.prompt import Prompt
import os
from dotenv import load_dotenv


class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""

    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")


class ArithmeticQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(BasicQA)

    def forward(self, question):
        return self.generate_answer(question=question)


def main():
    load_dotenv()
    console = Console()
    console.print("[bold green]Arithmetic QA Bot Initialized[/bold green]")

    # Configure DSPy LM
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        console.print(
            "[bold red]Error: OPENAI_API_KEY not found in .env file.[/bold red]"
        )
        console.print("Please create a .env file and add your OpenAI API key:")
        console.print('OPENAI_API_KEY="your_api_key_here"')
        return

    turbo = dspy.LM("openai/gpt-4o-mini", api_key=openai_api_key)
    dspy.settings.configure(lm=turbo)

    arithmetic_qa = ArithmeticQA()

    while True:
        question = Prompt.ask("Ask an arithmetic question (or type 'exit' to quit)")
        if question.lower() == "exit":
            break

        if not question.strip():
            console.print("[yellow]Please enter a question.[/yellow]")
            continue

        try:
            prediction = arithmetic_qa(question)
            console.print(f"[bold blue]Q:[/bold blue] {question}")
            console.print(f"[bold green]A:[/bold green] {prediction.answer}")
        except Exception as e:
            console.print(f"[bold red]Error processing question:[/bold red] {e}")


if __name__ == "__main__":
    main()
