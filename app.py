import streamlit as st
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.styles import inject_custom_css
from utils.config import get_api_key, STATUS_COLORS, STATUS_ICONS
from services.pdf_service import extract_text_from_pdf, get_pdf_metadata
from services.claim_service import extract_claims
from services.search_service import search_claim, format_evidence
from services.verification_service import verify_claim
from services.report_service import generate_csv_report, generate_summary_stats

st.set_page_config(
    page_title="TruthLayer AI – Fact Checking Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(inject_custom_css(), unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🔍</div>
            <div class="sidebar-logo-text">TruthLayer AI</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Navigation**")
        st.page_link("app.py", label="🏠 Home & Upload", icon=None)
        st.page_link("pages/01_analysis.py", label="📊 Analysis Dashboard", icon=None)
        st.page_link("pages/02_history.py", label="🗂️ Session History", icon=None)

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

        gemini_key = get_api_key("GEMINI_API_KEY")
        tavily_key = get_api_key("TAVILY_API_KEY")
        keys_ok = bool(gemini_key) and bool(tavily_key)

        if keys_ok:
            st.markdown(
                "<span class='info-chip' style='border-color:rgba(16,217,160,0.3);"
                "color:#10d9a0;background:rgba(16,217,160,0.08)'>✅ APIs Connected</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<span class='info-chip' style='border-color:rgba(239,68,68,0.3);"
                "color:#ef4444;background:rgba(239,68,68,0.08)'>⚠️ API Keys Missing</span>",
                unsafe_allow_html=True,
            )

        with st.expander("🔑 Configure API Keys", expanded=not keys_ok):
            st.markdown(
                "<div style='font-size:0.75rem;color:var(--text-muted);margin-bottom:0.75rem;'>"
                "Enter your keys below <b>or</b> add them to a <code>.env</code> file.</div>",
                unsafe_allow_html=True,
            )
            new_gemini = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="AIza...",
                value=st.session_state.get("_runtime_GEMINI_API_KEY", ""),
                key="_input_gemini",
                help="Get yours free at aistudio.google.com",
            )
            new_tavily = st.text_input(
                "Tavily API Key",
                type="password",
                placeholder="tvly-...",
                value=st.session_state.get("_runtime_TAVILY_API_KEY", ""),
                key="_input_tavily",
                help="Get yours free at app.tavily.com",
            )
            if st.button("💾 Save Keys", use_container_width=True):
                if new_gemini:
                    st.session_state["_runtime_GEMINI_API_KEY"] = new_gemini
                if new_tavily:
                    st.session_state["_runtime_TAVILY_API_KEY"] = new_tavily
                st.rerun()

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:0.72rem; color: var(--text-muted); line-height:1.8;'>
        <b style='color:var(--text-secondary)'>Pipeline</b><br>
        1. Upload PDF<br>
        2. Extract Text<br>
        3. Detect Claims<br>
        4. Web Verification<br>
        5. AI Evaluation<br>
        6. Generate Report
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:0.68rem; color: var(--text-muted); text-align:center;'>
        TruthLayer AI v1.0.0<br>Powered by Gemini + Tavily
        </div>
        """, unsafe_allow_html=True)


def render_hero():
    st.markdown("""
    <div class="hero-header">
        <div class="hero-badge">🔬 AI-Powered Fact Verification</div>
        <div class="hero-title">TruthLayer AI</div>
        <div class="hero-subtitle">
            Automatically detect, extract, and verify factual claims in any PDF document
            using real-time web search and advanced AI reasoning.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pipeline-steps">
        <div class="pipeline-step">📄 Upload PDF</div>
        <span class="step-arrow">›</span>
        <div class="pipeline-step">📝 Extract Text</div>
        <span class="step-arrow">›</span>
        <div class="pipeline-step">🎯 Detect Claims</div>
        <span class="step-arrow">›</span>
        <div class="pipeline-step">🌐 Web Search</div>
        <span class="step-arrow">›</span>
        <div class="pipeline-step">🤖 AI Evaluate</div>
        <span class="step-arrow">›</span>
        <div class="pipeline-step">📊 Report</div>
    </div>
    """, unsafe_allow_html=True)


def render_feature_cards():
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("🎯", "Claim Detection", "Extracts statistics, figures, dates, and assertions from any document"),
        ("🌐", "Live Verification", "Cross-references claims against trusted web sources in real-time"),
        ("🤖", "AI Reasoning", "Gemini evaluates evidence and provides nuanced fact-check verdicts"),
        ("📊", "Visual Reports", "Interactive dashboards with downloadable CSV analysis reports"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:1.5rem 1rem;">
                <div style="font-size:2rem; margin-bottom:0.75rem;">{icon}</div>
                <div style="font-weight:700; font-size:0.9rem; color:var(--text-primary); margin-bottom:0.5rem;">{title}</div>
                <div style="font-size:0.78rem; color:var(--text-muted); line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def _search_and_verify(claim_obj: dict) -> dict:
    claim = claim_obj.get("claim", "")
    search_result = search_claim(claim)
    evidence = format_evidence(search_result)
    sources = search_result.get("sources", [])
    return verify_claim(claim, evidence, sources)


def run_fact_check_pipeline(file_bytes: bytes, filename: str):
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚡ Running Fact-Check Pipeline</div>", unsafe_allow_html=True)

    progress_bar = st.progress(0)
    status_text = st.empty()
    start_time = time.time()

    # Step 1: Extract text
    status_text.markdown("**Step 1/4** — Extracting text from PDF...")
    try:
        text = extract_text_from_pdf(file_bytes)
        meta = get_pdf_metadata(file_bytes)
        progress_bar.progress(10)
    except Exception as e:
        st.error(f"PDF extraction failed: {e}")
        return

    # Step 2: Extract claims
    status_text.markdown("**Step 2/4** — Detecting factual claims with AI...")
    try:
        claims = extract_claims(text)
        progress_bar.progress(30)
    except Exception as e:
        st.error(f"Claim extraction failed: {e}")
        return

    if not claims:
        st.warning("No factual claims were detected in this document.")
        progress_bar.progress(100)
        status_text.empty()
        return

    st.info(f"Detected **{len(claims)} unique factual claims** — verifying concurrently...")

    # Step 3: Parallel search + verify
    status_text.markdown(f"**Step 3/4** — Verifying {len(claims)} claims in parallel (web search + AI)...")
    results = [None] * len(claims)
    completed = 0
    max_workers = min(4, len(claims))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(_search_and_verify, claim_obj): i
            for i, claim_obj in enumerate(claims)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                results[idx] = {
                    "claim": claims[idx].get("claim", ""),
                    "status": "Inaccurate",
                    "confidence": 0.2,
                    "reason": f"Verification failed: {e}",
                    "correct_fact": "",
                    "source": "",
                    "source_credibility": 0.2,
                }
            completed += 1
            pct = 30 + int((completed / len(claims)) * 60)
            progress_bar.progress(pct)
            status_text.markdown(
                f"**Step 3/4** — Verified {completed}/{len(claims)} claims "
                f"({round((completed/len(claims))*100)}% complete)..."
            )

    elapsed = round(time.time() - start_time, 1)
    progress_bar.progress(95)
    status_text.markdown("**Step 4/4** — Generating analysis report...")
    time.sleep(0.3)

    # Store in session state
    stats = generate_summary_stats(results)
    session_entry = {
        "filename": filename,
        "metadata": meta,
        "results": results,
        "stats": stats,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "elapsed_seconds": elapsed,
    }
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.insert(0, session_entry)
    st.session_state.current_results = session_entry

    progress_bar.progress(100)
    status_text.empty()

    st.success(f"Analysis complete — **{len(results)} claims** verified in **{elapsed}s**")
    st.balloons()

    render_results_preview(results, stats)


def render_results_preview(results: list, stats: dict):
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Results Overview</div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, "📋", stats["total"], "Total Claims"),
        (c2, "✅", stats["verified"], "Verified"),
        (c3, "⚠️", stats["inaccurate"], "Inaccurate"),
        (c4, "❌", stats["false"], "False"),
        (c5, "🎯", f"{stats['accuracy_score']}%", "Accuracy"),
    ]
    for col, icon, val, label in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("<div class='section-title' style='font-size:1.1rem;'>🔍 Claim Details</div>", unsafe_allow_html=True)
        for r in results:
            status = r.get("status", "Inaccurate")
            icon = STATUS_ICONS.get(status, "⚠️")
            color = STATUS_COLORS.get(status, "#ffb347")
            confidence_pct = int(r.get("confidence", 0.5) * 100)
            credibility_pct = int(r.get("source_credibility", 0.5) * 100)
            correct_html = ""
            if r.get("correct_fact") and status != "Verified":
                correct_html = f"<div class='correct-fact'>✏️ <b>Correct Fact:</b> {r['correct_fact']}</div>"

            st.markdown(f"""
            <div class="claim-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.75rem;">
                    <div class="claim-text" style="flex:1;">{r.get('claim','')}</div>
                    <span class="status-badge status-{status.lower()}" style="margin-left:1rem;white-space:nowrap;">
                        {icon} {status}
                    </span>
                </div>
                <div class="claim-reason">{r.get('reason','')}</div>
                {correct_html}
                <div class="claim-source">🔗 {r.get('source','') or 'No source'}</div>
                <div class="confidence-bar-wrapper" style="margin-top:0.75rem;">
                    <span style="font-size:0.7rem;color:var(--text-muted);min-width:80px;">Confidence</span>
                    <div class="confidence-bar-bg">
                        <div class="confidence-bar-fill" style="width:{confidence_pct}%;background:{'var(--gradient-accent)' if status=='Verified' else '#f59e0b' if status=='Inaccurate' else '#ef4444'};"></div>
                    </div>
                    <span class="confidence-label">{confidence_pct}%</span>
                </div>
                <div class="confidence-bar-wrapper">
                    <span style="font-size:0.7rem;color:var(--text-muted);min-width:80px;">Source Cred.</span>
                    <div class="confidence-bar-bg">
                        <div class="confidence-bar-fill" style="width:{credibility_pct}%;background:var(--gradient-accent);"></div>
                    </div>
                    <span class="confidence-label">{credibility_pct}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-title' style='font-size:1.1rem;'>📥 Download Report</div>", unsafe_allow_html=True)
        csv_bytes = generate_csv_report(results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        st.download_button(
            label="⬇️ Download CSV Report",
            data=csv_bytes,
            file_name=f"truthlayer_report_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='font-size:0.82rem;'>
            <div style='margin-bottom:0.5rem; font-weight:600; color:var(--text-primary);'>📈 Summary Stats</div>
            <div style='color:var(--text-muted);line-height:2;'>
                <span style='color:var(--verified);'>●</span> Verified: {stats['verified']}<br>
                <span style='color:var(--inaccurate);'>●</span> Inaccurate: {stats['inaccurate']}<br>
                <span style='color:var(--false);'>●</span> False: {stats['false']}<br>
                <br>
                <span style='color:var(--text-secondary);'>Avg Confidence: {stats['avg_confidence']}%</span><br>
                <span style='color:var(--text-secondary);'>Generated: {stats['generated_at']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 Open Full Dashboard", use_container_width=True):
            st.switch_page("pages/01_analysis.py")


def main():
    render_sidebar()
    render_hero()

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    render_feature_cards()
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col_upload, col_info = st.columns([3, 2])

    with col_upload:
        st.markdown("<div class='section-title'>📄 Upload PDF Document</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Upload any PDF — reports, articles, whitepapers, or research papers</div>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            label="Drop your PDF here",
            type=["pdf"],
            help="Maximum 50MB. The text will be extracted and analyzed for factual claims.",
            label_visibility="collapsed",
        )

        if uploaded_file:
            file_bytes = uploaded_file.read()
            meta = get_pdf_metadata(file_bytes)
            st.markdown(f"""
            <div class="glass-card" style="margin-top:1rem;">
                <div style="display:flex;align-items:center;gap:0.75rem;">
                    <span style="font-size:2rem;">📄</span>
                    <div>
                        <div style="font-weight:600;color:var(--text-primary);">{uploaded_file.name}</div>
                        <div style="font-size:0.78rem;color:var(--text-muted);">
                            {meta['pages']} pages · {round(len(file_bytes)/1024, 1)} KB · PDF Document
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            start_btn = st.button("🚀 Start Fact-Check Analysis", use_container_width=True)
            if start_btn:
                if not get_api_key("GEMINI_API_KEY") or not get_api_key("TAVILY_API_KEY"):
                    st.error(
                        "Please add your API keys using the **Configure API Keys** panel "
                        "in the sidebar, or create a `.env` file with GEMINI_API_KEY and TAVILY_API_KEY."
                    )
                else:
                    run_fact_check_pipeline(file_bytes, uploaded_file.name)

    with col_info:
        st.markdown("<div class='section-title'>ℹ️ How It Works</div>", unsafe_allow_html=True)
        steps = [
            ("1", "Upload", "Any PDF document with factual content"),
            ("2", "Extract", "AI reads and structures all text from the PDF"),
            ("3", "Detect", "Gemini identifies all verifiable factual claims"),
            ("4", "Search", "Tavily searches trusted web sources for each claim"),
            ("5", "Evaluate", "Gemini cross-references evidence and classifies claims"),
            ("6", "Report", "Download a full CSV report with sources and confidence scores"),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div style="display:flex;gap:0.75rem;margin-bottom:0.75rem;align-items:flex-start;">
                <div style="width:28px;height:28px;border-radius:50%;background:var(--gradient-accent);
                            display:flex;align-items:center;justify-content:center;
                            font-size:0.72rem;font-weight:700;color:white;flex-shrink:0;margin-top:2px;">
                    {num}
                </div>
                <div>
                    <div style="font-weight:600;font-size:0.88rem;color:var(--text-primary);">{title}</div>
                    <div style="font-size:0.78rem;color:var(--text-muted);line-height:1.5;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.8;">
                <b style="color:var(--text-primary);">⚡ Claim Types Detected</b><br>
                • Statistics & percentages<br>
                • Dates & historical events<br>
                • Company & financial figures<br>
                • Scientific & technical facts<br>
                • Product & market claims<br>
                • Geopolitical statements
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
