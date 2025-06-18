import streamlit as st
import openai
import json
import time
import random
from datetime import datetime, date

# Page config
st.set_page_config(
    page_title="🎯 UPSC MCQ Master",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Dynamic CSS with animations
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    animation: slideDown 0.8s ease-out;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

@keyframes slideDown {
    from { transform: translateY(-50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes fadeInUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

.main-header h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    animation: bounce 2s ease-in-out infinite;
}

.main-header p {
    font-size: 1.4rem;
    opacity: 0.95;
    font-weight: 300;
}

.metric-container {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    animation: fadeInUp 0.6s ease-out;
    transition: all 0.3s ease;
}

.metric-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

.custom-metric {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    color: white;
    margin: 0.5rem;
    transition: all 0.3s ease;
    animation: fadeInUp 0.8s ease-out;
}

.custom-metric:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
}

.metric-label {
    font-size: 1rem;
    opacity: 0.9;
    font-weight: 400;
}

.topic-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
    animation: fadeInUp 1s ease-out;
}

.topic-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    border: 2px solid transparent;
    transition: all 0.4s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.topic-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
    transition: left 0.5s;
}

.topic-card:hover::before {
    left: 100%;
}

.topic-card:hover {
    transform: translateY(-10px) scale(1.02);
    border-color: #667eea;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}

.topic-emoji {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
    animation: bounce 2s ease-in-out infinite;
}

.topic-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
}

.topic-subtitle {
    color: #666;
    font-size: 0.9rem;
    opacity: 0.8;
}

.question-container {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 25px;
    padding: 3rem;
    margin: 2rem 0;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.3);
    animation: fadeInUp 0.8s ease-out;
    position: relative;
    overflow: hidden;
}

.question-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
    background-size: 200% 100%;
    animation: gradientShift 3s ease-in-out infinite;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.question-text {
    font-size: 1.4rem;
    line-height: 1.7;
    color: #333;
    font-weight: 500;
    margin-bottom: 2rem;
}

.option-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border: 2px solid #e9ecef;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.option-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.5s;
}

.option-card:hover::before {
    left: 100%;
}

.option-card:hover {
    transform: translateX(10px);
    border-color: #667eea;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

.option-correct {
    background: linear-gradient(145deg, #d4edda 0%, #c3e6cb 100%) !important;
    border-color: #28a745 !important;
    color: #155724 !important;
    animation: pulse 1s ease-in-out;
}

.option-incorrect {
    background: linear-gradient(145deg, #f8d7da 0%, #f5c6cb 100%) !important;
    border-color: #dc3545 !important;
    color: #721c24 !important;
    animation: shake 0.5s ease-in-out;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

.explanation-container {
    background: linear-gradient(145deg, #e3f2fd 0%, #bbdefb 100%);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    border-left: 5px solid #2196f3;
    animation: slideInLeft 0.8s ease-out;
    box-shadow: 0 10px 30px rgba(33, 150, 243, 0.2);
}

@keyframes slideInLeft {
    from { transform: translateX(-50px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.explanation-title {
    color: #1976d2;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.explanation-text {
    line-height: 1.6;
    color: #0d47a1;
    font-size: 1.1rem;
}

.action-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.action-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    filter: brightness(1.1);
}

.action-button:active {
    transform: translateY(-1px);
}

.secondary-button {
    background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(108, 117, 125, 0.3);
}

.secondary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
}

.loading-container {
    text-align: center;
    padding: 4rem 2rem;
    animation: fadeInUp 0.6s ease-out;
}

.loading-spinner {
    width: 60px;
    height: 60px;
    border: 6px solid rgba(102, 126, 234, 0.3);
    border-top: 6px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 2rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-text {
    font-size: 1.3rem;
    color: #667eea;
    font-weight: 500;
    animation: pulse 2s ease-in-out infinite;
}

.success-message {
    background: linear-gradient(145deg, #d4edda 0%, #c3e6cb 100%);
    color: #155724;
    padding: 1.5rem;
    border-radius: 15px;
    border-left: 5px solid #28a745;
    margin: 1rem 0;
    animation: slideInRight 0.6s ease-out;
    box-shadow: 0 5px 15px rgba(40, 167, 69, 0.2);
}

.error-message {
    background: linear-gradient(145deg, #f8d7da 0%, #f5c6cb 100%);
    color: #721c24;
    padding: 1.5rem;
    border-radius: 15px;
    border-left: 5px solid #dc3545;
    margin: 1rem 0;
    animation: slideInRight 0.6s ease-out;
    box-shadow: 0 5px 15px rgba(220, 53, 69, 0.2);
}

@keyframes slideInRight {
    from { transform: translateX(50px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.bookmark-btn {
    background: linear-gradient(135deg, #ffc107 0%, #ff8f00 100%);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    animation: bounce 2s ease-in-out infinite;
}

.bookmark-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 25px rgba(255, 193, 7, 0.4);
}

.sidebar-section {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    animation: fadeInUp 0.8s ease-out;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2.5rem;
    }
    
    .topic-grid {
        grid-template-columns: 1fr;
    }
    
    .question-container {
        padding: 2rem 1.5rem;
    }
    
    .custom-metric {
        margin: 0.25rem;
        padding: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
    }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}
            
/* Fix white bars and spacing issues */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}

/* Remove default Streamlit spacing */
.stButton > button {
    margin: 0;
    border-radius: 15px !important;
    height: auto !important;
    min-height: 60px;
    white-space: pre-line !important;
    line-height: 1.4 !important;
    font-size: 0.9rem !important;
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%) !important;
    border: 2px solid #e9ecef !important;
    color: #333 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    border-color: #667eea !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2) !important;
    background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%) !important;
}

/* Fix column spacing */
.element-container {
    margin-bottom: 0 !important;
}

/* Remove extra padding */
.stMarkdown {
    margin-bottom: 0 !important;
}

/* Ensure consistent spacing */
div[data-testid="column"] {
    padding: 0.5rem;
}

/* Topic button specific styling */
.stButton > button[kind="secondary"] {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%) !important;
    border: 2px solid #e9ecef !important;
    padding: 1.5rem !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'total_points' not in st.session_state:
        st.session_state.total_points = 0
    if 'today_questions' not in st.session_state:
        st.session_state.today_questions = 0
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = ''
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    if 'bookmarked_questions' not in st.session_state:
        st.session_state.bookmarked_questions = []
    if 'daily_goal' not in st.session_state:
        st.session_state.daily_goal = 10  # Default goal: 10 questions per day

# OpenAI API function
def generate_mcq_question(topic, api_key):
    try:
        openai.api_key = api_key
        
        prompt = f"""
        Generate a high-quality UPSC Civil Services examination multiple choice question on {topic}.
        
        Requirements:
        1. Question should be at UPSC Prelims level difficulty
        2. Should test conceptual understanding, not just memorization
        3. Include 4 options (A, B, C, D)
        4. Provide detailed explanation for the correct answer
        5. Explanation should help in learning the concept
        
        Return the response in this exact JSON format:
        {{
            "question": "Your question here",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Detailed explanation here"
        }}
        
        Topic: {topic}
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
        
        question_data = json.loads(content)
        return question_data
        
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        return None

# Enhanced stats display
def display_stats():
    accuracy = 0
    if st.session_state.today_questions > 0:
        accuracy = round((st.session_state.correct_answers / st.session_state.today_questions) * 100)
    
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="metric-value">{st.session_state.total_points}</div>
            <div class="metric-label">Total Points</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="metric-value">100</div>
            <div class="metric-label">Daily Goal</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="metric-value">{st.session_state.today_questions}</div>
            <div class="metric-label">Today's Questions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="metric-value">{accuracy}%</div>
            <div class="metric-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    init_session_state()
    
    # Dynamic Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 UPSC MCQ Master</h1>
        <p>AI-Powered Unlimited Questions with Dynamic Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("⚙️ Configuration")
        
        api_key = st.text_input(
            "🔑 OpenAI API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your OpenAI API key to generate questions",
            placeholder="sk-..."
        )
        
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
        
        if st.session_state.api_key:
            st.markdown('<div class="success-message">✅ API Key configured successfully!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠️ Please add your OpenAI API key to continue</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Bookmarks Section
        if st.session_state.bookmarked_questions:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.header("⭐ Bookmarked Questions")
            for i, bookmark in enumerate(st.session_state.bookmarked_questions):
                if st.button(f"📝 {bookmark['topic']} - Question {i+1}", key=f"bookmark_{i}"):
                    st.session_state.current_question = bookmark
                    st.session_state.quiz_active = True
                    st.session_state.answer_submitted = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Daily Goal Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("🎯 Daily Goal")
        goal_options = [10, 20, 50, 100]
        current_goal_index = goal_options.index(st.session_state.daily_goal) if st.session_state.daily_goal in goal_options else 0
        
        selected_goal = st.selectbox(
            "Set your daily question goal:",
            options=goal_options,
            index=current_goal_index,
            format_func=lambda x: f"{x} questions per day"
        )
        
        if selected_goal != st.session_state.daily_goal:
            st.session_state.daily_goal = selected_goal
            st.success(f"Daily goal updated to {selected_goal} questions!")
            st.rerun()
        
        # Progress bar for daily goal
        progress = min(st.session_state.today_questions / st.session_state.daily_goal, 1.0)
        st.progress(progress)
        st.write(f"Progress: {st.session_state.today_questions}/{st.session_state.daily_goal} questions")
        
        if st.session_state.today_questions >= st.session_state.daily_goal:
            st.success("🎉 Daily goal achieved! Great work!")
            st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Reset Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("🔄 Reset Options")
        if st.button("Reset All Stats", type="secondary"):
            st.session_state.total_points = 0
            st.session_state.today_questions = 0
            st.session_state.correct_answers = 0
            st.success("Stats reset successfully!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# MODIFY the display_stats function (around line 450) - replace the second metric with:
    col1, col2 = st.columns(2)
    with col2:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="metric-value">{st.session_state.daily_goal}</div>
            <div class="metric-label">Daily Goal</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Reset Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("🔄 Reset Options")
        if st.button("Reset All Stats", key="reset_stats", type="secondary"):
            st.session_state.total_points = 0
            st.session_state.today_questions = 0
            st.session_state.correct_answers = 0
            st.success("Stats reset successfully!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display enhanced stats
    display_stats()
    
    # Main content with API key check
    if not st.session_state.api_key:
        st.markdown("""
        <div class="question-container">
            <div class="question-text">
                👈 Please enter your OpenAI API key in the sidebar to start your UPSC preparation journey!
            </div>
            <div class="explanation-container">
                <div class="explanation-title">📋 How to get your OpenAI API Key:</div>
                <div class="explanation-text">
                    1. Go to <strong>https://platform.openai.com/</strong><br>
                    2. Sign up or log in to your account<br>
                    3. Navigate to the <strong>API Keys</strong> section<br>
                    4. Create a new secret key<br>
                    5. Copy and paste it in the sidebar<br>
                    6. Start generating unlimited UPSC questions!
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if not st.session_state.quiz_active:
        # Enhanced Topic Selection
        st.markdown('<h2 style="text-align: center; color: #333; margin: 2rem 0;">📚 Choose Your UPSC Topic</h2>', unsafe_allow_html=True)
        
        topics_data = [
            {"emoji": "📜", "title": "History", "subtitle": "Ancient, Medieval & Modern"},
            {"emoji": "🌍", "title": "Geography", "subtitle": "Physical & Human Geography"},
            {"emoji": "🏛️", "title": "Polity", "subtitle": "Constitution & Governance"},
            {"emoji": "💰", "title": "Economy", "subtitle": "Macro & Micro Economics"},
            {"emoji": "🌱", "title": "Environment", "subtitle": "Ecology & Climate"},
            {"emoji": "🔬", "title": "Science & Technology", "subtitle": "Latest Developments"},
            {"emoji": "📰", "title": "Current Affairs", "subtitle": "National & International"},
            {"emoji": "🎨", "title": "Art & Culture", "subtitle": "Heritage & Traditions"}
        ]
        
        st.markdown('<div class="topic-grid">', unsafe_allow_html=True)
        
        cols = st.columns(4)
        for i, topic_data in enumerate(topics_data):
            with cols[i % 4]:
                if st.button("Select", key=f"topic_{i}", use_container_width=True):
                    st.session_state.selected_topic = topic_data["title"]
                    start_quiz()
                
                st.markdown(f"""
                <div class="topic-card" onclick="document.querySelector('[key=topic_{i}]').click()">
                    <span class="topic-emoji">{topic_data["emoji"]}</span>
                    <div class="topic-title">{topic_data["title"]}</div>
                    <div class="topic-subtitle">{topic_data["subtitle"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Enhanced Quiz interface
        display_quiz()

def start_quiz():
    """Start quiz with enhanced loading animation"""
    st.session_state.quiz_active = True
    st.session_state.answer_submitted = False
    
    # Show loading state
    st.markdown(f"""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <div class="loading-text">🤖 Generating {st.session_state.selected_topic} question...</div>
        <p style="color: #666; margin-top: 1rem;">Crafting the perfect question just for you!</p>
    </div>
    """, unsafe_allow_html=True)
    
    question_data = generate_mcq_question(st.session_state.selected_topic, st.session_state.api_key)
    
    if question_data:
        st.session_state.current_question = question_data
        st.session_state.current_question['topic'] = st.session_state.selected_topic
        time.sleep(1)  # Brief pause for effect
        st.rerun()
    else:
        st.markdown('<div class="error-message">Failed to generate question. Please try again.</div>', unsafe_allow_html=True)
        st.session_state.quiz_active = False

def display_quiz():
    """Display the current quiz question with enhanced UI"""
    if not st.session_state.current_question:
        start_quiz()
        return
    
    question = st.session_state.current_question
    
    # Enhanced Question header
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"""
        <h2 style="color: #333; margin-bottom: 1rem;">
            📝 {question.get('topic', 'Unknown')} Challenge
        </h2>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("⭐ Bookmark", key="bookmark_btn", help="Save this question for later review"):
            if question not in st.session_state.bookmarked_questions:
                st.session_state.bookmarked_questions.append(question.copy())
                st.markdown('<div class="success-message">Question bookmarked successfully! ⭐</div>', unsafe_allow_html=True)
                time.sleep(1)
            else:
                st.markdown('<div class="error-message">Question already bookmarked!</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("← Back to Topics", key="back_btn"):
            st.session_state.quiz_active = False
            st.session_state.current_question = None
            st.session_state.answer_submitted = False
            st.rerun()
    
    # Enhanced Question display
    st.markdown(f"""
    <div class="question-container">
        <div class="question-text">{question['question']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Options
    if not st.session_state.answer_submitted:
        st.markdown('<h3 style="color: #333; margin: 2rem 0 1rem 0;">🤔 Choose your answer:</h3>', unsafe_allow_html=True)
        
        for i, option in enumerate(question['options']):
            if st.button(f"{chr(65+i)}. {option}", key=f"option_{i}", use_container_width=True):
                submit_answer(i)
                break
        
        st.markdown(f"""
        <div style="margin-top: 2rem;">
            <div class="option-card">
                💡 <strong>Tip:</strong> Read all options carefully before selecting your answer!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Enhanced results display
        display_results()

def submit_answer(selected_option):
    """Process the submitted answer with enhanced feedback"""
    question = st.session_state.current_question
    correct_answer = question['correct_answer']
    
    st.session_state.today_questions += 1
    st.session_state.selected_answer = selected_option
    
    if selected_option == correct_answer:
        st.session_state.total_points += 1
        st.session_state.correct_answers += 1
    
    st.session_state.answer_submitted = True
    st.rerun()

def display_results():
    """Display enhanced results with animations and feedback"""
    question = st.session_state.current_question
    selected = st.session_state.selected_answer
    correct = question['correct_answer']
    
    st.markdown('<h3 style="color: #333; margin: 2rem 0 1rem 0;">📊 Your Results:</h3>', unsafe_allow_html=True)
    
    # Display options with results
    for i, option in enumerate(question['options']):
        if i == correct and i == selected:
            # Correct answer selected
            st.markdown(f"""
            <div class="option-card option-correct">
                ✅ {chr(65+i)}. {option} <strong>(Correct! Well done!)</strong>
            </div>
            """, unsafe_allow_html=True)
        elif i == correct:
            # Correct answer not selected
            st.markdown(f"""
            <div class="option-card option-correct">
                ✅ {chr(65+i)}. {option} <strong>(Correct Answer)</strong>
            </div>
            """, unsafe_allow_html=True)
        elif i == selected:
            # Wrong answer selected
            st.markdown(f"""
            <div class="option-card option-incorrect">
                ❌ {chr(65+i)}. {option} <strong>(Your Answer - Incorrect)</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Other options
            st.markdown(f"""
            <div class="option-card">
                {chr(65+i)}. {option}
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced explanation section
    st.markdown(f"""
    <div class="explanation-container">
        <div class="explanation-title">💡 Detailed Explanation</div>
        <div class="explanation-text">{question['explanation']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Results summary with animations
    if selected == correct:
        st.markdown("""
        <div class="success-message">
            🎉 <strong>Excellent!</strong> You got it right! Keep up the great work!
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("""
        <div class="error-message">
            💪 <strong>Don't worry!</strong> Every mistake is a learning opportunity. Review the explanation and try again!
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown('<div style="margin: 2rem 0; text-align: center;">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎯 Next Question", key="next_question", use_container_width=True):
            start_quiz()
    
    with col2:
        if st.button("📚 Change Topic", key="change_topic", use_container_width=True):
            st.session_state.quiz_active = False
            st.session_state.current_question = None
            st.session_state.answer_submitted = False
            st.rerun()
    
    with col3:
        if st.button("📊 View Stats", key="view_stats", use_container_width=True):
            show_detailed_stats()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_detailed_stats():
    """Display detailed statistics modal"""
    accuracy = 0
    if st.session_state.today_questions > 0:
        accuracy = round((st.session_state.correct_answers / st.session_state.today_questions) * 100)
    
    st.markdown(f"""
    <div class="question-container">
        <h2 style="text-align: center; color: #333; margin-bottom: 2rem;">📈 Your Performance Statistics</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
            <div class="custom-metric">
                <div class="metric-value">{st.session_state.total_points}</div>
                <div class="metric-label">Total Points Earned</div>
            </div>
            <div class="custom-metric">
                <div class="metric-value">{st.session_state.today_questions}</div>
                <div class="metric-label">Questions Attempted</div>
            </div>
            <div class="custom-metric">
                <div class="metric-value">{st.session_state.correct_answers}</div>
                <div class="metric-label">Correct Answers</div>
            </div>
            <div class="custom-metric">
                <div class="metric-value">{accuracy}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
        </div>
        
        <div class="explanation-container">
            <div class="explanation-title">🎯 Performance Analysis</div>
            <div class="explanation-text">
                {'🌟 Outstanding performance! You\'re doing excellent!' if accuracy >= 80 else
                 '💪 Good work! Keep practicing to improve further!' if accuracy >= 60 else
                 '📚 Focus on studying the explanations to boost your performance!'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced footer
def display_footer():
    """Display enhanced footer with additional information"""
    st.markdown("""
    <div style="margin-top: 4rem; padding: 2rem; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white;">
        <h3 style="margin-bottom: 1rem;">🚀 UPSC MCQ Master</h3>
        <p style="opacity: 0.9; margin-bottom: 1rem;">AI-Powered Unlimited Practice Questions for UPSC Preparation</p>
        <p style="opacity: 0.8; font-size: 0.9rem;">
            💡 Tip: Practice daily for better results | 📚 Review explanations carefully | 🎯 Focus on weak areas
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    display_footer()