import requests
import sett
import json
import time
import re
#import psycopg2
#from psycopg2 import sql

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'Message Non reconnu'
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

def enviar_Mensaje_whatsapp(data):
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
            return 'Message envoyé', 200
        else:
            return 'erreur lors de l\'envoi', response.status_code
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
                    "button": "Voir Options",
                    "sections": [
                        {
                            "title": "Sections",
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
##################################################recuperation données###########################
def extract_info_from_text(text):
    info_patterns = {
        'prénom': re.compile(r'pr[eé]nom: (.+)', re.IGNORECASE),
        'nom': re.compile(r'nom: (.+)', re.IGNORECASE),
        'immatriculation': re.compile(r'immatriculation: (.+)', re.IGNORECASE),
        # Ajoutez d'autres balises et motifs au besoin
    }

    extracted_info = {}

    for field, pattern in info_patterns.items():
        match = pattern.search(text)
        if match:
            extracted_info[field] = match.group(1).strip()

    return extracted_info
  
#def save_to_database(user_info):

    #prenom = user_info.get('prénom', '')
    #nom = user_info.get('nom', '')
    #immatriculation = user_info.get('immatriculation', '')

##################################################recuperation données###########################
def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("message de l'utilisateur: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)

    if "bonjour" in text or "salut" in text or "salam" in text or "retour à l'acceuil" in text or "bienvenue sur assurema" in text:
        body = "Bonjour 👋 Bienvenue sur Assurema votre assurance en ligne.\nComment pouvons-nous vous aider aujourd'hui ?"
        footer = "Equipe Assurema"
        options = ["✅ Packs assurances", "📅 Renouvellement","✅ Trouver une agence"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "packs" in text:
        body = "Veuillez choisir le pack d'assurance qui vous interesse"
        footer = "Equipe Assurema"
        options = ["✅ PACK GANALE", "✅ PACK SOPE","✅ PACK VIP","✅ A LA CARTE", "retour à l'acceuil"]
        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))
        list.append(listReplyData)
        list.append(sticker)
    elif "pack ganale" in text:
        body = "Garantie PACK GNALE\n-Responsabilité civile\n-Défense sur recours\n-Personnes transportés"
        footer = "Equipe Assurema"
        options = ["✅ OK.", "⛔ Non, Merci", "retour à l'acceuil"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "ok" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Très bien, veuillez Renseigner vos informations parexemple: \nprenom: Dacey;\nnom: Fall;\nimmatriculation: AR-490-AP")
        extracted_info = extract_info_from_text(text)
        print("Informations extraites:", extracted_info)
        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Prêt 👍🏻", "Business Intelligence.pdf")
        enviar_Mensaje_whatsapp(document)
        time.sleep(3)

        body = "Vous souhaitez prendre rendez-vous avec l'un de nos spécialistes pour discuter plus en détail de ces services ?"
        footer = "Equipe Assurema"
        options = ["✅ Si", "Non", "retour à l'acceuil"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "pack sope" in text:
        body = "Garanties du PACK SOPE\n-Responsabilité Civile\n-Défense sur recours\n-Personnes transportées\n-Bris de glace"
        footer = "Equipe Assurema"
        options = ["✅ OUI.", "⛔ Non, Merci", "retour à l'acceuil"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "pack vip" in text:
        body = "Garanties du PACK VIP\n-Responsabilité Civile\n-Défense sur recours\n-Personnes transportées\n-Bris de glace\n-Vol\n-Incendie\n"
        footer = "Equipe Assurema"
        options = ["✅ OUI.", "⛔ Non, Merci", "retour à l'acceuil"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "carte" in text:
        body = "Ce pack n'est pas encore disponible"
        footer = "Equipe Assurema"
        options = ["retour à l'acceuil"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "une agence" in text :
        body = "Liste de nos agences"
        footer = "Equipe Assurema"
        options = ["Agence sur la VDN","Agence parcelles","Agence Mbao", "Agence Pikine", "retour à l'acceuil"]
        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "renouvellement" in text :
        body = "Vous souhaitez prendre rendez-vous avec l'un de nos spécialistes pour discuter plus en détail de ces services ?"
        footer = "Equipe Assurema"
        options = ["📅 16: janvier 10:00", "📅 7 decembre, 14:00", "📅 8 decembre, 12:00", "Non, Merci", "retour à l'acceuil"]
        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "16: janvier 10:00" in text:
        body = "Excellent, vous avez sélectionné la réunion du 16 janvier 10 heures. Je vous enverrai un rappel la veille. Voulez-vous confirmer le rendez-vous ?"
        footer = "Equipe Assurema"
        options = ["✅ Oui", "❌ Non, Merci.", "retour à l'acceuil"]
        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "7 decembre, 14:00" in text:
        body = "Excellent, vous avez sélectionné la réunion du 7 decembre 14:00 heures. Je vous enverrai un rappel la veille. Voulez-vous confirmer le rendez-vous ?"
        footer = "Equipe Assurema"
        options = ["✅ Oui", "❌ Non, Merci.", "retour à l'acceuil"]
        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "8 decembre, 12:00" in text:
        body = "Excellent, vous avez sélectionné la réunion du 8 decembre 12:00 heures. Je vous enverrai un rappel la veille. Voulez-vous confirmer le rendez-vous ?"
        footer = "Equipe Assurema"
        options = ["✅ Oui", "❌ Non, Merci.", "retour à l'acceuil"]
        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "oui" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Très bien, Merci à Bientot")
        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(3)
        document = document_Message(number, sett.document_url, "Prêt 👍🏻", "Business Intelligence.pdf")
        enviar_Mensaje_whatsapp(document)
        time.sleep(3)
        body = "Vous souhaitez prendre rendez-vous avec l'un de nos spécialistes pour discuter plus en détail de ces services ?"
        footer = "Equipe Assurema"
        options = ["✅ Si", "Non", "retour à l'acceuil"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "non, merci" in text:
        textMessage = text_Message(number,"Parfait ! N'hésitez pas à nous contacter si vous avez d'autres questions. N'oubliez pas que vous pouvez nous joindre sur ce numéro xxxxxxxxxx pour plus d'aides - à plus tard ! 😊")
        list.append(textMessage)
    else :
        #data = text_Message(number,"Je suis désolé, je n'ai pas compris ce que vous avez dit.")
        #list.append(data)
        footer = "Equipe Assurema"
        body = "Je suis désolé, je n'ai pas compris ce que vous avez dit."
        options = ["retour à l'acceuil"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)

    for item in list:
        enviar_Mensaje_whatsapp(item)

