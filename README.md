# Ingredient Copilot 🧠

**"Designing AI-Native Consumer Health Experiences"**

Ingredient Copilot is an AI-native web application built for a hackathon. It helps users understand food ingredients at the moment of decision. Unlike traditional database-backed apps, it uses reasoning-driven AI to infer intent and provide narrative, health-conscious explanations.

## 🚀 AI-Native Experience
- **Intent Inference**: No forms, no health questionnaires. The AI silenty reasons about what matters to you based on the ingredient list.
- **Narrative Reasoning**: Instead of a list of definitions, you get a story about why these ingredients matter, what's uncertain, and how to think about them.
- **Honest Uncertainty**: The AI communicates when evidence is mixed or when quantity matters, avoiding absolute medical claims.

## 🛠 Tech Stack
- **Frontend**: Next.js (App Router), Vanilla CSS (Glassmorphism), React.
- **Backend**: FastAPI (Python), Google Gemini AI (Generative AI).
- **Deployment**: Vercel (Frontend) / Render (Backend) friendly.

## 📦 Setup & Installation

### Backend
1. Navigate to `backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file from `.env.example` and add your `GOOGLE_API_KEY`.
6. Run the server: `python main.py`

### Frontend
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
4. Open [http://localhost:3000](http://localhost:3000)

## 🧠 Architecture
- **Inference Engine**: Located in `backend/ai_engine.py`, uses a custom system prompt to guide LLM reasoning towards consumer health contexts.
- **UI Design System**: Located in `frontend/app/globals.css`, focused on a minimal, premium, glassmorphic aesthetic to reduce cognitive load.

## 🧪 Hackathon Alignment
- **AI-Native**: Focused on reasoning and intent, not data lookup.
- **Explainability**: Clear "Why" and "What's Uncertain" sections.
- **Technical Execution**: Modular FastAPI backend + performant React frontend.

---
Built with ❤️ for the Consumer Health Hackathon.
