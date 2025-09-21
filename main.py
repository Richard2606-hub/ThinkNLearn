import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="AI Language Learning Companion",
    page_icon="🌍",
    layout="wide"
)

# --- Custom CSS (to keep your original decoration) ---
st.markdown("""
    <style>
    .title {font-size:42px;font-weight:700;color:#333;text-align:center;}
    .title span {color:#4361ee;}
    .subtitle {text-align:center;font-size:20px;color:#555;}
    .stat-value {font-size:2rem;font-weight:700;color:#4361ee;}
    .tip-item {background:#f8f9fa;padding:15px;border-radius:8px;
               border-left:4px solid #4cc9f0;margin-bottom:15px;}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title">Language <span>Companion</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Breaking barriers, one language at a time 🌍</div>', unsafe_allow_html=True)
st.write("---")

# --- Sidebar Navigation ---
st.sidebar.title("📚 Learning Modules")
module = st.sidebar.radio(
    "Choose a Module:",
    [
        "💬 Feedback Generator",
        "❓ Quiz",
        "🗣 Dialogue Practice",
        "✍️ Self Test",
        "📖 Idioms & Expressions",
        "🎮 Gamified Learning",
        "📊 Progress Tracking"
    ]
)

# --- Feedback Generator ---
if "Feedback" in module:
    st.header("💬 Feedback Generator")
    user_text = st.text_area("Enter your text for feedback", "I goes to market yesterday.")
    level = st.selectbox("Select your proficiency level", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Generate Feedback"):
        # Placeholder – replace with Gemini/Lambda call later
        st.subheader("Feedback Results")
        st.write("✅ **Corrected Text:** I went to the market yesterday.")
        st.write("📖 **Explanation:** Past tense required after 'yesterday'.")
        st.write("💡 **Quick Tips:** Use 'went' for past actions.")

# --- Quiz ---
elif "Quiz" in module:
    st.header("❓ Quiz Module")
    st.write("This module will contain interactive quizzes to test your knowledge.")
    category = st.selectbox("Select Quiz Category", ["Grammar", "Vocabulary", "Reading Comprehension"])
    if st.button("Start Quiz"):
        st.success(f"Starting a {category} quiz...")

# --- Dialogue Practice ---
elif "Dialogue" in module:
    st.header("🗣 Dialogue Practice")
    st.write("This module will help you practice conversational skills.")
    scenario = st.selectbox("Select Scenario", ["Restaurant Ordering", "Asking for Directions", "Hotel Check-in"])
    if st.button("Start Practice"):
        st.success(f"Practicing scenario: {scenario}")

# --- Self Test ---
elif "Self Test" in module:
    st.header("✍️ Self Test")
    st.write("This module will allow you to test your knowledge.")
    if st.button("Begin Test"):
        st.success("Self Test started!")

# --- Idioms ---
elif "Idioms" in module:
    st.header("📖 Idioms & Expressions")
    idiom_type = st.selectbox("Select Category", ["Business Idioms", "Everyday Expressions", "Slang Terms"])
    if st.button("Explore Idioms"):
        st.info(f"Exploring {idiom_type}...")

# --- Gamified Learning ---
elif "Gamified" in module:
    st.header("🎮 Gamified Learning")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Level", "7", "Language Explorer")
    with col2:
        st.metric("Points", "1,245", "Top 30%")
    with col3:
        st.metric("Badges", "5", "Collect more!")
    if st.button("Play Games"):
        st.success("Launching games...")

# --- Progress Tracking ---
elif "Progress" in module:
    st.header("📊 Progress Tracking")
    col1, col2, col3 = st.columns(3)
    col1.metric("Days Streak", "12", "Keep going!")
    col2.metric("Words Learned", "247", "+15 this week")
    col3.metric("Accuracy", "78%", "Improved by 5%")

    st.subheader("Weekly Progress")
    st.progress(0.65)
    st.write("You've completed 65% of your weekly goal")

    st.subheader("Learning Tips")
    st.markdown('<div class="tip-item"><b>Practice Regularly</b><br>Try at least 15 minutes every day.</div>', unsafe_allow_html=True)
    st.markdown('<div class="tip-item"><b>Review Mistakes</b><br>Go back to previous errors to improve.</div>', unsafe_allow_html=True)

# --- Footer ---
st.write("---")
st.caption("© 2025 Language Companion. Built with Streamlit 🌍")
