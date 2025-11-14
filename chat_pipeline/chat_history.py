import redis, json

r = redis.Redis(host="localhost", port=6379, db=0)

class ChatHistory:
    def __init__(self) -> None:
        pass

    def storeChatHistory(self, userid:int, chat_history:list):
        for chat in chat_history:
            r.rpush(f"converstional:{userid}", json.dumps(chat))

    def retriveChatHistory(self, userid:int):
        history = r.lrange(f"converstional:{userid}", -6, -1)
        history = [json.loads(msg) for msg in history]                                  #type:ignore
        return history

chathistoryobj = ChatHistory()
