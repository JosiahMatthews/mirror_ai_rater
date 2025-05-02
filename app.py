import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Mirror AI Call Evaluator", page_icon="🔮", layout="centered")
st.title("🔮 Mirror AI Call Evaluator")

# === Section: Rep Info ===
st.markdown("### 🧑 Rep Information")
rep_name = st.text_input("Name of Rep", placeholder="e.g. Josiah")
reviewer_name = st.text_input("Name of Reviewer", value="Mirror AI Coach")
call_date = st.date_input("Date of Call", value=datetime.today())

# === Section: Call Outcome ===
st.markdown("### 📈 Outcome")
call_closed = st.checkbox("✅ Did the call close?")
revenue_total = st.number_input("💵 Revenue Collected (if closed)", min_value=0, step=100, format="%d") if call_closed else None

# === Section: Transcript Upload ===
st.markdown("### 📝 Upload Call Transcript (.txt)")
uploaded_file = st.file_uploader("Upload Transcript", type=["txt"])

if uploaded_file is not None:
    transcript = uploaded_file.read().decode("utf-8")
    word_count = len(transcript.split())
    call_length = f"{round(word_count / 140)} minutes"
    call_outcome_ui = "Yes" if call_closed else "No" if call_closed is False else "Objection follow-up"

    with st.spinner("🔍 Analyzing call transcript..."):
        system_prompt = f"""
        You are a brutal, elite-level sales call evaluator trained in buyer psychology, emotional influence, and persuasion frameworks (Robert Cialdini, NEPQ, high-ticket closing).

        Use ONLY the MIRRORS and F.A.S.T. frameworks below to analyze the transcript. Score each section 1–5. Provide time-stamped notes, objections if applicable, and brutally honest coaching.

        Before scoring, double-check if the call actually closed — use intuition and conversation flow, not just keyword detection like 'let's do it'. Provide a second opinion on whether this truly sounds like a close and update the call outcome accordingly.

        MIRRORS Sales Framework:
        M - Map The Mission:
        - Goal: put the focus on them and a vauge goal.
        - Ask: Why are we here? What are you looking for?

        I - Investigate Actions:
        - Goal: Reveal past efforts and attempts.
        - Ask: What have you tried? How long?

        R - Reveal The Root:
        - Goal: Identify emotional and logical pain.
        - Ask: Is it working? What's the root cause?

        R - Reframe The Gap:
        - Goal: Break illusion of DIY success.
        - Ask: Why not do it on your own? Why get help?

        O - Outline The Dream:
        - Goal: Tie goal to identity, joy, family figure out what chnages as a result of them solving this tieing an emotion to that tangible result.
        - Ask: What changes if you fix it? How would that feel?

        R - Risk Of The Future:
        - Goal: Highlight cost of inaction and why its not an option for them.
        - Ask: What happens if you don’t change?

        S - Secure The Yes:
        - Goal: Confirm identity shift & urgency is optional.
        - Ask: Are you ready to finally change this?

        F.A.S.T. Pitch Framework:
        F - Foundation (dream outcomes)
        A - Ascension (program solves pains)
        S - Shift (lifestyle transformation)
        T - Timeline & Trust (expectations & logic)

        FORMAT:
        Call Review:
        » Name of Rep: {rep_name}
        » Name of reviewer: {reviewer_name}
        » Date of call: {call_date.strftime('%Y-%m-%d')}
        » Length of call: {call_length}
        » UI-selected call outcome: {call_outcome_ui}
        » Revenue Collected (if any): {'$' + str(revenue_total) if revenue_total else 'N/A'}

        Score each MIRRORS and F.A.S.T. section 1-5 with clear notes and timestamps.
        Include: Total score, AI opinion on probability to close, summary, and 2 action steps.
        """

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ]
        )

        feedback = response.choices[0].message.content
        st.success("✅ Call evaluated successfully!")

        st.download_button("📩 Download Feedback", data=feedback, file_name="feedback_output.txt")
        st.text_area("📋 Call Review Output", value=feedback, height=600, disabled=True)
else:
    st.info("📄 Upload a transcript to begin your evaluation.")
