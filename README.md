# Projeto de Ciência de Dados para Dota 2

## Visão Geral

Este projeto tem como objetivo aplicar técnicas de ciência de dados ao universo do Dota 2, utilizando dados extraídos da [OpenDota API](https://docs.opendota.com/). Nosso foco será desenvolver um modelo preditivo que, a partir das estatísticas dos heróis, jogadores e partidas, consiga prever o resultado dos jogos. Além disso, o projeto visa identificar padrões de performance e sinergia entre heróis.

## Objetivos

- **Principal:**  
  Desenvolver um modelo preditivo que estime o resultado das partidas de Dota 2 com base em dados extraídos da OpenDota API.

- **Secundários:**  
  - Analisar padrões de desempenho dos heróis e jogadores.
  - Investigar a influência da combinação de heróis nas partidas.
  - Explorar e visualizar os dados para extrair insights relevantes sobre o jogo.

## Hipóteses

- **Hipótese Principal:**  
  É possível prever o resultado de uma partida de Dota 2 a partir dos dados de desempenho dos heróis e jogadores.

- **Questões de Pesquisa:**  
  - Quais métricas (estatísticas dos jogadores, heróis, tempo de jogo, etc.) têm maior impacto no resultado?
  - Como as sinergias entre heróis podem influenciar a performance do time?
  - Existe um padrão de desempenho que possa ser identificado para times vencedores?

## Dados e Fontes

- **Fonte Principal:**  
  [OpenDota API](https://docs.opendota.com/) – Utilizada para extrair dados históricos de partidas, estatísticas de heróis e jogadores.

- **Tipo de Dados:**  
  - Resultados de partidas
  - Estatísticas de desempenho dos heróis
  - Informações sobre jogadores e escolhas de itens

## Estrutura do Projeto

A organização do repositório segue uma estrutura modular para facilitar a documentação e o desenvolvimento:
/dota-data-project 
├── README.md # Visão macro do projeto (este arquivo) 
├── docs/ # Documentação detalhada │ 
    ├── objetivos.md # Detalhamento dos objetivos │ 
    ├── hipoteses.md # Documentação das hipóteses e questões de pesquisa │ 
    └── decisoes_arquitetura.md # Registro das decisões técnicas e arquiteturais 
├── data/ # Dados brutos e processados 
├── notebooks/ # Notebooks para análise exploratória e prototipagem 
├── src/ # Código fonte (scripts, funções, etc.) 
├── requirements.txt # Lista de dependências do projeto 
└── .gitignore 

## Fluxo do Projeto

1. **Extração dos Dados:**  
   Desenvolver scripts em Python para coletar dados da OpenDota API.

2. **Armazenamento e Organização:**  
   Salvar os dados extraídos em formatos como CSV ou JSON e, se necessário, utilizar um banco de dados local para facilitar consultas.

3. **Análise Exploratória (EDA):**  
   Realizar a limpeza e exploração dos dados para identificar padrões, outliers e preparar as features para modelagem.

4. **Engenharia de Features e Modelagem:**  
   Criar e selecionar variáveis que possam enriquecer o modelo preditivo. Em seguida, desenvolver o modelo utilizando técnicas de machine learning (com possibilidade de acelerar o processamento com GPU e CUDA).

5. **Documentação e Compartilhamento:**  
   Atualizar a documentação do projeto conforme o desenvolvimento e compartilhar os resultados e o código no repositório do GitHub.
