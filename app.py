import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# 1. HARD WORKSPACE CONFIGURATION (Matches Replit Desktop/Mobile Scaling)
st.set_page_config(
    page_title="THE ORB - WAR ROOM",
    page_icon="⬢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. IDENTICAL VISUAL ACCENTS & CSS THEMING INJECTION
st.markdown("""
    <style>
    /* Absolute Dark UI Canvas */
    .stApp, [data-testid="stSidebar"] {
        background-color: #0d0f12 !important;
        color: #e3e8ed !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Top Header Meta Panels */
    .meta-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1c2229;
        padding-bottom: 12px;
        margin-bottom: 20px;
    }
    
    /* Persistent Command Center Sidebar Restyling */
    [data-testid="stSidebarNav"] {display: none !important;}
    
    .sidebar-logo {
        padding: 10px 0px;
        border-bottom: 1px solid #1c2229;
        margin-bottom: 20px;
    }
    
    /* Premium Premium Cards Layout Containers */
    .war-card {
        background: #13171c !important;
        border: 1px solid #1c2229 !important;
        border-radius: 6px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
    }
    
    /* Typography Overrides */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    /* Glow Text Badges */
    .gold-accent { color: #ff9f43 !important; }
    .green-accent { color: #00ffa3 !important; }
    .red-accent { color: #ff4a5a !important; }
    
    /* Unified Data Fields Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #0d0f12 !important;
        color: #ffffff !important;
        border: 1px solid #1c2229 !important;
        border-radius: 4px !important;
    }
    
    /* Replit Golden Action Button styling */
    .stButton>button {
        background-color: #ff9f43 !important;
        color: #0d0f12 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.1s ease;
    }
    .stButton>button:hover {
        background-color: #f38b2b !important;
        color: #0d0f12 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INITIALIZE STATE REGISTRIES (Prevents Data Wipes on Clicks)
if "current_view" not in st.session_state:
    st.session_state.current_view = "War Room Live Desk"

if "journal_logs" not in st.session_state:
    st.session_state.journal_logs = [
        {"INSTRUMENT": "NQ", "SETUP": "Opening range reclaim", "LEVELS": "19142.50 / 19108.25 / 19215.00", "GRADE": "A", "RESULT": "PLANNED"}
    ]

# 4. DEEPSEEK SENTIMENT PARSER ENGINE
def get_ai_headline_grade(headline_text):
    if "DEEPSEEK_API_KEY" not in st.secrets or not st.secrets["DEEPSEEK_API_KEY"]:
        return "⚡ API Key Idle. Add it to Streamlit Secrets to parse."
    try:
        client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a prop firm macro analyst. Grade this headline for equity index directional bias. Output strictly a number from -5 to +5 followed by one brief sentence reason."},
                {"role": "user", "content": headline_text}
            ],
            max_tokens=60,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"System Offline: {str(e)}"

# ==========================================
# SIDEBAR NAVIGATION (COMMAND CENTER PANEL)
# ==========================================
with st.sidebar:
    # Golden Diamond Logo Header
    st.markdown("""
        <div class="sidebar-logo">
            <span style="color:#ff9f43; font-weight:800; font-size:18px; letter-spacing:1px;">⬢ THE ORB</span><br>
            <span style="color:#8a99a8; font-size:10px; letter-spacing:2px;">WAR ROOM / 01</span>
        </div>
        <p style="color:#8a99a8; font-size:11px; font-weight:700; letter-spacing:1px; margin-bottom:12px;">COMMAND CENTER</p>
    """, unsafe_allow_html=True)
    
    # Real-Time Operational View Selectors
    if st.button("🎛️ War Room Live Desk"):
        st.session_state.current_view = "War Room Live Desk"
    if st.button("📖 Trade Journal"):
        st.session_state.current_view = "Trade Journal"
    if st.button("🧩 Bias Matrix"):
        st.session_state.current_view = "Bias Matrix"
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Bottom Operational Telemetry Panels
    st.markdown("""
        <div style="border-top: 1px solid #1c2229; padding-top:16px;">
            <p style="margin:0; font-size:11px; color:#8a99a8;">● DATA LINK ACTIVE</p>
            <p style="margin:2px 0 0 0; font-size:13px; font-weight:700; color:#ffffff;">NYSE / NASDAQ <span class="green-accent" style="float:right;">LIVE</span></p>
        </div>
        <br>
        <div style="background:#13171c; padding:12px; border-radius:4px; border:1px solid #1c2229;">
            <p style="margin:0; font-size:10px; color:#8a99a8;">Active Trader</p>
            <p style="margin:2px 0 0 0; font-size:12px; font-weight:700; color:#ffffff;">NEW YORK / 09:41 ET</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# RENDER DYNAMIC OPERATIONAL VIEWPORTS
# ==========================================

# Top Session Navbar Workspace Title Panel
st.markdown("""
    <div class="meta-header">
        <span style="font-size:12px; color:#8a99a8; font-weight:600; letter-spacing:1px;">NYSE / OPENING RANGE DESK</span>
        <span style="font-size:12px; color:#ffffff; font-weight:600;">🕒 06:45 AM GMT+3 🔔</span>
    </div>
""", unsafe_allow_html=True)

# VIEWPORT A: THE CORE LIVE DESK
if st.session_state.current_view == "War Room Live Desk":
    
    # Hero Title Banner Block
    st.markdown("""
        <div class="war-card" style="padding: 40px 30px !important;">
            <p style="color:#ff9f43; font-size:11px; font-weight:700; letter-spacing:2px; margin:0;">⚡ MARKET OPEN PROTOCOL</p>
            <h1 style="font-size:42px; margin:12px 0px;">Make the first move<br>mean something.</h1>
            <p style="color:#8a99a8; font-size:14px; max-width:600px; margin:0;">The opening range is a small window. This desk keeps your bias, tape, and execution in one deliberate line of sight.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Telemetry Counter Blocks Matrix Layout
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
    metrics = [
        ("ACTIVE SESSION", "US Open", "RUNNING"),
        ("PRIMARY UNIVERSE", "NQ / ES", ""),
        ("FRESH SIGNALS", "18", ""),
        ("LOGGED TODAY", "1", ""),
        ("A-GRADE RATE", "100%", "")
    ]
    for idx, (label, val, sub) in enumerate(metrics):
        with [col_t1, col_t2, col_t3, col_t4, col_t5][idx]:
            st.markdown(f"""
                <div style="background:#13171c; border:1px solid #1c2229; padding:16px; border-radius:4px;">
                    <p style="margin:0; font-size:11px; color:#8a99a8; font-weight:600;">{label}</p>
                    <p style="margin:4px 0 0 0; font-size:24px; font-weight:800; color:#ffffff;">{val}</p>
                    {f'<p style="margin:2px 0 0 0; font-size:10px; color:#00ffa3;">● {sub}</p>' if sub else ''}
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Split Grid: Live News Stream Feed Container vs. Real-Time Bias Map Matrix
    col_left_desk, col_right_desk = st.columns([3, 2])
    
    with col_left_desk:
        st.markdown('<h4>01 / LIVE TAPE <span style="font-size:16px; color:#ffffff;">Headlines with a point</span></h4>', unsafe_allow_html=True)
        
        # Array data mapping for live news drops
        news_headlines = [
            ("MARKETS", "CNBC", "SHORT", "Fast-fashion giant Shein's shares drop 9% in Hong Kong market debut", "06:44 AM"),
            ("FX & COMMODITIES", "INVESTING.COM", "MIXED", "Square Enix shares jump 11% on privatization report", "06:27 AM"),
            ("MARKETS", "CNBC", "SHORT", "Bessent reportedly tells Russia no economic relief until Ukraine war ends as Europe snubs Moscow at G20", "06:22 AM")
        ]
        
        for idx, (cat, src, tag, text, time_lbl) in enumerate(news_headlines):
            st.markdown(f"""
                <div style="background:#13171c; border:1px solid #1c2229; padding:16px; border-radius:6px; margin-bottom:12px;">
                    <span style="font-size:10px; background:#1c2229; padding:3px 6px; border-radius:3px; color:#8a99a8; font-weight:700;">{cat}</span>
                    <span style="font-size:10px; color:#8a99a8; margin-left:8px;">{src}</span>
                    <span style="float:right; font-size:10px; font-weight:700; color:{'#ff4a5a' if tag=='SHORT' else '#ff9f43'};">{tag}</span>
                    <p style="margin:10px 0 6px 0; font-size:15px; font-weight:600; color:#ffffff;">{text}</p>
                    <span style="font-size:11px; color:#5c6875;">{time_lbl}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Action controls per news card
            c_aud, c_anz = st.columns(2)
            with c_aud:
                components.html(f"""
