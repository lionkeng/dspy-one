# qa_common/main.py
import os
from pathlib import Path
from dotenv import load_dotenv
import dspy
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import math  # For IDF in advanced retrieval


# --- DSPy Signatures ---
class AnswerQuestion(dspy.Signature):
    """Answer warranty questions using provided context."""

    question = dspy.InputField()
    context = dspy.InputField()
    answer = dspy.OutputField()


class SummarizeDoc(dspy.Signature):
    """Summarize a document."""

    document = dspy.InputField()
    summary = dspy.OutputField(desc="one paragraph")


# --- Document Loading ---
def load_documents(docs_folder_name="example_warranty_docs"):
    # Allow customization of the folder name if needed in the future
    # Assumes docs_folder_name is a direct child of the project root
    project_root = Path(__file__).resolve().parent.parent
    docs_dir = project_root / docs_folder_name
    texts = []
    for path in sorted(docs_dir.glob("*.txt")):
        texts.append(path.read_text())
    return texts


# --- Basic Retrieval (can be a starting point or used by simpler QA) ---
def base_simple_retrieve(query: str, dataset, k: int = 3):
    words = set(query.lower().split())
    scored = []
    for i, text in enumerate(dataset):
        doc_words = set(text.lower().split())
        score = len(words & doc_words)
        scored.append((score, i))
    top = sorted(scored, key=lambda x: x[0], reverse=True)[:k]
    return [dataset[i] for _, i in top]


# --- IDF Computation (used by advanced retrieval) ---
def compute_idf(dataset):
    """Compute IDF weights for words in the dataset."""
    df = {}
    num_docs = len(dataset)
    for doc in dataset:
        for w in set(doc.lower().split()):
            df[w] = df.get(w, 0) + 1
    # Add a check for df[w] > 0 to prevent math domain error for words not in any document (though unlikely with current logic)
    # or words that might appear in all documents (df[w] == num_docs leading to log(1)=0)
    return {w: math.log(num_docs / df[w]) for w in df if df[w] > 0 and df[w] < num_docs}


# --- Core Application Setup and Loop ---
def initialize_dspy():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # It's better to raise an error or handle it more explicitly than just returning None
        # For CLI apps, printing and exiting or raising an error is common.
        console = Console()
        console.print("[bold red]OPENAI_API_KEY not found in .env file.[/bold red]")
        console.print("Please create a .env file and add your OpenAI API key.")
        raise ValueError("OPENAI_API_KEY not found.")

    lm = dspy.LM("openai/gpt-4o-mini", api_key=api_key)
    dspy.settings.configure(lm=lm)
    return Console()  # Return console for use in specific main functions


def run_qa_loop(module, dataset, console, app_name="Warranty Assistant"):
    console.print(f"[bold green]{app_name}[/bold green]")

    # Determine project_root more robustly if qa_common is not in the root
    # Assuming qa_common is a top-level directory alongside example_warranty_docs
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parent.parent  # qa_common -> project_root

    docs_folder_name = "example_warranty_docs"
    docs_list_path = project_root / docs_folder_name

    if not docs_list_path.exists() or not docs_list_path.is_dir():
        console.print(
            f"[bold red]Error: Document directory not found at {docs_list_path}[/bold red]"
        )
        return

    docs_list = "\n".join(
        f"{i+1}. {Path(p).name}"
        for i, p in enumerate(sorted(docs_list_path.glob("*.txt")))
    )

    while True:
        if dataset:
            prompt_text = Text("Choose [qa] question, [sum] summarize, or [exit]")
            action = Prompt.ask(prompt_text)

            action_lower = action.lower()  # Normalize once
        else:
            action_lower = "qa"
        if action_lower == "exit":
            break
        elif action_lower == "qa":
            q = Prompt.ask("Enter your question (or 'exit' to quit)")
            if q.lower() == "exit":
                break
            if not q.strip():
                console.print("[yellow]Please enter a question.[/yellow]")
                continue
            try:
                # Display the question with bold blue Q. prefix
                console.print(f"[bold blue]Q.[/bold blue] {q}")
                pred = module(q)  # Assumes module has a forward method for QA
                console.print(f"[bold blue]A:[/bold blue] {pred.answer}")
                console.print()  # Add newline for spacing before next iteration
            except Exception as e:
                console.print(f"[bold red]Error processing QA:[/bold red] {e}")
                console.print()  # Add newline even after errors

        elif action_lower == "sum":
            if not dataset:
                console.print("[yellow]No documents loaded for summarization.[/yellow]")
                continue
            console.print("Documents:")
            console.print(docs_list)
            choice_str = Prompt.ask("Enter document number to summarize")
            if not choice_str.isdigit():
                console.print("[yellow]Invalid input. Please enter a number.[/yellow]")
                continue

            try:
                choice = int(choice_str)
                if not 1 <= choice <= len(dataset):
                    console.print("[yellow]Invalid document number.[/yellow]")
                    continue
                # Assumes module has a summarize_document method
                summary = module.summarize_document(choice - 1)
                console.print(f"[bold blue]Summary:[/bold blue] {summary.summary}")
            except ValueError:
                console.print("[yellow]Invalid document number format.[/yellow]")
            except Exception as e:
                console.print(
                    f"[bold red]Error processing summarization:[/bold red] {e}"
                )
        else:
            console.print(
                "[yellow]Invalid action. Please choose 'qa', 'sum', or 'exit'.[/yellow]"
            )
