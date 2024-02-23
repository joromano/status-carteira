
# Tracker para Carteira de Ações

## Live Demo

Uma versão hospedada desta aplicação está disponível em http://carteira.joromano.com

Para usuário de demonstração, utilize:
- Login: **demo1** / Senha: **demo1**
- Login: **demo2** / Senha: **demo2**

## Funcionalidades

  

- Acompanhar posição da carteira personalizada em tempo real (dados obtidos do Yahoo Finance)

- Gráficos para acompanhar a evolução dos investimentos

- Histórico de Operações

- Cache em banco de dados dos valores históricos dos ativos

- Suporte para múltiplos usuários

  

## Como Executar

 
- Clone este repositório para a sua máquina:
```
https://github.com/joromano/status-carteira.git
```
- Instale os pré-requisitos:
```
pip install -r requirements.txt
```
- Realize a migração do Banco de Dados:
```
python carteira/manage.py migrate
```
- Rode o servidor de desenvolvimento:
```
python carteira/manage.py runserver 0:80
```

## Arquitetura da Aplicação

A aplicação foi desenvolvida utilizando a framework Django (Python). O front-end é renderizado pela própria *engine* de templates do Python, para manter a aplicação simples. Caso haja a necessidade de expandir a aplicação, seria recomendado utilizar uma framework front-end (como o *React.js*) e criar métodos REST a partir do Django. Atualmente é utilizado o banco de dados SQLite por conta da baixa demanda, no entanto para ambientes de produção é fortemente sugerido utilizar um banco de dados mais robusto suportado pelo Django (PostgreSQL, MySQL...).