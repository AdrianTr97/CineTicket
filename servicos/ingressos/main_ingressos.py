from flask import Flask
from flask_cors import CORS
from controllers_ingressos import rotas_ingressos

app = Flask("ingressos")
CORS(app)
app.register_blueprint(rotas_ingressos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)