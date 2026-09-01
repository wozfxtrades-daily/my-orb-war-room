import streamlit as st
from datetime import datetime

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="THE ORB | War Room",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Custom CSS – dark-orange theme matching the original
# -------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {
        background-color: #0a0c10 !important;
        color: #e8eaed !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden !important;
        height: 0 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0d0f14 !important;
        border-right: 1px solid #1a1d24 !important;
        min-width: 260px !important;
        max-width: 260px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem !important;
    }

    .main .block-container {
        padding: 1rem 1.5rem 2rem 1.5rem !important;
        max-width: 100% !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    .orb-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        margin-bottom: 8px;
    }

    .orb-logo-icon {
        width: 32px;
        height: 32px;
        border: 1.5px solid #f0a030;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #f0a030;
        font-weight: 700;
        font-size: 14px;
    }

    .orb-logo-text {
        font-size: 18px;
        font-weight: 700;
        color: #f0a030;
        letter-spacing: 0.05em;
    }

    .orb-subtitle {
        font-size: 11px;
        color: #6b7280;
        letter-spacing: 0.08em;
        margin-left: 42px;
        margin-top: -4px;
        margin-bottom: 24px;
    }

    .nav-section-label {
        font-size: 10px;
        color: #4b5563;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0 16px;
        margin-bottom: 8px;
        margin-top: 8px;
    }

    .data-link-box {
        background: #111318;
        border: 1px solid #1e2229;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 12px;
    }

    .data-link-title {
        font-size: 10px;
        color: #6b7280;
        letter-spacing: 0.08em;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .data-link-live {
        color: #22c55e;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .trader-info {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 4px;
        color: #9ca3af;
        font-size: 13px;
    }

    .trader-avatar {
        width: 28px;
        height: 28px;
        background: #f0a030;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0a0c10;
        font-weight: 700;
        font-size: 12px;
    }

    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0 16px 0;
        border-bottom: 1px solid #1a1d24;
        margin-bottom: 20px;
    }

    .top-bar-left {
        font-size: 12px;
        color: #6b7280;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .top-bar-right {
        display: flex;
        align-items: center;
        gap: 16px;
        font-size: 12px;
        color: #9ca3af;
    }

    .hero-card {
        background: linear-gradient(180deg, #12151c 0%, #0e1117 100%);
        border: 1px solid #1e2229;
        border-radius: 12px;
        padding: 40px 48px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .hero-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(240, 160, 48, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(240, 160, 48, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
    }

    .hero-label {
        font-size: 11px;
        color: #f0a030;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 600;
        line-height: 1.15;
        color: #f3f4f6;
        margin-bottom: 12px;
        letter-spacing: -0.03em;
    }

    .hero-title .accent {
        color: #f0a030;
    }

    .hero-desc {
        font-size: 15px;
        color: #9ca3af;
        max-width: 520px;
        line-height: 1.5;
        margin-bottom: 28px;
    }

    .stat-card {
        background: #111318;
        border: 1px solid #1e2229;
        border-radius: 10px;
        padding: 16px 18px;
    }

    .stat-label {
        font-size: 10px;
        color: #6b7280;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .stat-value {
        font-size: 22px;
        font-weight: 600;
        color: #f3f4f6;
        letter-spacing: -0.02em;
    }

    .stat-sub {
        font-size: 11px;
        color: #22c55e;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }

    .section-title {
        font-size: 13px;
        color: #9ca3af;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .section-title .num {
        color: #f0a030;
    }

    .headline-card {
        background: #111318;
        border: 1px solid #1e2229;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 10px;
        transition: border-color 0.15s;
    }

    .headline-card:hover {
        border-color: #2a2e36;
    }

    .headline-meta {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
        font-size: 11px;
        color: #6b7280;
    }

    .headline-tag {
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .tag-short {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .tag-long {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .tag-mixed {
        background: rgba(240, 160, 48, 0.15);
        color: #f0a030;
        border: 1px solid rgba(240, 160, 48, 0.3);
    }

    .headline-text {
        font-size: 14px;
        color: #e5e7eb;
        line-height: 1.4;
        margin-bottom: 8px;
    }

    .headline-actions {
        font-size: 11px;
        color: #6b7280;
        display: flex;
        gap: 14px;
    }

    .bias-mini-card {
        background: #111318;
        border: 1px solid #1e2229;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    .bias-tf {
        font-size: 18px;
        font-weight: 600;
        color: #f3f4f6;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .bias-bar {
        height: 6px;
        background: #1e2229;
        border-radius: 3px;
        margin-bottom: 8px;
        overflow: hidden;
    }

    .bias-bar-fill {
        height: 100%;
        border-radius: 3px;
    }

    .bias-note {
        font-size: 12px;
        color: #9ca3af;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {
        background-color: #0d0f14 !important;
        border: 1px solid #2a2e36 !important;
        border-radius: 6px !important;
        color: #e5e7eb !important;
        font-size: 14px !important;
    }

    .stTextInput > label,
    .stSelectbox > label,
    .stNumberInput > label,
    .stSlider > label,
    .stTextArea > label {
        color: #6b7280 !important;
        font-size: 11px !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }

    .stSlider > div > div > div > div {
        background-color: #f0a030 !important;
    }

    .card {
        background: #111318;
        border: 1px solid #1e2229;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: #f3f4f6;
        margin-bottom: 4px;
    }

    .event-row {
        display: flex;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #1a1d24;
        font-size: 13px;
    }

    .event-time {
        width: 60px;
        color: #9ca3af;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
    }

    .event-flag {
        width: 24px;
        margin-right: 8px;
    }

    .event-name {
        flex: 1;
        color: #e5e7eb;
    }

    .event-vals {
        color: #6b7280;
        font-size: 12px;
        text-align: right;
    }

    .replit-badge {
        position: fixed;
        bottom: 16px;
        right: 16px;
        background: #1a1d24;
        border: 1px solid #2a2e36;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        color: #9ca3af;
        z-index: 100;
    }

    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0c10;
    }
    ::-webkit-scrollbar-thumb {
        background: #2a2e36;
        border-radius: 3px;
    }

    .stButton > button {
        background-color: #f0a030 !important;
        color: #0a0c10 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.03em !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.15s !important;
    }

    .stButton > button:hover {
        background-color: #f5b040 !important;
        color: #0a0c10 !important;
        border: none !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: #1a1d24 !important;
        color: #e5e7eb !important;
        border: 1px solid #2a2e36 !important;
    }

    div[data-testid="stHorizontalBlock"] > div {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "War Room"

if "trades" not in st.session_state:
    st.session_state.trades = [
        {
            "instrument": "NQ",
            "direction": "LONG",
            "setup": "Opening range reclaim",
            "levels": "19142.50 / 19108.25 / 19215.00",
            "grade": "A",
            "result": "PLANNED",
            "date": "AUG 31"
        }
    ]

if "bias" not in st.session_state:
    st.session_state.bias = {
        "5m":  {"dir": "LONG",  "conv": 72, "note": "Holding above the opening range midpoint."},
        "15m": {"dir": "MIXED", "conv": 54, "note": "Compression into the prior day high."},
        "1h":  {"dir": "SHORT", "conv": 61, "note": "Still below the weekly VWAP band."}
    }

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="orb-logo">
        <div class="orb-logo-icon">⬡</div>
        <div class="orb-logo-text">THE ORB</div>
    </div>
    <div class="orb-subtitle">WAR ROOM / 01</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">COMMAND CENTER</div>', unsafe_allow_html=True)

    pages = {
        "War Room":      ("LIVE DESK", "⬛"),
        "Trade Journal": ("LOG & REVIEW", "📓"),
        "Bias Matrix":   ("MULTI-TIMEFRAME", "⊞")
    }

    for name, (sub, icon) in pages.items():
        active = st.session_state.page == name
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = name
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="data-link-box">
        <div class="data-link-title">
            <span style="color:#22c55e">●</span> DATA LINK ACTIVE
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:6px;">
            <span style="color:#e5e7eb; font-size:13px; font-weight:500;">NYSE / NASDAQ</span>
            <span class="data-link-live">LIVE</span>
        </div>
    </div>
    <div class="trader-info">
        <div class="trader-avatar">AR</div>
        <div>
            <div style="color:#e5e7eb; font-weight:500;">Active trader</div>
            <div style="font-size:11px; color:#6b7280;">NEW YORK / 09:41 ET</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# TOP BAR
# -------------------------------------------------
now = datetime.now()
time_str = now.strftime("%I:%M %p GMT+3")

st.markdown(f"""
<div class="top-bar">
    <div class="top-bar-left">NYSE / OPENING RANGE DESK</div>
    <div class="top-bar-right">
        <span>◷ {time_str}</span>
        <span>🔔</span>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.session_state.page

# =================================================
# WAR ROOM
# =================================================
if page == "War Room":

    st.markdown("""
    <div class="hero-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div class="hero-label">⚡ MARKET OPEN PROTOCOL</div>
            <div style="font-size:11px; color:#6b7280; letter-spacing:0.08em;">ORB / 01–LIVE</div>
        </div>
        <div class="hero-title">
            Make the first move<br>
            <span class="accent">mean something.</span>
        </div>
        <div class="hero-desc">
            The opening range is a small window. This desk keeps your bias, tape, and execution in one deliberate line of sight.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2, _ = st.columns([1.2, 1.2, 6])
    with col_btn1:
        if st.button("+  LOG TRADE", key="hero_log", use_container_width=True):
            st.session_state.page = "Trade Journal"
            st.rerun()
    with col_btn2:
        if st.button("⊞  SET BIAS", key="hero_bias", use_container_width=True, type="secondary"):
            st.session_state.page = "Bias Matrix"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">ACTIVE SESSION</div>
            <div class="stat-value">US Open</div>
            <div class="stat-sub">● RUNNING</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">PRIMARY UNIVERSE</div>
            <div class="stat-value">NQ / ES</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">FRESH SIGNALS</div>
            <div class="stat-value">18</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">LOGGED TODAY</div>
            <div class="stat-value">1</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">A-GRADE RATE</div>
            <div class="stat-value">100%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("""
        <div class="section-header">
            <div class="section-title"><span class="num">01</span> / LIVE TAPE</div>
        </div>
        <h2 style="font-size:24px; margin:0 0 4px 0; color:#f3f4f6;">Headlines with a point</h2>
        <div style="font-size:12px; color:#6b7280; margin-bottom:16px;">Last sync 06:46 AM</div>
        """, unsafe_allow_html=True)

        headlines = [
            {"num": "01", "cat": "MARKETS", "src": "CNBC", "tag": "SHORT", "tag_cls": "tag-short",
             "text": "Fast-fashion giant Shein's shares drop 9% in Hong Kong market debut",
             "time": "06:44 AM"},
            {"num": "02", "cat": "FX & COMMODITIES", "src": "INVESTING.COM", "tag": "MIXED", "tag_cls": "tag-mixed",
             "text": "Square Enix shares jump 11% on privatization report",
             "time": "06:27 AM"},
            {"num": "03", "cat": "MARKETS", "src": "CNBC", "tag": "SHORT", "tag_cls": "tag-short",
             "text": "Bessent reportedly tells Russia no economic relief until Ukraine war ends as Europe snubs Moscow at G20",
             "time": "06:22 AM"},
            {"num": "04", "cat": "FX & COMMODITIES", "src": "INVESTING.COM", "tag": "SHORT", "tag_cls": "tag-short",
             "text": "Shein shares slide in Hong Kong debut on worries about trade and regulatory risks",
             "time": "06:06 AM"},
        ]

        for h in headlines:
            st.markdown(f"""
            <div class="headline-card">
                <div class="headline-meta">
                    <span style="color:#6b7280;">{h['num']}</span>
                    <span style="color:#9ca3af;">{h['cat']}</span>
                    <span style="color:#4b5563;">/</span>
                    <span style="color:#6b7280;">{h['src']}</span>
                    <span class="headline-tag {h['tag_cls']}">▾ {h['tag']}</span>
                </div>
                <div class="headline-text">{h['text']}</div>
                <div class="headline-actions">
                    <span>{h['time']}</span>
                    <span>🔊 read aloud</span>
                    <span>✨ analyze</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
            <div class="section-title"><span class="num">01.1</span> / MACRO CALENDAR</div>
        </div>
        <h3 style="font-size:20px; margin:0 0 4px 0; color:#f3f4f6;">High-impact events</h3>
        <div style="font-size:12px; color:#6b7280; margin-bottom:12px;">Only the releases most likely to move the opening range.</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="padding:12px 16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px; border-bottom:1px solid #1e2229; padding-bottom:10px;">
                <span style="background:#1e3a5f; color:#60a5fa; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">G20</span>
                <span style="font-weight:600; color:#f3f4f6;">September 1</span>
            </div>
            <div class="event-row">
                <div class="event-time">09:00</div>
                <div class="event-flag">🇩🇪</div>
                <div class="event-name">Retail Sales YY Real*</div>
                <div class="event-vals">Prior: 0%</div>
            </div>
            <div class="event-row">
                <div class="event-time">11:00</div>
                <div class="event-flag">🇮🇹</div>
                <div class="event-name">GDP Final QQ *</div>
                <div class="event-vals">Forecast: 0.2% &nbsp; Prior: 0.3%</div>
            </div>
            <div class="event-row">
                <div class="event-time">11:00</div>
                <div class="event-flag">🇮🇹</div>
                <div class="event-name">GDP Final YY *</div>
                <div class="event-vals">Forecast: 1% &nbsp; Prior: 0.8%</div>
            </div>
            <div class="event-row">
                <div class="event-time">12:00</div>
                <div class="event-flag">🇪🇺</div>
                <div class="event-name">Unemployment Rate</div>
                <div class="event-vals">Forecast: 6.3% &nbsp; Prior: 6.3%</div>
            </div>
            <div class="event-row">
                <div class="event-time">04:30</div>
                <div class="event-flag">🇬🇧</div>
                <div class="event-name">Real GDP YY SA</div>
                <div class="event-vals">Forecast: 1.8% &nbsp; Prior: 2.5%</div>
            </div>
            <div class="event-row">
                <div class="event-time">15:15</div>
                <div class="event-flag">🇺🇸</div>
                <div class="event-name">ADP National Employment</div>
                <div class="event-vals">Forecast: 47K &nbsp; Prior: 44K</div>
            </div>
            <div class="event-row">
                <div class="event-time">16:45</div>
                <div class="event-flag">🇨🇦</div>
                <div class="event-name">BoC Rate Decision</div>
                <div class="event-vals">Forecast: 2.25%</div>
            </div>
            <div style="margin-top:12px; font-size:12px; color:#60a5fa; cursor:pointer;">More events ›</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="section-header">
            <div class="section-title"><span class="num">02</span> / STRUCTURAL READ</div>
            <div style="font-size:12px; color:#f0a030; cursor:pointer;">OPEN EDITOR ›</div>
        </div>
        <h2 style="font-size:22px; margin:0 0 4px 0; color:#f3f4f6;">Bias matrix</h2>
        <div style="font-size:12px; color:#6b7280; margin-bottom:16px;">Your map before the noise starts.</div>
        """, unsafe_allow_html=True)

        bias_data = [
            ("5m",  "LONG",  "tag-long",  72, "#22c55e", "Holding above the opening range midpoint."),
            ("15m", "MIXED", "tag-mixed", 54, "#f0a030", "Compression into the prior day high."),
            ("1h",  "SHORT", "tag-short", 61, "#ef4444", "Still below the weekly VWAP band."),
        ]

        for tf, direction, tag_cls, conv, color, note in bias_data:
            st.markdown(f"""
            <div class="bias-mini-card">
                <div class="bias-tf">
                    <span>{tf}</span>
                    <span class="headline-tag {tag_cls}">▾ {direction}</span>
                </div>
                <div class="bias-bar">
                    <div class="bias-bar-fill" style="width:{conv}%; background:{color};"></div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="font-size:11px; color:#6b7280;"></span>
                    <span style="font-size:12px; color:#9ca3af;">{conv}%</span>
                </div>
                <div class="bias-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <div class="section-title"><span class="num">03</span> / EXECUTION</div>
            <div style="font-size:12px; color:#f0a030; cursor:pointer;">FULL JOURNAL ›</div>
        </div>
        <h2 style="font-size:22px; margin:0 0 4px 0; color:#f3f4f6;">Recent journal</h2>
        <div style="font-size:12px; color:#6b7280; margin-bottom:12px;">The last decisions made.</div>
        """, unsafe_allow_html=True)

        for t in st.session_state.trades:
            st.markdown(f"""
            <div class="headline-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="width:28px; height:28px; background:#1a3a2a; border-radius:6px; display:flex; align-items:center; justify-content:center; color:#4ade80; font-size:14px;">↗</div>
                    <div>
                        <div style="font-weight:600; color:#f3f4f6; font-size:14px;">{t['instrument']} &nbsp; <span style="color:#4ade80; font-size:12px;">{t['direction']}</span></div>
                        <div style="font-size:12px; color:#9ca3af;">{t['setup'].upper()} &nbsp;·&nbsp; {t['date']} · {t['result']}</div>
                    </div>
                </div>
                <div style="background:rgba(240,160,48,0.15); color:#f0a030; border:1px solid rgba(240,160,48,0.3); padding:4px 10px; border-radius:4px; font-weight:700; font-size:13px;">{t['grade']}</div>
            </div>
            """, unsafe_allow_html=True)

# =================================================
# TRADE JOURNAL
# =================================================
elif page == "Trade Journal":

    st.markdown("""
    <div class="section-title" style="margin-bottom:8px;"><span class="num">TRADE JOURNAL</span> / INPUT</div>
    <h1 style="font-size:32px; margin:0 0 4px 0; color:#f3f4f6; font-weight:600;">Log the decision.</h1>
    <div style="font-size:14px; color:#9ca3af; margin-bottom:28px;">A clean record beats a clean excuse.</div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1.3])

    with left:
        st.markdown("""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <div style="font-size:11px; color:#f0a030; letter-spacing:0.1em;">A / B / C LOGGER</div>
                <div style="width:20px; height:20px; border:2px solid #f0a030; border-radius:50%;"></div>
            </div>
            <div class="card-title" style="font-size:18px; margin-bottom:20px;">Capture the setup</div>
        </div>
        """, unsafe_allow_html=True)

        ticker = st.text_input("TICKER", placeholder="E.G. NVDA", key="tj_ticker")

        c_dir, c_grade = st.columns(2)
        with c_dir:
            direction = st.selectbox("DIRECTION", ["Long", "Short"], key="tj_dir")
        with c_grade:
            grade = st.selectbox("GRADE", ["A — clean", "B — acceptable", "C — forced"], key="tj_grade")

        setup = st.text_input("SETUP TYPE", value="Opening range breakout", key="tj_setup")

        c_e, c_s, c_t = st.columns(3)
        with c_e:
            entry = st.number_input("ENTRY", value=0.00, format="%.2f", key="tj_entry")
        with c_s:
            stop = st.number_input("STOP", value=0.00, format="%.2f", key="tj_stop")
        with c_t:
            target = st.number_input("TARGET", value=0.00, format="%.2f", key="tj_target")

        result_status = st.selectbox("RESULT STATUS",
                                     ["Planned", "Filled", "Stopped", "Target hit", "Scratched"],
                                     key="tj_result")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾  SAVE TO JOURNAL", use_container_width=True, key="save_trade"):
            new_trade = {
                "instrument": ticker.upper() if ticker else "—",
                "direction": direction.upper(),
                "setup": setup,
                "levels": f"{entry:.2f} / {stop:.2f} / {target:.2f}",
                "grade": grade[0],
                "result": result_status.upper(),
                "date": datetime.now().strftime("%b %d").upper()
            }
            st.session_state.trades.insert(0, new_trade)
            st.success("Trade logged.")
            st.rerun()

    with right:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <div style="font-size:11px; color:#6b7280; letter-spacing:0.1em;">SAVED ENTRIES</div>
                <div style="font-size:20px; font-weight:600; color:#f3f4f6;">Decision history</div>
            </div>
            <div style="font-size:12px; color:#6b7280;">1 ENTRIES VISIBLE</div>
        </div>
        """, unsafe_allow_html=True)

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            st.button("ALL", key="f_all", use_container_width=True)
        with f2:
            st.button("A-GRADE", key="f_a", use_container_width=True, type="secondary")
        with f3:
            st.button("B-GRADE", key="f_b", use_container_width=True, type="secondary")
        with f4:
            st.button("C-GRADE", key="f_c", use_container_width=True, type="secondary")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:grid; grid-template-columns: 1.2fr 1.8fr 2fr 0.6fr 1fr; gap:8px; padding:8px 12px; font-size:10px; color:#6b7280; letter-spacing:0.08em; border-bottom:1px solid #1e2229;">
            <div>INSTRUMENT</div>
            <div>SETUP</div>
            <div>LEVELS</div>
            <div>GRADE</div>
            <div>RESULT</div>
        </div>
        """, unsafe_allow_html=True)

        for t in st.session_state.trades:
            dir_color = "#4ade80" if t["direction"] == "LONG" else "#f87171"
            st.markdown(f"""
            <div style="display:grid; grid-template-columns: 1.2fr 1.8fr 2fr 0.6fr 1fr; gap:8px; padding:14px 12px; align-items:center; border-bottom:1px solid #1a1d24; font-size:13px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="color:#22c55e;">●</span>
                    <span style="font-weight:600; color:#f3f4f6;">{t['instrument']}</span>
                    <span style="color:{dir_color}; font-size:11px;">{t['direction']}</span>
                </div>
                <div style="color:#9ca3af;">{t['setup']}</div>
                <div style="color:#6b7280; font-family:'JetBrains Mono', monospace; font-size:12px;">{t['levels']}</div>
                <div>
                    <span style="background:rgba(240,160,48,0.15); color:#f0a030; border:1px solid rgba(240,160,48,0.3); padding:2px 8px; border-radius:4px; font-weight:700;">{t['grade']}</span>
                </div>
                <div style="color:#9ca3af;">{t['result']}</div>
            </div>
            """, unsafe_allow_html=True)

# =================================================
# BIAS MATRIX
# =================================================
elif page == "Bias Matrix":

    st.markdown("""
    <div class="section-title" style="margin-bottom:8px;"><span class="num">BIAS MATRIX</span> / STRUCTURE</div>
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
            <h1 style="font-size:32px; margin:0 0 4px 0; color:#f3f4f6; font-weight:600;">Choose your weather.</h1>
            <div style="font-size:14px; color:#9ca3af; margin-bottom:28px;">Write the map. Trade only when price agrees.</div>
        </div>
        <div style="font-size:12px; color:#6b7280; letter-spacing:0.08em;">◷ TOP-DOWN CONTEXT</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    timeframes = ["5m", "15m", "1h"]

    for i, tf in enumerate(timeframes):
        with cols[i]:
            b = st.session_state.bias[tf]
            dir_val = b["dir"]

            st.markdown(f"""
            <div class="card" style="min-height:80px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <div style="font-size:11px; color:#6b7280; letter-spacing:0.1em;">TIMEFRAME</div>
                    <span class="headline-tag {'tag-long' if dir_val=='LONG' else 'tag-mixed' if dir_val=='MIXED' else 'tag-short'}">▾ {dir_val}</span>
                </div>
                <div style="font-size:36px; font-weight:600; color:#f3f4f6; margin-bottom:12px;">{tf}</div>
                <div style="font-size:11px; color:#6b7280; letter-spacing:0.08em; margin-bottom:8px;">DIRECTIONAL READ</div>
            </div>
            """, unsafe_allow_html=True)

            d1, d2, d3 = st.columns(3)
            with d1:
                if st.button("LONG", key=f"dir_long_{tf}", use_container_width=True,
                             type="primary" if dir_val == "LONG" else "secondary"):
                    st.session_state.bias[tf]["dir"] = "LONG"
                    st.rerun()
            with d2:
                if st.button("MIXED", key=f"dir_mixed_{tf}", use_container_width=True,
                             type="primary" if dir_val == "MIXED" else "secondary"):
                    st.session_state.bias[tf]["dir"] = "MIXED"
                    st.rerun()
            with d3:
                if st.button("SHORT", key=f"dir_short_{tf}", use_container_width=True,
                             type="primary" if dir_val == "SHORT" else "secondary"):
                    st.session_state.bias[tf]["dir"] = "SHORT"
                    st.rerun()

            conv = st.slider("CONVICTION", 0, 100, b["conv"], key=f"conv_{tf}")
            st.session_state.bias[tf]["conv"] = conv

            note = st.text_area("OPERATOR NOTE", value=b["note"], key=f"note_{tf}", height=80)
            st.session_state.bias[tf]["note"] = note

            if st.button(f"💾  SAVE {tf.upper()} BIAS", key=f"save_{tf}", use_container_width=True):
                st.success(f"{tf} bias saved.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="display:flex; align-items:flex-start; gap:16px;">
        <div style="width:36px; height:36px; background:rgba(240,160,48,0.1); border:1px solid rgba(240,160,48,0.3); border-radius:8px; display:flex; align-items:center; justify-content:center; color:#f0a030; font-size:18px; flex-shrink:0;">⏱</div>
        <div>
            <div style="font-size:12px; color:#f0a030; letter-spacing:0.1em; margin-bottom:4px;">DESK DISCIPLINE</div>
            <div style="font-size:13px; color:#9ca3af; line-height:1.5;">
                Conviction is not a prediction. It is the amount of evidence you require before taking risk. If the timeframes disagree, size down or stand aside.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Footer badge
# -------------------------------------------------
st.markdown("""
<div class="replit-badge">⚡ Made with Replit</div>
""", unsafe_allow_html=True)
