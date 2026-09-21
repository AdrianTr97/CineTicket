from flask import Flask
from flask_cors import CORS
from controllers_filmes import rotas_filmes

app = Flask("filmes")
CORS(app)

# Registra as rotas separadas no aplicativo principal
app.register_blueprint(rotas_filmes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)