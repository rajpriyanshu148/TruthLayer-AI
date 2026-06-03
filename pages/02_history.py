import streamlit as st
from datetime import datetime

from utils.styles import inject_custom_css
from utils.config import STATUS_COLORS, STATUS_ICONS
from services.report_service import generate_csv_report

st.set_page_config(
    page_title="Session History – TruthLayer AI",
    page_icon="🗂️",
    layout="wide",
)
st.markdown(inject_custom_css(), unsafe_allow_html=True)


def render_history_card(i: int, entry: dict):
    stats = entry["stats"]
    total = stats.get("total", 0)
    verified = stats.get("verified", 0)
    inaccurate = stats.get("inaccurate", 0)
    false_count = stats.get("false", 0)
    accuracy = stats.get("accuracy_score", 0)

    verified_pct = int((verified / total * 100) if total > 0 else 0)
    inaccurate_pct = int((inaccurate / total * 100) if total > 0 else 0)
    false_pct = int((false_count / total * 100) if total > 0 else 0)

    st.markdown(f"""
    <div class="glass-card" style="margin-bottom:1rem;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
            <div>
                <div style="font-weight:700;font-size:1rem;color:var(--text-primary);margin-bottom:0.25rem;">
                    📄 {entry['filename']}
                </div>
                <div style="font-size:0.78rem;color:var(--text-muted);">{entry['timestamp']}</div>
            </div>
            <div style="display:flex;gap:1rem;flex-wrap:wrap;">
                <div style="text-align:center;">
                    <div style="font-size:1.3rem;font-weight:800;color:var(--verified);">{verified}</div>
                    <div style="font-size:0.68rem;color:var(--text-muted);">Verified</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem;font-weight:800;color:var(--inaccurate);">{inaccurate}</div>
                    <div style="font-size:0.68rem;color:var(--text-muted);">Inaccurate</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem;font-weight:800;color:var(--false);">{false_count}</div>
                    <div style="font-size:0.68rem;color:var(--text-muted);">False</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem;font-weight:800;background:var(--gradient-accent);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{accuracy}%</div>
                    <div style="font-size:0.68rem;color:var(--text-muted);">Accuracy</div>
                </div>
            </div>
        </div>
        <div style="margin-top:1rem;">
            <div style="display:flex;height:6px;border-radius:3px;overflow:hidden;gap:2px;">
                <div style="flex:{verified_pct};background:#10d9a0;border-radius:3px;"></div>
                <div style="flex:{inaccurate_pct};background:#f59e0b;border-radius:3px;"></div>
                <div style="flex:{false_pct};background:#ef4444;border-radius:3px;"></div>
            </div>
            <div style="display:flex;gap:1rem;margin-top:0.4rem;font-size:0.7rem;color:var(--text-muted);">
                <span><span style="color:#10d9a0;">■</span> {verified_pct}% Verified</span>
                <span><span style="color:#f59e0b;">■</span> {inaccurate_pct}% Inaccurate</span>
                <span><span style="color:#ef4444;">■</span> {false_pct}% False</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📊 View Dashboard", key=f"view_{i}", use_container_width=True):
            st.session_state.current_results = entry
            st.switch_page("pages/01_analysis.py")
    with col2:
        csv_bytes = generate_csv_report(entry["results"])
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_bytes,
            file_name=f"truthlayer_{i}_{ts}.csv",
            mime="text/csv",
            key=f"download_{i}",
            use_container_width=True,
        )


def main():
    st.markdown("""
    <div class="hero-header" style="padding:2rem 1rem 1rem;">
        <div class="hero-badge">🗂️ Session History</div>
        <div class="hero-title" style="font-size:2.5rem;">Past Analyses</div>
        <div class="hero-subtitle">View and download reports from all fact-check sessions in this session.</div>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.get("history", [])

    if not history:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem 2rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">📭</div>
            <div style="font-size:1.1rem;font-weight:600;color:var(--text-primary);margin-bottom:0.5rem;">No analyses yet</div>
            <div style="font-size:0.85rem;color:var(--text-muted);">Upload a PDF on the Home page to get started.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Go to Home & Upload"):
            st.switch_page("app.py")
        return

    st.markdown(f"<div class='section-subtitle'>{len(history)} analysis session(s) in history</div>", unsafe_allow_html=True)

    col_actions = st.columns([1, 3])
    with col_actions[0]:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.pop("current_results", None)
            st.rerun()

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    for i, entry in enumerate(history):
        render_history_card(i, entry)


main()
