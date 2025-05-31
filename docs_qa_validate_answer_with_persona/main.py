import dspy

# Import common components
from qa_common.main import (
    SummarizeDoc,  # Replaces local SummarizeDoc
    load_documents,  # Replaces local load_documents
    compute_idf,  # Replaces local compute_idf
    initialize_dspy,  # For setting up dspy and console
    run_qa_loop,  # For the main interaction loop
)


# Implement the AnswerQuestion signature with persona guidance
class AnswerQuestion(dspy.Signature):
    """Answer warranty questions influenced by persona and brand voice."""

    question = dspy.InputField()
    context = dspy.InputField()
    persona = dspy.InputField(desc="persona to adopt")
    brand_voice = dspy.InputField(desc="brand voice guidelines")
    tone = dspy.InputField(desc="tone of the response")
    answer = dspy.OutputField()


# This signature is unique to this module
class JudgeAnswer(dspy.Signature):
    """Judge the validity of an answer. Return a score from 1-10."""

    question = dspy.InputField()
    answer = dspy.InputField()
    rating = dspy.OutputField(desc="score 1-10")


class ValidateDocQAModule(dspy.Module):
    def __init__(self, dataset, persona: str, brand_voice: str, tone: str):
        super().__init__()
        self.dataset = dataset
        self.idf = compute_idf(dataset)  # Use imported compute_idf
        # Use imported signatures
        self.answer = dspy.ChainOfThought(AnswerQuestion)
        self.judge = dspy.Predict(JudgeAnswer)
        self.summarize = dspy.Predict(SummarizeDoc)
        self.persona = persona
        self.brand_voice = brand_voice
        self.tone = tone

    def forward(self, question):
        best_answer = None
        best_score = -1
        # The retry/validation logic is specific to this module
        for attempt in range(3):
            context = "\n".join(
                self.simple_retrieve(
                    question, self.dataset, k=3 + attempt, variation=attempt
                )
            )
            # Pass persona, brand_voice, and tone to the answer module
            pred = self.answer(
                question=question,
                context=context,
                persona=self.persona,
                brand_voice=self.brand_voice,
                tone=self.tone,
            )
            critique = self.judge(question=question, answer=pred.answer)
            try:
                score = float(critique.rating)
            except (ValueError, TypeError):
                score = 0.0
            if score > best_score:
                best_score = score
                best_answer = pred.answer
            if score >= 7:  # If a good answer is found, return it
                return dspy.Prediction(answer=pred.answer)
        return dspy.Prediction(
            answer=best_answer
        )  # Otherwise, return the best one found

    def summarize_document(self, index: int):
        text = self.dataset[index]
        return self.summarize(document=text)

    # This simple_retrieve is more complex and specific to this module's validation strategy
    def simple_retrieve(self, query: str, dataset, k: int = 3, variation: int = 0):
        """Retrieve passages using different scoring variations."""
        words = query.lower().split()
        tokens = set(words)
        scored = []
        bigrams_query = set(" ".join(words[i : i + 2]) for i in range(len(words) - 1))
        for i, text_item in enumerate(dataset):
            doc_tokens = text_item.lower().split()
            doc_set = set(doc_tokens)
            base = len(tokens & doc_set)
            current_score = base  # Default to base score
            if variation == 1:
                doc_bigrams = set(
                    " ".join(doc_tokens[j : j + 2]) for j in range(len(doc_tokens) - 1)
                )
                current_score = base + 2 * len(bigrams_query & doc_bigrams)
            elif variation == 2 and self.idf:
                # Ensure self.idf is not None and contains values
                current_score = sum(
                    self.idf.get(w, 0.0) for w in tokens if w in doc_set
                )

            scored.append((current_score, i))
        top = sorted(scored, key=lambda x: x[0], reverse=True)[:k]
        return [dataset[i] for _, i_val in top]


def main():
    try:
        console = initialize_dspy()
    except ValueError:
        # initialize_dspy now raises ValueError if OPENAI_API_KEY is not found
        # and prints a message, so we can just return.
        return
    persona = "knowledgeable customer support agent to help with Acme Homes warranty"
    brand_voice = "Acme Homes is a trusted brand in home builder. The key pillars of our are brand are quality, reliability, and customer satisfaction."
    tone = "friendly, professional, empathetic, and helpful"
    dataset = load_documents()
    module = ValidateDocQAModule(
        dataset, persona=persona, brand_voice=brand_voice, tone=tone
    )

    # Pass the app_name to the common loop
    run_qa_loop(
        module,
        dataset,
        console,
        app_name="Acme Homes Warranty Assistant (Validated QA)",
    )


if __name__ == "__main__":
    main()
