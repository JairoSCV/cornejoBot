from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('holaflask.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)

#Si se va a ejecutar en el propio equipo, asegurarse de que no corra otro programa en el puerto 80