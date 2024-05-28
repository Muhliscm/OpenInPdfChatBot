from src.OpenInPdfChatBot import logger
import src.OpenInPdfChatBot.utils.llm_chains_gen as llm_chains


class ConversationChain:
    def __init__(self, llm, vector_stores, prompt_template):
        self.llm = llm
        self.vector_stores = vector_stores
        self.prompt_template = prompt_template
        self.conv = None

    def create_conv_chain(self):
        self.conv = llm_chains.get_conversation_retrieval_chain(
            self.llm, self.vector_stores, self.prompt_template)
        logger.info("New conversation chain created")
        return self.conv

    def get_conv_chain(self):
        if self.conv is None:
            logger.error("Conversation chain has not been created yet")
            raise ValueError("Conversation chain has not been created yet")
        return self.conv

    def run_chain(self, user_inputs):
        if self.conv is None:
            logger.error("Conversation chain has not been created yet")
            raise ValueError("Conversation chain has not been created yet")

        logger.info(
            "Conversation chain run started with user inputs: %s", user_inputs)
        try:
            response = self.conv.invoke(user_inputs)
            logger.info(
                "Conversation chain run completed with response:")
            return response
        except Exception as e:
            logger.error("Error during conversation chain run: %s", e)
            raise e
