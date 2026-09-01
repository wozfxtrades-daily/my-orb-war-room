import streamlit as st
from datetime import datetime
import requests
from zoneinfo import ZoneInfo

# -------------------------------------------------
# Page config – sidebar always starts expanded
# -------------------------------------------------
st.set_page_config(
    page_title="Orb War Room v1.0",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# NewsAPI
# -------------------------------------------------
NEWS_API_KEY = "4cd70f3a0381475199273ebd100e932a"

@st.cache_data(ttl=300)
def fetch_headlines():
    try:
        params = {
            "q": "stocks OR markets OR economy OR nasdaq OR \"wall street\" OR fed OR inflation",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 7,
            "apiKey": NEWS_API_KEY
        }
        r = requests.get("https://newsapi.org/v2/everything", params=params, timeout=8)
        if r.status_code != 200:
            return []
        articles = r.json().get("articles", [])
        results = []
        for i, a in enumerate(articles):
            title = (a.get("title") or "").lower()
            if any(w in title for w in ["drop", "fall", "crash", "decline", "loss", "plunge", "slide", "slump"]):
                tag, tag_cls = "SHORT", "tag-short"
            elif any(w in title for w in ["jump", "surge", "rally", "gain", "rise", "soar", "climb", "rally"]):
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
                "source": ((a.get("source") or {}).get("name") or "News")[:16].upper(),
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
# CSS – closer to original screenshots + always-visible sidebar
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp {
    background-color: #0a0c10 !important;
    color: #e8eaed !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; height: 0 !important; }

/* Force sidebar to feel permanent */
[data-testid="stSidebar"] {
    background-color: #0d0f14 !important;
    border-right: 1px solid #1a1d24 !important;
    min-width: 250px !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0.8rem !important; }

/* Make the collapse button more visible so user can always find it */
[data-testid="stSidebarCollapseButton"] {
    background: #1a1d24 !important;
    border: 1px solid #2a2e36 !important;
    border-radius: 6px !important;
}

.main .block-container {
    padding: 0.8rem 1.4rem 2rem 1.4rem !important;
    max-width: 100% !important;
}

/* Logo */
.orb-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px 4px 14px; cursor: pointer;
}
.orb-logo-icon {
    width: 30px; height: 30px;
    border: 1.5px solid #f0a030; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    color: #f0a030; font-weight: 700; font-size: 13px;
}
.orb-logo-text {
    font-size: 15px; font-weight: 700; color: #f0a030; letter-spacing: 0.04em;
}
.orb-subtitle {
    font-size: 10px; color: #6b7280; letter-spacing: 0.08em;
    margin-left: 44px; margin-bottom: 18px;
}

.nav-label {
    font-size: 10px; color: #4b5563; letter-spacing: 0.12em;
    text-transform: uppercase; padding: 0 16px; margin-bottom: 6px;
}

.data-box {
    background: #111318; border: 1px solid #1e2229;
    border-radius: 8px; padding: 11px 13px; margin: 16px 10px 10px 10px;
}
.data-title { font-size: 10px; color: #6b7280; letter-spacing: 0.08em; }
.data-live { color: #22c55e; font-size: 11px; font-weight: 600; }

.trader {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 14px 14px 14px; color: #9ca3af; font-size: 13px;
}
.trader-av {
    width: 28px; height: 28px; background: #f0a030; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    color: #0a0c10; font-weight: 700; font-size: 12px;
}

/* Top bar */
.topbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 2px 0 12px 0; border-bottom: 1px solid #1a1d24; margin-bottom: 16px;
}
.topbar-left { font-size: 11px; color: #6b7280; letter-spacing: 0.1em; text-transform: uppercase; }
.topbar-right { font-size: 12px; color: #9ca3af; }

/* Hero */
.hero {
    background: linear-gradient(180deg, #12151c 0%, #0e1117 100%);
    border: 1px solid #1e2229; border-radius: 12px;
    padding: 32px 36px; margin-bottom: 18px; position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(240,160,48,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(240,160,48,0.025) 1px, transparent 1px);
    background-size: 36px 36px; pointer-events: none;
}
.hero-label { font-size: 11px; color: #f0a030; letter-spacing: 0.12em; margin-bottom: 12px; }
.hero-title {
    font-size: clamp(26px, 3.8vw, 38px); font-weight: 600; line-height: 1.15;
    color: #f3f4f6; margin-bottom: 10px; letter-spacing: -0.03em;
}
.hero-title span { color: #f0a030; }
.hero-desc { font-size: 14px; color: #9ca3af; max-width: 480px; line-height: 1.5; }

/* Stats */
.stat {
    background: #111318; border: 1px solid #1e2229;
    border-radius: 10px; padding: 13px 15px; height: 100%;
}
.stat-l { font-size: 10px; color: #6b7280; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 5px; }
.stat-v { font-size: 19px; font-weight: 600; color: #f3f4f6; }
.stat-s { font-size: 11px; color: #22c55e; margin-top: 3px; }

.sec { font-size: 12px; color: #9ca3af; letter-spacing: 0.08em; text-transform: uppercase; }
.sec span { color: #f0a030; }

/* Cards */
.card {
    background: #111318; border: 1px solid #1e2229;
    border-radius: 10px; padding: 14px 16px; margin-bottom: 9px;
}
.card:hover { border-color: #2a2e36; }

.tag {
    padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 600; letter-spacing: 0.04em;
}
.tag-short { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.tag-long  { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.tag-mixed { background: rgba(240,160,48,0.15); color: #f0a030; border: 1px solid rgba(240,160,48,0.3); }

.headline-title a {
    color: #e5e7eb !important; text-decoration: none !important; font-size: 14px; line-height: 1.4;
}
.headline-title a:hover { color: #f0a030 !important; }

/* Form */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #0d0f14 !important;
    border: 1px solid #2a2e36 !important;
    border-radius: 6px !important;
    color: #e5e7eb !important;
}
.stTextInput > label, .stSelectbox > label, .stNumberInput > label,
.stSlider > label, .stTextArea > label {
    color: #6b7280 !important; font-size: 11px !important;
    letter-spacing: 0.07em !important; text-transform: uppercase !important;
}
.stSlider > div > div > div > div { background-color: #f0a030 !important; }

/* Buttons */
.stButton > button {
    background-color: #f0a030 !important;
    color: #0a0c10 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 0.45rem 1rem !important;
}
.stButton > button:hover {
    background-color: #f5b040 !important;
    color: #0a0c10 !important;
}
.stButton > button[kind="secondary"] {
    background-color: #1a1d24 !important;
    color: #e5e7eb !important;
    border: 1px solid #2a2e36 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #f0a030 !important;
    color: #f0a030 !important;
}

/* Delete button smaller */
div[data-testid="column"] .stButton > button {
    font-size: 12px !important;
    padding: 0.3rem 0.6rem !important;
}

.badge {
    position: fixed; bottom: 12px; right: 12px;
    background: #1a1d24; border: 1px solid #2a2e36;
    border-radius: 16px; padding: 4px 11px; font-size: 11px; color: #9ca3af; z-index: 99;
}

@media (max-width: 768px) {
    .hero { padding: 22px 18px !important; }
    .hero-title { font-size: 24px !important; }
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
            "id": 1,
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
if "trade_counter" not in st.session_state:
    st.session_state.trade_counter = 2

# -------------------------------------------------
# SIDEBAR (permanent + clickable logo)
# -------------------------------------------------
with st.sidebar:
    # Clickable logo → always goes home
    if st.button("⬡  ORB WAR ROOM", key="logo_home", use_container_width=True):
        st.session_state.page = "War Room"
        st.rerun()

    st.markdown('<div class="orb-subtitle">VERSION 1.0</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-label">COMMAND CENTER</div>', unsafe_allow_html=True)

    for name, icon in [("War Room", "⬛"), ("Trade Journal", "📓"), ("Bias Matrix", "⊞")]:
        active = st.session_state.page == name
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = name
            st.rerun()

    # Live NY time
    ny = datetime.now(ZoneInfo("America/New_York")).strftime("%I:%M %p ET")

    st.markdown(f"""
    <div class="data-box">
        <div class="data-title"><span style="color:#22c55e">●</span> DATA LINK ACTIVE</div>
        <div style="display:flex;justify-content:space-between;margin-top:5px;">
            <span style="color:#e5e7eb;font-size:13px;font-weight:500;">NYSE / NASDAQ</span>
            <span class="data-live">LIVE</span>
        </div>
    </div>
    <div class="trader">
        <div class="trader-av">AR</div>
        <div>
            <div style="color:#e5e7eb;font-weight:500;">Active trader</div>
            <div style="font-size:11px;color:#6b7280;">NEW YORK / {ny}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# TOP BAR
# -------------------------------------------------
st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">NYSE / OPENING RANGE DESK</div>
    <div class="topbar-right">◷ {datetime.now().strftime("%I:%M %p")}</div>
</div>
""", unsafe_allow_html=True)

page = st.session_state.page

# =================================================
# WAR ROOM
# =================================================
if page == "War Room":
    st.markdown("""
    <div class="hero">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px;">
            <div class="hero-label">⚡ MARKET OPEN PROTOCOL</div>
            <div style="font-size:11px;color:#6b7280;">ORB WAR ROOM · v1.0</div>
        </div>
        <div class="hero-title">Make the first move<br><span>mean something.</span></div>
        <div class="hero-desc">The opening range is a small window. This desk keeps your bias, tape, and execution in one deliberate line of sight.</div>
    </div>
    """, unsafe_allow_html=True)

    b1, b2, _ = st.columns([1.2, 1.2, 5])
    with b1:
        if st.button("＋  LOG TRADE", key="log_btn", use_container_width=True):
            st.session_state.page = "Trade Journal"
            st.rerun()
    with b2:
        if st.button("⊞  SET BIAS", key="bias_btn", use_container_width=True, type="secondary"):
            st.session_state.page = "Bias Matrix"
            st.rerun()

    st.write("")
    s1, s2, s3, s4, s5 = st.columns(5)
    for col, label, value, sub in [
        (s1, "ACTIVE SESSION", "US Open", "● RUNNING"),
        (s2, "PRIMARY UNIVERSE", "NQ / ES", ""),
        (s3, "FRESH SIGNALS", "18", ""),
        (s4, "LOGGED TODAY", str(len(st.session_state.trades)), ""),
        (s5, "A-GRADE RATE", "100%", ""),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat">
                <div class="stat-l">{label}</div>
                <div class="stat-v">{value}</div>
                {"<div class='stat-s'>"+sub+"</div>" if sub else ""}
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.45, 1])

    with left:
        st.markdown('<div class="sec"><span>01</span> / LIVE TAPE</div>', unsafe_allow_html=True)
        st.markdown("### Headlines with a point")
        st.caption("Live via NewsAPI · refreshes every 5 min")

        headlines = fetch_headlines()
        if not headlines:
            st.info("Headlines temporarily unavailable. Try refreshing in a minute.")
        else:
            for h in headlines:
                st.markdown(f"""
                <div class="card">
                    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;font-size:11px;color:#6b7280;">
                        <span>{h['num']}</span>
                        <span style="color:#9ca3af;">{h['source']}</span>
                        <span class="tag {h['tag_cls']}">▾ {h['tag']}</span>
                    </div>
                    <div class="headline-title">
                        <a href="{h['url']}" target="_blank">{h['title']}</a>
                    </div>
                    <div style="font-size:11px;color:#6b7280;margin-top:5px;">{h['time']} ET · ↗ open source</div>
                </div>
                """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="sec"><span>02</span> / STRUCTURAL READ</div>', unsafe_allow_html=True)
        st.markdown("### Bias matrix")
        st.caption("Your map before the noise starts.")

        for tf, direction, tag_cls, conv, color, note in [
            ("5m",  "LONG",  "tag-long",  72, "#22c55e", "Holding above the opening range midpoint."),
            ("15m", "MIXED", "tag-mixed", 54, "#f0a030", "Compression into the prior day high."),
            ("1h",  "SHORT", "tag-short", 61, "#ef4444", "Still below the weekly VWAP band."),
        ]:
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-size:17px;font-weight:600;color:#f3f4f6;">{tf}</span>
                    <span class="tag {tag_cls}">▾ {direction}</span>
                </div>
                <div style="height:5px;background:#1e2229;border-radius:3px;margin-bottom:5px;overflow:hidden;">
                    <div style="width:{conv}%;height:100%;background:{color};border-radius:3px;"></div>
                </div>
                <div style="text-align:right;font-size:12px;color:#9ca3af;margin-bottom:4px;">{conv}%</div>
                <div style="font-size:12px;color:#9ca3af;">{note}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sec" style="margin-top:14px;"><span>03</span> / EXECUTION</div>', unsafe_allow_html=True)
        st.markdown("### Recent journal")
        for t in st.session_state.trades[:3]:
            st.markdown(f"""
            <div class="card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-weight:600;color:#f3f4f6;font-size:13px;">{t['instrument']} <span style="color:#4ade80;font-size:11px;">{t['direction']}</span></div>
                    <div style="font-size:11px;color:#9ca3af;">{t['setup']} · {t['date']}</div>
                </div>
                <div style="background:rgba(240,160,48,0.15);color:#f0a030;border:1px solid rgba(240,160,48,0.3);padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">{t['grade']}</div>
            </div>
            """, unsafe_allow_html=True)

# =================================================
# TRADE JOURNAL
# =================================================
elif page == "Trade Journal":
    st.markdown('<div class="sec"><span>TRADE JOURNAL</span> / INPUT</div>', unsafe_allow_html=True)
    st.markdown("## Log the decision.")
    st.caption("A clean record beats a clean excuse.")

    left, right = st.columns([1, 1.35])

    with left:
        st.markdown("""
        <div class="card">
            <div style="font-size:11px;color:#f0a030;letter-spacing:0.1em;margin-bottom:4px;">A / B / C LOGGER</div>
            <div style="font-size:16px;font-weight:600;color:#f3f4f6;">Capture the setup</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("trade_form", clear_on_submit=True):
            ticker = st.text_input("TICKER", placeholder="E.G. NVDA")
            c1, c2 = st.columns(2)
            with c1:
                direction = st.selectbox("DIRECTION", ["Long", "Short"])
            with c2:
                grade = st.selectbox("GRADE", ["A — clean", "B — acceptable", "C — forced"])
            setup = st.text_input("SETUP TYPE", value="Opening range breakout")
            e, s, t = st.columns(3)
            with e: entry = st.number_input("ENTRY", value=0.0, format="%.2f")
            with s: stop = st.number_input("STOP", value=0.0, format="%.2f")
            with t: target = st.number_input("TARGET", value=0.0, format="%.2f")
            result = st.selectbox("RESULT STATUS", ["Planned", "Filled", "Stopped", "Target hit", "Scratched"])
            submitted = st.form_submit_button("💾  SAVE TO JOURNAL", use_container_width=True)

            if submitted:
                st.session_state.trades.insert(0, {
                    "id": st.session_state.trade_counter,
                    "instrument": ticker.upper() if ticker else "—",
                    "direction": direction.upper(),
                    "setup": setup,
                    "levels": f"{entry:.2f} / {stop:.2f} / {target:.2f}",
                    "grade": grade[0],
                    "result": result.upper(),
                    "date": datetime.now().strftime("%b %d").upper()
                })
                st.session_state.trade_counter += 1
                st.success("Trade saved.")
                st.rerun()

    with right:
        st.markdown("##### Decision history")
        if not st.session_state.trades:
            st.info("No trades logged yet.")
        else:
            for t in st.session_state.trades:
                col1, col2 = st.columns([5, 1])
                with col1:
                    dir_c = "#4ade80" if t["direction"] == "LONG" else "#f87171"
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:6px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div>
                                <span style="font-weight:600;color:#f3f4f6;">{t['instrument']}</span>
                                <span style="color:{dir_c};font-size:12px;margin-left:6px;">{t['direction']}</span>
                                <div style="font-size:12px;color:#9ca3af;margin-top:2px;">{t['setup']} · {t['levels']}</div>
                                <div style="font-size:11px;color:#6b7280;">{t['date']} · {t['result']}</div>
                            </div>
                            <span style="background:rgba(240,160,48,0.15);color:#f0a030;border:1px solid rgba(240,160,48,0.3);padding:2px 8px;border-radius:4px;font-weight:700;">{t['grade']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("✕", key=f"del_{t['id']}", help="Delete this trade"):
                        st.session_state.trades = [x for x in st.session_state.trades if x["id"] != t["id"]]
                        st.rerun()

# =================================================
# BIAS MATRIX
# =================================================
elif page == "Bias Matrix":
    st.markdown('<div class="sec"><span>BIAS MATRIX</span> / STRUCTURE</div>', unsafe_allow_html=True)
    st.markdown("## Choose your weather.")
    st.caption("Write the map. Trade only when price agrees.")

    cols = st.columns(3)
    for i, tf in enumerate(["5m", "15m", "1h"]):
        with cols[i]:
            b = st.session_state.bias[tf]
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:11px;color:#6b7280;">TIMEFRAME</span>
                    <span class="tag {'tag-long' if b['dir']=='LONG' else 'tag-mixed' if b['dir']=='MIXED' else 'tag-short'}">▾ {b['dir']}</span>
                </div>
                <div style="font-size:30px;font-weight:600;color:#f3f4f6;margin:6px 0 10px 0;">{tf}</div>
            </div>
            """, unsafe_allow_html=True)

            d1, d2, d3 = st.columns(3)
            with d1:
                if st.button("LONG", key=f"l_{tf}", use_container_width=True, type="primary" if b["dir"]=="LONG" else "secondary"):
                    st.session_state.bias[tf]["dir"] = "LONG"
                    st.rerun()
            with d2:
                if st.button("MIXED", key=f"m_{tf}", use_container_width=True, type="primary" if b["dir"]=="MIXED" else "secondary"):
                    st.session_state.bias[tf]["dir"] = "MIXED"
                    st.rerun()
            with d3:
                if st.button("SHORT", key=f"s_{tf}", use_container_width=True, type="primary" if b["dir"]=="SHORT" else "secondary"):
                    st.session_state.bias[tf]["dir"] = "SHORT"
                    st.rerun()

            conv = st.slider("CONVICTION", 0, 100, b["conv"], key=f"c_{tf}")
            st.session_state.bias[tf]["conv"] = conv
            note = st.text_area("OPERATOR NOTE", value=b["note"], key=f"n_{tf}", height=70)
            st.session_state.bias[tf]["note"] = note
            if st.button(f"SAVE {tf.upper()} BIAS", key=f"save_{tf}", use_container_width=True):
                st.success(f"{tf} bias saved")

    st.write("")
    st.markdown("""
    <div class="card" style="display:flex;gap:12px;align-items:flex-start;">
        <div style="width:32px;height:32px;background:rgba(240,160,48,0.1);border:1px solid rgba(240,160,48,0.3);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#f0a030;flex-shrink:0;">⏱</div>
        <div>
            <div style="font-size:12px;color:#f0a030;letter-spacing:0.08em;margin-bottom:3px;">DESK DISCIPLINE</div>
            <div style="font-size:13px;color:#9ca3af;line-height:1.5;">Conviction is not a prediction. It is the amount of evidence you require before taking risk. If the timeframes disagree, size down or stand aside.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="badge">Orb War Room v1.0</div>', unsafe_allow_html=True)
