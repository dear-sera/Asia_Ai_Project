import collections
import json

import requests
from bs4 import BeautifulSoup
import re
import telegram
import threading


class Stock_info:
    nums = collections.deque()
    no_arr = collections.deque()
    title_arr = collections.deque()
    name_arr = collections.deque()

    def __init__(self, nums, no_arr, title_arr, name_arr):
        self.nums = nums
        self.name_arr = name_arr
        self.no_arr = no_arr
        self.title_arr = title_arr

    def test(self):
        print(self.no_arr)


def parsingStockInfo() -> Stock_info:
    url = "https://finance.naver.com/sise/lastsearch2.nhn"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url, headers=headers)

    a = 1

    nums = collections.deque()
    no_arr = collections.deque()
    title_arr = collections.deque()
    name_arr = collections.deque()

    header = "==============상위 10 종목================"

    # response가 정상적으로 코드를 받았다면,
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        table = '#contentarea > div.box_type_l > table > tr > '

        no = table + 'td.no'  # class = no
        title = table + 'td > a.tltle'
        numbers = table + 'td.number'
        types = "#contentarea > div.box_type_l > table > tr.type1 > th"

        no_list = soup.select(no)
        title_list = soup.select(title)
        number_list = soup.select(numbers)
        type_list = soup.select(types)

        for n in number_list:
            if a <= 4:
                nums.append(re.sub('[^a-z 0-9 % .+-]', '', n.get_text()))
            a += 1
            if a == 11:
                a = 1

        for i in range(1, 6):
            name_arr.append(type_list[i].get_text())

        for i in range(0, 10):
            no_arr.append(no_list[i].get_text())
            title_arr.append(title_list[i].get_text())

        st = Stock_info(nums, no_arr, title_arr, name_arr)

        return st

    else:
        print(response.status_code)


def sendMessage(st: Stock_info):
    names = st.name_arr
    no = st.no_arr
    titles = st.title_arr
    nums = st.nums
    info_message = "=====================================================\n"

    info_message += '{:4s}'.format('순위 | ')

    for i in range(1, 6):
        if i == 1:
            info_message += '{:12s}'.format(names.popleft())
        else:
            info_message += '{:5s}'.format(names.popleft())
        info_message += ' | '

    info_message += '\n'

    for i in range(0, 10):
        info_message += '{:6s}'.format(no.popleft())
        info_message += ' | '
        info_message += '{:12s}'.format(titles.popleft())
        info_message += ' | '

        for j in range(0, 4):
            info_message += '{:5s}'.format(nums.popleft())
            info_message += ' | '

        info_message += '\n'

    my_token = '1741282663:AAEDtZ9fPBtkZILfACXinRHGQbrYWwrfxIQ'
    bot = telegram.Bot(token=my_token)
    bot.sendMessage(chat_id=1707831075, text=info_message)
