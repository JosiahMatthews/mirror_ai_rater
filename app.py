import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Mirror AI Rater", page_icon="🔮")
st.title("🔮 Mirror AI Call Evaluator")

# Input fields
rep_name = st.text_input("Name of Rep")
reviewer_name = st.text_input("Name of Reviewer", value="Mirror AI Coach")
call_date = st.date_input("Date of Call", value=datetime.today())

uploaded_file = st.file_uploader("Upload Call Transcript (.txt)", type=["txt"])

if uploaded_file is not None:
    transcript = uploaded_file.read().decode("utf-8")
    word_count = len(transcript.split())
    call_length = f"{round(word_count / 140)} minutes"

    # Auto-detect call outcome
    lowered = transcript.lower()
    if any(phrase in lowered for phrase in ["i'm ready to get started", "let's do it"]):
        call_outcome = "Yes"
    elif any(phrase in lowered for phrase in ["i'll talk to my partner", "i need to check with", "follow up with me"]):
        call_outcome = "Soft Yes"
    elif any(phrase in lowered for phrase in ["i'll think about it", "sounds good but not now"]):
        call_outcome = "Soft No"
    else:
        call_outcome = "Objection follow-up"

    with st.spinner("Analyzing call..."):
        system_prompt = f"""
        You are a brutal, elite-level sales call evaluator trained in buyer psychology, emotional influence, and persuasion frameworks (Robert Cialdini, NEPQ, high-ticket closing).
        
        Use ONLY the MIRRORS and F.A.S.T. frameworks below to analyze the transcript. Score each section 1–5. Provide time-stamped notes, objections if applicable, and brutally honest coaching.

        MIRRORS Sales Framework:
        M - Map The Mission:
        - Goal: Build trust, lower threat, align expectations.
        - Ask: Why are we here? What are you hoping to get?

        I - Investigate Actions:
        - Goal: Reveal past efforts.
        - Ask: What have you tried? How long?

        R - Reveal The Root:
        - Goal: Identify emotional pain.
        - Ask: Is it working? What's the root cause?

        R - Reframe The Gap:
        - Goal: Break illusion of DIY success.
        - Ask: Why not do it on your own? Why get help?

        O - Outline The Dream:
        - Goal: Tie goal to identity, joy, family.
        - Ask: What changes if you fix it? How would that feel?

        R - Risk Of The Future:
        - Goal: Highlight cost of inaction.
        - Ask: What happens if you don’t change?

        S - Secure The Yes:
        - Goal: Confirm identity shift & urgency.
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
        » Call outcome: {call_outcome}

        Score from 1 - 5 on each MIRRORS and F.A.S.T. category with notes and timestamps.
        Include: Total score, probability to close, what went well, and 2 clear action steps.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ]
        )

        feedback = response.choices[0].message.content
        st.success("🎉 Call evaluated successfully!")

        st.download_button("Download Feedback", data=feedback, file_name="feedback_output.txt")
        st.text_area("Call Review Output", value=feedback, height=600)

else:
    st.info("🔹 Upload a call transcript to begin.")
