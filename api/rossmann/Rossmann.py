# Importa as bibliotecas necessárias para execução
import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime


class Rossmann( object ):
    def __init__(self):
        
        # Armazena o caminho absoluto do projeto
        self.home_path='C:/Users/giova/Principal/DataScience/ComunidadeDS/repos/ds_producao/dsproducao/'
        
        # Carrega todas as transformações salvas nos arquivos pickle
        self.competition_distance_scaler = pickle.load( open( self.home_path + 'parameter/competition_distance_scaler.pkl', 'rb' ) )
        self.competition_time_month_scaler = pickle.load( open( self.home_path + 'parameter/competition_time_month_scaler.pkl', 'rb' ) )
        self.promo_time_week_scaler = pickle.load( open( self.home_path + 'parameter/promo_time_week_scaler.pkl', 'rb' ) )
        self.year_scaler = pickle.load( open( self.home_path + 'parameter/year_scaler.pkl', 'rb' ) )
        self.store_type_scaler = pickle.load( open( self.home_path + 'parameter/store_type_scaler.pkl', 'rb' ) )
         
    
    # Função recebe o df1 como entrada e retorna o df1 limpo 
    def data_cleaning( self, df1 ):
        
        ### Renamed colums

        # Nome antigo das colunas (iremos retirar dos dados originais Sales e Customers)
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday',
                    'StoreType', 'Assortment', 'CompetitionDistance', 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 
                    'Promo2', 'Promo2SinceWeek','Promo2SinceYear', 'PromoInterval']

        # Cria uma função lambda para renomear as colunas antigas, com letra minuscula no inicio e underscore entre nomes
        snakecase = lambda x: inflection.underscore( x )

        # Aplica a função sobre a lista cols_old
        cols_new = list( map ( snakecase, cols_old ) ) 

        # Rename 
        df1.columns = cols_new

        ### Data Types

        # Como a data está em string, vamos mudar para date
        df1['date'] = pd.to_datetime( df1['date'] )

        ### Fillout NA

        # Função para atribuir ao campo competition_distance que estiver com dado faltante um valor acima da máxima distância do competidor
        df1['competition_distance'] = df1['competition_distance'].apply( lambda x: 200000.0 if math.isnan( x ) else x )  

        # Tratando os dados faltantes em competition_open_since_month 
        df1['competition_open_since_month'] = df1.apply ( lambda x: x['date'].month if math.isnan( x['competition_open_since_month'] ) else x['competition_open_since_month'], axis=1)

        # Tratando competition_open_since_year
        df1['competition_open_since_year'] = df1.apply ( lambda x: x['date'].year if math.isnan( x['competition_open_since_year'] ) else x['competition_open_since_year'], axis=1 )

        # Tratando os dados faltantes em promo2_since_week
        df1['promo2_since_week'] = df1.apply ( lambda x: x['date'].week if math.isnan( x['promo2_since_week'] ) else x['promo2_since_week'], axis=1 )  

        # Tratando os dados faltantes em promo2_since_year
        df1['promo2_since_year'] = df1.apply ( lambda x: x['date'].year if math.isnan( x['promo2_since_year'] ) else x['promo2_since_year'], axis=1 )    


        # Tratando os dados faltantes em promo_interval

        # Criando um dicionário para fazermos o mapeamento do nome dos meses 
        month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Set', 10: 'Oct', 11: 'Nov', 12: 'Dez'}

        # Colocar zeros onde tiver dado faltante
        df1['promo_interval'].fillna( 0, inplace=True )

        # Cria nova coluna que recebe o nome do mês da data de venda, com base no mapeamento
        df1['month_map'] = df1['date'].dt.month.map( month_map )

        # Cria uma coluna para verificar se no mês da venda havia promoção
        df1['is_promo'] = df1[['promo_interval', 'month_map']].apply( lambda x: 0 if x['promo_interval'] == 0 else 1 if x['month_map'] in x['promo_interval'].split( ',' ) else 0, axis=1 )


        ### Change Data Types

        # Transformação de dados nas colunas que alteramos
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype( int )
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype( int )

        df1['promo2_since_week'] = df1['promo2_since_week'].astype( int )
        df1['promo2_since_year'] = df1['promo2_since_year'].astype( int )

        # O retorno da função será o df1 com os dados limpos
        return df1
    
    
    def feature_engineering( self, df2 ):
        
        ### Variáveis a serem derivadas da variável Date
            
        #####  year
        df2['year'] = df2['date'].dt.year

        ##### month
        df2['month'] = df2['date'].dt.month

        ##### day
        df2['day'] = df2['date'].dt.day

        ##### week of year
        df2['week_of_year'] = df2['date'].dt.isocalendar().week

        ##### year week
        df2['year_week'] = df2['date'].dt.strftime( '%Y-%W' )


        ####### competition since

        # Percorre todas as linhas do df2 e monta uma data a partir de 2 colunas para fazer a diferença em meses
        df2['competition_since'] = df2.apply( lambda x: datetime.datetime( year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1), axis=1 )

        # Tempo de competição em meses, dado pela diferença da data de inicio da loja e da abertura do competidor
        df2['competition_time_month'] = ( ( df2['date'] - df2['competition_since'] )/30 ).apply( lambda x: x.days).astype( int )


        ####### promo since

        # Monta a data de início da promoção com ano e semana do ano (será preciso passar para string para fazer a junção)
        df2['promo_since'] = df2['promo2_since_year'].astype( str ) + '-' + df2['promo2_since_week'].astype( str )

        # Faz a subtração da data acima convertida, menos 7 dias. Não é necessario usar axis=1 porque vamos aplicar só sobre a coluna promo_since
        df2['promo_since'] = df2['promo_since'].apply( lambda x: ( datetime.datetime.strptime( x + '-1', '%Y-%W-%w' ) - datetime.timedelta( days=7 ) ) ) 

        # Cria uma coluna com o tempo da promoção em semanas, dada pela subtração da data pela data de inicio da promocao
        df2['promo_time_week'] = ( ( df2['date'] - df2['promo_since'] ) / 7 ).apply( lambda x: x.days ).astype( int )



        ##### assortment
        # obs: de acordo com a base de dados Rossman: a = basic; b = extra; c = extended

        df2['assortment'] = df2['assortment'].apply( lambda x: 'basic' if x == 'a' else 'extra' if x == 'b' else 'extended' ) 

        ##### state holiday
        # obs: de acordo com a base de dados: a = public holiday, b = Easter holiday, c = Christmas, 0 = None

        df2['state_holiday'] = df2['state_holiday'].apply( lambda x: 'public_holiday' if x == 'a' else 'easter_holiday' if x == 'b' else 'christmas' if x == 'c' else 'regular_day' ) 


        ### Passo 3: Filtragem das variáveis 
        
        # 3.1: Filtragem das linhas
        # A variável open só é interessante se a loja estiver aberta, ou seja, 1
        df2 = df2[ df2['open'] != 0 ] 
        
        # 3.2: Seleção das colunas
        # Variáveis que sairão do modelo. Open, por exemplo, não tem variabilidade. É tudo 1, não faz sentido manter
        cols_drop = ['open', 'promo_interval', 'month_map']
        df2.drop( cols_drop, axis=1, inplace=True )

        # Retorna o df2 modificado para o modelo de machine learning
        return df2
    
    
    def data_preparation ( self, df5 ):
        
        ###### competition_distance: outliers relevantes - RobustScale

        # Usa o fit transform, que encontra o quartil 1 e 3 dos dados. Teremos a variável em uma nova escala, retirando os outliers
        df5['competition_distance'] = self.competition_distance_scaler.fit_transform( df5[['competition_distance']].values )


        ####### competition_time_month: outliers relevantes - RobustScale

        # Usa o fit transform, que encontra o quartil 1 e 3 dos dados. Teremos a variável em uma nova escala, retirando os outliers
        df5['competiton_time_month'] = self.competition_time_month_scaler.fit_transform( df5[['competition_distance']].values )


        ###### promo_time_week: pouca relevância dos outliers - MinMaxScale

        # Dado que os outliers não são tão relevantes, usa o MinMax Scaler para fazer o Rescaling
        df5['promo_time_week'] = self.promo_time_week_scaler.fit_transform( df5[['promo_time_week']].values )


        ###### year: pouca relevância dos outliers - MinMaxScale

        # Dado que os outliers não são tão relevantes, usa o MinMax Scaler para fazer o Rescaling
        df5['year'] = self.year_scaler.fit_transform( df5[['year']].values )


        ### Encoding ########

        #### Variáveis categóricas que serão transformadas em numéricas por encoding: state_holiday; store_type; assortment 

        ### state_holiday (ou é feriado, ou não é) 
        # Utiliza o One Hot Encoding para substituir o valor da variável por 0 ou 1
        df5 = pd.get_dummies( df5, prefix=['state_holiday'], columns=['state_holiday'] )

        #####################

        ### store_type (Na descrição do dataset não informa a definição do tipo de lojas, apenas que há lojas a, b, c, etc)
        # Vamos utilizar o Label Encoder, do pacote sklearn.preprocessing 

        # Aplica o Label Encoder
        df5['store_type'] = self.store_type_scaler.fit_transform( df5['store_type'] )

        #####################

        ### assortment (tipos de sortimento: basic (será igual a 1); extra (será igual a 2); extended (será igual a 3))
        # Uso do Ordinal Encoding

        # Cria dicionário para atribuir valores a cada tipo
        assortment_dict = {'basic': 1, 'extra': 2,'extended': 3}

        # Substitui os valores de assortment no df5, criando uma forma de aplicar o Ordinal Encoding nos dados
        df5['assortment'] = df5['assortment'].map( assortment_dict )


        ### Transformações de natureza

        #### Para as variáveis com natureza cíclica, iremos aplicar a transformação cíclica utilizando seno e cosseno 

        ### month

        # Cria uma nova coluna com valores de seno e cosseno de cada mês da data de venda (ciclo = 12 meses)
        df5['month_sin'] = df5['month'].apply( lambda x: np.sin( x * ( 2. * np.pi/12 ) ) )
        df5['month_cos'] = df5['month'].apply( lambda x: np.cos( x * ( 2. * np.pi/12 ) ) )

        ### day

        # Cria uma nova coluna com valores de seno e cosseno de cada dia da data de venda (ciclo = 30 dias)
        df5['day_sin'] = df5['day'].apply( lambda x: np.sin( x * ( 2. * np.pi/30 ) ) )
        df5['day_cos'] = df5['day'].apply( lambda x: np.cos( x * ( 2. * np.pi/30 ) ) )

        ### week of year

        # Cria uma nova coluna com valores de seno e cosseno de cada semana do ano da data de venda (ciclo = 52 semanas)
        df5['week_of_year_sin'] = df5['week_of_year'].apply( lambda x: np.sin( x * ( 2. * np.pi/52 ) ) )
        df5['week_of_year_cos'] = df5['week_of_year'].apply( lambda x: np.cos( x * ( 2. * np.pi/52 ) ) )


        ### day of week

        # Cria uma nova coluna com valores de seno e cosseno de cada dia da semana da data de venda (ciclo = 7 dias)
        df5['day_of_week_sin'] = df5['day_of_week'].apply( lambda x: np.sin( x * ( 2. * np.pi/7 ) ) )
        df5['day_of_week_cos'] = df5['day_of_week'].apply( lambda x: np.cos( x * ( 2. * np.pi/7 ) ) ) 
        
        # Lista das variáveis mais relevantes selecionadas pelo algoritmo Boruta 
        # adicionando também as variáveis month_sin; month_cos; week_of_year_sin, que julgo relevantes devido ao resultado da análise exploratória
        cols_selected = ['store', 'promo', 'store_type', 'assortment', 'competition_distance', 'competition_open_since_month',
                         'competition_open_since_year', 'promo2', 'promo2_since_week', 'promo2_since_year', 'competition_time_month',
                         'promo_time_week', 'day_of_week_sin', 'day_of_week_cos', 'month_cos', 'day_sin', 'day_cos', 'week_of_year_cos'
                         ]

        # Retorna o df5 somente com as colunas selecionadas para o modelo
        return df5 [cols_selected]
    
    # Cria função para fazer a predição utilizando o modelo treinado
    def get_prediction( self, model, original_data, test_data ):
        # prediction
        pred = model.predict( test_data )
        
        # Faz a junção dos dados originais com a predição (a predição será um coluna a mais)
        original_data['prediction'] = np.expm1( pred )
        
        return original_data.to_json( orient='records', date_format='iso' )