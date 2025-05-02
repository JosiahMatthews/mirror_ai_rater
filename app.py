import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Page Config ---
st.set_page_config(page_title="Mirror AI Evaluator", page_icon="🔮", layout="centered")

# --- Custom Style ---
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        background-color: #0d1117;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    .big-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section {
        margin-bottom: 1.5rem;
    }
    .score-card {
        padding: 1rem;
        background: #161b22;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .highlight {
        color: #58a6ff;
        font-weight: bold;
    }
    .probability-bar {
        height: 22px;
        background: linear-gradient(90deg, #00FF85 0%, #FFD000 50%, #FF3B3B 100%);
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='big-title'>🔮 Mirror AI Call Evaluator</div>", unsafe_allow_html=True)

# --- Inputs ---
rep_name = st.text_input("👤 Name of Rep", placeholder="e.g. Josiah")
reviewer_name = st.text_input("🧠 Name of Reviewer", value="Mirror AI Coach")
call_date = st.date_input("📆 Date of Call", value=datetime.today())
uploaded_file = st.file_uploader("📎 Upload Call Transcript (.txt)", type=["txt"])

if uploaded_file:
    transcript = uploaded_file.read().decode("utf-8")
    word_count = len(transcript.split())
    call_length = f"{round(word_count / 140)} minutes"

    lowered = transcript.lower()
    if any(kw in lowered for kw in ["i'm ready to get started", "let's do it"]):
        call_outcome = "Yes"
    elif any(kw in lowered for kw in ["i need to check", "talk to my partner"]):
        call_outcome = "Soft Yes"
    elif any(kw in lowered for kw in ["i'll think about it", "not now"]):
        call_outcome = "Soft No"
    else:
        call_outcome = "Objection follow-up"

    with st.spinner("🧠 Analyzing call transcript..."):
        system_prompt = f"""
You are a brutal, elite-level sales evaluator using the MIRRORS + F.A.S.T. framework only.
Score 1-5 for each category, note strengths and timestamp failures, then summarize close probability.

MIRRORS:
Map The Mission → trust + goal clarity  
Investigate Actions → past efforts + inconsistency  
Reveal The Root → emotional depth + frustration  
Reframe The Gap → break DIY illusion  
Outline The Dream → personal goals + identity  
Risk of Future → fear of staying stuck  
Secure The Yes → urgency + identity match

F.A.S.T.:
Foundation → dream outcomes  
Ascension → pains matched to offer  
Shift → clear transformation  
Timeline & Trust → realistic, grounded belief

Give:
1. Each section score 1–5  
2. Close probability (0–100%)  
3. Summary of strengths/weaknesses  
4. Two clear coaching action steps

Rep: {rep_name} | Reviewer: {reviewer_name} | Date: {call_date.strftime('%Y-%m-%d')} | Length: {call_length} | Outcome: {call_outcome}
"""
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ]
        )

        feedback = response.choices[0].message.content
        st.success("✅ Review complete!")

        # --- Visual Enhancements ---
        if "probability to close" in feedback.lower():
            import re
            match = re.search(r"Probability to close: (\d+)%", feedback)
            if match:
                pct = int(match.group(1))
                st.markdown("### 🔥 Probability to Close")
                st.progress(pct / 100)

        st.download_button("⬇️ Download Feedback", feedback, file_name="call_review.txt")
        st.text_area("📋 Full Feedback", value=feedback, height=600)

else:
    st.info("📄 Upload a transcript to begin your evaluation.")
