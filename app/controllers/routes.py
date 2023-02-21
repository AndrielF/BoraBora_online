from app import app, db
from models.classes import *
from flask import request, session, render_template, url_for, flash, redirect 



@app.route("/")
def home():
    return render_template("home.html")
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route("/autenticar", methods=['GET', 'POST'])
def autenticar():
    usuario = participantes.query.filter_by(usuario=request.form['usuario']).first()
    usuario_org = organizadores.query.filter_by(usuario=request.form['usuario']).first()
        
    if usuario and usuario.senha == request.form['senha']:
        flash('Usuário logado com sucesso')
        session['usuario_logado'] = usuario.usuario     # verificar esse .usuario -> agora -> .nome
        return render_template('home-logado.html', usuario=usuario.nome)
    elif usuario_org and usuario_org.senha == request.form['senha']:
        flash('Usuário logado com sucesso')
        session['usuario_logado'] = usuario_org.usuario
        return render_template('home-logado-organizacao.html', usuario=usuario_org.nome)
    else:
        flash('Usuário ou senha inválidos')
        return redirect(url_for('home'))


@app.route("/")
def voltar_home():
    return redirect(url_for('home'))


@app.route("/lista-eventos")
def lista_eventos():
    lista_eventos = eventos.query.all()
    return render_template("eventos.html", eventos=lista_eventos)


@app.route("/home-logado", methods=['GET', 'POST'])
def voltar_home_logado():
    return render_template("home-logado.html", usuario=session['usuario_logado'])   # erro no session['usuario_logado'].nome


@app.route("/sign_out", methods=['GET', 'POST'])
def sign_out():
    session.pop('usuario_logado', None)
    flash('Usuário deslogado com sucesso')
    return redirect(url_for('home'))


@app.route("/editar-participante/", methods=['GET', 'POST'])
def editar_conta():
    usuario = session['usuario_logado']
    usuario = participantes.query.filter_by(usuario=usuario).first()
    return render_template("editar-participante.html", usuario=usuario)


@app.route("/salvar-edicao-participante", methods=['POST'])
def editar_participante():
    usuario = participantes.query.filter_by(usuario=session['usuario_logado']).first()
    usuario.email = request.form['email']
    usuario.telefone = request.form['telefone']
    usuario.nome = request.form['nome']
    usuario.cpf = request.form['cpf']
    usuario.nascimento = request.form['nascimento']
    usuario.genero = request.form['genero']
    usuario.usuario = request.form['usuario']
    usuario.senha = request.form['senha']
    db.session.commit()
    flash('Dados atualizados com sucesso')
    return render_template('home-logado.html', usuario=usuario.nome)


@app.route("/exluir-conta")
def excluir_conta():
    usuario = participantes.query.filter_by(usuario=session['usuario_logado']).first()
    db.session.delete(usuario)
    db.session.commit()
    flash('Conta excluída com sucesso')
    return redirect(url_for('home'))



@app.route("/validar-ingresso")
def validar_ingresso():
    return render_template("validar-ingresso.html")

 
codigos = {
    "codigo1": "1234", "codigo2": "5678", "codigo3": "9012",
    "codigo4": "3456", "codigo5": "1111", "codigo6": "2222",
    "codigo7": "3333", "codigo8": "4444", "codigo9": "5555",
    "codigo10": "6666", "codigo11": "7777", "codigo12": "8888",
    "codigo13": "9999", "codigo14": "0000", "codigo15": "123",
}


@app.route('/resultado_validar', methods=['GET','POST'])
def resultado_validar():
    codigo = request.form.get('codigo')
    if codigo in codigos.values():
        resultado = 'Ingresso válido, pode curtir a festa!'
        resultado_css = 'valido'
    else:
        resultado = 'Ingresso reprovado, já foi validado ou é falso!'
        resultado_css = 'reprovado'
    return render_template('resultado-validacao.html', resultado=resultado, resultado_css=resultado_css)


@app.route("/home-organizador")
def voltar_home_logado_org():
    return render_template('home-logado-organizacao.html', usuario=session['usuario_logado'])


@app.route("/criar-evento", methods=['GET', 'POST'])
def criar_evento():
    return render_template("criar-evento.html", organizador=session['usuario_logado'])


@app.route('/novo-evento', methods=['POST'])
def novo_evento():
    titulo = request.form['titulo']
    data = request.form['data']
    local = request.form['local']
    descricao = request.form['descricao']
    organizador = request.form['organizador']
    ingressos = request.form['ingressos']
    preco = request.form['preco']
    evento = eventos(
        titulo=titulo, 
        data=data, 
        local=local, 
        descricao=descricao, 
        organizador=organizador, 
        ingressos=ingressos, 
        preco=preco
        )
    db.session.add(evento)
    db.session.commit()
    flash('Evento criado com sucesso')
    return render_template('home-logado-organizacao.html', usuario=session['usuario_logado'])


@app.route("/editar-evento", methods=['GET', 'POST'])
def editar_evento():
    evento = eventos.query.order_by(eventos.id.desc()).first()
    return render_template("editar-evento.html", evento=evento)


@app.route("/salvar-edicao-evento", methods=['POST'])
def salvar_edicao_evento():
    evento = eventos.query.order_by(eventos.id.desc()).first()
    evento.titulo = request.form['titulo']
    evento.data = request.form['data']
    evento.local = request.form['local']
    evento.descricao = request.form['descricao']
    evento.organizador = request.form['organizador']
    evento.ingressos = request.form['ingressos']
    evento.preco = request.form['preco']
    db.session.commit()
    flash('Evento atualizado com sucesso')
    return render_template('home-logado-organizacao.html', usuario=session['usuario_logado'])


@app.route("/excluir-evento")
def excluir_evento():
    evento = eventos.query.order_by(eventos.id.desc()).first()
    db.session.delete(evento)
    db.session.commit()
    flash('Evento excluído com sucesso')
    return render_template('home-logado-organizacao.html', usuario=session['usuario_logado'])








@app.route("/editar-organizador", methods=['GET', 'POST'])
def editar_organizador():
    usuario = session['usuario_logado']
    usuario = organizadores.query.filter_by(usuario=usuario).first()
    return render_template("editar-organizador.html", usuario=usuario)


@app.route("/salvar_edicao_organizador", methods=['GET', 'POST'])
def salvar_editar_organizador():
    usuario = organizadores.query.filter_by(usuario=session['usuario_logado']).first()
    usuario.email = request.form['email']
    usuario.telefone = request.form['telefone']
    usuario.nome = request.form['nome']
    usuario.cnpj = request.form['cnpj']
    usuario.ramo = request.form['ramo']
    usuario.usuario = request.form['usuario']
    usuario.senha = request.form['senha']
    db.session.commit()
    flash('Dados atualizados com sucesso')
    return render_template('home-logado-organizacao.html', usuario=usuario.nome)



@app.route("/exluir-conta")
def excluir_conta_organizador():
    usuario = organizadores.query.filter_by(usuario=session['usuario_logado']).first()
    db.session.delete(usuario)
    db.session.commit()
    flash('Conta excluída com sucesso')
    return redirect(url_for('home'))










@app.route("/sign-in", methods=['GET', 'POST'])
def sign_in():
    return render_template("sign-in.html")


@app.route('/criar', methods=['POST'])
def criar():
    email = request.form['email']
    telefone = request.form['telefone']
    nome = request.form['nome']
    cpf = request.form['cpf']
    nascimento = request.form['nascimento']
    genero = request.form['genero']
    usuario = request.form['usuario']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']

    if senha != confirmar_senha:
        flash('As senhas não correspondem')
        return redirect(url_for('sign_in'))
    elif participantes.query.filter_by(usuario=usuario).first():
        flash('Usuário já existe, logue-se para entrar!')
        return render_template('login.html')
    else:
        usuario = participantes(
            email=email, 
            telefone=telefone, 
            nome=nome, 
            cpf=cpf, 
            nascimento=nascimento, 
            genero=genero, 
            usuario=usuario, 
            senha=senha
            )
        db.session.add(usuario)
        db.session.commit()
        session['usuario_logado'] = usuario.usuario
        flash('Usuário criado e logado com sucesso')
        return render_template('home-logado.html', usuario=usuario.nome)
    

@app.route("/sign-in-organizador", methods=['GET', 'POST'])
def sign_in_organizador():
    return render_template("sign-in-organizador.html")


@app.route('/criar-organizador', methods=['POST'])
def criar_organizador():
    email = request.form['email']
    telefone = request.form['telefone']
    nome = request.form['nome']
    cnpj = request.form['cnpj']
    ramo = request.form['ramo']
    usuario = request.form['usuario']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']

    if senha != confirmar_senha:
        flash('As senhas não correspondem')
        return redirect(url_for('sign_in'))
    elif organizadores.query.filter_by(usuario=usuario).first():
        flash('Usuário já existe, logue-se para entrar!')
        return render_template('login.html')
    else:
        usuario = organizadores(
            email=email, 
            telefone=telefone, 
            nome=nome, 
            cnpj=cnpj, 
            ramo=ramo, 
            usuario=usuario, 
            senha=senha
            )
        db.session.add(usuario)
        db.session.commit()
        session['usuario_logado'] = usuario.usuario
        flash('Usuário criado e logado com sucesso')
        return render_template('home-logado-organizacao.html', usuario=usuario.nome)
    