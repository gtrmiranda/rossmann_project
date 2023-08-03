import pickle 
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann

# Carrega o modelo
model = pickle.load( open( 'C:/Users/giova/Principal/DataScience/ComunidadeDS/repos/ds_producao/dsproducao/model/model_rossmann.pkl', 'rb' ) )

# Utilizaremos a classe Flask do flask para construir a API

# Inicia a API
app = Flask( __name__ )

# end point: url que vai receber as requests
@app.route( '/rossmann/predict', methods=['POST'] )     # opções: post ou get: post para apenas enviar

def rossmann_predict():
    
    # obtem o dado
    test_json = request.get_json()
    
    # Se tiver dado, o json é convertido em dataframe. Se não, retorna vazio
    if test_json:
        
        # Duas opções: json com uma linha ou com mais linhas
        if isinstance( test_json, dict ):   # Exemplo único
            test_raw = pd.DataFrame( test_json, index=[0] )

        else:   # Mais de um exemplo
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
    
        # Instancia a Rossmann Class
        pipeline = Rossmann()

         # data cleanning
        df1 = pipeline.data_cleaning( test_raw )
    
        # feature engineering
        df2 = pipeline.feature_engineering( df1 )
    
        # data preparation
        df3 = pipeline.data_preparation( df2 )
    
        # prediction
        df_response = pipeline.get_prediction( model, test_raw, df3 )
    
        return df_response

         
    else:
        return Response( '{}', status=200, mimetype='application/json' ) 

    
if __name__ == '__main__':
    app.run( '0.0.0.0' )  # local host: a aplicação está rodando apenas localmente, para simular o ambiente web