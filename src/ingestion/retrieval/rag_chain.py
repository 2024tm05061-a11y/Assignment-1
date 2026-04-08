from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

from src.ingestion.retrieval.vector_store import build_vector_store


PROMPT_TEMPLATE = """
You are a technical documentation assistant.

Answer the question ONLY using the context below.
If the answer is not present, say:
"The document does not contain this information."

Context:
{context}

Question:
{question}

Answer (include page references if available):
"""


def build_rag_chain(pdf_path: str):
    vector_store = build_vector_store(pdf_path)

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE
    )

    generator = pipeline(
        "text-generation",
        model="google/flan-t5-base",
        max_new_tokens=200
    )

    llm = HuggingFacePipeline(pipeline=generator)

    def rag_answer(question: str):
        documents = retriever.get_relevant_documents(question)

        context = "\n\n".join(
            f"(Page {d.metadata.get('page')}) {d.page_content}"
            for d in documents
        )

        formatted_prompt = prompt.format(
            context=context,
            question=question
        )

        answer = llm.invoke(formatted_prompt)

        return {
            "answer": answer,
            "sources": documents
        }

    return rag_answer