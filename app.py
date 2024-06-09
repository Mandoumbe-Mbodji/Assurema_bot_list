from flask import Flask, request, render_template
import sett 
import services

app = Flask(__name__)

@app.route('/bienvenue', methods=['GET'])
def  bienvenue():
    return 'Bonjour chez assurema, de Flask'

@app.route('/formulaire')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecte', 403
    except Exception as e:
        return e,403
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number,messageId,name)
        return 'envoyé'

    except Exception as e:
        return 'non envoyé ' + str(e)

if __name__ == '__main__':
    app.run()


