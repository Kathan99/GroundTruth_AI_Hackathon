import os
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from app.privacy import PrivacyManager
from app.context import ContextManager
from app.rag import RAGManager
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    user_id: str
    query: str
    lat: float
    lon: float
    masked_query: str
    context_str: str
    rag_str: str
    response: str

class SupportAgent:
    def __init__(self):
        self.privacy = PrivacyManager()
        self.context = ContextManager()
        self.rag = RAGManager()
        
        try:
            print("Ingesting knowledge base...")
            self.rag.ingest_pdf("data/store_policies.pdf")
            print("Knowledge base ready.")
        except Exception as e:
            print(f"Error ingesting PDF: {e}")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("Warning: GROQ_API_KEY not found.")
            self.llm = None
        else:
            self.llm = ChatGroq(
                api_key=api_key,
                model_name="llama-3.3-70b-versatile",
                temperature=0.7
            )

        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("anonymize", self.anonymize_node)
        workflow.add_node("retrieve_context", self.context_node)
        workflow.add_node("retrieve_rag", self.rag_node)
        workflow.add_node("generate", self.generate_node)

        workflow.set_entry_point("anonymize")
        workflow.add_edge("anonymize", "retrieve_context")
        workflow.add_edge("retrieve_context", "retrieve_rag")
        workflow.add_edge("retrieve_rag", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()

    def anonymize_node(self, state: AgentState):
        masked = self.privacy.anonymize(state["query"])
        return {"masked_query": masked}

    def context_node(self, state: AgentState):
        ctx = self.context.format_context(state["user_id"], state["lat"], state["lon"])
        return {"context_str": ctx}

    def rag_node(self, state: AgentState):
        rag_docs = self.rag.search(state["masked_query"])
        rag_str = "\n".join([f"- {doc}" for doc in rag_docs])
        return {"rag_str": rag_str}

    def generate_node(self, state: AgentState):
        if not self.llm:
            return {"response": "Error: LLM not configured."}

        try:
            with open("app/prompt.txt", "r") as f:
                prompt_template = f.read()
        except FileNotFoundError:
            prompt_template = "Context: {context_str}. Info: {rag_str}"
        
        system_prompt = prompt_template.format(
            context_str=state["context_str"], 
            rag_str=state["rag_str"]
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state["masked_query"])
        ]
        
        response = self.llm.invoke(messages)
        return {"response": response.content}

    def process_query(self, user_id: str, query: str, lat: float, lon: float):
        """
        Invokes the graph.
        """
        initial_state = {
            "user_id": user_id,
            "query": query,
            "lat": lat,
            "lon": lon,
            "masked_query": "",
            "context_str": "",
            "rag_str": "",
            "response": ""
        }
        
        result = self.graph.invoke(initial_state)
        return result["response"]

if __name__ == "__main__":
    agent = SupportAgent()
    
    user_id = "USR-001"
    query = "How much is a Medium Masala Chai?"
    lat = 19.10
    lon = 72.78
    
    print(f"Query: {query}")
    response = agent.process_query(user_id, query, lat, lon)
    print(f"Response: {response}")
