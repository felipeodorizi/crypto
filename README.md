# Freelance-Tecnologia
Repositório do Freelance Tecnologia Workana

# Comandos para criar o ambiente e instalar as bibliotecas

conda create --name crypto python=3.8

conda activate crypto

pip install -r requirements.txt 


# No MySQL Rodar comandos do Arquivo

crypto.sql


Configuras Dados do Banco de Dados no Arquivo de Configuracao

config.db


#  Rodando Historico

Para Salvar o historico da Moeda no MySQL 

python historico.py  ou python historico.py  -h

Para ver opcao do historico.py

historico.py -t ticker

Rodando historico BTC-USD

python historico.py -t BTC-USD



#  Rodando Fechamento Ontem


python fechamento_diario.py ou python fechamento_diario.py  -h

Para ver opcao do fechamento_diario.py

fechamento_diario.py -t ticker


#  Colocando em Cron


Para garantir que o Script pode ser executado

chmod 755 insert_yesterday_crypto.sh

Alterar os Caminhos no Script Bash

CAMINHO_ANACONDA
e
CAMINHO_SCRIPT_PYTHON


Verificar se existe algum Cron Rodando

crontab -l

Se existir rodar comando

crontab -l > cronfile


Alterar o caminho do Script insert_yesterday_crypto.sh no Arquivo cron.txt

Substituir o Caminho em CAMINHO_DO_SCRIPT pelo caminho correto


depois concatenar nos crons antigos 

cat cron.txt >> cronfile

Verificar se adicionou corretamente

more cronfile

crontab cronfile


Caso nao tenha nenhum rodando

crontab cron.txt

