from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import openai
import os

app = Flask(__name__)

# הגדרות OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# הגדרות Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    caller_number = request.form.get("From", "")
    user_input = request.form.get("SpeechResult", "")

    if "לתרום" in user_input:
        # שלח קישור לתרומה
        donation_url = "https://chabadthailand.co.il/donations/#step-1"
        sms_text = "תודה על הרצון לתרום לבית חב"ד! ניתן לתרום כאן: " + donation_url
        twilio_client.messages.create(
            body=sms_text,
            from_=TWILIO_PHONE,
            to=caller_number
        )
        response.say("שלחתי לך קישור לתרומה בהודעת טקסט. תודה רבה!", language="he-IL", voice="Polly.Carmit")
    elif "לדבר עם הרב" in user_input or "רוצה את הרב" in user_input:
        response.say("מעבירה אותך כעת לרב, רגע בבקשה.", language="he-IL", voice="Polly.Carmit")
        response.dial("+66818695164")  # מספר הרב
    else:
        # תשובה עם GPT
        gpt_prompt = f"את העוזרת של הרב מבית חב"ד בבנגקוק. מישהו אמר: "{user_input}". מה תעני בקצרה בעברית?"
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": gpt_prompt}]
        )
        answer = reply["choices"][0]["message"]["content"]
        response.say(answer, language="he-IL", voice="Polly.Carmit")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
