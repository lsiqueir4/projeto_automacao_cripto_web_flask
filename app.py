from flask import Flask, render_template, request, redirect, flash
import os, time, scrapy, json

app = Flask(__name__)

cripto_lista = [] #list dos checkbox

lista_dicionario = [] #lista de cotacoes coletadas

lista_filtrada = [] #lista com os filtros do checkbox

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
    #ADD COTACOES DO JSON NA VARIAVEL lista_dicionario
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

#FILTRANDO A LISTA COM OS DADOS DO CHECKBOX
def filtrar_cotacoes():
    for cotacoes in lista_dicionario:
        if cotacoes['nome'] in cripto_lista:
            lista_filtrada.append(cotacoes)
    print(f'LISTA FILTRADA:{lista_filtrada}')

#home
@app.route('/', methods = ['GET', 'POST'])
def home():

    erro = None

    if request.method == 'GET':
        return render_template('home.html')

    #pegando os dados do checkbox como list
    if request.method == 'POST':
        data = request.form.getlist('criptomoedas')
        for i in data: #for para inserir dados do checkbox na list
            cripto_lista.append(i) 
        print(cripto_lista) 
        if not cripto_lista: #Se a lista está vazia
            pass
        else:
            chamar_spider()
            time.sleep(2)
            pegar_json()
            print(lista_dicionario) #cotacoes coletadas
            time.sleep(2)
            filtrar_cotacoes()
            return redirect('/cotacoes/')
        return render_template('home.html') 

#Pagina das cotações coletadas
@app.route('/cotacoes/', methods = ['GET'])
def pagina_cotacoes():
    return render_template('cotacoes.html')
    
    
         
if __name__ == '__main__':
    #rodando o web
    app.run(debug=True)
    

