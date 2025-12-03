# H-002 | Hyper-Personalized Customer Support Agent

> **Tagline:** A privacy-first, context-aware AI agent that delivers hyper-personalized retail support in milliseconds using Groq, LangGraph, and RAG.

## 1. The Problem 

**Context:** Retail customers today expect instant, relevant answers. They ask questions like "Is this store open?", "Do you have size 10 in stock?", or "Where is my order?".

**The Pain Point:** Standard chatbots are "dumb." They give generic FAQ answers. They don't know who the customer is, where they are standing, or what they like. A user standing outside a coffee shop in the rain doesn't want a link to the website; they want to know if they can come inside for a hot drink.

> **My Solution:** I built a **Hyper-Personalized Agent** that combines User History, Real-time Location, and Store Inventory. It knows you love Masala Chai, it knows you are 50m away from the Andheri outlet, and it knows there's a 20% coupon available.

## 2. Expected End Result

**For the User:**

*   **Input:** User texts "I'm cold" (with location metadata).
*   **Action:** The Agent analyzes the intent, checks the weather context, finds the nearest store, and retrieves the user's favorite drink.
*   **Output:** "Hi Zayan! Since you're just 2 mins away from our Andheri West outlet, come on in! We have your favorite **Masala Chai** ready, and here's a **20% off coupon** to warm you up."

## 3. Technical Approach

I built this system to be **Production-Ready**, focusing on modularity, privacy, and speed.

**System Architecture:**

1.  **Orchestration (LangGraph):**
    *   The agent logic is modeled as a **State Graph** (Nodes: Anonymize -> Context -> RAG -> Generate).
    *   This ensures a structured, reliable flow and easy extensibility.

2.  **Privacy Layer (PII Masking):**
    *   Before any data hits the LLM, it passes through **Microsoft Presidio**.
    *   I implemented custom regex recognizers to detect and mask Indian phone numbers (`+91-...`) and names.
    *   The LLM only sees `<PERSON>` or `<PHONE_NUMBER>`, ensuring user privacy.

3.  **Context Engine:**
    *   I built a custom engine that aggregates **User Data** (Preferences, Loyalty), **Store Data** (Stock, Hours), and **Location** (Haversine distance calculation).
    *   This structured context is injected dynamically into the System Prompt.

4.  **RAG Pipeline (Knowledge Base):**
    *   Static knowledge (Store Policies, Returns) is stored in **Qdrant** (Persistent Storage).
    *   We use **FastEmbed** for lightweight, fast embeddings.
    *   **Optimization:** The system uses persistent storage to avoid re-ingesting the PDF on every restart.

5.  **Generative AI (The Brain):**
    *   Powered by **Groq** (Llama 3.3 70B) for ultra-low latency inference.
    *   The prompt orchestrates all the inputs to generate a friendly, helpful, and accurate response.

## 4. Tech Stack

*   **Language:** Python 3.13
*   **Orchestration:** LangGraph, LangChain
*   **API Framework:** FastAPI
*   **LLM Engine:** Groq (Llama 3.3 70B)
*   **Vector Database:** Qdrant (Persistent Local Storage)
*   **Privacy:** Microsoft Presidio, Spacy
*   **Frontend:** HTML, CSS, JavaScript (Served via FastAPI)

## 5. Challenges & Learnings

*This project required balancing personalization with privacy.*

**Challenge 1: Privacy vs. Utility**
*   **Issue:** To be helpful, the bot needs to use the user's name and phone number. But sending PII to a cloud LLM is a security risk.
*   **Solution:** I implemented a **Bi-Directional Masking** strategy. The application layer holds the real data, while the LLM layer operates on tokens like `<PERSON>`.

**Challenge 2: RAG Accuracy for Tables**
*   **Issue:** The LLM struggled to read pricing from PDF tables when chunked.
*   **Solution:** I implemented a "Quick Reference" text-based chapter in the PDF generation script and optimized the chunking strategy (Sliding Window) to ensure the LLM always retrieves the correct price context.

**Challenge 3: Hybrid Location Resolution**
*   **Issue:** Users often deny browser geolocation or are far from the store, yet still want store-specific info ("I am in Gurgaon").
*   **Solution:** I built a **Hybrid Location Engine**. It prioritizes precise GPS coordinates if available. If not, it falls back to a text-based search, extracting city names from the user's query to find the relevant store context.

**Challenge 4: Smart User Identification**
*   **Issue:** Users don't always provide their ID in a structured format (e.g., "My ID is USR-006" vs just "USR-006").
*   **Solution:** I implemented a **Regex-based Extraction Logic** in the backend. It intelligently parses natural language queries to identify User IDs (`USR-\d+`) or Phone Numbers, allowing for a seamless "Guest to Member" transition without rigid command syntax.

**Challenge 5: Contextual Hallucinations**
*   **Issue:** The LLM would sometimes invent store hours or offers when the context was missing.
*   **Solution:** I enforced a strict **"RAG is Truth"** policy in the system prompt and engineered the context manager to explicitly state "Active Offers: None" or "Out of Stock" items, leaving no room for ambiguity.

## 6. How to Run

### 1. Prerequisites
- Python 3.9+
- Groq API Key

### 2. Setup
```bash
# Clone the repository
git clone <repo-url>
cd GroundTruth_AI_Hack

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Environment Variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Generate Data (Optional)
The project comes with sample data, but you can regenerate it:
```bash
python generate_data.py  # Generates users.json and stores.json
python generate_pdf.py   # Generates the robust store_policies.pdf
```

### 4. Run the Application
Start the FastAPI server (which serves both the API and the Frontend):
```bash
uvicorn app.main:app --reload
```

### 5. Use the Agent
Simply open your browser and visit:
**`http://127.0.0.1:8000/`**

- Type a message in the chat interface (e.g., "How much is a Medium Masala Chai?").
- The agent will:
    1. Mask your PII.
    2. Retrieve your context (User: Zayan, Location: Mumbai).
    3. Search the PDF Knowledge Base.
    4. Generate a personalized response.


