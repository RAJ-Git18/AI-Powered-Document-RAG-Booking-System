def ragPrompt(question: str, context: str, chat_history: list[str]):
    prompt = f"""
                You are a helpful assistant having a conversation with a user.

                Use the following information to answer the user's next question:
                1. Chat History — the last few exchanges between llm and the user.
                2. Context — factual information retrieved from a knowledge source.
                3. User Question — the new query to answer.

                Guidelines:
                - Give a very short, single-paragraph answer.
                - Use chat history to maintain continuity and avoid repeating.
                - Use the context for factual accuracy.
                - If context doesn’t help, respond thoughtfully based on general understanding.

                ---
                Chat History:
                {chat_history}

                Context:
                {context}

                Question:
                {question}
              
                    """

    return prompt


def decisivePrompt(question: str):
    prompt = f"""
                    You are an assistant that manages interview scheduling.

                    For the following user message:
                    "{question}"

                    Decide:
                    - intent: 'booking' or 'question'
                    - if intent = 'booking', extract name, email, date, time if present.

                    Return JSON like and make sure that the date and time is in ISO format:
                    {{"intent": "...", "name": "...", "email": "...", "date": "...", "time": "..."}}.
            """
    return prompt
