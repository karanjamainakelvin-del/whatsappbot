from flask import Flask, request
from google import genai
from google.genai._interactions.resources.webhooks import Body
from twilio.twiml.messaging_response import MessagingResponse 
import os
app=Flask(__name__)
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def generate_answer(question):
    response=client.completions.create(
        model="gemini-2.5-flash",
        prompt=question,
        max_tokens=150
    )
    ans=response.choices[0].text
    return ans
@app.route('/gemini', methods=['POST'])
def gemini():
    incoming_message=request.values.get('Body', "").lower()
    print("Question : ", incoming_message)
    answer=generate_answer(incoming_message)
    print("Bot Answer : ", answer)
    bot_response=MessagingResponse()
    message=bot_response.message()
    message.body(answer)
    return str(bot_response)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False, port=5000)

