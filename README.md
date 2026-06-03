<div align="center">

# 🔍 TruthLayer AI
### AI-Powered Fact Checking Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google_Gemini-API-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![Tavily](https://img.shields.io/badge/Tavily-Search_API-6366F1?style=flat-square)](https://tavily.com)
[![License](https://img.shields.io/badge/License-MIT-10d9a0?style=flat-square)](LICENSE)

**Automatically detect, verify, and classify every factual claim in your PDF documents using live web search and advanced AI reasoning.**

[🚀 Live Demo](#demo) · [📖 Docs](#installation-guide) · [🐛 Report Bug](issues) · [✨ Features](#features)

---

</div>

## 📌 Overview

TruthLayer AI is a production-grade fact-checking platform that transforms any PDF document into a comprehensive verification report. It combines **Google Gemini's reasoning capabilities** with **Tavily's real-time web search** to extract factual claims, cross-reference them against trusted sources, and classify each as **Verified**, **Inaccurate**, or **False** — complete with confidence scores, source credibility ratings, and downloadable CSV reports.

Built for Product Managers, journalists, researchers, compliance teams, and anyone who needs to validate information at scale.

---

## ✨ Features

| Category | Feature |
|----------|---------|
| 📄 **Input** | PDF upload up to 50MB, multi-page support, metadata extraction |
| 🎯 **Detection** | Statistics, dates, percentages, company figures, financial data, technical claims |
| 🌐 **Verification** | Real-time Tavily web search with trusted source ranking |
| 🤖 **AI Evaluation** | Gemini 1.5 Flash reasoning with structured JSON output |
| 📊 **Dashboard** | Interactive Plotly charts — donut, histogram, scatter, timeline |
| 📈 **Scoring** | Per-claim confidence score + source credibility score |
| 🧹 **Quality** | Automatic duplicate claim removal via similarity filtering |
| 📥 **Export** | One-click CSV report download with all claim metadata |
| 🗂️ **History** | Session history with per-document verdict breakdowns |
| 🎨 **UI/UX** | Dark mode, glassmorphism, animated KPI cards, premium design |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TruthLayer AI Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📄 PDF Upload                                              │
│       │                                                     │
│       ▼                                                     │
│  📝 Text Extraction  ──────────  PyMuPDF                   │
│       │                                                     │
│       ▼                                                     │
│  🎯 Claim Detection  ──────────  Gemini 1.5 Flash           │
│       │                         (Structured JSON output)    │
│       ▼                                                     │
│  🧹 Deduplication   ──────────  Similarity filtering        │
│       │                         (SequenceMatcher > 82%)    │
│       ▼                                                     │
│  🌐 Web Search      ──────────  Tavily Search API           │
│  (per claim)                    (Advanced depth)            │
│       │                                                     │
│       ▼                                                     │
│  🤖 AI Evaluation   ──────────  Gemini 1.5 Flash           │
│       │                         (Evidence cross-reference)  │
│       ▼                                                     │
│  📊 Dashboard       ──────────  Plotly + Streamlit          │
│       │                                                     │
│       ▼                                                     │
│  📥 CSV Report      ──────────  Pandas                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Module Structure

```
truthlayer-ai/
├── app.py                      # Main entry point, upload UI, pipeline orchestration
├── pages/
│   ├── 01_analysis.py          # Interactive analysis dashboard (Plotly charts)
│   └── 02_history.py           # Session history with per-document breakdowns
├── services/
│   ├── pdf_service.py          # PyMuPDF text extraction + metadata
│   ├── claim_service.py        # Gemini claim extraction (structured JSON)
│   ├── search_service.py       # Tavily web search + evidence formatting
│   ├── verification_service.py # Gemini claim evaluation + scoring
│   └── report_service.py       # CSV generation + summary statistics
├── utils/
│   ├── config.py               # Environment variables, prompts, constants
│   ├── styles.py               # CSS injection (glassmorphism, dark theme)
│   └── helpers.py              # Deduplication, scoring, formatting utilities
├── .streamlit/
│   └── config.toml             # Streamlit dark theme + server config
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 📸 Screenshots

| Home Page | Analysis Dashboard |
|-----------|-------------------|
| *Upload PDF with drag-and-drop* | *Interactive Plotly charts* |

| Fact Check Results | Session History |
|-------------------|----------------|
| *Claim cards with confidence bars* | *Multi-session verdict breakdowns* |

---

## 🚀 Installation Guide

### Prerequisites

- Python 3.10 or higher
- [Google Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key) (free tier available)
- [Tavily API Key](https://tavily.com) (free tier: 1000 searches/month)

### Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/truthlayer-ai.git
cd truthlayer-ai
```

**2. Create a virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**5. Run the application**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 Environment Variables

| Variable | Required | Description | Get It |
|----------|----------|-------------|--------|
| `GEMINI_API_KEY` | ✅ Yes | Google Gemini API key for AI reasoning | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `TAVILY_API_KEY` | ✅ Yes | Tavily Search API key for web search | [Tavily Dashboard](https://app.tavily.com) |

---

## ☁️ Deployment on Streamlit Cloud

**1. Push to GitHub**
```bash
git init
git add .
git commit -m "feat: initial TruthLayer AI release"
git remote add origin https://github.com/yourusername/truthlayer-ai.git
git push -u origin main
```

**2. Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub repository
4. Set **Main file path**: `app.py`
5. Click **"Advanced settings"** → **Secrets**
6. Add your secrets:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   TAVILY_API_KEY = "your_tavily_api_key"
   ```
7. Click **"Deploy!"**

> ⚠️ **Important**: On Streamlit Cloud, use the Secrets manager instead of a `.env` file. The `python-dotenv` load will silently fail on Cloud, and the app will fall back to environment variables — which Streamlit Cloud injects automatically from your secrets.

---

## 🎬 Demo

### 30-Second Demo Script

```
[0:00] Open TruthLayer AI — hero page loads with animated gradient title
       "TruthLayer AI" and pipeline step indicators.

[0:05] Drag and drop a PDF (e.g., a company annual report or news article).
       File metadata appears: page count, file size.

[0:08] Click "Start Fact-Check Analysis" — progress bar activates.
       Step 1: PDF extraction.
       Step 2: Gemini detects 18 factual claims.
       Step 3: Each claim searched via Tavily in real-time.

[0:18] Progress completes. Success toast + balloons animation.
       KPI cards animate in: 18 Total, 12 Verified ✅, 4 Inaccurate ⚠️, 2 False ❌.
       Accuracy score: 66.7%.

[0:22] Scroll to claim cards. Each shows:
       - Claim text
       - Status badge (color-coded)
       - Reason from AI
       - Corrected fact (for False/Inaccurate)
       - Confidence bar + Source credibility bar

[0:27] Click "Open Full Dashboard" — Plotly donut chart, confidence histogram,
       scatter plot, and timeline render.

[0:30] Click "Download CSV Report" — report downloads instantly.
```

---

## 🔮 Future Improvements

- [ ] **Multi-document batch analysis** — process entire document sets
- [ ] **PDF annotation export** — highlight claims directly on the original PDF
- [ ] **Custom claim taxonomy** — user-defined claim categories
- [ ] **Webhook integration** — trigger analysis via API endpoint
- [ ] **Claim tracking over time** — detect if a claim changes across document versions
- [ ] **Team collaboration** — shared workspaces and annotation tools
- [ ] **OpenAI / Claude fallback** — multi-provider AI support
- [ ] **Browser extension** — fact-check web pages directly
- [ ] **Slack / Teams bot** — post-analysis summaries to channels
- [ ] **Audit trail** — full logging of every verification decision

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.35+, Custom CSS, Glassmorphism |
| **AI Reasoning** | Google Gemini 1.5 Flash |
| **Web Search** | Tavily Search API |
| **PDF Processing** | PyMuPDF (fitz) |
| **Data & Charts** | Pandas, Plotly |
| **Environment** | python-dotenv |
| **Deployment** | Streamlit Cloud / Any Python host |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ by the TruthLayer AI team · [Report Issues](issues) · [Star this repo ⭐](.)

</div>
