import streamlit as st
import streamlit as st
import requests

API_URL = "https://owivtumnfb.execute-api.ap-southeast-5.amazonaws.com/i"

st.title("Gemini via Lambda + API Gateway")

user_input = st.text_area("Ask Gemini:")

if st.button("Send"):
    resp = requests.post(API_URL, json={"input": user_input})
    if resp.status_code == 200:
        st.write("Gemini says:", resp.json()["reply"])
    else:
        st.error(f"Error {resp.status_code}: {resp.text}")



# --- Streamlit Page Config ---
st.set_page_config(page_title="Language Companion", page_icon="🌍", layout="wide")

# --- Inject CSS from your HTML theme ---
st.markdown("""
    <style>
    /* Global */
    body {background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);}
    .main {background: none;}
    .block-container {padding-top: 0rem; padding-bottom: 0rem;}
    
    /* Header */
    .app-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 25px; background: white; border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    .logo {display: flex; align-items: center; gap: 12px;}
    .logo h1 {margin:0; font-size: 28px; font-weight:700; color:#333;}
    .logo span {color:#4361ee;}
    .header-buttons button {
        padding:10px 20px; border-radius:50px; font-weight:600; cursor:pointer;
        margin-left:10px; transition: all 0.3s ease;
    }
    .btn-outline {
        border:2px solid #4361ee; background:white; color:#4361ee;
    }
    .btn-outline:hover {background:#f0f4ff;}
    .btn-primary {
        border:none; background:#4361ee; color:white;
    }
    .btn-primary:hover {background:#3a56d4;}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: white; border-radius: 12px; padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    section[data-testid="stSidebar"] h1 {font-size: 1.5rem; margin-bottom: 20px;}
    
    /* Cards */
    .card {
        background:white; padding:25px; border-radius:12px;
        box-shadow:0 5px 15px rgba(0,0,0,0.05); margin-bottom:20px;
    }
    .card h2 {margin-bottom:15px; font-size:1.4rem; color:#333;}
    </style>
""", unsafe_allow_html=True)

# --- Custom Header ---
st.markdown("""
<div class="app-header">
    <div class="logo">
        <span style="font-size:30px;color:#4361ee;">🅰️</span>
        <h1>Language <span>Companion</span></h1>
    </div>
    <div class="header-buttons">
        <button class="btn-outline">👤 Guest Mode</button>
        <button class="btn-primary">⚙ Settings</button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Learning Modules")
module = st.sidebar.radio(
    "Select a module:",
    ["💬 Feedback Generator", "❓ Quiz", "🗣 Dialogue Practice",
     "✍ Self Test", "📖 Idioms & Expressions",
     "🎮 Gamified Learning", "📊 Progress Tracking"]
)

# --- Module Pages ---
if "Feedback" in module:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 💬 Feedback Generator")
    text = st.text_area("Enter your text for feedback", "I goes to market yesterday.")
    level = st.selectbox("Select your proficiency level", ["Beginner", "Intermediate", "Advanced"])
    if st.button("🔮 Generate Feedback"):
        # Placeholder (connect to Gemini/Lambda later)
        st.success("Corrected: **I went to the market yesterday.**")
        st.info("Explanation: 'yesterday' means past tense, so use 'went'.")
    st.markdown('</div>', unsafe_allow_html=True)

elif "Quiz" in module:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## ❓ Quiz Module")
    st.write("Test your knowledge with quick quizzes.")
    category = st.selectbox("Choose a category", ["Grammar", "Vocabulary", "Reading"])
    if st.button("▶ Start Quiz"):
        st.success(f"Launching {category} quiz...")
    st.markdown('</div>', unsafe_allow_html=True)

elif "Dialogue" in module:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🗣 Dialogue Practice")
    scenario = st.selectbox("Pick a scenario", ["Restaurant", "Directions", "Hotel Check-in"])
    if st.button("▶ Start Practice"):
        st.success(f"Starting {scenario} dialogue...")
    st.markdown('</div>', unsafe_allow_html=True)

elif "Self Test" in module:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## ✍ Self Test")
    if st.button("Begin Test"):
        st.success("Self Test started!")
    st.markdown('</div>', unsafe_allow_html=True)

elif "Idioms" in module:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📖 Idioms & Expressions")
    idiom = st.selectbox("Select category", ["Business", "Everyday", "Slang"])
    if st.button("Explore"):
        st.info(f"Showing {idiom} idioms...")
    st.markdown('</div>', unsafe_allow_html=True)

elif "Gamified" in module:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎮 Gamified Learning")
    col1, col2, col3 = st.columns(3)
    col1.metric("Level", "7")
    col2.metric("Points", "1245")
    col3.metric("Badges", "5")
    if st.button("▶ Play Game"):
        st.success("Launching gamified activity...")
    st.markdown('</div>', unsafe_allow_html=True)

elif "Progress" in module:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 Progress Tracking")
    col1, col2, col3 = st.columns(3)
    col1.metric("Day Streak", "12")
    col2.metric("Words Learned", "247")
    col3.metric("Accuracy", "78%")
    st.progress(0.65)
    st.info("Weekly Goal: 65% complete")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("<p style='text-align:center;color:#777;margin-top:40px;'>© 2025 Language Companion</p>", unsafe_allow_html=True)
