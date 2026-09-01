import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import openai
import json
from streamlit.components.v1 import html
import re

# Page configuration
st.set_page_config(
    page_title="THE ORB - WAR ROOM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    /* Main dark theme */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #d4af37 !important;
        font-family: 'Courier New', monospace;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* Command center header */
    .command-center {
        background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
        border-bottom: 2px solid #d4af37;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    /* Gold accent boxes */
    .gold-box {
        background: #1a1a1a;
        border: 1px solid #d4af37;
        border-radius: 4px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Cards */
    .card {
        background: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Bias matrix buttons */
    .bias-btn {
        background: #1a1a1a;
        border: 1px solid #333;
        color: #e0e0e0;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin: 0.2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .bias-btn-active {
        background: #d4af37;
        color: #0a0a0a;
        border: 1px solid #d4af37;
    }
    .bias-btn-short {
        background: #8b0000;
        color: #fff;
        border: 1px solid #8b0000;
    }
    .bias-btn-long {
        background: #006400;
        color: #fff;
        border: 1px solid #006400;
    }
    
    /* Metrics */
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #d4af37;
        font-family: 'Courier New', monospace;
    }
    
    /* News items */
    .news-item {
        background: #0d0d0d;
        border-left: 3px solid #d4af37;
        padding: 0.5rem 1rem;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    
    /* Status indicators */
    .status-live {
        color: #00ff00;
        font-weight: 700;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    
    /* Custom containers */
    .desk-container {
        background: #0d0d0d;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #1a1a1a;
        margin-bottom: 1rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stColumns {
            flex-direction: column;
        }
        .card {
            padding: 0.5rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #d4af37;
        border-radius: 4px;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border-color: #333 !important;
    }
    .stSelectbox > div > div > select {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border-color: #333 !important;
    }
    .stNumberInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border-color: #333 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #d4af37 !important;
        color: #0a0a0a !important;
        border: none !important;
        font-weight: 700 !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        background: #c4a030 !important;
        transform: scale(1.02);
    }
    
    /* Dataframes */
    .stDataFrame {
        background: #0d0d0d !important;
        border: 1px solid #1a1a1a !important;
    }
    .stDataFrame th {
        background: #1a1a1a !important;
        color: #d4af37 !important;
    }
    .stDataFrame td {
        color: #e0e0e0 !important;
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
    st.session_state.bias_5m = {'direction': 'MIXED', 'conviction': 50, 'note': ''}
if 'bias_15m' not in st.session_state:
    st.session_state.bias_15m = {'direction': 'MIXED', 'conviction': 50, 'note': ''}
if 'bias_1h' not in st.session_state:
    st.session_state.bias_1h = {'direction': 'MIXED', 'conviction': 50, 'note': ''}

if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "WAR ROOM"

if 'headlines' not in st.session_state:
    st.session_state.headlines = []

# Fetch RSS feed function
@st.cache_data(ttl=300)
def fetch_rss_feed():
    try:
        # Using a free financial RSS feed (Investing.com feed)
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
                        link = item.find('link').text if item.find('link') is not None else ""
                        
                        # Clean up titles
                        title = re.sub(r'[^\x00-\x7F]+', '', title)
                        if title and not title.startswith('('):
                            headlines.append({
                                'title': title[:150],
                                'time': pub_date[:16] if pub_date else datetime.now().strftime('%H:%M'),
                                'link': link
                            })
            except:
                continue
                
        # Add some sample headlines if feed fails
        if not headlines:
            headlines = [
                {'title': 'Market opens mixed as tech sector leads gains', 'time': datetime.now().strftime('%H:%M'), 'link': '#'},
                {'title': 'Fed signals cautious approach to rate cuts', 'time': datetime.now().strftime('%H:%M'), 'link': '#'},
                {'title': 'Oil prices stabilize after weekly decline', 'time': datetime.now().strftime('%H:%M'), 'link': '#'},
                {'title': 'Retail sales data beats expectations', 'time': datetime.now().strftime('%H:%M'), 'link': '#'},
            ]
        
        return headlines[:20]  # Limit to 20 headlines
    except:
        # Fallback headlines
        return [
            {'title': 'S&P 500 opens higher as tech stocks rally', 'time': datetime.now().strftime('%H:%M'), 'link': '#'},
            {'title': 'Fed rate decision looms, markets cautious', 'time': datetime.now().strftime('%H:%M'), 'link': '#'},
            {'title': 'Oil futures decline on demand concerns', 'time': datetime.now().strftime('%H:%M'), 'link': '#'},
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
        # Try to extract the numeric score
        score_match = re.search(r'[-+]?\d+\.?\d*', result)
        if score_match:
            score = float(score_match.group())
            score = max(-5, min(5, score))  # Clamp to [-5, 5]
            return score, result
        else:
            return 0, "Neutral"
    except Exception as e:
        st.error(f"AI Analysis Error: {str(e)}")
        return 0, "Analysis unavailable"

# Sidebar navigation
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h1 style='color: #d4af37;'>⚔️ THE ORB</h1>
    <h3 style='color: #d4af37;'>WAR ROOM / 01</h3>
    <hr style='border-color: #d4af37;'>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "COMMAND CENTER",
    ["🏛️ WAR ROOM", "📊 TRADE JOURNAL", "📈 BIAS MATRIX"],
    label_visibility="collapsed"
)

st.sidebar.markdown("""
<div style='text-align: center; color: #00ff00; font-size: 0.8rem;'>
    <span class="status-live">● LIVE</span><br>
    DATA LINK ACTIVE<br>
    NYSE / NASDAQ<br>
    Active trader
</div>
<br>
<div style='text-align: center; color: #666; font-size: 0.7rem;'>
    NEW YORK / 09:41 ET
</div>
""", unsafe_allow_html=True)

# Page content
if page == "🏛️ WAR ROOM":
    st.markdown("""
    <div class='command-center'>
        <h1 style='text-align: center;'>🏛️ WAR ROOM / 01</h1>
        <h3 style='text-align: center; color: #666;'>LIVE DESK</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h3>📰 LIVE TAPE</h3>", unsafe_allow_html=True)
        
        # Refresh button
        if st.button("🔄 Refresh Headlines"):
            st.cache_data.clear()
            st.rerun()
        
        # Fetch and display headlines
        headlines = fetch_rss_feed()
        st.session_state.headlines = headlines
        
        for idx, headline in enumerate(headlines):
            col_news, col_actions = st.columns([4, 1])
            with col_news:
                st.markdown(f"""
                <div class='news-item'>
                    <strong>{headline['time']}</strong> - {headline['title']}
                </div>
                """, unsafe_allow_html=True)
            with col_actions:
                if st.button("🔊", key=f"speak_{idx}"):
                    # Text-to-speech using browser's speech synthesis
                    js_code = f"""
                    <script>
                    var utterance = new SpeechSynthesisUtterance('{headline['title']}');
                    utterance.rate = 0.9;
                    window.speechSynthesis.speak(utterance);
                    </script>
                    """
                    st.components.v1.html(js_code, height=0)
                
                if st.button("📊", key=f"analyze_{idx}"):
                    with st.spinner("Analyzing sentiment..."):
                        score, reasoning = analyze_sentiment(headline['title'])
                        sentiment_color = "#00ff00" if score > 0 else "#ff0000" if score < 0 else "#d4af37"
                        st.markdown(f"""
                        <div style='background: #1a1a1a; padding: 0.5rem; border-radius: 4px; margin: 0.3rem 0;'>
                            <span style='color: {sentiment_color}; font-weight: 700;'>Score: {score:.1f}</span><br>
                            <span style='color: #999; font-size: 0.8rem;'>{reasoning[:100]}...</span>
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>📅 MACRO CALENDAR</h3>", unsafe_allow_html=True)
        
        # TradingView Economic Calendar Widget
        calendar_html = """
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
            {
                "colorTheme": "dark",
                "isTransparent": false,
                "width": "100%",
                "height": "500",
                "locale": "en",
                "importanceFilter": "1",
                "countryFilter": "US,EU,GB,CA,AU,CN,JP"
            }
            </script>
        </div>
        <!-- TradingView Widget END -->
        """
        st.components.v1.html(calendar_html, height=530)
        
        # Display some key economic events
        st.markdown("""
        <div class='card'>
            <h4 style='color: #d4af37;'>HIGH-IMPACT EVENTS</h4>
            <div style='font-size: 0.8rem;'>
                <div><span style='color: #ff0000;'>●</span> 09:00 Retail Sales YY Real*</div>
                <div><span style='color: #ff0000;'>●</span> 11:00 GDP Final QQ*</div>
                <div><span style='color: #ff0000;'>●</span> 12:00 Unemployment Rate</div>
                <div><span style='color: #ff0000;'>●</span> 15:30 Initial Jobless Claims*</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 TRADE JOURNAL":
    st.markdown("""
    <div class='command-center'>
        <h1 style='text-align: center;'>📊 TRADE JOURNAL</h1>
        <h3 style='text-align: center; color: #666;'>LOG & REVIEW</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### A / B / C LOGGER")
    st.markdown("*Capture the setup*")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        ticker = st.text_input("TICKER", placeholder="E.G. NVDA", key="ticker_input")
        
        direction = st.selectbox(
            "DIRECTION",
            ["Long", "Short"],
            key="direction_select"
        )
        
        grade = st.selectbox(
            "GRADE",
            ["A — clean", "B — mixed", "C — risky"],
            key="grade_select"
        )
        
        setup_type = st.selectbox(
            "SETUP TYPE",
            ["Opening range breakout", "VWAP pullback", "Breakout retest", "Trend continuation"],
            key="setup_select"
        )
    
    with col2:
        entry = st.number_input("ENTRY", value=0.00, step=0.01, key="entry_input")
        stop = st.number_input("STOPS", value=0.00, step=0.01, key="stop_input")
        target = st.number_input("TARGETS", value=0.00, step=0.01, key="target_input")
    
    with col3:
        st.markdown("### LEVELS")
        st.text_input("LEVELS", placeholder="19142.50 / 19108.25 / 19215.00", key="levels_input")
        
        st.markdown("### STATUS")
        status = st.selectbox(
            "RESULT STATUS",
            ["Planned", "Executed", "Closed (Win)", "Closed (Loss)"],
            key="status_select"
        )
    
    if st.button("⚔️ SAVE TO JOURNAL", use_container_width=True):
        if ticker and entry > 0:
            new_entry = pd.DataFrame({
                'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M')],
                'Ticker': [ticker.upper()],
                'Direction': [direction],
                'Grade': [grade.split(' — ')[0]],
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
    
    # Display trade log
    if not st.session_state.trade_log.empty:
        st.markdown("### 📊 RECENT JOURNAL")
        
        # Filter options
        filter_grade = st.selectbox(
            "FILTER BY GRADE",
            ["ALL", "A", "B", "C"],
            key="filter_grade"
        )
        
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
        
        # Stats
        total_trades = len(filtered_df)
        win_trades = len(filtered_df[filtered_df['Status'] == 'Closed (Win)'])
        loss_trades = len(filtered_df[filtered_df['Status'] == 'Closed (Loss)'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trades", total_trades)
        with col2:
            win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0
            st.metric("Win Rate", f"{win_rate:.1f}%")
        with col3:
            st.metric("Wins", win_trades)
        with col4:
            st.metric("Losses", loss_trades)
    else:
        st.info("📭 No trades logged yet. Start logging your executions above!")

elif page == "📈 BIAS MATRIX":
    st.markdown("""
    <div class='command-center'>
        <h1 style='text-align: center;'>📈 BIAS MATRIX</h1>
        <h3 style='text-align: center; color: #666;'>MULTI-TIMEFRAME</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Choose your weather.")
    st.markdown("*Write the map. Trade only when price agrees.*")
    
    col1, col2, col3 = st.columns(3)
    
    # 5m Bias
    with col1:
        st.markdown("""
        <div class='card'>
            <h4 style='text-align: center; color: #d4af37;'>5m</h4>
        </div>
        """, unsafe_allow_html=True)
        
        direction_5m = st.radio(
            "DIRECTIONAL READ",
            ["LONG", "MIXED", "SHORT"],
            key="bias_5m_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        conviction_5m = st.slider(
            "CONVICTION",
            0, 100, st.session_state.bias_5m['conviction'],
            key="conviction_5m"
        )
        
        note_5m = st.text_area(
            "OPERATOR NOTE",
            value=st.session_state.bias_5m['note'],
            placeholder="e.g., Holding above the opening range midpoint.",
            key="note_5m",
            height=60
        )
        
        if st.button("💾 SAVE 5M BIAS", key="save_5m", use_container_width=True):
            st.session_state.bias_5m = {
                'direction': direction_5m,
                'conviction': conviction_5m,
                'note': note_5m
            }
            st.success("5m bias saved!")
        
        # Display saved bias
        st.markdown(f"""
        <div style='background: #1a1a1a; padding: 0.5rem; border-radius: 4px;'>
            <strong>Current Bias:</strong> 
            <span style='color: {"#00ff00" if st.session_state.bias_5m["direction"] == "LONG" else "#ff0000" if st.session_state.bias_5m["direction"] == "SHORT" else "#d4af37"};'>
                {st.session_state.bias_5m["direction"]}
            </span><br>
            <strong>Conviction:</strong> <span style='color: #d4af37;'>{st.session_state.bias_5m["conviction"]}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 15m Bias
    with col2:
        st.markdown("""
        <div class='card'>
            <h4 style='text-align: center; color: #d4af37;'>15m</h4>
        </div>
        """, unsafe_allow_html=True)
        
        direction_15m = st.radio(
            "DIRECTIONAL READ",
            ["LONG", "MIXED", "SHORT"],
            key="bias_15m_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        conviction_15m = st.slider(
            "CONVICTION",
            0, 100, st.session_state.bias_15m['conviction'],
            key="conviction_15m"
        )
        
        note_15m = st.text_area(
            "OPERATOR NOTE",
            value=st.session_state.bias_15m['note'],
            placeholder="e.g., Compression into the prior day high.",
            key="note_15m",
            height=60
        )
        
        if st.button("💾 SAVE 15M BIAS", key="save_15m", use_container_width=True):
            st.session_state.bias_15m = {
                'direction': direction_15m,
                'conviction': conviction_15m,
                'note': note_15m
            }
            st.success("15m bias saved!")
        
        # Display saved bias
        st.markdown(f"""
        <div style='background: #1a1a1a; padding: 0.5rem; border-radius: 4px;'>
            <strong>Current Bias:</strong> 
            <span style='color: {"#00ff00" if st.session_state.bias_15m["direction"] == "LONG" else "#ff0000" if st.session_state.bias_15m["direction"] == "SHORT" else "#d4af37"};'>
                {st.session_state.bias_15m["direction"]}
            </span><br>
            <strong>Conviction:</strong> <span style='color: #d4af37;'>{st.session_state.bias_15m["conviction"]}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 1h Bias
    with col3:
        st.markdown("""
        <div class='card'>
            <h4 style='text-align: center; color: #d4af37;'>1h</h4>
        </div>
        """, unsafe_allow_html=True)
        
        direction_1h = st.radio(
            "DIRECTIONAL READ",
            ["LONG", "MIXED", "SHORT"],
            key="bias_1h_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        conviction_1h = st.slider(
            "CONVICTION",
            0, 100, st.session_state.bias_1h['conviction'],
            key="conviction_1h"
        )
        
        note_1h = st.text_area(
            "OPERATOR NOTE",
            value=st.session_state.bias_1h['note'],
            placeholder="e.g., Still below the weekly VWAP band.",
            key="note_1h",
            height=60
        )
        
        if st.button("💾 SAVE 1H BIAS", key="save_1h", use_container_width=True):
            st.session_state.bias_1h = {
                'direction': direction_1h,
                'conviction': conviction_1h,
                'note': note_1h
            }
            st.success("1h bias saved!")
        
        # Display saved bias
        st.markdown(f"""
        <div style='background: #1a1a1a; padding: 0.5rem; border-radius: 4px;'>
            <strong>Current Bias:</strong> 
            <span style='color: {"#00ff00" if st.session_state.bias_1h["direction"] == "LONG" else "#ff0000" if st.session_state.bias_1h["direction"] == "SHORT" else "#d4af37"};'>
                {st.session_state.bias_1h["direction"]}
            </span><br>
            <strong>Conviction:</strong> <span style='color: #d4af37;'>{st.session_state.bias_1h["conviction"]}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Desk discipline note
    st.markdown("""
    <hr style='border-color: #d4af37;'>
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
