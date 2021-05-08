#clusterinfo.py
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import re

def get_soup(url):
    req = requests.get(url)  # html태그와 content내용을 Response 객체로 반환
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def get_df_data_on_site(soup):
    col = []
    data = []
    box = soup.select('.tinytable > tbody tr')  # n 개의 div
    title = soup.select('.tinytable > thead th')  # n 개의 div

    for txt in title:
        col.append(txt.text)

    for row in box:
        row_data = []
        boxbox = row.select('td')

        for txt in boxbox:
            row_data.append(txt.text)

        data.append(row_data)

    return col, data


def make_refine_df(col, data):
    df = pd.DataFrame(data, columns=col)
    drop_col = ['X', '1d', '1w', '1m', '6m']
    df.drop(drop_col, axis=1, inplace=True)
    df.drop(columns=['Ins', 'ΔOwn'], axis=1, inplace=True)
    filingTime = []
    filingDate = []
    for index, row in df.iterrows():
        lst = row['Filing\xa0Date'].split(" ")
        filingDate.append(lst[0])
        filingTime.append(lst[1])
    df.drop(columns=['Filing\xa0Date'], axis=1, inplace=True)

    df2 = pd.DataFrame.from_dict({"Filing\xa0Date": filingDate, "Filing\xa0Time": filingTime})

    df = pd.concat([df2, df], axis=1)

    return df

if __name__ == "__main__":
    url = 'http://openinsider.com/latest-cluster-buys'
    soup = get_soup(url)
    col, data = get_df_data_on_site(soup)
    df = make_refine_df(col, data)