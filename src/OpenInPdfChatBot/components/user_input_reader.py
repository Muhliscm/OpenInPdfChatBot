
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from src.OpenInPdfChatBot.components.pdf_to_vector_conveter import PdfFilesToVectorPipeline
from src.OpenInPdfChatBot.components.prompt_templates import chat_prompt_template
from src.OpenInPdfChatBot import logger
from src.OpenInPdfChatBot.components.llm_chains import ConversationChain
from src.OpenInPdfChatBot.utils.llm_chains_gen import hugging_face_pipe_gen
from src.OpenInPdfChatBot.constants import PDF_FILE_DIR, LLM_MODEL
from langchain_community.llms import HuggingFacePipeline


tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(
    LLM_MODEL, torch_dtype=torch.float32)

pipe = hugging_face_pipe_gen(model, tokenizer)
llm = HuggingFacePipeline(pipeline=pipe)

# path for pdf files storage
pipeline = PdfFilesToVectorPipeline(PDF_FILE_DIR)
pipeline.start_pipeline()
vector_stores = pipeline.get_vector_stores()

conv_chain = ConversationChain(
    llm, vector_stores, chat_prompt_template)
conv_chain.create_conv_chain()


def result_processor(bot_response):
    results = {}
    invalid_responses = ["no", "not enough information"]
    result = bot_response.get('result')
    if result in invalid_responses:
        results.update(
            {"Answer": "I can only answer from the given documents"})
        return results
    else:
        results.update({"Answer": result})
        references = []
        source_documents = bot_response["source_documents"]
        print(bot_response)
        for document in source_documents:
            document_path = document.metadata['source']
            document_name = document_path.split("/")[-1]
            paragraph = document.page_content

            references.append(
                {"Document Name": document_name, "Paragraph": paragraph})

        results.update({"References": references})
        return results


def user_input_handler(user_query):
    try:
        bot_response = conv_chain.run_chain(
            user_query)
        result = result_processor(bot_response)
        return result

    except Exception as e:
        logger.error(
            "Failed to get response from bot: %s", e)
        return "Failed to get response from bot"
