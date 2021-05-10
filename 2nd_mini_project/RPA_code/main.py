from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import requests
import fnmatch
import time
import re
import os


def get_soup(url):
    req = requests.get(url)  # html태그와 content내용을 Response 객체로 반환
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    return soup


#################################################################################
def get_df_data_on_site(soup):
    col = []
    data = []
    box = soup.select('#filing_table > tbody tr')  # n 개의 div
    title = soup.select('#filing_table > thead td')  # n 개의 div

    for txt in title:
        col.append(txt.text)

    for row in box:
        row_data = []
        boxbox = row.select('td')

        for txt in boxbox:
            row_data.append(txt.text)

        data.append(row_data)

    return col, data


#################################################################################
def refine_df_and_version(col, data):
    df = pd.DataFrame(data, columns=col)

    p_date = re.compile(r'.{10}')
    p_word = re.compile(r'[a-zA-Z]*$')

    try:
        drop_col = ['Filing']
        df.drop(drop_col, axis=1, inplace=True)
    except:
        pass

    df['Type'] = df['TransactionDate']

    for i in range(len(df)):
        m_date = p_date.search(df.iloc[i]['TransactionDate'])
        m_word = p_word.search(df.iloc[i]['TransactionDate'])
        Y, M, D, h, m = split_datetime(df['ReportedDateTime'].iloc[i])

        df['Type'].iloc[i] = m_word.group()
        df['TransactionDate'].iloc[i] = m_date.group()[2:]
        df['ReportedDateTime'].iloc[i] = '{}-{}-{} {}:{}'.format(Y, M, D, h, m)

        version = '.{}.{}.{}.{}.{}'.format(Y, M, D, h, m)

    return df, version


#################################################################################
def set_initial_DB(name, form):
    print('making dataframe.... {}....'.format(name))
    soup = get_soup(url_form.format(form))
    col, data = get_df_data_on_site(soup)
    df, version = refine_df_and_version(col, data)

    dir_DB = 'D:/AI/pjt2/DB'
    filename = 'df_{}{}.xlsx'.format(name.lower(), version)

    print('saving to DB as \'{}\''.format(filename))

    df.to_excel('{}/{}'.format(dir_DB, filename), index=False)


#################################################################################
def split_datetime(datetype):  # ex) '2021-04-2911:20 pm' / '2021-04-28:02 am'
    date = datetype[2:10]
    time = datetype[10:-3]
    ap = datetype[-2:]
    Y, M, D = date.split('-')
    h, m = time.split(':')

    if ap[0] == 'p':
        h = str((int(h) + 12)) if h != '0' else '00'
    else:
        if len(h) == 1:
            h = '0' + h

    return Y, M, D, h, m


#################################################################################
def df_name(name):
    return locals()['df_{}'.format(name.lower())]


#################################################################################
def df_from_db(tic, web_df):
    p = re.compile(tic)
    dirname = 'D:/AI/pjt2/DB'
    filenames = os.listdir(dirname)

    for db_filename in os.listdir(dirname):
        if fnmatch.fnmatch(db_filename, '*{}*'.format(tic)):
            return pd.read_excel('{}/{}'.format(dirname, db_filename)), ''

    return web_df, '[NEW DATA]\n'


#################################################################################
def version_from_db(tic):
    p = re.compile(tic)
    dirname = 'D:/AI/pjt2/DB'
    filenames = os.listdir(dirname)
    for filename in filenames:
        if p.search(filename): break

    return filename[-19:-5].split('.')


#################################################################################
def version_from_web(df):
    temp = df.iloc[-1]['ReportedDateTime']
    temp = temp.split(' ')

    return temp[0].split('-') + temp[1].split(':')


#################################################################################
def update_new_data(web_df, tic):
    i = 0
    db_df, note = df_from_db(tic, web_df)

    if version_from_db(tic) != version_from_web(web_df):

        for datetime in web_df[::-1]['ReportedDateTime']:
            if db_df.iloc[-1]['ReportedDateTime'] == datetime:
                df_df = pd.concat([db_df, web_df.iloc[-(i + 1):-1]])
                break
            else:
                i += 1
        return db_df, note + txt_log(tic, i), 1
    else:
        return db_df, note + txt_log(tic, i), 0


#################################################################################
def save_db(df, name, version):
    dir_DB = 'D:/AI/pjt2/DB'
    newname = 'df_{}{}.xlsx'.format(name.lower(), version)
    filename = newname
    for db_filename in os.listdir('D:/AI/pjt2/DB'):
        if fnmatch.fnmatch(db_filename, '*{}*'.format(name)):
            filename = db_filename
            break

    if filename != newname:
        os.rename('{}/{}'.format(dir_DB, filename), '{}/{}'.format(dir_DB, newname))

    print('saving to DB as \'{}\''.format(newname))
    df.to_excel('{}/{}'.format(dir_DB, newname), index=False)


#################################################################################
def txt_log(tic, update_count):
    return 'in \'{}\', {} data(s) updated\n'.format(tic, update_count)


#################################################################################
def make_log(txt, cnt):
    dir_DB = 'D:/AI/pjt2/log'
    now = datetime.datetime.now()
    file_name = 'log{}({}).txt'.format(now.strftime('.%F.%H.%M.%S'), cnt)
    full_name = '{}/{}'.format(dir_DB, file_name)
    f = open(full_name, 'w')
    f.write(txt)
    f.close()


#################################################################################

if __name__ == '__main__':
    url_lib = {'TESLA': '1318605',
               'APPLE': '320193',
               'PALANTIR': '1321655',
               'COUPANG': '1834584',
               'UNITY': '1810806',
               'GOLUB_CAPITAL_BDC': '1476765',
               'AMAZON': '1018724',
               'DATADOG': '1561550'}
    url_form = 'https://www.secform4.com/insider-trading/{}.htm'
    txt_for_log = ''
    update_count = 0

    for name, form in url_lib.items():
        name = name.lower()
        soup = get_soup(url_form.format(form))
        col, data = get_df_data_on_site(soup)
        df, version = refine_df_and_version(col, data)
        df, txt, cnt = update_new_data(df, name)
        txt_for_log += txt
        update_count += cnt
        save_db(df, name, version)

    make_log(txt_for_log, update_count)

    print('\n\ncomplete\n\nend in...')
    for i in range(3, -1, -1):
        time.sleep(1)
        print(i)
