from langchain.chains import RetrievalQA
from transformers import pipeline


def hugging_face_pipe_gen(model, tokenizer):

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0,
        top_p=0.95,
        repetition_penalty=1.15
    )
    return pipe


def get_conversation_retrieval_chain(llm, vector_stores, prompt):
    """ function to create conversational chain

    Args:
        llm (_type_): llm instance
        vector_stores (_type_): vector db has vectors in it
        prompt (_type_): prompt template

    Returns:
        _type_: conversational chain for document chat bot
    """

    conversation_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_stores.as_retriever(search_kwargs={"k": 3}),
        # chain_type_kwargs={'prompt': prompt},
        return_source_documents=True

    )
    return conversation_chain
