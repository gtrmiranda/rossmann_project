### Faz o teste da API (executar primeiro o handler.py)

import pandas as pd
import json
import requests

from flask import Flask, request, Response


#### Constants #####

TOKEN = '6436277982:AAHo-QgbdZh7sTBMPdB529Ip3aTZevWhhEk'

# Info about the bot
#https://api.telegram.org/bot6436277982:AAHo-QgbdZh7sTBMPdB529Ip3aTZevWhhEk/getMe

# get updates
#https://api.telegram.org/bot6436277982:AAHo-QgbdZh7sTBMPdB529Ip3aTZevWhhEk/getUpdates

# send message
#https://api.telegram.org/bot6436277982:AAHo-QgbdZh7sTBMPdB529Ip3aTZevWhhEk/sendMessage?chat_id=1099613770&text=Hi Giovanni, I am doing good, thanks!

# set webhok
#https://api.telegram.org/bot6436277982:AAHo-QgbdZh7sTBMPdB529Ip3aTZevWhhEk/setWebhook?url=https://rossmann-bot-lxqa.onrender.com

#########################

def send_message( chat_id, text ):
    
    # Monta a url
    url = 'https://api.telegram.org/bot{}/'.format( TOKEN )
    url = url + 'sendMessage?chat_id={}'.format( chat_id )
    
    # Controi o texto a ser devolvido
    r = requests.post( url, json={'text': text} )
    # Devolve mensagem com o status code. Se for 200, tudo ok
    print( 'Status code {}'.format( r.status_code ) )
    
    return None

############ 

##### Função para carregar os datasets 

def load_dataset( store_id ):
    
    # Carrega o dataset de teste disponibiizado na página do projeto Rossmann no Kaggle
    df10 = pd.read_csv( 'data/test.csv' )
    df_stores_raw = pd.read_csv( 'data/store.csv', low_memory=False )

    # Faz o merge entre o dataset de teste e as lojas
    df_test =pd.merge( df10, df_stores_raw, how='left', on='Store' )

    #### Ao inves de fazermos as predições para todas as lojas, faremos para apenas uma para ficar mais rápido

    # Recebe a loja para fazer as predições de vendas
    df_test = df_test[df_test['Store'] == store_id]
    
    # Se o retorno não for vazio (se tiver essa loja nos dados de teste), executa o restante do código
    if not df_test.empty:
        
        # Remove dias que a loja estiver fechada
        df_test = df_test[df_test['Open'] != 0]

        # Obtem as lojas que não têm o campo Open vazio (sinal ~ obtem a diferença)
        df_test = df_test[~df_test['Open'].isnull()]

        # Remove o ID
        df_test = df_test.drop( 'Id', axis=1 )

        # Converte o dataframe para o formato json (para ser lido por outro sistema). A orientação 'records' grava no modelo chave/valor
        data = json.dumps( df_test.to_dict( orient='records' ) )

    else:
        data = 'error'
    
    return data

####### Função para executar a predição

def predict( data ):

    #### API Call  #####

    # Testando chamada da API remota no Render
    url = 'https://teste-rossmann-api-whlz.onrender.com/rossmann/predict'

    header = {'Content-type': 'application/json'}
    data = data

    # Faz a requisição. O método post envia dados
    r = requests.post( url, data=data, headers=header )

    # Nosso objetivo é o status code = 200 que significa que tudo ocorreu bem
    print( 'Status Code {}'.format( r.status_code ) )


    # Converte o resultado do json acima de volta para um dataframe pandas. Monta as colunas a partir da primeira linha
    d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys() )

    return d1

### Cria função para pegar chat_id e text do json gerado após inicialização do bot

def parse_message( message ):
    
    # Obtém de dentro do json gerado message, chat, id e text (informamos as chaves)
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']
    
    # Remove a barra gerada pelo Telegram no inicio das mensagens
    store_id.replace( '/', '' )
    
    # Se for passado texto, tenta converter o store_id informado em número
    try: 
        store_id = int( store_id )
        
    # Se não for informado id, inclui excessão
    except ValueError:
      
        store_id = 'error'
    
    
    return chat_id, store_id 

##################

### API inicialize
app = Flask( __name__ )

# Cria o endpoint, ou seja, a rota, que é por onde a mensagem irá chegar
@app.route( '/', methods=['GET', 'POST'] )
def index():
    
    # Se o método for POST, sei que foi recebida uma mensagem e será gerado um json. Se for GET, nada foi digitado e retorna uma msg
    if request.method == 'POST':
        message = request.get_json()
        
        # a msg recebida é gigante. Então, precisamos parciar e pegar o chat id e o texto
        chat_id, store_id = parse_message( message )
        
        # Verifica o store_id enviado. Se estiver tudo ok, roda as funções
        if store_id != 'error':
            # loading data
            data = load_dataset( store_id )
            
            if data != 'error':
                
                # prediction
                d1 = predict( data )
                
                # calculation
                # Mostra soma de predições de vendas para as próximas seis semanas
                d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()

                msg = 'Store Number {} will sell R${:,.2f} in the next 6 weeks'.format(
                    d2['store'].values[0], d2['prediction'].values[0] )
                
                send_message( chat_id, msg )
                return Response( 'Ok', status=200 )
            
            else:
                send_message( chat_id, 'Store Not Available' )
                return Response( 'OK', status=200 )

        else:
            send_message( chat_id, 'Store ID is Wrong' )
            return Response( 'OK', status=200 )
        
    else:
        return '<h1> Rossmann Telegram BOT </h1>'

######################

if __name__ == '__main__':
    # Roda o app no host 0000 pela porta padrão do Flask (porta 5000)
    app.run( host='0.0.0.0', port=5000 )     
        


