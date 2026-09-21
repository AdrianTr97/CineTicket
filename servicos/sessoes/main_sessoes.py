from flask import Flask
from flask_cors import CORS
from controllers_sessoes import rotas_sessoes

app = Flask("sessoes")
CORS(app)
app.register_blueprint(rotas_sessoes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)