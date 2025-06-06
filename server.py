from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import openai
import os
from twilio.rest import Client

app = Flask(__name__)

openai.api_key = os.environ["OPENAI_API_KEY"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    caller_number = request.form.get("From", "")
    user_input = request.form.get("SpeechResult", "")
    response.say("שלום, אני העוזרת של הרב נחמיה מבית חב״ד בבנגקוק. אנחנו מתקשרים לכל מי שביקר בבית חב״ד לאחרונה כדי לבקש את עזרתו בתרומה. נשמח שתשמע אותנו לרגע.", language="he-IL", voice="Polly.Carmit")


    sentiment_prompt = f"נתח רגש למשפט הבא בעברית בקצרה מאוד (חיובי, שלילי, ניטרלי): {user_input}"
    try:
        sentiment_reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": sentiment_prompt}]
        )
        sentiment = sentiment_reply["choices"][0]["message"]["content"].strip()
    except:
        sentiment = "לא זוהה רגש"

    if "לתרום" in user_input:
        sms_text = 'תודה על הרצון לתרום לבית חב״ד! קישור לתרומה: https://chabadthailand.co.il/donations/#step-1'
        client.messages.create(
            body=sms_text,
            from_=TWILIO_PHONE,
            to=caller_number
        )
        response.say("שלחתי לך קישור לתרומה. תודה רבה!", language="he-IL", voice="Polly.Carmit")
    elif "רב" in user_input or "לדבר עם הרב" in user_input:
        response.say("מעבירה אותך לרב כעת. רגע בבקשה.", language="he-IL", voice="Polly.Carmit")
        response.dial("+66818695164")
    else:
        gpt_prompt = f'את העוזרת של הרב מבית חב״ד בבנגקוק. מישהו אמר: "{user_input}". תעני בעברית בקצרה.'
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": gpt_prompt}]
        )
        answer = reply["choices"][0]["message"]["content"]
        response.say(answer, language="he-IL", voice="Polly.Carmit")

    response.record(max_length=120, transcribe=True)
    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
