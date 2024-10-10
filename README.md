# Desafio Computer and Information Research Scientist

Este projeto implementa uma aplicação em Python com funcionalidades em C++, integrando pré-processamento de texto, codificação de sentenças e cálculo de similaridade. A aplicação inclui um servidor HTTP que responde a consultas sobre um texto fornecido.

## Funcionalidades

- Pré-processamento: Divide uma dissertação em frases.
- Codificação de Sentenças: Gera embeddings para as frases e consultas usando modelos baseados no BERT.
- Similaridade de Sentenças: Calcula a frase que mais responde a cada consulta.
- Interface Web: Disponibiliza uma API REST para receber e processar textos e consultas.
- Docker: Suporte para execução do projeto em container.


## Requisitos

- Testado e executado em ambiente Linux
- Python 3.x
- Compilador C++ compatível com Python (usando pybind11)
- Docker (opcional)

## Instalação

### Passo 1: Instalar as dependências

Execute o seguinte comando para instalar os requisitos do projeto:

`pip install -r requirements.txt`

### Passo 2: Compilar o código C++

Use o comando abaixo para compilar as extensões C++:

`python setup.py build_ext --inplace`

### Passo 3: Executar o código

Para rodar a aplicação localmente:

`python main.py`

A interface da API estará disponível em: http://127.0.0.1:5000.

## Docker

### Passo 1: Construir a imagem Docker

Se preferir rodar o projeto em um container Docker, use o comando:

`docker build -t most_challenge . --debug`

### Passo 2: Rodar o container

Depois de construir a imagem, execute o container:

`docker run -p 5000:5000 most_challenge`

A interface estará acessível em: http://127.0.0.1:5000.

## Como usar a API

A API aceita um POST na rota /answers, onde você deve enviar um JSON no seguinte formato:

### Exemplo de entrada:

```json
{
  "essay": "Texto da dissertação aqui.",
  "queries": [
    "Primeira consulta",
    "Segunda consulta"
  ]
}
```

### Exemplo de resposta:

```json
{
  "answers": [
    "Resposta para a primeira consulta",
    "Resposta para a segunda consulta"
  ]
}
```

## Estrutura do Projeto

- main.py: Script principal que inicializa o servidor Flask.
- setup.py: Script de compilação para as extensões C++.
- sentence_embedding.cpp: Definição da classe em C++.
- requirements.txt: Lista de dependências do projeto.
