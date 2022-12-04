from yahoo_fin.stock_info import get_data
from yahoofinancials import YahooFinancials
from datetime import datetime
import sys
import mysql.connector
from mysql.connector import Error
import pandas as pd
import getopt
from datetime import date
from datetime import timedelta
import ast


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# Setar Configuracoes do MySQL no Arquivo config.db
# Lendo configuracoes do Banco de Dados
with open('config.db') as f:
    data = f.read()

db_config = ast.literal_eval(data)

#
# Ler os Argumentos
#
argv = sys.argv
currency = ""
arg_help = "{0} -t <ticker> ".format(argv[0])

if len(argv) < 2:
    print(arg_help)  # print the help message 
    exit(0)

try:
    opts, args = getopt.getopt(argv[1:], "hi:t:", ["help", "ticker="])
except:
    print(arg_help)
    sys.exit(2)
    
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(arg_help)  # print the help message
        sys.exit(2)
    elif opt in ("-t", "--ticker"):
        currency = arg

#
#
#

# Data de Hoje
today = date.today()
print("Today is: ", today)

# Ontem
yesterday = today - timedelta(days = 1)
print("Yesterday was: ", yesterday)

# Data de 10 anos atras 
start = datetime(yesterday.year-10, yesterday.month, yesterday.day)

#
# Le as informacoes da Biblioteca yahoo_fin
#
df = get_data(currency, start_date=start, end_date=yesterday,
                        index_as_date = True, interval="1d")

#
# Se estiver vazio por erro ele 
# Le os dados da Biblioteca YahooFinancials
#
if df.empty:
    print("YahooFinancials")
    str_start = start.strftime("%Y-%m-%d")
    print("Start:", str_start)

    str_end = yesterday.strftime("%Y-%m-%d")
    print("End:", str_end)    

    yahoo_financials = YahooFinancials(currency)
    data=yahoo_financials.get_historical_price_data(str_start, str_end, "daily")
    df = pd.DataFrame(data[currency]['prices'])
    df = df.drop('date', axis=1).set_index('formatted_date')

    # Grava os dados da Biblioteca YahooFinancials
    for index, row in df.iterrows():
        # access data using column names
        print(index, currency, row['close'], row['adjclose'], row['volume'])

        connection = create_db_connection(db_config['host'], db_config['login'], db_config['password'], db_config['db'])

        sql = f"INSERT INTO yf_crypto VALUES (NULL,'{currency}', '{pd.to_datetime(index)}', {row['close']}, {row['adjclose']}, '{row['volume']}', 0) "
        print(sql)
        execute_query(connection, sql)


else:
    # Grava os dados da Biblioteca Yahoo_Fin
    print("yahoo_fin")
    for index, row in df.iterrows():
        # access data using column names
        print(index, row['ticker'], row['close'], row['adjclose'], row['volume'])
        connection = create_db_connection(db_config['host'], db_config['login'], db_config['password'], db_config['db'])

        sql = f"INSERT INTO yf_crypto VALUES (NULL,'{row['ticker']}', '{index.date()}', {row['close']}, {row['adjclose']}, '{row['volume']}', 0) "

        print (sql)
        execute_query(connection, sql)


