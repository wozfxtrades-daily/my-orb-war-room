import streamlit as st
from datetime import datetime
import requests
from zoneinfo import ZoneInfo
import time

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Orb War Room v1.0",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# NewsAPI configuration
# -------------------------------------------------
NEWS_API_KEY = "4cd70f3a0381475199273ebd100e932a"
NEWS_URL = "https://newsapi.org/v2/everything"

@st.cache_data(ttl=300)  # Cache for 5 minutes → saves your daily quota
def fetch_headlines():
    """Fetch latest market/finance headlines. Returns list of dicts."""
    try:
        params = {
            "q": "stocks OR markets OR economy OR nasdaq OR \"wall street\" OR fed OR inflation",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 8,
            "apiKey": NEWS_API_KEY
        }
        r = requests.get(NEWS_URL, params=params, timeout=8)
        if r.status_code != 200:
            return []
        articles = r.json().get("articles", [])
        results = []
        for i, a in enumerate(articles):
            # Simple bias tag based on keywords (very rough)
            title = (a.get("title") or "").lower()
            if any(w in title for w in ["drop", "fall", "crash", "decline", "loss", "plunge", "slide"]):
                tag, tag_cls = "SHORT", "tag-short"
            elif any(w in title for w in ["jump", "surge", "rally", "gain", "rise", "soar", "climb"]):
                tag, tag_cls = "LONG", "tag-long"
            else:
                tag, tag_cls = "MIXED", "tag-mixed"

            published = a.get("publishedAt", "")
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                time_str = dt.astimezone(ZoneInfo("America/New_York")).strftime("%I:%M %p")
            except:
                time_str = "—"

            results.append({
                "num": f"{i+1:02d}",
                "source": (a.get("source", {}) or {}).get("name", "News")[:18].upper(),
                "tag": tag,
                "tag_cls": tag_cls,
                "title": a.get("title") or "No title",
                "url": a.get("url") or "#",
                "time": time_str
            })
        return results
    except Exception:
        return []

# -------------------------------------------------
# Custom CSS – dark-orange theme + better responsiveness
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
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem !important;
    }

    .main .block-container {
        padding: 1rem 1.2rem 2rem 1.2rem !important;
        max-width: 100% !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    /* Logo */
    .orb-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        margin-bottom: 4px;
    }
    .orb-logo-icon {
        width: 32px; height: 32px;
        border: 1.5px solid #f0a030;
        border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        color: #f0a030; font-weight: 700; font-size: 14px;
    }
    .orb-logo-text {
        font-size: 16px; font-weight: 700; color: #f0a030; letter-spacing: 0.04em;
    }
    .orb-subtitle {
        font-size: 11px; color: #6b7280; letter-spacing: 0.06em;
        margin-left: 42px; margin-top: -2px; margin-bottom: 20px;
    }

    .nav-section-label {
        font-size: 10px; color: #4b5563; letter-spacing: 0.12em;
        text-transform: uppercase; padding: 0 16px; margin-bottom: 8px;
    }

    .data-link-box {
        background: #111318; border: 1px solid #1e2229;
        border-radius: 8px; padding: 12px 14px; margin-bottom: 12px;
    }
    .data-link-title {
        font-size: 10px; color: #6b7280; letter-spacing: 0.08em;
        display: flex; align-items: center; gap: 6px;
    }
    .data-link-live { color: #22c55e; font-size: 11px; font-weight: 600; }

    .trader-info {
        display: flex; align-items: center; gap: 10px;
        padding: 8px 4px; color: #9ca3af; font-size: 13px;
    }
    .trader-avatar {
        width: 28px; height: 28px; background: #f0a030; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        color: #0a0c10; font-weight: 700; font-size: 12px;
    }

    /* Top bar */
    .top-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 4px 0 14px 0; border-bottom: 1px solid #1a1d24; margin-bottom: 18px;
    }
    .top-bar-left { font-size: 12px; color: #6b7280; letter-spacing: 0.1em; text-transform: uppercase; }
    .top-bar-right { display: flex; align-items: center; gap: 14px; font-size: 12px; color: #9ca3af; }

    /* Hero */
    .hero-card {
        background: linear-gradient(180deg, #12151c 0%, #0e1117 100%);
        border: 1px solid #1e2229; border-radius: 12px;
        padding: 36px 40px; margin-bottom: 20px; position: relative; overflow: hidden;
    }
    .hero-card::before {
        content: ''; position: absolute; top:0; left:0; right:0; bottom:0;
        background-image:
            linear-gradient(rgba(240,160,48,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(240,160,48,0.03) 1px, transparent 1px);
        background-size: 40px 40px; pointer-events: none;
    }
    .hero-label {
        font-size: 11px; color: #f0a030; letter-spacing: 0.12em;
        text-transform: uppercase; margin-bottom: 14px;
    }
    .hero-title {
        font-size: clamp(28px, 4vw, 40px); font-weight: 600; line-height: 1.15;
        color: #f3f4f6; margin-bottom: 12px; letter-spacing: -0.03em;
    }
    .hero-title .accent { color: #f0a030; }
    .hero-desc {
        font-size: 15px; color: #9ca3af; max-width: 520px;
        line-height: 1.5; margin-bottom: 8px;
    }

    /* Stats */
    .stat-card {
        background: #111318; border: 1px solid #1e2229;
        border-radius: 10px; padding: 14px 16px; height: 100%;
    }
    .stat-label { font-size: 10px; color: #6b7280; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px; }
    .stat-value { font-size: 20px; font-weight: 600; color: #f3f4f6; }
    .stat-sub { font-size: 11px; color: #22c55e; margin-top: 4px; }

    .section-title { font-size: 13px; color: #9ca3af; letter-spacing: 0.08em; text-transform: uppercase; }
    .section-title .num { color: #f0a030; }

    /* Headlines */
    .headline-card {
        background: #111318; border: 1px solid #1e2229;
        border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
        transition: border-color 0.15s;
    }
    .headline-card:hover { border-color: #3a3f4a; }
    .headline-meta {
        display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
        margin-bottom: 8px; font-size: 11px; color: #6b7280;
    }
    .headline-tag {
        padding: 2px 8px; border-radius: 4px; font-size: 10px;
        font-weight: 600; letter-spacing: 0.05em;
    }
    .tag-short { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
    .tag-long  { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
    .tag-mixed { background: rgba(240,160,48,0.15); color: #f0a030; border: 1px solid rgba(240,160,48,0.3); }

    .headline-text {
        font-size: 14px; color: #e5e7eb; line-height: 1.4; margin-bottom: 6px;
    }
    .headline-text a {
        color: #e5e7eb !important; text-decoration: none !important;
    }
    .headline-text a:hover {
        color: #f0a030 !important; text-decoration: underline !important;
    }
    .headline-actions { font-size: 11px; color: #6b7280; display: flex; gap: 12px; }

    /* Bias mini cards */
    .bias-mini-card {
        background: #111318; border: 1px solid #1e2229;
        border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
    }
    .bias-tf {
        font-size: 18px; font-weight: 600; color: #f3f4f6;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;
    }
    .bias-bar { height: 6px; background: #1e2229; border-radius: 3px; margin-bottom: 6px; overflow: hidden; }
    .bias-bar-fill { height: 100%; border-radius: 3px; }
    .bias-note { font-size: 12px; color: #9ca3af; }

    /* Form inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #0d0f14 !important;
        border: 1px solid #2a2e36 !important;
        border-radius: 6px !important;
        color: #e5e7eb !important;
        font-size: 14px !important;
    }
    .stTextInput > label, .stSelectbox > label, .stNumberInput > label,
    .stSlider > label, .stTextArea > label {
        color: #6b7280 !important; font-size: 11px !important;
        letter-spacing: 0.08em !important; text-transform: uppercase !important;
    }
    .stSlider > div > div > div > div { background-color: #f0a030 !important; }

    .card {
        background: #111318; border: 1px solid #1e2229;
        border-radius: 12px; padding: 18px 20px; margin-bottom: 14px;
    }

    .event-row {
        display: flex; align-items: center; padding: 9px 0;
        border-bottom: 1px solid #1a1d24; font-size: 13px;
    }
    .event-time { width: 55px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
    .event-flag { width: 22px; margin-right: 6px; }
    .event-name { flex: 1; color: #e5e7eb; }
    .event-vals { color: #6b7280; font-size: 12px; text-align: right; }

    .replit-badge {
        position: fixed; bottom: 14px; right: 14px;
        background: #1a1d24; border: 1px solid #2a2e36;
        border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #9ca3af; z-index: 100;
    }

    /* Primary orange buttons */
    .stButton > button {
        background-color: #f0a030 !important;
        color: #0a0c10 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.03em !important;
        padding: 0.5rem 1.1rem !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        background-color: #f5b040 !important;
        color: #0a0c10 !important;
        border: none !important;
    }
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background-color: #1a1d24 !important;
        color: #e5e7eb !important;
        border: 1px solid #2a2e36 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #f0a030 !important;
        color: #f0a030 !important;
    }

    /* Better mobile stacking */
    @media (max-width: 768px) {
        .hero-card { padding: 24px 20px !important; }
        .hero-title { font-size: 26px !important; }
        .stat-value { font-size: 18px !important; }
    }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0c10; }
    ::-webkit-scrollbar-thumb { background: #2a2e36; border-radius: 3px; }
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
        <div class="orb-logo-text">ORB WAR ROOM</div>
    </div>
    <div class="orb-subtitle">VERSION 1.0</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">COMMAND CENTER</div>', unsafe_allow_html=True)

    pages = {
        "War Room":      "⬛",
        "Trade Journal": "📓",
        "Bias Matrix":   "⊞"
    }

    for name, icon in pages.items():
        active = st.session_state.page == name
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = name
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Live New York time
    ny_now = datetime.now(ZoneInfo("America/New_York"))
    ny_time_str = ny_now.strftime("%I:%M %p ET")

    st.markdown(f"""
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
            <div style="font-size:11px; color:#6b7280;">NEW YORK / {ny_time_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# TOP BAR
# -------------------------------------------------
now = datetime.now()
time_str = now.strftime("%I:%M %p")

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
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
            <div class="hero-label">⚡ MARKET OPEN PROTOCOL</div>
            <div style="font-size:11px; color:#6b7280; letter-spacing:0.08em;">ORB WAR ROOM · v1.0</div>
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

    # ---- LOG TRADE & SET BIAS buttons (both properly painted) ----
    col_btn1, col_btn2, _ = st.columns([1.3, 1.3, 5])
    with col_btn1:
        # Primary orange button
        if st.button("＋  LOG TRADE", key="hero_log", use_container_width=True):
            st.session_state.page = "Trade Journal"
            st.rerun()
    with col_btn2:
        # Secondary but still orange-accent on hover
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
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div class="section-title"><span class="num">01</span> / LIVE TAPE</div>
        </div>
        <h2 style="font-size:22px; margin:0 0 4px 0; color:#f3f4f6;">Headlines with a point</h2>
        <div style="font-size:12px; color:#6b7280; margin-bottom:14px;">Live via NewsAPI · cached 5 min</div>
        """, unsafe_allow_html=True)

        headlines = fetch_headlines()

        if not headlines:
            st.info("Could not load live headlines right now. Check your API key or try again in a minute.")
        else:
            for h in headlines:
                st.markdown(f"""
                <div class="headline-card">
                    <div class="headline-meta">
                        <span style="color:#6b7280;">{h['num']}</span>
                        <span style="color:#9ca3af;">{h['source']}</span>
                        <span class="headline-tag {h['tag_cls']}">▾ {h['tag']}</span>
                    </div>
                    <div class="headline-text">
                        <a href="{h['url']}" target="_blank" rel="noopener noreferrer">{h['title']}</a>
                    </div>
                    <div class="headline-actions">
                        <span>{h['time']} ET</span>
                        <span>↗ open source</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Macro calendar (static for now)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-title"><span class="num">01.1</span> / MACRO CALENDAR</div>
        <h3 style="font-size:18px; margin:6px 0 4px 0; color:#f3f4f6;">High-impact events</h3>
        <div style="font-size:12px; color:#6b7280; margin-bottom:10px;">Key releases that can move the opening range.</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="padding:12px 16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px; border-bottom:1px solid #1e2229; padding-bottom:8px;">
                <span style="background:#1e3a5f; color:#60a5fa; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">TODAY</span>
                <span style="font-weight:600; color:#f3f4f6;">Economic Calendar</span>
            </div>
            <div class="event-row">
                <div class="event-time">08:30</div>
                <div class="event-flag">🇺🇸</div>
                <div class="event-name">Retail Sales</div>
                <div class="event-vals">Watch</div>
            </div>
            <div class="event-row">
                <div class="event-time">10:00</div>
                <div class="event-flag">🇺🇸</div>
                <div class="event-name">Business Inventories</div>
                <div class="event-vals">Watch</div>
            </div>
            <div class="event-row">
                <div class="event-time">14:00</div>
                <div class="event-flag">🇺🇸</div>
                <div class="event-name">Fed Speakers</div>
                <div class="event-vals">High impact</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div class="section-title"><span class="num">02</span> / STRUCTURAL READ</div>
        </div>
        <h2 style="font-size:20px; margin:0 0 4px 0; color:#f3f4f6;">Bias matrix</h2>
        <div style="font-size:12px; color:#6b7280; margin-bottom:12px;">Your map before the noise starts.</div>
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
                <div style="text-align:right; font-size:12px; color:#9ca3af; margin-bottom:4px;">{conv}%</div>
                <div class="bias-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-title"><span class="num">03</span> / EXECUTION</div>
        <h2 style="font-size:20px; margin:6px 0 4px 0; color:#f3f4f6;">Recent journal</h2>
        <div style="font-size:12px; color:#6b7280; margin-bottom:10px;">The last decisions made.</div>
        """, unsafe_allow_html=True)

        for t in st.session_state.trades:
            st.markdown(f"""
            <div class="headline-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:26px; height:26px; background:#1a3a2a; border-radius:6px; display:flex; align-items:center; justify-content:center; color:#4ade80; font-size:13px;">↗</div>
                    <div>
                        <div style="font-weight:600; color:#f3f4f6; font-size:13px;">{t['instrument']} <span style="color:#4ade80; font-size:11px;">{t['direction']}</span></div>
                        <div style="font-size:11px; color:#9ca3af;">{t['setup']} · {t['date']}</div>
                    </div>
                </div>
                <div style="background:rgba(240,160,48,0.15); color:#f0a030; border:1px solid rgba(240,160,48,0.3); padding:3px 9px; border-radius:4px; font-weight:700; font-size:12px;">{t['grade']}</div>
            </div>
            """, unsafe_allow_html=True)

# =================================================
# TRADE JOURNAL
# =================================================
elif page == "Trade Journal":

    st.markdown("""
    <div class="section-title" style="margin-bottom:6px;"><span class="num">TRADE JOURNAL</span> / INPUT</div>
    <h1 style="font-size:28px; margin:0 0 4px 0; color:#f3f4f6; font-weight:600;">Log the decision.</h1>
    <div style="font-size:14px; color:#9ca3af; margin-bottom:22px;">A clean record beats a clean excuse.</div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1.3])

    with left:
        st.markdown("""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <div style="font-size:11px; color:#f0a030; letter-spacing:0.1em;">A / B / C LOGGER</div>
                <div style="width:18px; height:18px; border:2px solid #f0a030; border-radius:50%;"></div>
            </div>
            <div style="font-size:17px; font-weight:600; color:#f3f4f6; margin-bottom:16px;">Capture the setup</div>
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
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div>
                <div style="font-size:11px; color:#6b7280; letter-spacing:0.1em;">SAVED ENTRIES</div>
                <div style="font-size:18px; font-weight:600; color:#f3f4f6;">Decision history</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        f1, f2, f3, f4 = st.columns(4)
        with f1: st.button("ALL", key="f_all", use_container_width=True)
        with f2: st.button("A-GRADE", key="f_a", use_container_width=True, type="secondary")
        with f3: st.button("B-GRADE", key="f_b", use_container_width=True, type="secondary")
        with f4: st.button("C-GRADE", key="f_c", use_container_width=True, type="secondary")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:grid; grid-template-columns: 1.1fr 1.6fr 1.8fr 0.5fr 0.9fr; gap:6px; padding:8px 10px; font-size:10px; color:#6b7280; letter-spacing:0.06em; border-bottom:1px solid #1e2229;">
            <div>INSTRUMENT</div><div>SETUP</div><div>LEVELS</div><div>GRADE</div><div>RESULT</div>
        </div>
        """, unsafe_allow_html=True)

        for t in st.session_state.trades:
            dir_color = "#4ade80" if t["direction"] == "LONG" else "#f87171"
            st.markdown(f"""
            <div style="display:grid; grid-template-columns: 1.1fr 1.6fr 1.8fr 0.5fr 0.9fr; gap:6px; padding:12px 10px; align-items:center; border-bottom:1px solid #1a1d24; font-size:13px;">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="color:#22c55e;">●</span>
                    <span style="font-weight:600; color:#f3f4f6;">{t['instrument']}</span>
                    <span style="color:{dir_color}; font-size:11px;">{t['direction']}</span>
                </div>
                <div style="color:#9ca3af;">{t['setup']}</div>
                <div style="color:#6b7280; font-family:'JetBrains Mono', monospace; font-size:11px;">{t['levels']}</div>
                <div>
                    <span style="background:rgba(240,160,48,0.15); color:#f0a030; border:1px solid rgba(240,160,48,0.3); padding:2px 7px; border-radius:4px; font-weight:700;">{t['grade']}</span>
                </div>
                <div style="color:#9ca3af;">{t['result']}</div>
            </div>
            """, unsafe_allow_html=True)

# =================================================
# BIAS MATRIX
# =================================================
elif page == "Bias Matrix":

    st.markdown("""
    <div class="section-title" style="margin-bottom:6px;"><span class="num">BIAS MATRIX</span> / STRUCTURE</div>
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
        <div>
            <h1 style="font-size:28px; margin:0 0 4px 0; color:#f3f4f6; font-weight:600;">Choose your weather.</h1>
            <div style="font-size:14px; color:#9ca3af; margin-bottom:20px;">Write the map. Trade only when price agrees.</div>
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
            <div class="card" style="min-height:70px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <div style="font-size:11px; color:#6b7280; letter-spacing:0.1em;">TIMEFRAME</div>
                    <span class="headline-tag {'tag-long' if dir_val=='LONG' else 'tag-mixed' if dir_val=='MIXED' else 'tag-short'}">▾ {dir_val}</span>
                </div>
                <div style="font-size:32px; font-weight:600; color:#f3f4f6; margin-bottom:10px;">{tf}</div>
                <div style="font-size:11px; color:#6b7280; letter-spacing:0.08em; margin-bottom:6px;">DIRECTIONAL READ</div>
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
    <div class="card" style="display:flex; align-items:flex-start; gap:14px;">
        <div style="width:34px; height:34px; background:rgba(240,160,48,0.1); border:1px solid rgba(240,160,48,0.3); border-radius:8px; display:flex; align-items:center; justify-content:center; color:#f0a030; font-size:16px; flex-shrink:0;">⏱</div>
        <div>
            <div style="font-size:12px; color:#f0a030; letter-spacing:0.1em; margin-bottom:4px;">DESK DISCIPLINE</div>
            <div style="font-size:13px; color:#9ca3af; line-height:1.5;">
                Conviction is not a prediction. It is the amount of evidence you require before taking risk. If the timeframes disagree, size down or stand aside.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("""
<div class="replit-badge">Orb War Room v1.0</div>
""", unsafe_allow_html=True)
