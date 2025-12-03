# H-002 | Customer Experience Automation

> **Tagline:** A privacy-first, context-aware AI agent that delivers hyper-personalized retail support in milliseconds using Groq and RAG.

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

