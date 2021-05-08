import pandas as pd
import fnmatch
import os
import re
import telegram
import threading

def df_from_db(tic):
    dirname = 'D:/AI/pjt2/DB'

    for db_filename in os.listdir(dirname):
        if fnmatch.fnmatch(db_filename, '*{}*'.format(tic)):
            break

    return pd.read_excel('{}/{}'.format(dirname, db_filename))


def msg_text(name='tesla'):
    df = df_from_db(name)
    df = df[::-1]
    txt = ''
    for i in range(3):
        data = df.iloc[i]
        txt += '\n\'{}\' {}s {} shares\nin price as {} on {}\n(reported {})\n' \
            .format(data['InsiderRelationship'], data['Type'], data['SharesTraded'],
                    data['AveragePrice'], data['TransactionDate'], data['ReportedDateTime'])
    my_token = '1741282663:AAEDtZ9fPBtkZILfACXinRHGQbrYWwrfxIQ'
    bot = telegram.Bot(token=my_token)
    bot.sendMessage(chat_id=1707831075, text=txt)
