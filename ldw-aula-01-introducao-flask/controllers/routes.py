from flask import render_template

def init_app(app):
    # definindo a rota principal da aplicação '/'
    @app.route('/')
    # toda rota precisa de um função para executar 
    def home():
        return render_template('index.html')



    # definindo a rota principal da aplicação '/'
    @app.route('/games')
    # toda rota precisa de um função para executar 
    def games():
        # essas variáveis estariam vindo de fora 
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        # lista 
        players = ['Isabely', 'Ana', 'Gustavo', 'Yasmin']
        # dicionário 
        console = {'Nome' : 'PS5', 'Fabricante': 'Sony', 'Ano': 2020}
        # o primeiro title é a var que vai ser criada na página 
        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)

