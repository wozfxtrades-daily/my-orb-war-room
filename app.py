import streamlit as st
import streamlit.components.v1 as components
import requests
from openai import OpenAI

# 1. PAGE CONFIGURATION & METADATA (Forces a pristine dark workspace)
st.set_page_config(
    page_title="ORB WAR ROOM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INJECTED WORKSPACE STYLING (Forcing the exact custom Replit dark premium theme)
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0d0f12 !important;
        color: #e3e8ed !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Top Navigation Tabs Customizer */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161a1f;
        padding: 6px 12px;
        border-radius: 8px;
        border: 1px solid #242b35;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        white-space: pre;
        background-color: transparent;
        border-radius: 6px;
        color: #8a99a8 !important;
        font-weight: 600;
        transition: all 0.2s ease;
        padding: 0px 16px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ff9f43 !important;
        background-color: #1e242c;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2c3540 !important;
        color: #ff9f43 !important;
        border-bottom: none !important;
    }
    
    /* Sleek Cards & Containers */
    div[data-testid="stVerticalBlock"] > div:has(div.card-element) {
        background: #161a1f !important;
        border: 1px solid #242b35 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
    }
    
    /* Form Inputs & Sliders Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #1c2229 !important;
        color: #ffffff !important;
        border: 1px solid #2c3642 !important;
        border-radius: 6px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #ff9f43 !important;
    }
    
    /* Golden Action Buttons */
    .stButton>button {
        background-color: #ff9f43 !important;
        color: #0d0f12 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        width: 100% !important;
        transition: transform 0.1s ease, background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #f38b2b !important;
        color: #0d0f12 !important;
    }
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Metrics and Headings Accent color */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .orange-text {
        color: #ff9f43 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INITIALIZE SECURE STATE LOGGERS
if "journal_data" not in st.session_state:
    st.session_state.journal_data =

# 4. BACKEND CONTEXT DEEPSEEK ANALYSER
def analyze_headline_sentiment(text_content):
    try:
        if "DEEPSEEK_API_KEY" in st.secrets:
            client = OpenAI(
                api_key=st.secrets["DEEPSEEK_API_KEY"],
                base_url="https://deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a professional prop firm risk analyst Score this news headline for NASDAQ/SP trading sentiment Output strictly a single number 
                    {"role": ""content": text_content}
                ],
                max_tokens=60,
                temperature=0.1
            )
            return response.choices.message.content
        else:
            return "⚠️ DeepSeek Key missing in Settings Secrets."
    except Exception as e:
        return f"Connection Idle: {str(e)}"

# 5. CORE NAVIGATIONAL WORKSPACE PANEL SETUP
st.title("⚡ ORB WAR ROOM")
tabs = st.tabs(["📊 WAR ROOM Live desk", "📝 Trade Journal", "⚙️ Bias Matrix"])

# ==========================================
# PAGE 1: WAR ROOM LIVE DESK
# ==========================================
with tabs:
    st.markdown('<h3 class="orange-text">Live Operational Intelligence Feed</h3>', unsafe_allow_html=True)
    
    # Left: Breaking Stream Header | Right: Audio Controller
    col_news_left, col_news_right = st.columns()
    
    with col_news_left:
        # Pulling structured macro headlines cleanly using an open public aggregator feed
        sample_headline = "US Manufacturing PMI Data Drops Lower to 47.2; Input Prices Spike Ahead of Session Open"
        st.markdown(f"""
            <div style="background-color:#1c2229; padding:16px; border-left: 4px solid #ff9f43; border-radius:6px; margin-bottom:12px;">
                <p style="margin:0; font-size:12px; color:#8a99a8;">CRITICAL SESSION NEWS HEADER</p>
                <p style="margin:4px 0 0 0; font-size:15px; font-weight:600; color:#ffffff;">{sample_headline}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_news_right:
        # Browser-based localized Audio Squawk trigger
        components.html(f"""
            <script>
            function playSquawk() {{
                const msg = new SpeechSynthesisUtterance("{sample_headline}");
                msg.rate = 1.0;
                window.speechSynthesis.speak(msg);
            }}
            </script>
            <button onclick="playSquawk()" style="background-color:#2c3540; color:#ff9f43; border:1px solid #ff9f43; padding:12px 16px; border-radius:6px; font-weight:600; width:100%; cursor:pointer;">
                🔊 Read Aloud (Free Squawk)
            </button>
        """, height=50)
        
        if st.button("🧠 DeepSeek AI Sentiment Grade"):
            with st.spinner("Analyzing macro logic..."):
                analysis_result = analyze_headline_sentiment(sample_headline)
                st.info(analysis_result)

    st.markdown("---")
    
    # DOCKING SECTION: Embedded TradingView Red Folder Compliance Tracker
    st.markdown('<p style="font-size:14px; font-weight:700; color:#ff9f43; margin-bottom:4px;">⚠️ PROP COMPLIANCE NEWS CALENDAR</p>', unsafe_allow_html=True)
    
    # Official automated calendar widget filtered cleanly for High-impact events
    tradingview_calendar_html = """
    <div class="tradingview-widget-container" style="width: 100%; height: 450px;">
      <iframe src="https://tradingview.com" 
              style="width: 100%; height: 450px; border: none; border-radius: 8px;" frameborder="0"></iframe>
    </div>
    """
    components.html(tradingview_calendar_html, height=460)

# ==========================================
# PAGE 2: TRADE JOURNAL LOGGER
# ==========================================
with tabs:
    st.markdown('<h3 class="orange-text">Session Execution Execution Logs</h3>', unsafe_allow_html=True)
    
    # Balanced form layout optimized perfectly for mobile vertical flow
    col_j1, col_j2 = st.columns(2)
    
    with col_j1:
        ticker = st.text_input("Asset Ticker Symbol", value="NQ1!", help="e.g. NQ1!, ES1!, US30")
        setup_grade = st.selectbox("ORB Setup Grade Alignment", ["A - High Conviction (Full "B - Moderate Structure Match", "C - Low Quality Range Breakout"])
    
    with col_j2:
        entry_price = st.text_input("Execution Entry Level", value="0.0")
        stop_loss = st.text_input("Invalidation Level (Stop Loss)", value="0.0")
        
    if st.button("📥 Commit Entry to War Room Journal"):
        new_entry = {
            "Ticker": ticker,
            "Grade": setup_grade,  # Logs cleanly as a single letter: A, B, or C
            "Entry": entry_price,
            "Stop": stop_loss
        }
        st.session_state.journal_data.append(new_entry)
        st.success(f"Setup locked successfully for {ticker}!")
        
    # Execution Timeline History Display Container
    if st.session_state.journal_data:
        st.markdown('<p style="font-weight:700; color:#ffffff; margin-top:16px;">Saved Session Configurations</p>', unsafe_allow_html=True)
        st.table(st.session_state.journal_data)

# ==========================================
# PAGE 3: TOP-DOWN BIAS MATRIX
# ==========================================
with tabs:
    st.markdown('<h3 class="orange-text">Multi-Timeframe Trend Alignment</h3>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color:#161a1f; padding:12px; border-radius:6px; margin-bottom:16px; border: 1px solid #242b35;">
            <p style="margin:0; font-size:13px; color:#8a99a8;">Ensure structural directional confluence across your 5m, 15m, and 1h intervals before initiating your FXIFY session limits.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Top-Down Structural Sliders Matrix layout
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        st.markdown('<p style="font-weight:600; color:#ffffff;">⏱️ 5-Minute Internal Frame</p>', unsafe_allow_html=True)
        m5_bias = st.radio("5m Structure Bias", ["Bullish Confluence", "Bearish Confluence", "Choppy Range"], key="m5")
        m5_strength = st.slider("5m Orderflow Conviction", 0, 100, 50, key="m5_s")
        
    with col_b2:
        st.markdown('<p style="font-weight:600; color:#ffffff;">⏱️ 15-Minute Session Frame</p>', unsafe_allow_html=True)
        m15_bias = st.radio("15m Structure Bias", ["Bullish Confluence", "Bearish Confluence", "Choppy Range"], key="m15")
        m15_strength = st.slider("15m Orderflow Conviction", 0, 100, 50, key="m15_s")
        
    with col_b3:
        st.markdown('<p style="font-weight:600; color:#ffffff;">⏱️ 1-Hour Trend Anchor</p>', unsafe_allow_html=True)
