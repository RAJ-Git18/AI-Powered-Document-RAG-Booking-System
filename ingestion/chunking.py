import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

class Chunking:
    def __init__(self):
        pass

    def fixedChunking(self, text, chunk_size=500) -> list[str]: #this takes the text and return the list of the chunked text
        self.text = text
        self.chunk_size = chunk_size
        self.chunk_list = []
        for chunk in range(0, len(self.text), self.chunk_size):
            self.chunk_list.append(self.text[chunk : chunk + self.chunk_size])

        return self.chunk_list

    def split_into_sentences(self, text:str):
        text = text.replace("\n", " ")
        parts = re.split(r"(?<=[.!?])\s+", text)
        return [p.strip() for p in parts if p.strip()]

    def semanticChunking(self, text, threshold: float = 0.60, max_sentences=5)->list[str]:
        sentences = self.split_into_sentences(text)

        # embed all sentences
        embeddings = model.encode(sentences, convert_to_tensor=True)

        chunks = []
        current_chunk = [sentences[0]]  # start first chunk

        for i in range(1, len(sentences)):
            current_embedding = model.encode(
                " ".join(current_chunk), convert_to_tensor=True
            )
            next_embedding = embeddings[i]

            # similarity between current chunk and next sentence
            similarity = float(util.pytorch_cos_sim(current_embedding, next_embedding))

            # compare the simlailarity with threshold to either append or join the sentences
            if similarity > threshold and len(current_chunk) < max_sentences:
                current_chunk.append(sentences[i])
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]

        chunks.append(" ".join(current_chunk))

        return chunks


chunkingObj = Chunking()
