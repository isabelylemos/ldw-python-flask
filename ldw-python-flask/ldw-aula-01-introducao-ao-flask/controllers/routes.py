from flask import render_template, request

def init_app(app):
    players = ['Yan', 'Ferrari', 'Valéria', 'Amanda']
    gamelist = [{}]
    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/games', methods=['GET', 'POST'])
    def games():
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        
        # dicionario em python (objeto)
        console = {'name':'Playstation 5',
                'manucfacturer': 'Sony',
                'year': 2020}
        
        # tratando uma requisição post com request
        if request.method == 'POST':
            #coletando o texto da input
            if request.form.get('player'):
                players.append(request.form.get('player'))
        
        return render_template('games.html', 
                            title = title, 
                            year = year, 
                            category = category,
                            players = players,
                            console = console)
        
        
    @app.route('/newgame', methods=['GET', 'POST'])
    def newgame():
        
        if request.method == 'POST':
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({'Título':request.form.get('title'), 'Ano':request.form.get('year'), 'Categoria':request.form.get('category')})
        return render_template('newGame.html', gamelist=gamelist)