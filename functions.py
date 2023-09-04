import os

import openai
import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

import pickle
from variables import *
from orjson import loads, dumps

openai.api_key = "OPENAI API KEY"
os.environ['OPENAI_API_KEY'] = "OPENAI API KEY"



### Credicel Specific Funcs ############################

def getFromTag(userTag,requestedInfo):
    url = 'https://www.credicel.mx/api/pagos.php'
    form_data = {
        'function': 'buscarPago',
        'buscar': userTag
    }
    
    server = requests.post(url, data=form_data)
    output = loads(server.text)
    status = output['status']

    print("Status:",status)
    print('\nThe response from the server is:', output)
    
    if status == 1: return output["data"][requestedInfo]
    else: return "NOT FOUND"
  
def getTag_Others(searchFunc, userValue , valueType, returnWhat, doPrint= "yes"):
    url = 'https://www.credicel.mx/api/bot/botWA.php'
    form_data = {
        'function'             : '{}'.format(searchFunc),
        '{}'.format(valueType) : '{}'.format(userValue)
    }
    
    server = requests.post(url, data=form_data)
    output = loads(server.text)
    status = output['status']

    if doPrint == "yes":
        print("Status:",status)
        print('\nThe response from the server is:', output)

    if status  == 1: return output[returnWhat]
    else: return "NOT FOUND"



### Chat Storing Funcs #################################

def last_Messages(user_Data):
    last_Messages = []
    conversation_Text = ""
    chat_Len = -5 if len(list(user_Data)) >= 5 else len(list(user_Data))*-1
    
    for i in range(chat_Len, 0):
        try:
            last_Value = list(user_Data)[i]
            last_Value = user_Data[last_Value]

            last_Messages.append(last_Value)
        except IndexError:
            break
        
    for i in last_Messages:
        conversation_Text += f"\n    Usuario: {i['Usuario']}\n    Bot: {i['Bot']}"
        
    return conversation_Text

def get_Conversation(no_User):
    no_User = "no_" + no_User
    try:
        with open("chats/{}.json".format(no_User), "rb") as f:
            json_Data = loads(f.read())
            return json_Data
    except FileNotFoundError:
        with open("chats/{}.json".format(no_User), "wb") as f:
            empty_Dict = {}
            f.write(dumps(empty_Dict))
            return empty_Dict


def log_Conversation(no_User, msg_User, msg_Bot, timestamp):
    
    print("log:\n", "User:",  msg_User, "Bot:" ,msg_Bot, "Time:", timestamp)
    no_User = "no_" + no_User

    with open("chats/{}.json".format(no_User), "rb") as f:
        json_Data = loads(f.read())

    try:
        dct_Index = int(list(json_Data)[-1]) + 1
    except IndexError:
        dct_Index = "0"

    up_Dict = {
        str(dct_Index): {
            "Usuario": msg_User,
            "Bot": msg_Bot,
            "Timestamp": timestamp
        }
    }

    json_Data.update(up_Dict)
    with open("chats/{}.json".format(no_User), "wb") as f:
        f.write(dumps(json_Data))

    print(json_Data)



### Process Conversation ###############################

def process_LookUp(conversation, removeThis, lookUpThis, typeIs, modelEngine):
    
    global saldo_PromptText
    
    if "N0MBR3_Bu$c4Nd0 " not in conversation:
        userInfo = (conversation.replace(removeThis,'')).replace('\n','').replace(' ','').replace('\n','')
    else:
        userInfo = (conversation.replace(removeThis,'')).replace('\n','')
    
    tagUser = getTag_Others(lookUpThis, userInfo, typeIs, "tag")
    
    if "NOT FOUND" in tagUser:
        lookUp_Answer = "NOT FOUND" + typeIs 
    else:
        conversation = "\nSu tag es {}. Si tiene alguna pregunta adicional, por favor contáctenos. Gracias.".format(str(tagUser))
        new_Prompt = saldo_PromptText + conversation
        lookUp_Answer = str(modelEngine.query(new_Prompt))
    
    return lookUp_Answer
    
def check_Keyword(conversation, modelEngine,timeStamp):
    
    if "T4gR3c1b1d0_Buscando" in conversation:
        if "SALDO" in conversation:            
            userTag = ((conversation.replace('T4gR3c1b1d0_Buscando SALDO','')).replace(' ','')).replace('\n','')
            print(userTag)
            
            infoUser = getFromTag(userTag, 'pago_liquidar')
            
            if infoUser != "NOT FOUND":
                pre_answerKeyword = f'Su saldo a liquidar de su crédito de CredicCel es de ${str(infoUser)}. Esta consulta solo es valida para la siguiente fecha {timeStamp}. Si tiene alguna pregunta adicional, por favor contáctenos. Gracias.'
                answerKeyword = str(modelEngine.query(saldo_PromptText + pre_answerKeyword))
            else:
                answerKeyword = str(modelEngine.query("Eres un empleado de Atención al Cliente de CrediCel y debes informa en un mensaje breve al cliente que no se encontro su credito y que su tag no se encontro en el sistema"))
                
    elif "N0MBR3_Bu$c4Nd0" in conversation:
        answerKeyword = process_LookUp(conversation, 'N0MBR3_Bu$c4Nd0 ', 'tagXNombre', 'name', modelEngine)
    elif "NuM3_Bu$c4Nd0" in conversation:
        answerKeyword = process_LookUp(conversation, 'NuM3_Bu$c4Nd0 ', 'tagXCell', 'cell', modelEngine)
    elif "CU5P_Bu$c4Nd0" in conversation:
        answerKeyword = process_LookUp(conversation, 'CU5P_Bu$c4Nd0 ', 'tagXCurp', 'curp', modelEngine)
    elif "IMEI-R3c1b1d0_Buscando" in conversation:
        answerKeyword = process_LookUp(conversation, 'IMEI-R3c1b1d0_Buscando ', 'tagXImei', 'imei', modelEngine)

    return answerKeyword

def process(specialAnswer, phoneNumber, data_Processed, modelEngine,timeStamp):
    
    global search_PromptText
    global continue_PromptText
    global nameChange_PromptText
    
    phone_Check = getTag_Others('tagXCell', phoneNumber, 'cell', 'cliente', 'no')
    
    if "1NF0-4SK3D_special" in specialAnswer:
        
        new_Prompt = search_PromptText + data_Processed
        
        specialAnswer = str(modelEngine.query(new_Prompt))
        
        if 'Bot: ' in specialAnswer:specialAnswer = specialAnswer.replace('Bot: ','')
        
        if 'BU5SC4R' in specialAnswer:
            specialAnswer = specialAnswer.replace('BU5SC4R ','')
            keyword_Function = check_Keyword(specialAnswer, modelEngine,timeStamp)
            
            if "NOT FOUND" in keyword_Function:
                keyword_Function = (keyword_Function.replace("NOT FOUND",'')).replace('\n','')
                specialAnswer = str(modelEngine.query(continue_PromptText + keyword_Function))
            else:
                specialAnswer = keyword_Function
            
    elif phone_Check != 'NOT FOUND':
        specialAnswer = str(modelEngine.query(f'"{specialAnswer}"\n {nameChange_PromptText} {phone_Check}'))
    
    if (data_Processed.count('Hola') > 1 or data_Processed.count('Buenos días') > 1 or data_Processed.count('Buenas tardes') > 1 or data_Processed.count('Buenas noches') > 1) and ('Hola' in specialAnswer or 'Buenos días' in specialAnswer or 'Buenas noches' in specialAnswer or 'Buenas tardes' in specialAnswer):
        print("\nRemoviendo saludo\n")
        specialAnswer = str(modelEngine.query(f'Remueve el saludo en el siguiente texto y si hay un agradecimiento por contactar a Credicel o algo similar tambien remuevelo, enfocate en la pregunta y en tratar de ayudar a resolverla: {specialAnswer}'))
    
    return specialAnswer
