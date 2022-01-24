from flask import Flask, render_template, request, redirect, flash
import os, time, scrapy, json

app = Flask(__name__)

cripto_lista = []

lista_dicionario = []

#Chamada da Spider para coletar as cotações
def chamar_spider():
    try:
        raw_string = r"scrapy runspider .\criptoflask_spider.py -o cotacao.json"
        os.system(raw_string)
        time.sleep(3)
        print('DADOS COLETADOS COM SUCESSO!')
    except:
        print('ERRO! WEB SCRAP NÃO EFETUADO!')

#Função para pegar o JSON criado, 
# armazená-lo em uma variavel e depois excluí-lo
def pegar_json():
    try:
        with open ('cotacao.json') as json_file:
            cotacoes = json.load(json_file)
        time.sleep(2)
        for cotacao in cotacoes:
            lista_dicionario.append(cotacao)
        print('JSON COLETADO COM SUCESSO!')
        #EXCLUINDO JSON
        try:
            os.remove('cotacao.json')
            print('JSON EXCLUIDO COM SUCESSO!')
        except:
            print('NÃO FOI POSSIVEL EXCLUIR O JSON')
    except ValueError as v:
        print(f"ERRO! COLETA DO ARQUIVO JSON FALHOU, ERRO:{v}")

#home
@app.route('/', methods = ['GET', 'POST'])
def home():

    erro = None

    if request.method == 'GET':
        return render_template('home.html')

    #pegando os dados do checkbox como list
    if request.method == 'POST':
        data = request.form.getlist('criptomoedas')
        for i in data:
            cripto_lista.append(i) 
        print(cripto_lista)
        if not cripto_lista:
            erro = 'Você não selecionou nenhuma criptomoeda!'
        else:
            flash('Estamos coletando suas cotações')
            chamar_spider()
            time.sleep(2)
            pegar_json()
            print(lista_dicionario)
            time.sleep(2)
            return redirect('/cotacoes/')
        return render_template('home.html', error=erro) 

#Pagina das cotações coletadas
@app.route('/cotacoes/', methods = ['GET'])
def pagina_cotacoes():
    for i in lista_dicionario:
        print (i)
        return i

if __name__ == '__main__':
    #rodando o web
    app.run(debug=True)
    

