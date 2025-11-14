from google import genai
from chat_pipeline.prompts import decisivePrompt
from chat_pipeline.rag_pipeline import rag_obj
import json
from store import storeBookingInfo

client = genai.Client()


class Decisive:
    def __init__(self):
        pass

    def toPyObj(self, llm_response: str):
        cleaned_json = (
            llm_response.replace("```json\n", "")
            .replace("\n```", "")
            .replace("\n", "")
            .strip()
        )
        return json.loads(cleaned_json)

    def decideIntent(self, question: str, embedding, chat_history: list[str], search_type: str):
        llm_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=decisivePrompt(question=question),
        )

        py_obj_response = self.toPyObj(str(llm_response.text))

        print(llm_response.text)

        if py_obj_response["intent"] == "booking":
            print("booking")
            print(type(py_obj_response))
            response = storeBookingInfo(booking_dict=py_obj_response)
            return response
        
        elif py_obj_response["intent"] == "question":
            print("answering")
            response = rag_obj.ragAnswer(
                text=question, embedding=embedding, chat_history=chat_history, search_type=search_type
            )
            return response


decisiveObj = Decisive()
