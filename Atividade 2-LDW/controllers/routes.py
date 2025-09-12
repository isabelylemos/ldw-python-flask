from flask import render_template, request, redirect, url_for
import urllib.request, json

def init_app(app):
    atoreslist = ['Leighton Meester', 'Blake Lively', 'Ellen Pompeo', 'Sandra Oh', 'Wentworth Miller']
    serielist = [{'Título': 'Gossip Girl', 'Ano': 2007, 'Gênero': 'Drama'}, {'Título': 'Prison Break', 'Ano': 2005, 'Gênero': 'Drama'}, {'Título': 'Grey\'s Anatomy', 'Ano': 2007, 'Gênero': 'Drama'}]

    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route("/atores", methods=['GET', 'POST'])
    def listar_atores():
        if request.method == 'POST':
            if request.form.get('ator'):
                atoreslist.append(request.form.get('ator'))
                return redirect(url_for('listar_atores')) 
            
        return render_template(
            'atores.html',
            atores=atoreslist
        )
    
    @app.route('/newSerie', methods=['GET', 'POST'])
    def newSerie():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('genero'):
                serielist.append({
                    'Título': request.form.get('titulo'),
                    'Ano': request.form.get('ano'),
                    'Gênero': request.form.get('genero')
                })
                return redirect(url_for('newSerie'))
                
        return render_template('newSerie.html', serielist=serielist)

    @app.route("/apiseries", methods=['GET', 'POST'])
    @app.route("/apiseries/<int:id>", methods=['GET', 'POST'])
    def apiseries(id=None):
        url = "https://api.tvmaze.com/shows"  # endpoint que retorna várias séries
        response = urllib.request.urlopen(url)  
        data = response.read()
        seriesList = json.loads(data)  # transforma o JSON em dicionário

        if id:  # se o usuário passou um ID
            serieInfo = {}
            for serie in seriesList:
                if serie['id'] == id:  
                    serieInfo = serie
                    break
            if serieInfo:
                return render_template('serieInfo.html', serieInfo=serieInfo)
            else:
                return f"Série com ID {id} não encontrada."
        else:
            return render_template('apiseries.html', seriesList=seriesList)