from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import http.client

app = Flask(__name__)

# Configuracion de la base de datos SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

# Modelo de la tabla log
class Log(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fecha_y_hora=db.Column(db.DateTime,default=datetime.utcnow)
    texto=db.Column(db.TEXT)

# Crear la tabla sino existe
with app.app_context():
    db.create_all()

# Funcion para ordenar los registros por fecha y hora
def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x:x.fecha_y_hora, reverse=True)

@app.route('/')
def index():
    # Obtener todos los registros de la base de datos
    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html',registros=registros_ordenados)

mensajes_log = []

# Funcion para agregar mensajes y guardar en la base de datos
def agregar_mensajes_log(texto):
    mensajes_log.append(texto)

    # Guardar el mensaje en la BBDD
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()

# Token de verificacion para la configuracion
TOKEN = "CORNEJO"

@app.route('/webhook',methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificarToken(request)
        return challenge
    elif request.method == 'POST':
        response = recibirMensajes(request)
        return response

def verificarToken(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN:
        return challenge
    else:
        return jsonify({'error':'Token inválido'}),401

def recibirMensajes(req):
    try:
        req = request.get_json()
        entry = req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        objeto_mensaje = value['messages']

        if objeto_mensaje:
            messages = objeto_mensaje[0]

            if "type" in messages:
                tipo = messages['type']
                
                # Guardar log en BBDD
                agregar_mensajes_log(json.dumps(tipo))

                if tipo == 'interactive':
                    return 0
                
                if 'text' in messages:
                    texto = messages['text']['body']
                    numero = messages['from'] 
                    
                    # Llamar a la función para agregar el texto al log y base de datos
                    enviar_mensajes_whatsapp(texto,numero)

                    # Guardar log en BBDD
                    agregar_mensajes_log(json.dumps(messages))

       

        return jsonify({'message':'EVENT_RECEIVED'})
    except Exception as e:
        return jsonify({'message':'EVENT_RECEIVED'})


def enviar_mensajes_whatsapp(texto, numero):
    texto = texto.lower()

    if 'hola' in texto:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hola 🙉, ¿como estás crack?"
            }
        }
    elif "1" in texto:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Lorem ipsum etc etc"
            }
        }
    elif "2" in texto:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "location",
            "location": {
                "latitude": "-12.070706368751747",
                "longitude": "-77.09867179517134",
                "name": "CABAL",
                "address": "Av. Elmer Faucett 261 San Miguel"
            }
        }
    elif "3" in texto:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "document",
            "document": {
                "link": "https://www.renfe.com/content/dam/renfe/es/General/PDF-y-otros/Ejemplo-de-descarga-pdf.pdf",
                "caption": "Temario del curso #001"
            }
        }
    elif "4" in texto:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "audio",
            "audio": {
                "link": "https://sax-ensemble.com/wp-content/uploads/2014/11/Gliding_Trough_S_Kemper_Sax_Ensemble.mp3"
            }
        }
    elif "5" in texto:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "video",
            "video": {
                "link": "https://www.youtube.com/watch?v=6e0XWqAeTwc",
                "caption": "UY ESA NO"
            }
        }
    elif "6" in texto:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "En breve me pondré en contacto contigo 🐾🐾"
            }
        }
    elif "7" in texto:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "📅 Horario de atención: Lunes a Viernes \n Horario: 9:00 am a 5:00 pm"
            }
        }
    elif "0" in texto:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hola, visita mi perfil de GitHub para más información https://github.com/JairoSCV \n 👀 Por favor, ingresa un número para recibir información \n\n1️⃣Información del curso \n2️⃣Ubicación \n3️⃣Enviar temario \n4️⃣Audio explicando \n5️⃣Video de introducción \n6️⃣Hablar con Cornejo \n7️⃣Horario de atención \n0️⃣Regresar al Menú"
            }
        }
    elif "boton" in texto:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "interactive",
            "interactive":{
                "type": "button",
                "body":{
                    "text":"¿Confirmas tu registro?"
                },
                "footer":{
                    "text":"Selecciona una de las opciones"
                },
                "action":{
                    "buttons":[
                        {
                            "type":"reply",
                            "reply":{
                                "id":"btnSi",
                                "title":"Si"
                            }
                        },
                        {
                            "type":"reply",
                            "reply":{
                                "id":"btnNo",
                                "title":"No"
                            }
                        },
                        {
                            "type":"reply",
                            "reply":{
                                "id":"btnTalvez",
                                "title":"Talvez"
                            }
                        }
                    ]
                }
            }
        }
    else:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hola, visita mi perfil de GitHub para más información https://github.com/JairoSCV \n 👀 Por favor, ingresa un número para recibir información \n\n1️⃣Información del curso \n2️⃣Ubicación \n3️⃣Enviar temario \n4️⃣Audio explicando \n5️⃣Video de introducción \n6️⃣Hablar con Cornejo \n7️⃣Horario de atención \n0️⃣Regresar al Menú"
            }
        }
    
    # Convertir el diccionario a formato JSON
    data = json.dumps(data)

    # Necesitamos el header (token + Url)
    headers = {
        "Content-Type":"application/json",
        "Authorization":"Bearer EAAZAMe6iZAJXIBO9WRAzV6QZBBZCHAdncJu4tZAtZBH34HfIi3NAZAyvKJzZB447R1hkVgnRpr5ODo5OOAskGEjZB8oqvMiy5NYqdXm7QkZC40oBaGKRFN6CplIZAQX2VzDwhfIcZAc2er7rYHsaYveY9CxsTTFlz1CF1jMty2ZCK3ubqxh77ZCmMHTycMnJukkktBtmrWgwZDZD"
    }

    # Necesitamos libreria Http
    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
        connection.request("POST","/v21.0/534099586452118/messages",data,headers)
        response = connection.getresponse()
        print(response.status, response.reason)
    except Exception as e:
        agregar_mensajes_log(json.dumps(e))
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)

#Si se va a ejecutar en el propio equipo, asegurarse de que no corra otro programa en el puerto 80