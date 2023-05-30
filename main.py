from flask import Flask, jsonify, request
from heyoo import WhatsApp

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def webhookWhatsapp():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == "tokenVerificacion":
            return request.args.get('hub.challenge')
        else:
            f = open("textData.txt", "r")
            textContents = f.read()
            f.close()
            return textContents.replace('\n', '<br>')

    data = request.get_json()
    phoneNumber = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    messageBody = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    
    f = open("textData.txt", "a")
    f.write("\nTelefono:" + phoneNumber + " | Mensaje:" + messageBody)
    f.close()
    
    # Sending the message back
    whatsappToken = "tokenWhatsApp"
    numberId = "numberID"
    whatsapp = WhatsApp(whatsappToken, numberId)
    whatsapp.send_message(messageBody, phoneNumber.replace("521","52"))
    
    return jsonify({"status": "success"}, 200)

if __name__ == "__main__":
    app.run(debug=True)
