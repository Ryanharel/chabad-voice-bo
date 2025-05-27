from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import openai
import os

app = Flask(__name__)

# הגדרות OpenAI
openai.api_key = os.getenv("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")

# הגדרות Twilio
TWILIO_ACCOUNT_SID = os.getenv("ACa2b89d3832a14af36ef280ca88946ef5")
TWILIO_AUTH_TOKEN = os.getenv("713f6f33375405cde5e76e4ee1d4002c")
TWILIO_PHONE = os.getenv("+16165850853")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    caller_number = request.form.get("From", "")
    user_input = request.form.get("SpeechResult", "")

    if "לתרום" in user_input:
        # שלח קישור לתרומה
        donation_url = "https://chabadthailand.co.il/donations/#step-1"
        sms_text = 'הזכה על הזכות לתרום לבית חב"ד! ייתן ה׳ שתזכה לברכה והצלחה!' + donation_url
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
        gpt_prompt = f'את העוזרת של הרב מבית חב"ד בבנגקוק. מישהו אמר: "{user_input}". תעני בעברית בקצרה.'
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": gpt_prompt}]
        )
        answer = reply["choices"][0]["message"]["content"]
        response.say(answer, language="he-IL", voice="Polly.Carmit")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
