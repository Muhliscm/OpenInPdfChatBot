import src.OpenInPdfChatBot.utils.common as utils
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.OpenInPdfChatBot import logger


class PdfFilesToVectorPipeline:
    def __init__(self, path) -> None:
        self.path = path
        self.vector_stores = None

    def start_pipeline(self):
        logger.info("PDF to vector pipeline started for path: %s", self.path)
        try:
            documents = utils.document_loader(self.path)
            logger.info("PDF Documents loaded")

            text_chunks = utils.get_document_chunks(documents)
            logger.info("Text chunks created")

            embeddings = utils.get_embeddings(
                HuggingFaceEmbeddings, 'sentence-transformers/all-MiniLM-L6-v2')
            logger.debug("Embeddings model loaded")

            self.vector_stores = utils.get_vectorstore_from_document(
                Chroma, embeddings, text_chunks)
            logger.info("PDFs to vector pipeline completed successfully")

        except Exception as e:
            logger.error("Error in PDF to vector pipeline: %s", e)
            raise

    def get_vector_stores(self):
        if self.vector_stores is None:
            logger.error(
                "Vector stores have not been created yet. Run start_pipeline() first.")
            raise ValueError(
                "Vector stores have not been created yet. Run start_pipeline() first.")
        return self.vector_stores
