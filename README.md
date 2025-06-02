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

### Run the `no_dspy` example

```sh
uv run no-dspy-cli
```

This example mirrors `docs_qa_validate_answer_with_persona` but is implemented with LangChain instead of DSPy.

### Run the `cloudflare_mcp` example

```sh
uv run cloudflare-mcp-cli
```

This example connects to Cloudflare's documentation via MCP and provides AI-powered search and summarization. You can ask questions about Cloudflare Workers, Pages, and other services interactively.

### Run the `echo_server_mcp` example

```sh
uv run echo-server-mcp
```

This starts a local MCP server that echoes back any input it receives. Useful for testing MCP client connections and understanding the protocol.

### `cloudflare_mcp`

This advanced example demonstrates real-world integration with external documentation sources through the Model Context Protocol (MCP). The `CloudflareMCPModule` connects to Cloudflare's documentation server, searches for relevant information, and provides AI-powered summarization of the results.

**Key Features:**

- **MCP Integration**: Uses the Model Context Protocol to connect to live documentation servers
- **Fresh Connections**: Creates new connections per query to avoid async cleanup issues
- **AI Summarization**: Leverages DSPy with OpenAI to generate intelligent summaries
- **Fallback Mode**: Gracefully degrades to simple summarization when no LM is configured
- **Rich Formatting**: Beautiful terminal output with progress indicators and structured display

**Architecture:**

- `CloudflareMCPModule`: Main DSPy module that handles MCP connections and summarization
- `MCPResultFormatter`: Rich formatting utilities for beautiful terminal output
- Fresh connection strategy eliminates persistent connection management

#### Demo Scripts

The `demo/` directory contains several demonstration scripts showcasing different aspects of the system:

**`demo_clean_summary.py`** - Minimal demo showing clean Q&A output:

```sh
uv run demo/demo_clean_summary.py
```

**`demo_rich_formatting.py`** - Showcases the beautiful rich terminal formatting:

```sh
uv run demo/demo_rich_formatting.py
```

**`demo_dspy_summarization.py`** - Comprehensive test with multiple questions:

```sh
uv run demo/demo_dspy_summarization.py
```

**`dspy_prediction_demo.py`** - Educational demo explaining DSPy Prediction objects:

```sh
uv run demo/dspy_prediction_demo.py
```

#### Testing

**`cloudflare_mcp/test_cloudflare_mcp.py`** - Comprehensive test suite that:

- Tests multiple query types and edge cases
- Validates the fresh connection approach
- Demonstrates error handling and recovery
- Verifies AI summarization quality

```sh
uv run cloudflare_mcp/test_cloudflare_mcp.py
```

This example showcases how DSPy can be integrated with modern protocols like MCP to create intelligent documentation search systems with robust error handling and beautiful user interfaces.

### `echo_server_mcp`

This simple example provides a minimal MCP (Model Context Protocol) server implementation using FastMCP. The server exposes a single `echo` tool that returns whatever input it receives, making it perfect for testing MCP client implementations and understanding the protocol basics.

**Key Features:**

- **FastMCP Implementation**: Uses the FastMCP library for easy server creation
- **SSE Transport**: Runs on Server-Sent Events for real-time communication
- **Single Echo Tool**: Provides a simple `echo(query: str) -> dict` function
- **Local Testing**: Runs on localhost:8000 for local development and testing

**Use Cases:**

- Testing MCP client implementations (like the cloudflare_mcp example)
- Understanding MCP protocol fundamentals
- Development and debugging of MCP-based applications
- Educational purposes for learning about tool-based AI architectures

The server starts on port 8000 and can be accessed by any MCP-compatible client. It's particularly useful when developing and testing the `cloudflare_mcp` example or other MCP clients.

## Example Descriptions

### `simple_math`

This introductory example demonstrates how DSPy can be used to build a very small QA system. It defines a short signature (`BasicQA`) and a module (`ArithmeticQA`) that wraps `dspy.ChainOfThought` to answer arithmetic questions interactively. The CLI uses `rich` for prompts and configures an OpenAI model via `dspy.LM`.

### `doc_qa`

The document QA example showcases retrieval-augmented generation and summarization. It automatically loads a set of warranty documents, performs a simple keyword-based retrieval to supply context, and then answers questions using `dspy.ChainOfThought`.

**Key DSPy features**

- Retrieval: Use DSPy's retrieval utilities to build embeddings from the documents and fetch relevant passages.

- Chaining Modules: Compose multiple modules—one for retrieval and one for generating answers or summaries.

- Signatures with Richer Output: Instead of short factoid answers, use multi-sentence outputs (summaries) and structured data fields.

### `no_dspy`

This companion example implements the same validated QA workflow using LangChain instead of DSPy, showcasing how to build the flow without DSPy modules

## Improving Retrieval with Bigrams and IDF

`simple_retrieve` now supports scoring based on both individual words and word pairs (bigrams). For each document, bigrams that match the query contribute more weight, and each term is scaled by its _inverse document frequency_ (IDF), which lowers the impact of common words. This IDF weighting is computed once when the module loads the dataset. Using bigrams and IDF helps rank documents more consistently than random shuffling because matches on rare phrases are prioritized.

## Contributing More Examples

- Add a new directory (e.g., `my_example/`) with an `__init__.py` and your code.
- Add the directory name to the `[tool.hatch.build.targets.wheel].packages` list in `pyproject.toml`.
- Add a new entry point under `[project.scripts]` for your CLI.

---

**Author:** Keng Lim (<lionkeng@gmail.com>)
