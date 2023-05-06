import os
import openai
import requests
from flask import Flask, request, Response

app = Flask(__name__)
instanceId = "WhatsApp Bussines placeholder"
token = "WhatsApp Bussines placeholder"

openai.api_key = os.getenv("openAI_Key")

def generate_response(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="La siguiente es una conversación con un asistente de AI. El asistente es útil, creativo, ingenioso y muy amigable.\n\nHumano: Hola, ¿quién eres?\nAI: Soy un AI creado por OpenAI. ¿En qué puedo ayudarte hoy?\nHumano: Quiero cancelar mi suscripción.\nAI:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response.choices[0].text.strip()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    number = data['messages'][0]['author'].replace('@c.us', '')
    message = data['messages'][0]['body']
    response_text = generate_response(message)
    send_message(number, response_text)
    return Response(status=200)

def send_message(number, message):
    url = f"https://api.chat-api.com/instance{instanceId}/sendMessage?token={token}"
    data = {
        "phone": number,
        "body": message
    }
    response = requests.post(url, json=data)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
