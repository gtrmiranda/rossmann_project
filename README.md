# Rossmann Project
Modelo de previsão de vendas para cada uma das lojas da rede de farmácias Rossmann utilizando Machine Learning.

![rossmann_image](https://github.com/gtrmiranda/rossmann_project/assets/106852152/10da31e6-d4b7-4bbf-9bb6-0b22f168a3ed)


# 1. Sobre a Rossmann
Uma das maiores redes de farmácias da Europa, a Rosmann tem cerca de 56 mil funcionários e mais de 4 mil lojas em diversos países. 
É uma empresa em expansão com um grande sortimento de produtos, incluindo marca própria. 

## 1.1. O Problema de Negócio
O CFO da Rede Rossmann necessita efetuar a reforma de lojas da rede. Como parte do planejamento orçamentário, ele precisa de uma previsão de 
receitas para as próximas seis semanas em cada uma de suas lojas.

## 1.2. Premissas 
- A análise não levará em conta dias em que as lojas estão fechadas, como feriados.
- Apenas lojas com registro de vendas serão analisadas.
- Para lojas sem competidor próximo, será considerada a existência de competidor em uma distância maior que a máxima observada nas demais lojas.

## 1.3. Técnicas e Ferramentas Utilizadas
- Linguagem de programação Python;
- Jupyter Notebook;
- Visual Studio Code;
- Git e Github;
- Técnicas de Limpeza, Tratamento e Análise de Dados
- Algoritmos de Machine Learning de Classificação e Regressão
- Bibliotecas de Machine Learning Sklear e Scipy
- Flask e Python APIs;
- Render Cloud;
- Desenvolvimento de Bot para Celular no app Telegram

# 2. Desenvolvimento da Solução
O projeto foi desenvolvido seguindo o método CRISP-DM. Os seguintes passos foram seguidos para a entrega do modelo de predição à equipe de negócios da empresa:  

Passo 01 - Descrição dos Dados: O objetivo foi conhecer os dados, identificar outliers e analisar métricas estatísticas básicas 
como: média, mediana, máximo, mínimo, range, skew, kurtosis e desvio padrão. 

Passo 02 - Feature Engineering: O objetivo desta etapa é obter novos atributos com base nas variáveis ​​originais, com o objetivo de melhor descrever 
o fenômeno a ser modelado. 

Passo 03 - Filtragem de Variáveis: O objetivo desta etapa foi filtrar linhas e excluir colunas que não são relevantes para o modelo 
ou não fazem parte do escopo do negócio.

Passo 04 - Análise Exploratória de Dados: O objetivo desta etapa foi explorar melhor os dados para encontrar insights, entender melhor a relevância 
das variáveis no aprendizado do modelo de machine learning.

Passo 05 - Preparação dos Dados: O objetivo desta etapa é preparar os dados para a aplicação do modelo de aprendizado de máquina. 
Foram utilizadas técnicas como Rescaling e Transformation, através de encodings e nature transformation.

Passo 06 - Seleção de Variáveis: O objetivo desta etapa foi selecionar os melhores atributos para treinar o modelo. Foi utilizado o algoritmo 
Boruta para fazer a seleção das variáveis que otimizariam o modelo de machine learning.

Passo 07 - Machine Learning Modeling: O objetivo desta etapa é fazer os testes e o treinamento de alguns modelos de machine learning, 
com o intuito de comparar suas respectivas performance e a partir daí, escolher o melhor modelo para o projeto. A técnica de Cross Validation foi utilizada 
para garantir a performance real sobre os dados selecionados.

Passo 08 - Hyperparameter Fine Tunning: O objetivo desta etapa é escolher os melhores valores para cada um dos parâmetros do modelo selecionado 
na etapa anterior.

Passo 09 - Tradução e Interpretação do Erro: O objetivo desta etapa é converter as métricas de desempenho do modelo para valores monetários, tornando 
facilmente interpretáveis para a equipe de negócios. 

Passo 10 - Deploy do Modelo em Produção: O objetivo desta etapa é publicar o modelo em um ambiente de nuvem para que outras pessoas 
ou serviços possam usar os resultados para melhorar a decisão de negócios. A plataforma de aplicação em nuvem escolhida foi a Render Cloud. 

Passo 11 - Telegram Bot: O objetivo desta etapa é criar um bot no aplicativo do telegram, que possibilite consultar a previsão a qualquer momento
por meio de um celular.

# 3. Modelos de Predição Utilizados
- Média (para baseline);
- Regressão Linear;
- Regressão Linear com Regularização (Lasso);
- Random Forest Regressor;
- XGBoost Regressor.

# 4. Performance dos modelos de machine learning

## 4.1. Performance geral dos modelos 
![modelos](https://github.com/gtrmiranda/rossmann_project/assets/106852152/70cac642-5f89-4d2f-9d0a-ed7ba14bb44a)

## 4.2. Performance real após aplicação de cross validation
![modelos_crossvalidation](https://github.com/gtrmiranda/rossmann_project/assets/106852152/e4d656ba-4b7d-4af5-bc31-8bb1d7dfdb4f)

## 4.3. Performance XGBoost após Fine Tunning
![XGBoost_FineTuning](https://github.com/gtrmiranda/rossmann_project/assets/106852152/4ab8dfe5-035e-4b16-8a18-2547d7d59af9)

## 4.4. Tradução do erro para valores monetários
- Para facilitar o entendimento do erro, foi feita a adaptação para valores de receita em reais para cada uma das lojas da rede, levando-se em conta
o melhor e pior cenário predito. 
  
![traducao_erro_negocio](https://github.com/gtrmiranda/rossmann_project/assets/106852152/a1632d9f-d337-4a32-8f5d-39fe46755c36)

## 4.5. Previsão de receita geral da rede
- Foi calculada a previsão de receita para toda a rede de farmácias, levando0se em conta o melhor e o pior cenário de predição.
  
![Receita_geral](https://github.com/gtrmiranda/rossmann_project/assets/106852152/a6df5d88-19e6-4eee-b4ba-f390a4d5907b)

# 5. Resultados
- Com base no primeiro ciclo do CRISP-DM, o modelo final apresentou melhor desempenho utilizando o algoritmo de Machine Learning XGBoost Regressor.
- Ao final, obteve-se um desempenho satisfatório, com Erro Médio Percentual Absoluto (MAPE) de 11,84% para mais ou para menos.
- Esse erro pode ser traduzido em valores monetários por meio do Erro Médio Absoluto (MAE), que apresentou resultado de R$ 783,18 para mais ou para menos.
- Para facilitar o acesso ao modelo de predição de receitas em cada loja, foi desenvolvido um Bot no app Telegram, de maneira que a receita prevista
para cada loja da Rede Rossmann pode ser acessada pelo celular.

# 6. Considerações finais
- Ao desenvolver o presente projeto, foi possível aplicar ferramentas e técnicas diversas relacionados à Ciência de Dados, bem como traduzir de forma
didática e direta os resultados obtidos.
- Outros ciclos do CRISP-DM serão desenvolvidos com o objetivo de otimizar ainda mais a performance do modelo de predição. 
- O Modelo de Predição de Vendas da Rede Rossmann é replicável para qualquer modelo de negócio que necessite prever receitas de vendas.
- O desenvolvimento do projeto Rossmann se apresenta como importante comprovação de minha experiência enquanto cientista de dados em constante evolução.  
