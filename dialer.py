from twilio.rest import Client

# פרטי חשבון Twilio שלך
account_sid = 'ACa2b89d3832a14af36ef280ca88946ef5'
auth_token = '713f6f33375405cde5e76e4ee1d4002c'
client = Client(account_sid, auth_token)

# הגדר את המספרים
to_number = '+66855476900'  # המספר שאליו תתקשר (לדוג' שלך או של תורם)
from_number = '+16165850853'    # המספר שקיבלת מ-Twilio

# בצע את השיחה
call = client.calls.create(
    url='https://chabad-voice-bo.onrender.com/voice',  # כתובת שתחזיר את תוכן השיחה
    to=to_number,
    from_=from_number
)

print("המערכת התקשרה בהצלחה!")
