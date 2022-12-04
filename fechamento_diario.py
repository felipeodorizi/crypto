from datetime import date
from datetime import timedelta
from yahoo_fin.stock_info import get_data
from yahooquery import Ticker
from yahoofinancials import YahooFinancials
import sys
import mysql.connector
from mysql.connector import Error
import pandas as pd
import getopt
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

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def yesterday_currency_yquery(currency):
    cur = Ticker(currency)
    df=cur.history(period="1d")
    df = df.iloc[:1]

    dic_currency = {}

    if df.empty:
        return dic_currency

    dic_currency['close'] = df.close.values[0]
    dic_currency['adjclose'] = df.adjclose.values[0]
    dic_currency['ticker'] = df.index.values[0][0]
    dic_currency['date'] = df.index.values[0][1]
    dic_currency['volume'] = df.volume.values[0]

    return dic_currency

def yesterday_currency_yfin(currency):
    # Get today's date
    today = date.today()
    #print("Today is: ", today)

    # Yesterday date
    yesterday = today - timedelta(days = 1)
    print("Yesterday was: ", yesterday)

    df = get_data(currency, start_date=yesterday, end_date=yesterday, index_as_date = True, interval="1d")
    
    dic_currency = {}
    if df.empty:
        return dic_currency

    dic_currency['close'] = df.close.values[0]
    dic_currency['adjclose'] = df.adjclose.values[0]
    dic_currency['ticker'] = df.ticker.values[0]
    dic_currency['date'] = pd.to_datetime(df.index.values[0])
    dic_currency['volume'] = df.volume.values[0]

    return dic_currency


def yesterday_currency_financials(currency):
    # Get today's date
    today = date.today()
 
    # Yesterday date
    yesterday = today - timedelta(days = 1)

    str_today = today.strftime("%Y-%m-%d")
    str_yesterday = yesterday.strftime("%Y-%m-%d")


    yahoo_financials = YahooFinancials('BTC-USD')
    data=yahoo_financials.get_historical_price_data(str_yesterday, str_today, "daily")
    df = pd.DataFrame(data['BTC-USD']['prices'])
    df = df.iloc[:1]

    print(df)

    dic_currency = {}
    if df.empty:
        return dic_currency

    dic_currency['close'] = df.close.values[0]
    dic_currency['adjclose'] = df.adjclose.values[0]
    dic_currency['ticker'] = currency
    dic_currency['date'] = pd.to_datetime(df.formatted_date.values[0])
    dic_currency['volume'] = df.volume.values[0]

    return dic_currency


def change_is_last(ticker):
    print("change_is_last")
    sql_select = f"SELECT * FROM  `crypto`.`yf_crypto` WHERE yf_crypto.ticker='BTC-USD' AND is_last=1"
    print(sql_select)
    connection = create_db_connection(db_config['host'], db_config['login'], db_config['password'], db_config['db'])
    #connection = create_db_connection("localhost", "root", "root", "crypto")
    results = read_query(connection, sql_select)
    print(results)
    id = -1
    for result in results:
        id= result[0]
        print(id)
        sql_update = f"UPDATE `crypto`.`yf_crypto`  SET `is_last` = '0' WHERE `idyf_crypto` = '{id}'"
        execute_query(connection, sql_update)


def save_currency(dict_cur):
    print("gravar dados")
    print(dict_cur['close'])
    #connection = create_db_connection("localhost", "root", "root", "crypto")
    connection = create_db_connection(db_config['host'], db_config['login'], db_config['password'], db_config['db'])
    sql = f"INSERT INTO yf_crypto VALUES (NULL,'{dict_cur['ticker']}', '{dict_cur['date']}', '{dict_cur['close']}', '{dict_cur['adjclose']}','{dict_cur['volume']}', 1) "
    print(sql)
    execute_query(connection, sql)


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
# Le as informacoes da Biblioteca yahoo_fin
#
# Se estiver vazio por erro ele 
# Le os dados da Biblioteca YahooFinancials
#
dict_cur = yesterday_currency_yfin(currency)

if dict_cur:
    print("1")
    change_is_last(currency)
    save_currency(dict_cur)
else:
    dict_cur = yesterday_currency_financials(currency)
    change_is_last(currency)
    save_currency(dict_cur)






