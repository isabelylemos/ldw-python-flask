from flask import render_template, request, url_for, redirect
from models.database import db, Serie, Ator
import urllib
import json

# Lista de jogadores
jogadores = ['Jogador 1', 'Jogador 2', 'Jogador 3',
             'Jogador 4', 'Jogador 5', 'Jogador 6', 'Jogador 7']
# Lista de jogos
serielist = [{'Título': 'CS-GO', 'Ano': 2012, 'Categoria': 'FPS Online'}]


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/series', methods=['GET', 'POST'])
    def series():
        serie = serielist[0]

        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('series'))
        return render_template('series.html',
                               serie=serie,
                               jogadores=jogadores)

    @app.route('/newSeries', methods=['GET', 'POST'])
    def newSeries():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                serielist.append({'Título': request.form.get('titulo'), 'Ano': request.form.get(
                    'ano'), 'Categoria': request.form.get('categoria')})
                return redirect(url_for('newSeries'))

        return render_template('newSeries.html',
                               serielist=serielist)

    # CRUD GAMES - LISTAGEM, CADASTRO E EXCLUSÃO
    @app.route('/series/estoque', methods=['GET', 'POST'])
    @app.route('/series/estoque/delete/<int:id>')
    def seriesEstoque(id=None):
        if id:
            serie = Serie.query.get(id)
            # Deleta o jogo cadastro pela ID
            db.session.delete(serie)
            db.session.commit()
            return redirect(url_for('seriesEstoque'))
        # Cadastra um novo jogo
        if request.method == 'POST':
            newserie = Serie(request.form['titulo'], request.form['ano'], request.form['categoria'],
                           request.form['preco'], request.form['quantidade'], request.form['ator'])
            db.session.add(newserie)
            db.session.commit()
            return redirect(url_for('seriesEstoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            series_page = Serie.query.paginate(page=page, per_page=per_page)
            
            # SELECIONANDO TODOS OS CONSOLES CADASTRADOS
            ators = Ator.query.all()

            return render_template('seriesEstoque.html', seriesEstoque=series_page, ators=ators)

    # CRUD GAMES - EDIÇÃO
    @app.route('/series/edit/<int:id>', methods=['GET', 'POST'])
    def serieEdit(id):
        g = Serie.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            g.titulo = request.form['titulo']
            g.ano = request.form['ano']
            g.categoria = request.form['categoria']
            g.preco = request.form['preco']
            g.quantidade = request.form['quantidade']
            # Alterando o Ator
            g.ator_id = request.form['ator']
            
            db.session.commit()
            return redirect(url_for('seriesEstoque'))
        # SELECIONANDO OS CONSOLE
        ators = Ator.query.all()
        return render_template('editserie.html', g=g, ators=ators)

    # CRUD CONSOLES - LISTAGEM, CADASTRO E EXCLUSÃO
    @app.route('/ators/estoque', methods=['GET', 'POST'])
    @app.route('/ators/estoque/delete/<int:id>')
    def atorsEstoque(id=None):
        if id:
            ator = Ator.query.get(id)
            # Deleta o ator cadastro pela ID
            db.session.delete(ator)
            db.session.commit()
            return redirect(url_for('atorsEstoque'))
        # Cadastra um novo ator
        if request.method == 'POST':
            newator = Ator(
                request.form['nome'], request.form['fabricante'], request.form['ano_lancamento'])
            db.session.add(newator)
            db.session.commit()
            return redirect(url_for('atorsEstoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            ators_page = Ator.query.paginate(
                page=page, per_page=per_page)
            return render_template('atorsestoque.html', atorsestoque=ators_page)

    # CRUD CONSOLES - EDIÇÃO
    @app.route('/ators/edit/<int:id>', methods=['GET', 'POST'])
    def atorEdit(id):
        ator = Ator.query.get(id)
        # Edita o ator com as informações do formulário
        if request.method == 'POST':
            ator.nome = request.form['nome']
            ator.fabricante = request.form['fabricante']
            ator.ano_lancamento = request.form['ano_lancamento']
            db.session.commit()
            return redirect(url_for('atorsEstoque'))
        return render_template('editator.html', ator=ator)

    @app.route('/apiseries', methods=['GET', 'POST'])
    @app.route('/apiseries/<int:id>', methods=['GET', 'POST'])
    def apiseries(id=None):
        url = 'https://www.freetoserie.com/api/series'
        res = urllib.request.urlopen(url)
        data = res.read()
        seriesjson = json.loads(data)
        if id:
            ginfo = []
            for g in seriesjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('serieInfo.html', ginfo=ginfo)
            else:
                return f'Serie com a ID {id} não foi encontrado.'
        else:
            return render_template('apiseries.html', seriesjson=seriesjson)
