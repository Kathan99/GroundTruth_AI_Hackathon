# H-002 | Customer Experience Automation

> **Tagline:** A privacy-first, context-aware AI agent that delivers hyper-personalized retail support in milliseconds using Groq and RAG.

## 1. The Problem 

**Context:** Retail customers today expect instant, relevant answers. They ask questions like "Is this store open?", "Do you have size 10 in stock?", or "Where is my order?".

**The Pain Point:** Standard chatbots are "dumb." They give generic FAQ answers. They don't know who the customer is, where they are standing, or what they like. A user standing outside a coffee shop in the rain doesn't want a link to the website; they want to## 🚀 How to Run

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

### 4. Run the Backend
Start the FastAPI server (with LangGraph agent):
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 5. Launch the Frontend
Simply open the `frontend/index.html` file in your browser:
```bash
open frontend/index.html  # Mac
# Or double-click the file in your file explorer
```

### 6. Usage
- Type a message in the chat interface (e.g., "How much is a Medium Masala Chai?").
- The agent will:
    1. Mask your PII.
    2. Retrieve your context (User: Zayan, Location: Mumbai).
    3. Search the PDF Knowledge Base.
    4. Generate a personalized response.
Andheri West outlet, come on in! We have your favorite **Masala Chai** ready, and here's a **20% off coupon** to warm you up."

## 3. Technical Approach

I built this system to be **Production-Ready**, focusing on modularity, privacy, and speed.

**System Architecture:**

1.  **Privacy Layer (PII Masking):**
    *   Before any data hits the LLM, it passes through **Microsoft Presidio**.
    *   I implemented custom regex recognizers to detect and mask Indian phone numbers (`+91-...`) and names.
    *   The LLM only sees `<PERSON>` or `<PHONE_NUMBER>`, ensuring user privacy.

2.  **Context Engine:**
    *   I built a custom engine that aggregates **User Data** (Preferences, Loyalty), **Store Data** (Stock, Hours), and **Location** (Haversine distance calculation).
    *   This structured context is injected dynamically into the System Prompt.

3.  **RAG Pipeline (Knowledge Base):**
    *   Static knowledge (Store Policies, Returns) is stored in **Qdrant** (Vector DB).
    *   We use **FastEmbed** for lightweight, fast embeddings.
    *   Relevant policies are retrieved and passed to the LLM to prevent hallucinations.

4.  **Generative AI (The Brain):**
    *   Powered by **Groq** (Llama 3.3 70B) for ultra-low latency inference.
    *   The prompt orchestrates all the inputs to generate a friendly, helpful, and accurate response.

## 4. Tech Stack

*   **Language:** Python 3.13
*   **API Framework:** FastAPI
*   **LLM Engine:** Groq (Llama 3.3 70B)
*   **Vector Database:** Qdrant (In-Memory for speed)
*   **Privacy:** Microsoft Presidio, Spacy
*   **PDF Processing:** PyPDF, ReportLab

## 5. Challenges & Learnings

*This project required balancing personalization with privacy.*

**Challenge 1: Privacy vs. Utility**
*   **Issue:** To be helpful, the bot needs to use the user's name and phone number. But sending PII to a cloud LLM is a security risk.
*   **Solution:** I implemented a **Bi-Directional Masking** strategy. The application layer holds the real data, while the LLM layer operates on tokens like `<PERSON>`. The application can re-hydrate the response if needed, or simply act on the intent without exposing raw data.

**Challenge 2: Qdrant API Changes**
*   **Issue:** During implementation, I encountered API mismatches with the `qdrant-client` library (missing `search` method).
*   **Solution:** I debugged the library version and switched to the robust `query_points` API, ensuring reliable vector retrieval.

## 6. Visual Proof

## 7. How to Run

