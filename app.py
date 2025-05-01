import openai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load .env API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load transcript
with open("transcript_input.txt", "r", encoding="utf-8") as file:
    transcript = file.read()

# Auto-estimate call length
word_count = len(transcript.split())
call_length = f"{round(word_count / 140)} minutes"  # assuming avg 140 wpm

# Auto-detect call outcome
if any(phrase in transcript.lower() for phrase in ["i'm ready to get started", "let's do it"]):
    call_outcome = "Yes"
elif any(phrase in transcript.lower() for phrase in ["i'll talk to my partner", "i need to check with", "follow up with me"]):
    call_outcome = "Soft Yes"
elif any(phrase in transcript.lower() for phrase in ["i'll think about it", "i'll have to think", "sounds good but not now"]):
    call_outcome = "Soft No"
else:
    call_outcome = "No"

rep_name = "Josiah Matthews"
reviewer_name = "Mirror AI Coach"
call_date = datetime.today().strftime('%Y-%m-%d')

# Define system message with deep framework and scoring instructions
system_message = {
    "role": "system",
    "content": (
        "You are a brutal, elite-level sales call evaluator trained in buyer psychology, emotional influence, and persuasion frameworks (e.g., Robert Cialdini, NEPQ, and elite high-ticket closers).\n\n"
        "Your job is to use ONLY the MIRRORS and F.A.S.T. frameworks defined below to analyze the transcript and evaluate if the rep is gathering the correct emotional and logical intel at each phase.\n"
        "Calls don’t need to follow the exact script, but they MUST extract the correct information — or call it out as a failure.\n\n"
        "MIRRORS Sales Framework:\n"
        "M - Map The Mission:\n"
        "- Psychological Goal: Build trust quickly, set expectations, reduce threat response.\n"
        "- Must ask: Why are we here? What are you hoping to get from this?\n"
        "- The buyer should feel like the call is helpful, casual, and collaborative, not a pitch.\n\n"
        "I - Investigate Actions:\n"
        "- Psychological Goal: Reveal patterns and behaviors without resistance.\n"
        "- Ask: What have you tried? How long have you been trying that?\n"
        "- Great answers show trial-and-error, inconsistency, or buyer burnout.\n\n"
        "R - Reveal The Root:\n"
        "- Psychological Goal: Get the buyer to admit failure and explore the emotional WHY.\n"
        "- Ask: Is it working? If not, what’s not working? What’s really causing that?\n"
        "- Strong calls expose hidden pain, shame, or exhaustion here.\n\n"
        "R - Reframe The Gap:\n"
        "- Psychological Goal: Break the illusion of ‘I can figure it out on my own.’\n"
        "- Ask: So why not just keep doing it alone? Why get help?\n"
        "- A good answer shows the buyer realizes they need external change to succeed.\n\n"
        "O - Outline The Dream:\n"
        "- Psychological Goal: Shift from current pain to emotional visualization of the future.\n"
        "- Ask: What’s your goal? Where are you now? What changes if you get there?\n"
        "- Strong reps tie goals to identity, family, legacy, or joy — not just weight loss.\n\n"
        "R - Risk Of The Future:\n"
        "- Psychological Goal: Inject consequence and fear of inaction.\n"
        "- Ask: What happens if you don’t fix this? Are you okay with that?\n"
        "- Strong calls make the future feel heavy, real, and unacceptable.\n\n"
        "S - Secure The Yes:\n"
        "- Psychological Goal: Anchor emotional decision to identity and commitment.\n"
        "- Ask: So are you ready to finally change this?\n"
        "- Weak closes come from generic tie-downs. Strong closes confirm urgency + identity alignment.\n\n"
        "F.A.S.T. Pitch Framework:\n"
        "F - Foundation:\n"
        "- Lay out 2–5 dream outcomes the buyer wants (energy, consistency, freedom, etc).\n"
        "A - Ascension:\n"
        "- Show how 3 unique deliverables help remove the buyer’s 3 biggest pains.\n"
        "S - Shift:\n"
        "- Paint the transformation: what life will feel like with these changes installed.\n"
        "T - Timeline & Trust:\n"
        "- Set expectations for 3–6–12 month results and prove certainty with analogies, stats, or logic.\n\n"
        "🔥 Evaluation Guidelines:\n"
        "- Every step must be covered in some form.\n"
        "- Don’t score based on script order — score based on depth of intel collected.\n"
        "- Reward boldness, emotional depth, and buyer admissions.\n"
        "- Penalize filler words, passive tone, generic tie-downs, and missed pain stacking.\n\n"
        "Then provide a comprehensive call review including:\n"
        "- For each MIRRORS and F.A.S.T. step, score 1-5 based on execution and emotional depth.\n"
        "- Probability to close based on trust, urgency, pain depth, clarity.\n"
        "- Call outcome (did the sale close: yes/no/soft yes/objection follow-up)\n\n"
        "Then format a full review like this:\n"
        f"Call Review Example\nCall review:\n» Name of Rep: {rep_name}\n» Name of reviewer: {reviewer_name}\n» Date of call: {call_date}\n» Length of call: {call_length}\n» Call outcome: {call_outcome}\n"
    )
}

# Run GPT analysis
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        system_message,
        {"role": "user", "content": transcript}
    ]
)

# Save feedback
feedback = response.choices[0].message.content
with open("feedback_output.txt", "w", encoding="utf-8") as file:
    file.write(feedback)

print("✅ Brutal feedback saved to feedback_output.txt")
