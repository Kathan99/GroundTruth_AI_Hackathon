import os
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import TextEmbedding
from pypdf import PdfReader

class RAGManager:
    def __init__(self, collection_name="store_policies"):
        self.client = QdrantClient(path="qdrant_data")
        self.collection_name = collection_name
        self.embedding_model = TextEmbedding()
        
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )

    def ingest_pdf(self, pdf_path: str):
        """
        Reads a PDF, chunks the text, embeds it, and stores it in Qdrant.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
        count_result = self.client.count(collection_name=self.collection_name)
        if count_result.count > 0:
            print("Data already exists in Qdrant. Skipping ingestion.")
            return count_result.count

        print("Ingesting PDF...")
        reader = PdfReader(pdf_path)
        text_chunks = []
        
        window_size = 20
        overlap = 5
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                
                if not lines:
                    continue
                    
                for i in range(0, len(lines), window_size - overlap):
                    chunk_lines = lines[i:i + window_size]
                    chunk_text = "\n".join(chunk_lines)
                    text_chunks.append(chunk_text)
        
        if not text_chunks:
            return 0

        embeddings = list(self.embedding_model.embed(text_chunks))
        
        points = [
            models.PointStruct(
                id=idx,
                vector=embedding.tolist(),
                payload={"text": chunk}
            )
            for idx, (chunk, embedding) in enumerate(zip(text_chunks, embeddings))
        ]
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return len(points)

    def search(self, query: str, limit: int = 5) -> List[str]:
        """
        Searches for relevant context based on the query.
        """
        query_embedding = list(self.embedding_model.embed([query]))[0]
        
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=limit
        ).points
        
        return [hit.payload["text"] for hit in results]

if __name__ == "__main__":
    rag = RAGManager()
    
    if not os.path.exists("data/store_policies.pdf"):
        print("PDF not found, skipping ingestion test.")
    else:
        count = rag.ingest_pdf("data/store_policies.pdf")
        print(f"Ingested {count} chunks.")
        
        query = "What is the return policy?"
        results = rag.search(query)
        print(f"Query: {query}")
        print("Results:")
        for res in results:
            print(f"- {res}")
