from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from escola import app, db
from modelos import Candidato, Voto
from funcoes import recuperaImagem, deletaArquivo, FormularioCandidato, FormularioVoto
import time

@app.route('/')
def index():
    listaCandidatos = Candidato.query.order_by(Candidato.id)
    return render_template('lista.html', titulo='Candidatos Representantes de Classe Secitec 2024', candidatos=listaCandidatos)

@app.route('/novo')
def novo():
    form = FormularioCandidato()
    return render_template('novo.html', titulo='Cadastro de um novo candidato', form=form)

#Criando um candidato
@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioCandidato(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))
    nome = form.nome.data
    descricao = form.descricao.data  
    imagem = request.files.get('imagem')
    if imagem is None:
        flash('Nenhuma imagem foi enviada')
        return redirect(url_for('novo'))
    candidato = Candidato.query.filter_by(nome=nome).first()
    if candidato:
        flash('Candidato já cadastrado')
        return redirect(url_for('novo'))
    novoCandidato = Candidato(nome=nome, descricao=descricao, imagem=imagem.filename)  
    db.session.add(novoCandidato)
    db.session.commit()
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    imagem.save(f'{upload_path}/foto{novoCandidato.id}-{timestamp}.png')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    consultaCandidato = Candidato.query.filter_by(id=id).first()
    form = FormularioCandidato(obj=consultaCandidato) 
    imagemCandidato = recuperaImagem(id)
    return render_template('editar.html', titulo='Edição de dados do candidato', candidato=consultaCandidato, imagemCandidato=imagemCandidato, form=form)

#Ação de atualizar um candidato
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioCandidato(request.form)
    if form.validate_on_submit():
        candidatoConsulta = Candidato.query.filter_by(id=request.form['id']).first()
        candidatoConsulta.nome = form.nome.data
        candidatoConsulta.descricao = form.descricao.data
        imagem = request.files['arquivo']  
        candidatoConsulta.imagem = imagem.filename
        db.session.add(candidatoConsulta)
        db.session.commit()
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deletaArquivo(candidatoConsulta.id)
        imagem.save(f'{upload_path}/foto{candidatoConsulta.id}-{timestamp}.png')
    return redirect(url_for('index'))

#Ação de deletar um candidato
@app.route('/deletar/<int:id>')
def deletar(id):
    candidatoConsulta = Candidato.query.filter_by(id=id).first()
    Candidato.query.filter_by(id=id).delete()
    db.session.commit()
    deletaArquivo(candidatoConsulta.id)
    flash('Candidato excluído com sucesso!')
    return redirect(url_for('index'))

#Rota das fotos
@app.route('/uploads/<nomeArquivo>')
def imagem(nomeArquivo):
    return send_from_directory('uploads', nomeArquivo)

#Rota da votação
@app.route('/votar', methods=['GET', 'POST'])
def candidato_id():
    form = FormularioVoto()  # Cria um novo formulário de voto
    if request.method == 'POST':
        if form.validate_on_submit():  # Valida o formulário
            candidato_id = request.form.get('candidato_id')
            # Caso seja um voto em branco
            voto_branco = request.form.get('voto_branco')  
            if voto_branco == '1':  # Alterado para verificar se o valor é '1'
                voto = Voto(candidato_id=1)  # Substituído 20 por 1
                db.session.add(voto)
                flash('Voto em branco registrado com sucesso!')
            elif not Candidato.query.get(candidato_id):
                voto = Voto(candidato_id=2)  # Substituído 21 por 2
                db.session.add(voto)
                flash('Voto nulo! Você selecionou um número de candidato inválido.')
            else:
                voto = Voto(candidato_id=int(candidato_id))  
                db.session.add(voto)
                flash('Voto registrado com sucesso!')
            db.session.commit() 
            return redirect(url_for('index'))
    candidatos = Candidato.query.all()
    return render_template('candidato_id.html', candidatos=candidatos, form=form)  

@app.route('/resultados')
def resultados():
    candidatos = Candidato.query.all()
    total_votos = Voto.query.count()
    return render_template('resultados.html', candidatos=candidatos, total_votos=total_votos)