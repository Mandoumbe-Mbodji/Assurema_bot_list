import requests
import sett
import json
import time

def obtenir_Msg_whatsapp(message):
    if 'type' not in message :
        text = 'message non reconnu'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'message non traité'
    
    
    return text

def envoi_Msg_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("est envoyé ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'message envoyé', 200
        else:
            return 'erreur dans l\'envoi du message', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)

    if "hola" in text:
        body = "Bonjour 👋 Bienvenue sur Assurema, comment pouvons-nous vous aider aujourd'hui ??"
        footer = "L\'équipe Assurema"
        options = ["✅ Assurema_Pack", "✅ Renouvellement assurance"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "Assurema_Pack" in text:
        body = "Vous avez  le choix entre plusieurs Packs. Lequel de ces Packs Assurema souhaitez-vous explorer ?"
        footer = "L\'équipe Assurema"
        options = ["PACK GANALE", "PACK SOPE", "PACK VIP"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "PACK VIP" in text:
        body="Merci d\'avoir choisi le pack VIP, Voulez-vous remplir le formulaire?"
        footer = "L\'équipe Assurema"
        options = ["✅ Oui, envoyer le PDF.", "⛔ Non, merci"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "Oui, envoyer le PDF" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Très bien, veuillez patienter un instant.")

        envoi_Msg_whatsapp(sticker)
        envoi_Msg_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Listo 👍🏻", "PACK VIP.pdf")
        envoi_Msg_whatsapp(document)
        time.sleep(3)

        body = "Vous souhaitez prendre rendez-vous avec l\'un de nos spécialistes pour discuter plus en détail de ces Assurema_Pack ?"
        footer = "L\'équipe Assurema"
        options = ["✅ Oui, je veux bien", "Non, merci." ]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "Oui, je veux bien" in text :
        body = "Super. Veuillez sélectionner une date et une heure pour la réunion :"
        footer = "L\'équipe Assurema"
        options = ["📅 demain 15:00 AM", "📅 apres demain 15:00 PM", "📅 surlendemain, 15:00 PM"]

        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "demain 15:00 AM" in text:
        body = "Excellent, vous avez sélectionné demain 15 heures. Je vous enverrai un rappel la veille. Vous avez besoin d'aide pour autre chose aujourd'hui ?"
        footer = "L\'équipe Assurema"
        options = ["✅ Oui, s'\il vous plait", "❌ Non, merci."]


        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "Non, merci." in text:
        textMessage = text_Message(number,"Parfait ! N\'hésitez pas à nous contacter si vous avez d'autres questions. N'oubliez pas que nous proposons également du matériel gratuit pour la communauté - à plus tard ! 😊")
        list.append(textMessage)
    else :
        data = text_Message(number,"Je suis désolé, je n'ai pas compris ce que vous avez dit. Voulez-vous que je vous aide à choisir l'une de ces options ?")
        list.append(data)

    for item in list:
        envoi_Msg_whatsapp(item)

# apparemment pour le Mexique, whatsapp ajoute 521 comme préfixe au lieu de 52,
# ce code résout ce problème.
#def replace_start(s):
    #if s.startswith("521"):
        #return "52" + s[3:]
   # else:
       # return s

# para argentina
#def replace_start(s):
   # if s.startswith("549"):
       # return "54" + s[3:]
   # else:
       # return s
