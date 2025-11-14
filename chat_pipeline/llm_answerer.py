from google import genai
from chat_pipeline.prompts import ragPrompt

client = genai.Client()

class LLMAnswerer:
    def __init__(self):
        pass

    def llmAnswer(self, question: str, context: str, chat_history:list[str]):
        llm_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=ragPrompt(question=question, context=context, chat_history=chat_history),
        )
        return llm_response.text


llm_answerer_obj = LLMAnswerer()
