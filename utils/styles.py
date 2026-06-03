def inject_custom_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: rgba(255, 255, 255, 0.04);
    --bg-card-hover: rgba(255, 255, 255, 0.07);
    --border-color: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(99, 102, 241, 0.4);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-primary: #6366f1;
    --accent-secondary: #8b5cf6;
    --accent-cyan: #06b6d4;
    --verified: #10d9a0;
    --inaccurate: #f59e0b;
    --false: #ef4444;
    --gradient-hero: linear-gradient(135deg, #0a0e1a 0%, #1a1040 50%, #0a0e1a 100%);
    --gradient-accent: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
    --gradient-card: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.05));
    --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.2);
    --radius-card: 16px;
    --radius-btn: 10px;
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background: var(--gradient-hero);
    min-height: 100vh;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--accent-primary); border-radius: 3px; }

/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
header[data-testid="stHeader"] { background: transparent; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10, 14, 26, 0.95);
    border-right: 1px solid var(--border-color);
    backdrop-filter: blur(20px);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Hero Header */
.hero-header {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.2));
    border: 1px solid rgba(99,102,241,0.4);
    color: var(--accent-primary);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.5rem;
    animation: fadeInDown 0.6s ease;
}

.hero-title {
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    background: var(--gradient-accent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    animation: fadeInUp 0.7s ease;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto 2rem;
    line-height: 1.7;
    animation: fadeInUp 0.8s ease;
}

/* Glass Cards */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-card);
    padding: 1.5rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: var(--shadow-card);
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease;
}

.glass-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-card), var(--shadow-glow);
    transform: translateY(-2px);
}

/* KPI Metric Cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-card);
    padding: 1.25rem 1rem;
    text-align: center;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--gradient-accent);
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-glow);
    border-color: var(--border-hover);
}

.metric-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-accent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.25rem;
}

.metric-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Status Badges */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.status-verified {
    background: rgba(16, 217, 160, 0.15);
    border: 1px solid rgba(16, 217, 160, 0.3);
    color: var(--verified);
}

.status-inaccurate {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: var(--inaccurate);
}

.status-false {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: var(--false);
}

/* Claim Result Cards */
.claim-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-card);
    padding: 1.25rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(20px);
    transition: all 0.25s ease;
}

.claim-card:hover {
    border-color: var(--border-hover);
    background: var(--bg-card-hover);
}

.claim-text {
    font-size: 0.95rem;
    color: var(--text-primary);
    font-weight: 500;
    margin-bottom: 0.75rem;
    line-height: 1.6;
}

.claim-reason {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 0.5rem;
}

.claim-source {
    font-size: 0.75rem;
    color: var(--accent-cyan);
    font-family: 'JetBrains Mono', monospace;
}

.correct-fact {
    background: rgba(6, 182, 212, 0.08);
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 8px;
    padding: 0.6rem 0.85rem;
    font-size: 0.82rem;
    color: var(--accent-cyan);
    margin-top: 0.5rem;
}

/* Confidence Bar */
.confidence-bar-wrapper {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.confidence-bar-bg {
    flex: 1;
    height: 4px;
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    overflow: hidden;
}

.confidence-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: var(--gradient-accent);
    transition: width 1s ease;
}

.confidence-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    min-width: 32px;
    text-align: right;
}

/* Upload Area */
.upload-zone {
    background: var(--bg-card);
    border: 2px dashed rgba(99, 102, 241, 0.3);
    border-radius: var(--radius-card);
    padding: 3rem 2rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.upload-zone:hover {
    border-color: var(--accent-primary);
    background: rgba(99, 102, 241, 0.05);
}

.upload-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

/* Pipeline Steps */
.pipeline-steps {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1.5rem 0;
}

.pipeline-step {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 100px;
    padding: 0.4rem 1rem;
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.pipeline-step.active {
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.2));
    border-color: var(--accent-primary);
    color: var(--text-primary);
}

.pipeline-step.done {
    background: rgba(16, 217, 160, 0.1);
    border-color: rgba(16, 217, 160, 0.3);
    color: var(--verified);
}

.step-arrow {
    color: var(--text-muted);
    font-size: 0.7rem;
}

/* Divider */
.section-divider {
    height: 1px;
    background: var(--border-color);
    margin: 2rem 0;
}

/* Section Title */
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.section-subtitle {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-btn) !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stFileUploader {
    background: var(--bg-card) !important;
    border: 2px dashed rgba(99, 102, 241, 0.3) !important;
    border-radius: var(--radius-card) !important;
    padding: 1rem !important;
}

.stProgress > div > div > div > div {
    background: var(--gradient-accent) !important;
    border-radius: 4px !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-btn) !important;
    color: var(--text-primary) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius-card) !important;
    padding: 0.25rem !important;
    gap: 0.25rem !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.3)) !important;
    color: var(--text-primary) !important;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.animate-pulse { animation: pulse 2s ease-in-out infinite; }

/* Sidebar nav styles */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0;
    margin-bottom: 1.5rem;
}

.sidebar-logo-icon {
    width: 36px;
    height: 36px;
    background: var(--gradient-accent);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}

.sidebar-logo-text {
    font-size: 1.1rem;
    font-weight: 700;
    background: var(--gradient-accent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.info-chip {
    display: inline-block;
    background: rgba(6, 182, 212, 0.1);
    border: 1px solid rgba(6, 182, 212, 0.25);
    color: var(--accent-cyan);
    font-size: 0.72rem;
    padding: 0.2rem 0.6rem;
    border-radius: 100px;
    font-weight: 500;
}
</style>
"""
