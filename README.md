# dspy-examples

This repository showcases a series of CLI programs that illustrate the capabilities of [DSPy](https://dspy.ai/api/). The examples are designed to gradually increase in complexity, starting from simple to more advanced use cases.

## Installation

1. **Clone the repository and navigate to the project root:**

   ```sh
   git clone <your-repo-url>
   cd dspy-examples
   ```

2. **Create and activate a virtual environment (recommended):**

   ```sh
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```sh
   uv pip install .
   ```

4. **Set up your OpenAI API key:**
   - Create a `.env` file in the project root with the following content:
     ```
     OPENAI_API_KEY="your_openai_api_key_here"
     ```

## Running an Example

Each example is a standalone CLI program. You can run them using the script entry points defined in `pyproject.toml`.

### Run the `simple_math` example

```sh
uv run simple-math-cli
```

You will be prompted to enter arithmetic questions, and the program will answer them using DSPy and OpenAI.

### Run the `doc_qa` example

```sh
uv run doc-qa-cli
```

This CLI automatically loads sample warranty documents for Acme Homes and lets you ask questions or generate summaries.

### Run the `docs_qa_validate_answer` example

```sh
uv run docs-qa-validate-cli
```

This variant retries answering a question up to three times while a judge model scores the response.

### Run the `docs_qa_validate_answer_with_persona` example

```sh
uv run docs-qa-validate-persona-cli
```

This version also shapes answers according to a specified persona, brand voice, and tone.

## Example Descriptions

### `simple_math`

This introductory example demonstrates how DSPy can be used to build a very small QA system. It defines a short signature (`BasicQA`) and a module (`ArithmeticQA`) that wraps `dspy.ChainOfThought` to answer arithmetic questions interactively. The CLI uses `rich` for prompts and configures an OpenAI model via `dspy.LM`.

### `doc_qa`

The document QA example showcases retrieval-augmented generation and summarization. It automatically loads a set of warranty documents, performs a simple keyword-based retrieval to supply context, and then answers questions using `dspy.ChainOfThought`.

**Key DSPy features**

- Retrieval: Use DSPy’s retrieval utilities to build embeddings from the documents and fetch relevant passages.

- Chaining Modules: Compose multiple modules—one for retrieval and one for generating answers or summaries.

- Signatures with Richer Output: Instead of short factoid answers, use multi-sentence outputs (summaries) and structured data fields.

## Improving Retrieval with Bigrams and IDF

`simple_retrieve` now supports scoring based on both individual words and word pairs (bigrams). For each document, bigrams that match the query contribute more weight, and each term is scaled by its _inverse document frequency_ (IDF), which lowers the impact of common words. This IDF weighting is computed once when the module loads the dataset. Using bigrams and IDF helps rank documents more consistently than random shuffling because matches on rare phrases are prioritized.

## Contributing More Examples

- Add a new directory (e.g., `my_example/`) with an `__init__.py` and your code.
- Add the directory name to the `[tool.hatch.build.targets.wheel].packages` list in `pyproject.toml`.
- Add a new entry point under `[project.scripts]` for your CLI.

---

**Author:** Keng Lim (<lionkeng@gmail.com>)
