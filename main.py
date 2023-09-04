from imports import *
from functions import *

app = Flask(__name__)

whatsapp = WhatsApp(whatsappToken, numberId)

llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llmPredictor, prompt_helper=promptHelper)
index.storage_context.persist(persist_dir="persist_dir")

modelEngine = index.as_query_engine()


@app.route("/", methods=["POST", "GET"])
def webhookWhatsapp():
    
    if request.method == "GET":
        if request.args.get('hub.verify_token') == "capybaraCapybara": 
            return request.args.get('hub.challenge')
        else:
            with open("textData.txt", "r") as f:
                textContents = f.read()
            return textContents.replace('\n', '<br>')

    try:        
        data = request.get_json()
        message_info = data['entry'][0]['changes'][0]['value']['messages'][0]
        phoneNumber = message_info['from']
        messageBody = message_info['text']['body']
        timeStamp = datetime.fromtimestamp(int(message_info['timestamp']))
    except KeyError:
        return jsonify({"status": "success"}, 200)
    
    data_Processed = get_Conversation(phoneNumber)
    data_Processed = last_Messages(data_Processed) + f"\n    Usuario: {messageBody}\n    Bot: "
    
    complete_Prompt = prompt_Text + data_Processed
    
    print("\nComplete Prompt:", complete_Prompt,"\n")
    
    if "1NF0-4SK3D_special" in data_Processed:
        modelAnswer = data_Processed
    else:
        modelAnswer = str(modelEngine.query(complete_Prompt))
        print("\nModel answer: ", modelAnswer)

    processedAnswer = process(modelAnswer, phoneNumber.replace("521",''), data_Processed, modelEngine,timeStamp)
    
    whatsapp.send_message(processedAnswer, phoneNumber.replace("521","52"))


    answerLogger = "\n<b>Respuesta</b>: <samp>{}</samp>".format(processedAnswer.replace('\n', ' '))
    log_entry = "\n<section><b>Telefono</b>: {} | <b>Mensaje</b>: {} | <b>Fecha</b>: {}{}".format(phoneNumber, messageBody, timeStamp, answerLogger)
    with open("textData.txt", "a") as f:
        f.write(log_entry)

    log_Conversation(phoneNumber, messageBody, processedAnswer, timeStamp)

    return jsonify({"status": "success"}, 200)



###########################
if __name__ == "__main__":
    app.run(host='0.0.0.0')
###########################
