from flask import Flask, render_template # importando flask
# Criando uma instância d flask
from controllers import routes

app = Flask(__name__, template_folder='views') # __name__ representa o nome do arquivo que esta sendo executado

routes.init_app(app)

# se for executado diretamente pelo interpretador
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True) #iniciando o servidor





