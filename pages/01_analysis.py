import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from utils.styles import inject_custom_css
from utils.config import STATUS_COLORS, STATUS_ICONS
from services.report_service import generate_csv_report

st.set_page_config(
    page_title="Analysis Dashboard – TruthLayer AI",
    page_icon="📊",
    layout="wide",
)
st.markdown(inject_custom_css(), unsafe_allow_html=True)


def create_donut_chart(verified: int, inaccurate: int, false: int):
    labels = ["Verified", "Inaccurate", "False"]
    values = [verified, inaccurate, false]
    colors = ["#10d9a0", "#f59e0b", "#ef4444"]
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color="#0a0e1a", width=2)),
        textinfo="label+percent",
        textfont=dict(color="white", size=12, family="Inter"),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
    )])
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=20, l=20, r=20),
        height=280,
        annotations=[dict(
            text=f"<b>{verified+inaccurate+false}</b><br>Claims",
            x=0.5, y=0.5, font_size=16,
            font_color="white", font_family="Inter",
            showarrow=False,
        )],
    )
    return fig


def create_confidence_histogram(results: list):
    confidences = [r.get("confidence", 0.5) * 100 for r in results]
    statuses = [r.get("status", "Inaccurate") for r in results]
    df = pd.DataFrame({"Confidence": confidences, "Status": statuses})
    color_map = {"Verified": "#10d9a0", "Inaccurate": "#f59e0b", "False": "#ef4444"}
    fig = px.histogram(
        df, x="Confidence", color="Status",
        nbins=10, barmode="stack",
        color_discrete_map=color_map,
        labels={"Confidence": "Confidence Score (%)"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title_font_color="#94a3b8"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Count", title_font_color="#94a3b8"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="white"),
        bargap=0.1,
        height=280,
        margin=dict(t=20, b=40, l=40, r=20),
    )
    return fig


def create_credibility_scatter(results: list):
    df = pd.DataFrame([{
        "Claim": r.get("claim", "")[:40] + "...",
        "Confidence": round(r.get("confidence", 0.5) * 100, 1),
        "Credibility": round(r.get("source_credibility", 0.5) * 100, 1),
        "Status": r.get("status", "Inaccurate"),
    } for r in results])
    color_map = {"Verified": "#10d9a0", "Inaccurate": "#f59e0b", "False": "#ef4444"}
    fig = px.scatter(
        df, x="Credibility", y="Confidence",
        color="Status", color_discrete_map=color_map,
        hover_data=["Claim"],
        labels={"Credibility": "Source Credibility (%)", "Confidence": "Confidence Score (%)"},
    )
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color="#0a0e1a")))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="white"),
        height=280,
        margin=dict(t=20, b=40, l=40, r=20),
    )
    return fig


def create_status_timeline(results: list):
    x = list(range(1, len(results) + 1))
    y_conf = [r.get("confidence", 0.5) * 100 for r in results]
    colors = [STATUS_COLORS.get(r.get("status", "Inaccurate"), "#ffb347") for r in results]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y_conf,
        mode="lines+markers",
        line=dict(color="rgba(99,102,241,0.4)", width=2),
        marker=dict(color=colors, size=10, line=dict(color="#0a0e1a", width=1)),
        hovertemplate="Claim #%{x}<br>Confidence: %{y:.1f}%<extra></extra>",
        name="Confidence",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Inter"),
        xaxis=dict(title="Claim #", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(title="Confidence %", gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
        showlegend=False,
        height=280,
        margin=dict(t=20, b=40, l=40, r=20),
    )
    return fig


def render_dashboard(session: dict):
    stats = session["stats"]
    results = session["results"]
    filename = session["filename"]

    st.markdown(f"""
    <div class="hero-header" style="padding:2rem 1rem 1rem;">
        <div class="hero-badge">📊 Analysis Dashboard</div>
        <div class="hero-title" style="font-size:2.5rem;">Fact-Check Report</div>
        <div class="hero-subtitle">{filename} · {session['timestamp']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, "📋", stats["total"], "Total Claims"),
        (c2, "✅", stats["verified"], "Verified"),
        (c3, "⚠️", stats["inaccurate"], "Inaccurate"),
        (c4, "❌", stats["false"], "False"),
        (c5, "🎯", f"{stats['accuracy_score']}%", "Accuracy Score"),
    ]
    for col, icon, val, label in kpis:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    chart_c1, chart_c2 = st.columns(2)
    with chart_c1:
        st.markdown("<div class='section-title' style='font-size:1rem;'>📊 Verdict Distribution</div>", unsafe_allow_html=True)
        st.plotly_chart(
            create_donut_chart(stats["verified"], stats["inaccurate"], stats["false"]),
            use_container_width=True, config={"displayModeBar": False},
        )
    with chart_c2:
        st.markdown("<div class='section-title' style='font-size:1rem;'>📈 Confidence Distribution</div>", unsafe_allow_html=True)
        st.plotly_chart(
            create_confidence_histogram(results),
            use_container_width=True, config={"displayModeBar": False},
        )

    chart_c3, chart_c4 = st.columns(2)
    with chart_c3:
        st.markdown("<div class='section-title' style='font-size:1rem;'>🔗 Confidence vs Source Credibility</div>", unsafe_allow_html=True)
        st.plotly_chart(
            create_credibility_scatter(results),
            use_container_width=True, config={"displayModeBar": False},
        )
    with chart_c4:
        st.markdown("<div class='section-title' style='font-size:1rem;'>📉 Confidence Timeline</div>", unsafe_allow_html=True)
        st.plotly_chart(
            create_status_timeline(results),
            use_container_width=True, config={"displayModeBar": False},
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔍 All Claims</div>", unsafe_allow_html=True)

    filter_status = st.selectbox(
        "Filter by Status",
        options=["All", "Verified", "Inaccurate", "False"],
        key="dashboard_filter",
    )
    filtered = results if filter_status == "All" else [r for r in results if r.get("status") == filter_status]

    st.markdown(f"<div class='section-subtitle'>Showing {len(filtered)} of {len(results)} claims</div>", unsafe_allow_html=True)

    for r in filtered:
        status = r.get("status", "Inaccurate")
        icon = STATUS_ICONS.get(status, "⚠️")
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
                    <div class="confidence-bar-fill" style="width:{confidence_pct}%;"></div>
                </div>
                <span class="confidence-label">{confidence_pct}%</span>
            </div>
            <div class="confidence-bar-wrapper">
                <span style="font-size:0.7rem;color:var(--text-muted);min-width:80px;">Source Cred.</span>
                <div class="confidence-bar-bg">
                    <div class="confidence-bar-fill" style="width:{credibility_pct}%;"></div>
                </div>
                <span class="confidence-label">{credibility_pct}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    csv_bytes = generate_csv_report(results)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    st.download_button(
        label="⬇️ Download Full CSV Report",
        data=csv_bytes,
        file_name=f"truthlayer_report_{timestamp}.csv",
        mime="text/csv",
        use_container_width=False,
    )


def main():
    st.markdown(inject_custom_css(), unsafe_allow_html=True)

    if "current_results" not in st.session_state or not st.session_state.current_results:
        st.markdown("""
        <div class="hero-header">
            <div class="hero-badge">📊 Analysis Dashboard</div>
            <div class="hero-title" style="font-size:2.5rem;">No Analysis Yet</div>
            <div class="hero-subtitle">Upload a PDF on the Home page to run a fact-check analysis first.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Go to Home & Upload", use_container_width=False):
            st.switch_page("app.py")
        return

    render_dashboard(st.session_state.current_results)


main()
