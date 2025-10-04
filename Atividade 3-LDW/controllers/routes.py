from flask import render_template, request, redirect, url_for
import urllib.request, json
from models.database import db, Serie, Ator

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
    
        # CRUD SERIES - LISTAGEM, CADASTRO E EXCLUSÃO
    @app.route('/series/estoque', methods=['GET', 'POST'])
    @app.route('/series/estoque/delete/<int:id>')
    def seriesEstoque(id=None):
        if id:
            serie = Serie.query.get(id)
            # Deleta a série cadastrada pela ID
            db.session.delete(serie)
            db.session.commit()
            return redirect(url_for('seriesEstoque'))
        # Cadastra uma nova série
        if request.method == 'POST':
            newserie = Serie(request.form['titulo'], request.form['ano'], request.form['genero'], request.form['ator'])
            db.session.add(newserie)
            db.session.commit()
            return redirect(url_for('seriesEstoque'))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = 3
            series_page = Serie.query.paginate(page=page, per_page=per_page)
            atores = Ator.query.all()
            return render_template('seriesestoque.html', seriesestoque=series_page, atores=atores)

    # CRUD SERIES - EDIÇÃO
    @app.route('/series/edit/<int:id>', methods=['GET', 'POST'])
    def serieEdit(id):
        s = Serie.query.get(id)
        if request.method == 'POST':
            s.titulo = request.form['titulo']
            s.ano = request.form['ano']
            s.genero = request.form['genero']
            s.ator_id = request.form['ator']
            db.session.commit()
            return redirect(url_for('seriesEstoque'))
        atores = Ator.query.all()
        return render_template('editserie.html', s=s, atores=atores)
    
    @app.route('/atores/estoque', methods=['GET', 'POST'])
    @app.route('/atores/estoque/delete/<int:id>')
    def atoresEstoque(id=None):
        if id:
            ator = Ator.query.get(id)
            # Deleta o console cadastro pela ID
            db.session.delete(ator)
            db.session.commit()
            return redirect(url_for('atoresEstoque'))
        # Cadastra um novo ator
        if request.method == 'POST':
            newator = Ator(
                request.form['nome'], request.form['idade'], request.form['pais'])
            db.session.add(newator)
            db.session.commit()
            return redirect(url_for('atoresEstoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            atores_page = Ator.query.paginate(
                page=page, per_page=per_page)
            return render_template('atoresestoque.html', atoresestoque=atores_page)

    # CRUD atores - EDIÇÃO
    @app.route('/atores/edit/<int:id>', methods=['GET', 'POST'])
    def atorEdit(id):
        ator = Ator.query.get(id)
        # Edita o ator com as informações do formulário
        if request.method == 'POST':
            ator.nome = request.form['nome']
            ator.idade = request.form['idade']
            ator.pais = request.form['pais']
            db.session.commit()
            return redirect(url_for('atoresEstoque'))
        return render_template('editator.html', ator=ator)


    @app.route("/apiseries", methods=['GET', 'POST'])
    @app.route("/apiseries/<int:id>", methods=['GET', 'POST'])
    def apiseries(id=None):
        if id:
            url = f"https://api.tvmaze.com/shows/{id}"
            try:
                response = urllib.request.urlopen(url)
                data = response.read()
                serieInfo = json.loads(data)

                if serieInfo.get("id"):
                    return render_template("serieInfo.html", serieInfo=serieInfo)
                else:
                    return f"Série com ID {id} não encontrada."
            except:
                return f"Erro ao buscar a série com ID {id}."
        else:
            url = "https://api.tvmaze.com/shows"
            response = urllib.request.urlopen(url)
            data = response.read()
            seriesList = json.loads(data)[:44]

            return render_template("apiseries.html", seriesList=seriesList)
        
  