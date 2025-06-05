# מערכת שיחות התרמה לבית חב"ד

מערכת זו מבצעת שיחות טלפוניות אוטומטיות לתורמים פוטנציאליים לבית חב"ד בבנגקוק.  
המערכת מנוהלת על ידי ממשק גרפי ומחוברת ל־Twilio ול־OpenAI לצורך ניתוח שיחה, שליחת SMS, והעברה לרב.

## הפעלה

1. העלה את הקבצים ל־Render
2. הגדר את משתני הסביבה:
   - `OPENAI_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_PHONE`
3. הפעל את הממשק המקומי (PyQt) כדי לחייג
4. Twilio יפנה ל־Webhook: `/voice`

## מפתחים
- נבנה על ידי יאיר 🙂
