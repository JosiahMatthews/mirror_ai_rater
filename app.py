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

        MIRRORS Sales Framework:\n
        M - Map The Mission:\n
        - Psychological Goal: Build trust quickly, set expectations, reduce threat response.\n
        - Must ask: Why are we here? What are you hoping to get from this?\n
        - The buyer should feel like the call is helpful, casual, and collaborative, not a pitch.\n
        I - Investigate Actions:\n
        - Psychological Goal: Reveal patterns and behaviors without resistance.\n
        - Ask: What have you tried? How long have you been trying that?\n
        - Great answers show trial-and-error, inconsistency, or buyer burnout.\n
        R - Reveal The Root:\n
        - Psychological Goal: Get the buyer to admit failure and explore the emotional WHY.\n
        - Ask: Is it working? If not, what’s not working? What’s really causing that?\n
        - Strong calls expose hidden pain, shame, or exhaustion here.\n
        R - Reframe The Gap:\n
        - Psychological Goal: Break the illusion of ‘I can figure it out on my own.’\n
        - Ask: So why not just keep doing it alone? Why get help?\n
        - A good answer shows the buyer realizes they need external change to succeed.\n
        O - Outline The Dream:\n
        - Psychological Goal: Shift from current pain to emotional visualization of the future.\n
        - Ask: What’s your goal? Where are you now? What changes if you get there?\n
        - Strong reps tie goals to identity, family, legacy, or joy — not just weight loss.\n
        R - Risk Of The Future:\n
        - Psychological Goal: Inject consequence and fear of inaction.\n
        - Ask: What happens if you don’t fix this? Are you okay with that?\n
        - Strong calls make the future feel heavy, real, and unacceptable.\n
        S - Secure The Yes:\n
        - Psychological Goal: Anchor emotional decision to identity and commitment.\n
        - Ask: So are you ready to finally change this?\n
        - Weak closes come from generic tie-downs. Strong closes confirm urgency + identity alignment.\n
        F.A.S.T. Pitch Framework:\n
        F - Foundation:\n
        - Lay out 2–5 dream outcomes the buyer wants (energy, consistency, freedom, etc).\n
        A - Ascension:\n
        - Show how 3 unique deliverables help remove the buyer’s 3 biggest pains.\n
        S - Shift:\n
        - Paint the transformation: what life will feel like with these changes installed.\n
        T - Timeline & Trust:\n
        - Set expectations for 3–6–12 month results and prove certainty with analogies, stats, or logic.\n
        🔥 Evaluation Guidelines:\n
        - Every step must be covered in some form.\n
        - Don’t score based on script order — score based on depth of intel collected.\n
        - Reward boldness, emotional depth, and buyer admissions.\n
        - Penalize filler words, passive tone, generic tie-downs, and missed pain stacking.\n
        FORMAT:\n
        Call Review:\n
        » Name of Rep: {rep_name}\n
        » Name of reviewer: {reviewer_name}\n
        » Date of call: {call_date.strftime('%Y-%m-%d')}\n
        » Length of call: {call_length}\n
        » Call outcome: {call_outcome}\n
        Score from 1 - 5 on each MIRRORS and F.A.S.T. category with notes and timestamps.\n
        Include: Total score, probability to close, what went well, and 2 clear action steps.
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
        st.success("🎉 Call evaluated successfully!")

        st.download_button("Download Feedback", data=feedback, file_name="feedback_output.txt")
        st.text_area("Call Review Output", value=feedback, height=600)

else:
    st.info("🔹 Upload a call transcript to begin.")
