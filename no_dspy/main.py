import os
from types import SimpleNamespace
from dotenv import load_dotenv
from rich.console import Console

from qa_common.main import (
    load_documents,
    compute_idf,
    run_qa_loop,
)

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class ValidateDocQAModule:
    def __init__(self, dataset, persona: str, brand_voice: str, tone: str):
        self.dataset = dataset
        self.idf = compute_idf(dataset)
        self.persona = persona
        self.brand_voice = brand_voice
        self.tone = tone
        api_key = os.getenv("OPENAI_API_KEY")
        self.answer_llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
        self.judge_llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
        self.summary_llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

    def __call__(self, question: str):
        return self.forward(question)

    def forward(self, question: str):
        best_answer = None
        best_score = -1
        for attempt in range(3):
            context = "\n".join(
                self.simple_retrieve(
                    question, self.dataset, k=3 + attempt, variation=attempt
                )
            )
            answer = self._answer_question(question, context)
            rating = self._judge_answer(question, answer)
            try:
                score = float(rating)
            except (ValueError, TypeError):
                score = 0.0
            if score > best_score:
                best_score = score
                best_answer = answer
            if score >= 7:
                break
        return SimpleNamespace(answer=best_answer)

    def summarize_document(self, index: int):
        text = self.dataset[index]
        summary = self._summarize(text)
        return SimpleNamespace(summary=summary)

    def _answer_question(self, question: str, context: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"You are {self.persona}. Use the following brand voice: {self.brand_voice}. Respond in a {self.tone} tone.",
                ),
                ("human", "Context:\n{context}\nQuestion: {question}\nAnswer:"),
            ]
        )
        messages = prompt.format(context=context, question=question)
        return self.answer_llm.invoke(messages).content.strip()

    def _judge_answer(self, question: str, answer: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You judge if an answer correctly and helpfully addresses the question. Rate from 1 to 10.",
                ),
                ("human", "Question: {question}\nAnswer: {answer}\nScore:"),
            ]
        )
        messages = prompt.format(question=question, answer=answer)
        return self.judge_llm.invoke(messages).content.strip()

    def _summarize(self, text: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Summarize the following document in one paragraph."),
                ("human", "{text}"),
            ]
        )
        messages = prompt.format(text=text)
        return self.summary_llm.invoke(messages).content.strip()

    def simple_retrieve(self, query: str, dataset, k: int = 3, variation: int = 0):
        words = query.lower().split()
        tokens = set(words)
        scored = []
        bigrams_query = set(" ".join(words[i : i + 2]) for i in range(len(words) - 1))
        for i, text_item in enumerate(dataset):
            doc_tokens = text_item.lower().split()
            doc_set = set(doc_tokens)
            base = len(tokens & doc_set)
            current_score = base
            if variation == 1:
                doc_bigrams = set(
                    " ".join(doc_tokens[j : j + 2]) for j in range(len(doc_tokens) - 1)
                )
                current_score = base + 2 * len(bigrams_query & doc_bigrams)
            elif variation == 2 and self.idf:
                current_score = sum(
                    self.idf.get(w, 0.0) for w in tokens if w in doc_set
                )
            scored.append((current_score, i))
        top = sorted(scored, key=lambda x: x[0], reverse=True)[:k]
        return [dataset[i] for _, i in top]


def main():
    load_dotenv()
    console = Console()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold red]OPENAI_API_KEY not found in .env file.[/bold red]")
        return

    persona = "knowledgeable customer support agent to help with Acme Homes warranty"
    brand_voice = "Acme Homes is a trusted brand in home builder. The key pillars of our are brand are quality, reliability, and customer satisfaction."
    tone = "friendly, professional, empathetic, and helpful"
    dataset = load_documents()
    module = ValidateDocQAModule(
        dataset, persona=persona, brand_voice=brand_voice, tone=tone
    )

    run_qa_loop(
        module,
        dataset,
        console,
        app_name="Acme Homes Warranty Assistant (LangChain)",
    )


if __name__ == "__main__":
    main()
