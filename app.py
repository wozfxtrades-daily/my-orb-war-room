import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import openai
import re
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(
    page_title="THE ORB",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for exact replica
st.markdown("""
<style>
    /* Reset and base */
    .stApp {
        background-color: #0a0a0a;
        color: #c0c0c0;
        font-family: 'Courier New', monospace;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0.5rem;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #d4af37 !important;
        font-family: 'Courier New', monospace;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    h1 {
        font-size: 2.2rem !important;
        text-align: center;
        border-bottom: 1px solid #d4af37;
        padding-bottom: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.5rem !important;
        border-bottom: 1px solid #333;
        padding-bottom: 0.3rem;
    }
    
    /* Top banner */
    .top-banner {
        background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
        border-bottom: 2px solid #d4af37;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .top-banner h1 {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .top-banner .subtitle {
        color: #666;
        font-size: 0.8rem;
        letter-spacing: 3px;
    }
    
    /* Status bar */
    .status-bar {
        background: #0d0d0d;
        border: 1px solid #1a1a1a;
        padding: 0.3rem 1rem;
        margin: 0.3rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        font-size: 0.7rem;
        color: #666;
    }
    
    .status-bar .live {
        color: #00ff00;
        font-weight: 700;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    
    .status-bar .gold {
        color: #d4af37;
    }
    
    /* Cards */
    .card {
        background: #0d0d0d;
        border: 1px solid #1a1a1a;
        border-radius: 4px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    .card-gold {
        border-color: #d4af37;
        border-left: 3px solid #d4af37;
    }
    
    /* News items */
    .news-item {
        background: #0d0d0d;
        border-left: 2px solid #d4af37;
        padding: 0.3rem 0.5rem;
        margin: 0.2rem 0;
        font-size: 0.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .news-item .time {
        color: #666;
        font-size: 0.7rem;
        min-width: 60px;
    }
    
    .news-item .title {
        flex: 1;
        margin: 0 0.5rem;
    }
    
    .news-item .actions {
        display: flex;
        gap: 0.3rem;
    }
    
    /* Bias matrix */
    .bias-container {
        background: #0d0d0d;
        border: 1px solid #1a1a1a;
        border-radius: 4px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .bias-container .timeframe {
        color: #d4af37;
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    
    .bias-container .direction-buttons {
        display: flex;
        justify-content: center;
        gap: 0.3rem;
        margin: 0.5rem 0;
    }
    
    .bias-container .direction-btn {
        background: #1a1a1a;
        border: 1px solid #333;
        color: #666;
        padding: 0.2rem 1rem;
        border-radius: 3px;
        font-size: 0.7rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Courier New', monospace;
    }
    
    .bias-container .direction-btn.active-long {
        background: #006400;
        color: #00ff00;
        border-color: #00ff00;
    }
    
    .bias-container .direction-btn.active-short {
        background: #8b0000;
        color: #ff0000;
        border-color: #ff0000;
    }
    
    .bias-container .direction-btn.active-mixed {
        background: #d4af37;
        color: #0a0a0a;
        border-color: #d4af37;
    }
    
    .bias-container .conviction {
        font-size: 2rem;
        font-weight: 700;
        color: #d4af37;
        margin: 0.3rem 0;
    }
    
    .bias-container .note {
        color: #666;
        font-size: 0.7rem;
        font-style: italic;
        margin: 0.3rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: #d4af37 !important;
        color: #0a0a0a !important;
        border: none !important;
        font-weight: 700 !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px;
        padding: 0.3rem 1.5rem !important;
        transition: all 0.3s !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #c4a030 !important;
        transform: scale(1.02);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #c0c0c0 !important;
        border: 1px solid #333 !important;
        border-radius: 3px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.8rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 1px #d4af37 !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: #1a1a1a !important;
    }
    .stSlider > div > div > div > div {
        background: #d4af37 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background: #0d0d0d !important;
        border: 1px solid #1a1a1a !important;
    }
    .stDataFrame th {
        background: #1a1a1a !important;
        color: #d4af37 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stDataFrame td {
        color: #c0c0c0 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.7rem !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0d0d;
    }
    ::-webkit-scrollbar-thumb {
        background: #d4af37;
        border-radius: 3px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .status-bar {
            flex-direction: column;
            align-items: stretch;
            gap: 0.3rem;
            font-size: 0.6rem;
        }
        .news-item {
            flex-direction: column;
            align-items: stretch;
            gap: 0.2rem;
        }
        .news-item .actions {
            justify-content: flex-end;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.2rem !important;
        }
        .bias-container .conviction {
            font-size: 1.5rem;
        }
        .stColumns {
            flex-direction: column !important;
        }
    }
    
    /* Gold text */
    .gold {
        color: #d4af37;
    }
    
    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #1a1a1a;
        margin: 0.5rem 0;
    }
    
    /* Small text */
    .small-text {
        font-size: 0.7rem;
        color: #666;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.3rem;
    }
    .status-indicator.green {
        background: #00ff00;
    }
    .status-indicator.yellow {
        background: #d4af37;
    }
    .status-indicator.red {
        background: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'trade_log' not in st.session_state:
    st.session_state.trade_log = pd.DataFrame(columns=[
        'Timestamp', 'Ticker', 'Direction', 'Grade', 'Setup Type', 
        'Entry', 'Stop', 'Target', 'Status'
    ])

if 'bias_5m' not in st.session_state:
    st.session_state.bias_5m = {'direction': 'MIXED', 'conviction': 72, 'note': 'Holding above the opening range midpoint.'}
if 'bias_15m' not in st.session_state:
    st.session_state.bias_15m = {'direction': 'MIXED', 'conviction': 54, 'note': 'Compression into the prior day high.'}
if 'bias_1h' not in st.session_state:
    st.session_state.bias_1h = {'direction': 'MIXED', 'conviction': 61, 'note': 'Still below the weekly VWAP band.'}

if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "WAR ROOM"

if 'headlines' not in st.session_state:
    st.session_state.headlines = []

# Fetch RSS feed
@st.cache_data(ttl=300)
def fetch_rss_feed():
    try:
        feeds = [
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC",
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=QQQ",
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=NVDA"
        ]
        
        headlines = []
        for feed_url in feeds:
            try:
                response = requests.get(feed_url, timeout=10)
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    for item in root.findall('.//item'):
                        title = item.find('title').text if item.find('title') is not None else ""
                        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                        
                        title = re.sub(r'[^\x00-\x7F]+', '', title)
                        if title and not title.startswith('('):
                            headlines.append({
                                'title': title[:150],
                                'time': pub_date[:16] if pub_date else datetime.now().strftime('%H:%M')
                            })
            except:
                continue
        
        if not headlines:
            headlines = [
                {'title': 'Square Enix shares jump 11% on privatization report', 'time': datetime.now().strftime('%H:%M')},
                {'title': 'Shein shares slide in Hong Kong debut on worries about trade and regulatory risks', 'time': datetime.now().strftime('%H:%M')},
                {'title': 'S&P 500 opens higher as tech stocks rally', 'time': datetime.now().strftime('%H:%M')},
                {'title': 'Fed signals cautious approach to rate cuts', 'time': datetime.now().strftime('%H:%M')},
                {'title': 'Oil prices stabilize after weekly decline', 'time': datetime.now().strftime('%H:%M')},
                {'title': 'Retail sales data beats expectations', 'time': datetime.now().strftime('%H:%M')},
                {'title': 'Market opens mixed as tech sector leads gains', 'time': datetime.now().strftime('%H:%M')},
                {'title': 'Bond yields decline on economic uncertainty', 'time': datetime.now().strftime('%H:%M')},
            ]
        
        return headlines[:20]
    except:
        return [
            {'title': 'Market opens mixed as tech sector leads gains', 'time': datetime.now().strftime('%H:%M')},
            {'title': 'Fed signals cautious approach to rate cuts', 'time': datetime.now().strftime('%H:%M')},
            {'title': 'Oil prices stabilize after weekly decline', 'time': datetime.now().strftime('%H:%M')},
        ]

# DeepSeek AI Integration
def analyze_sentiment(text):
    try:
        openai.api_key = st.secrets["DEEPSEEK_API_KEY"]
        openai.api_base = "https://api.deepseek.com/v1"
        
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a financial sentiment analyzer. Rate the following news headline from -5 (extremely bearish) to +5 (extremely bullish). Return only the number and a brief reasoning."},
                {"role": "user", "content": f"Headline: {text}"}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        score_match = re.search(r'[-+]?\d+\.?\d*', result)
        if score_match:
            score = float(score_match.group())
            score = max(-5, min(5, score))
            return score, result
        else:
            return 0, "Neutral"
    except Exception as e:
        st.error(f"AI Analysis Error: {str(e)}")
        return 0, "Analysis unavailable"

# Top banner
st.markdown("""
<div class='top-banner'>
    <h1>⚔️ THE ORB</h1>
    <div class='subtitle'>NYSE / OPENING RANGE DESK</div>
</div>
""", unsafe_allow_html=True)

# Status bar
st.markdown(f"""
<div class='status-bar'>
    <div><span class='live'>● LIVE</span> DATA LINK ACTIVE</div>
    <div><span class='gold'>NYSE / NASDAQ</span></div>
    <div>ACTIVE SESSION: US Open</div>
    <div>PRIMARY UNIVERSE: NQ/ES</div>
    <div>FRESH SIGNALS: 18</div>
    <div>LOGGED TODAY: 1</div>
    <div>A-GRADE RATE: 100%</div>
    <div><span class='gold'>ACTIVE TRADER</span> NEW YORK / 09:41 ET</div>
</div>
""", unsafe_allow_html=True)

# Navigation
nav_cols = st.columns([1, 1, 1, 1])
with nav_cols[0]:
    if st.button("🏛️ WAR ROOM", use_container_width=True):
        st.session_state.selected_page = "WAR ROOM"
with nav_cols[1]:
    if st.button("📊 TRADE JOURNAL", use_container_width=True):
        st.session_state.selected_page = "TRADE JOURNAL"
with nav_cols[2]:
    if st.button("📈 BIAS MATRIX", use_container_width=True):
        st.session_state.selected_page = "BIAS MATRIX"
with nav_cols[3]:
    st.markdown("<div style='text-align: right; color: #666; font-size: 0.7rem; padding-top: 0.3rem;'>COMMAND CENTER</div>", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# Page content
if st.session_state.selected_page == "WAR ROOM":
    st.markdown("<h2>WAR ROOM / 01</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #666; margin-bottom: 1rem;'>LIVE DESK · Make the first move mean something.</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h3>01 / LIVE TAPE</h3>", unsafe_allow_html=True)
        st.markdown("<div class='small-text'>Headlines with a point · Last sync " + datetime.now().strftime('%H:%M') + "</div>", unsafe_allow_html=True)
        
        # Category filters
        cat_cols = st.columns(3)
        with cat_cols[0]:
            st.markdown("<div style='background: #1a1a1a; padding: 0.2rem; text-align: center; border-radius: 3px; color: #d4af37; font-size: 0.7rem;'>Market | CNBC | SHORT</div>", unsafe_allow_html=True)
        with cat_cols[1]:
            st.markdown("<div style='background: #1a1a1a; padding: 0.2rem; text-align: center; border-radius: 3px; color: #666; font-size: 0.7rem;'>FX & Commodities | INVESTING.COM | MIXED</div>", unsafe_allow_html=True)
        with cat_cols[2]:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        headlines = fetch_rss_feed()
        st.session_state.headlines = headlines
        
        for idx, headline in enumerate(headlines[:10]):
            with st.container():
                cols = st.columns([1, 4, 1])
                with cols[0]:
                    st.markdown(f"<div class='small-text'>{headline['time']}</div>", unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"<div>{headline['title']}</div>", unsafe_allow_html=True)
                with cols[2]:
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("🔊", key=f"speak_{idx}"):
                            js_code = f"""
                            <script>
                            var utterance = new SpeechSynthesisUtterance('{headline['title']}');
                            utterance.rate = 0.9;
                            window.speechSynthesis.speak(utterance);
                            </script>
                            """
                            st.components.v1.html(js_code, height=0)
                    with col_btn2:
                        if st.button("📊", key=f"analyze_{idx}"):
                            with st.spinner("Analyzing..."):
                                score, reasoning = analyze_sentiment(headline['title'])
                                sentiment_color = "#00ff00" if score > 0 else "#ff0000" if score < 0 else "#d4af37"
                                st.markdown(f"""
                                <div style='background: #1a1a1a; padding: 0.3rem; border-radius: 3px; margin-top: 0.2rem;'>
                                    <span style='color: {sentiment_color}; font-weight: 700;'>Score: {score:.1f}</span>
                                    <span style='color: #666; font-size: 0.6rem; display: block;'>{reasoning[:80]}...</span>
                                </div>
                                """, unsafe_allow_html=True)
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>02 / STRUCTURAL READ</h3>", unsafe_allow_html=True)
        st.markdown("<div class='small-text'>Bias matrix · Your map before the noise starts.</div>", unsafe_allow_html=True)
        
        # 5m
        st.markdown("""
        <div class='bias-container'>
            <div class='timeframe'>5m</div>
            <div class='conviction'>72%</div>
            <div class='note'>Holding above the opening range midpoint.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 15m
        st.markdown("""
        <div class='bias-container'>
            <div class='timeframe'>15m</div>
            <div class='conviction'>54%</div>
            <div class='note'>Compression into the prior day high.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 1h
        st.markdown("""
        <div class='bias-container'>
            <div class='timeframe'>1h</div>
            <div class='conviction'>61%</div>
            <div class='note'>Still below the weekly VWAP band.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3>03 / EXECUTION</h3>", unsafe_allow_html=True)
        st.markdown("<div class='small-text'>Recent journal · Build for free</div>", unsafe_allow_html=True)
        
        if not st.session_state.trade_log.empty:
            st.dataframe(
                st.session_state.trade_log.tail(5),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Timestamp": st.column_config.DatetimeColumn("Time", format="MM/DD HH:mm"),
                    "Ticker": st.column_config.TextColumn("Ticker"),
                    "Direction": st.column_config.TextColumn("Dir"),
                    "Grade": st.column_config.TextColumn("Grade"),
                }
            )
        else:
            st.markdown("<div style='color: #666; text-align: center; padding: 1rem;'>No trades logged yet</div>", unsafe_allow_html=True)

elif st.session_state.selected_page == "TRADE JOURNAL":
    st.markdown("<h2>TRADE JOURNAL / INPUT</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #666; margin-bottom: 1rem;'>Log the decision. A clean record beats a clean excuse.</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>A / B / C LOGGER</h3>", unsafe_allow_html=True)
        st.markdown("<div class='small-text'>Capture the setup</div>", unsafe_allow_html=True)
        
        ticker = st.text_input("TICKER", placeholder="E.G. NVDA", key="ticker_input")
        direction = st.selectbox("DIRECTION", ["Long", "Short"], key="direction_select")
        grade = st.selectbox("GRADE", ["A – clean", "B – mixed", "C – risky"], key="grade_select")
        setup_type = st.selectbox("SETUP TYPE", ["Opening range breakout", "VWAP pullback", "Breakout retest", "Trend continuation"], key="setup_select")
        
        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='small-text'>INSTRUMENT: NO LONG · SETUP: OPENING RANGE RECLAIM</div>", unsafe_allow_html=True)
        st.text_input("LEVELS", value="19142.50 / 19108.25 / 19215.00", key="levels_input")
        st.markdown("<div class='small-text'>GRADE: A · RESULT: PLANNED</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>EXECUTION</h3>", unsafe_allow_html=True)
        st.markdown("<div class='small-text'>Entry / Stop / Target</div>", unsafe_allow_html=True)
        
        entry = st.number_input("ENTRY", value=0.00, step=0.01, key="entry_input")
        stop = st.number_input("STOPS", value=0.00, step=0.01, key="stop_input")
        target = st.number_input("TARGETS", value=0.00, step=0.01, key="target_input")
        
        status = st.selectbox("RESULT STATUS", ["Planned", "Executed", "Closed (Win)", "Closed (Loss)"], key="status_select")
        
        if st.button("⚔️ SAVE TO JOURNAL", use_container_width=True):
            if ticker and entry > 0:
                new_entry = pd.DataFrame({
                    'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M')],
                    'Ticker': [ticker.upper()],
                    'Direction': [direction],
                    'Grade': [grade.split(' – ')[0]],
                    'Setup Type': [setup_type],
                    'Entry': [entry],
                    'Stop': [stop],
                    'Target': [target],
                    'Status': [status]
                })
                st.session_state.trade_log = pd.concat([st.session_state.trade_log, new_entry], ignore_index=True)
                st.success(f"✅ Trade logged for {ticker.upper()}!")
                st.rerun()
            else:
                st.error("⚠️ Please enter a ticker and entry price")
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    st.markdown("<h3>RECENT JOURNAL</h3>", unsafe_allow_html=True)
    
    if not st.session_state.trade_log.empty:
        filter_grade = st.selectbox("FILTER BY GRADE", ["ALL", "A", "B", "C"], key="filter_grade")
        
        if filter_grade != "ALL":
            filtered_df = st.session_state.trade_log[st.session_state.trade_log['Grade'] == filter_grade]
        else:
            filtered_df = st.session_state.trade_log
        
        st.dataframe(
            filtered_df.tail(20),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Timestamp": st.column_config.DatetimeColumn("Time", format="MM/DD HH:mm"),
                "Ticker": st.column_config.TextColumn("Symbol"),
                "Direction": st.column_config.TextColumn("Dir"),
                "Grade": st.column_config.TextColumn("Grade"),
                "Setup Type": st.column_config.TextColumn("Setup"),
                "Entry": st.column_config.NumberColumn("Entry", format="$%.2f"),
                "Stop": st.column_config.NumberColumn("Stop", format="$%.2f"),
                "Target": st.column_config.NumberColumn("Target", format="$%.2f"),
                "Status": st.column_config.TextColumn("Status")
            }
        )
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trades", len(filtered_df))
        with col2:
            win_trades = len(filtered_df[filtered_df['Status'] == 'Closed (Win)'])
            win_rate = (win_trades / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.metric("Win Rate", f"{win_rate:.1f}%")
        with col3:
            st.metric("Wins", win_trades)
        with col4:
            loss_trades = len(filtered_df[filtered_df['Status'] == 'Closed (Loss)'])
            st.metric("Losses", loss_trades)
    else:
        st.info("📭 No trades logged yet. Start logging your executions above!")

elif st.session_state.selected_page == "BIAS MATRIX":
    st.markdown("<h2>BIAS MATRIX / STRUCTURE</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #666; margin-bottom: 1rem;'>Choose your weather. Write the map. Trade only when price agrees.</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # 5m
    with col1:
        st.markdown("""
        <div class='bias-container'>
            <div class='timeframe'>5m</div>
        </div>
        """, unsafe_allow_html=True)
        
        direction_5m = st.radio(
            "DIRECTIONAL READ",
            ["LONG", "MIXED", "SHORT"],
            key="bias_5m_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='text-align: center; color: #666; font-size: 0.7rem;'>CONVICTION</div>", unsafe_allow_html=True)
        conviction_5m = st.slider(
            "CONVICTION",
            0, 100, st.session_state.bias_5m['conviction'],
            key="conviction_5m",
            label_visibility="collapsed"
        )
        st.markdown(f"<div style='text-align: center; font-size: 1.5rem; font-weight: 700; color: #d4af37;'>{conviction_5m}%</div>", unsafe_allow_html=True)
        
        note_5m = st.text_area(
            "OPERATOR NOTE",
            value=st.session_state.bias_5m['note'],
            placeholder="e.g., Holding above the opening range midpoint.",
            key="note_5m",
            height=60,
            label_visibility="collapsed"
        )
        
        if st.button("💾 SAVE 5M BIAS", key="save_5m", use_container_width=True):
            st.session_state.bias_5m = {
                'direction': direction_5m,
                'conviction': conviction_5m,
                'note': note_5m
            }
            st.success("5m bias saved!")
    
    # 15m
    with col2:
        st.markdown("""
        <div class='bias-container'>
            <div class='timeframe'>15m</div>
        </div>
        """, unsafe_allow_html=True)
        
        direction_15m = st.radio(
            "DIRECTIONAL READ",
            ["LONG", "MIXED", "SHORT"],
            key="bias_15m_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='text-align: center; color: #666; font-size: 0.7rem;'>CONVICTION</div>", unsafe_allow_html=True)
        conviction_15m = st.slider(
            "CONVICTION",
            0, 100, st.session_state.bias_15m['conviction'],
            key="conviction_15m",
            label_visibility="collapsed"
        )
        st.markdown(f"<div style='text-align: center; font-size: 1.5rem; font-weight: 700; color: #d4af37;'>{conviction_15m}%</div>", unsafe_allow_html=True)
        
        note_15m = st.text_area(
            "OPERATOR NOTE",
            value=st.session_state.bias_15m['note'],
            placeholder="e.g., Compression into the prior day high.",
            key="note_15m",
            height=60,
            label_visibility="collapsed"
        )
        
        if st.button("💾 SAVE 15M BIAS", key="save_15m", use_container_width=True):
            st.session_state.bias_15m = {
                'direction': direction_15m,
                'conviction': conviction_15m,
                'note': note_15m
            }
            st.success("15m bias saved!")
    
    # 1h
    with col3:
        st.markdown("""
        <div class='bias-container'>
            <div class='timeframe'>1h</div>
        </div>
        """, unsafe_allow_html=True)
        
        direction_1h = st.radio(
            "DIRECTIONAL READ",
            ["LONG", "MIXED", "SHORT"],
            key="bias_1h_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='text-align: center; color: #666; font-size: 0.7rem;'>CONVICTION</div>", unsafe_allow_html=True)
        conviction_1h = st.slider(
            "CONVICTION",
            0, 100, st.session_state.bias_1h['conviction'],
            key="conviction_1h",
            label_visibility="collapsed"
        )
        st.markdown(f"<div style='text-align: center; font-size: 1.5rem; font-weight: 700; color: #d4af37;'>{conviction_1h}%</div>", unsafe_allow_html=True)
        
        note_1h = st.text_area(
            "OPERATOR NOTE",
            value=st.session_state.bias_1h['note'],
            placeholder="e.g., Still below the weekly VWAP band.",
            key="note_1h",
            height=60,
            label_visibility="collapsed"
        )
        
        if st.button("💾 SAVE 1H BIAS", key="save_1h", use_container_width=True):
            st.session_state.bias_1h = {
                'direction': direction_1h,
                'conviction': conviction_1h,
                'note': note_1h
            }
            st.success("1h bias saved!")
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #1a1a1a; padding: 1rem; border-left: 4px solid #d4af37; margin: 1rem 0;'>
        <h4 style='color: #d4af37;'>DESK DISCIPLINE</h4>
        <p style='color: #999; font-style: italic;'>
            Conviction is not a prediction. It is the amount of evidence you require before taking risk.
            If the timeframes disagree, size down or stand aside.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 1rem; color: #444; font-size: 0.7rem; border-top: 1px solid #1a1a1a; margin-top: 2rem;'>
    Made with ⚔️ THE ORB · Active Trader · NEW YORK / 09:41 ET
</div>
""", unsafe_allow_html=True)
