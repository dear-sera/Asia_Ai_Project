"""
종교/역학, 예술/대중문화 카테고리의 책 제목, 책 소개 크롤링
"""

import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
import crawling as crawling

# 크롬 드라이버 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument('headless')  # 브라우저 안보임 / 잘 동작하는지 확인한 후 마지막에 실행할 것
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')

# 드라이버 경로
chromedriver = './chromedriver.exe'

# selenium webdriver에 크롬 드라이버 연동
driver = webdriver.Chrome(chromedriver, options=options)
driver.implicitly_wait(10)

cid_to_cat = {
    '1': 'Novel_Poem',
    '170': 'Economic_Management',
    '1230': 'Home_Cook_Beauty',
    '1237': 'Religion_Mysticism',
    '517': 'Art_Culture',
    '76001': 'reference_book',
    '55890': 'Health_Hobby_Leisure',
    '987': 'Science'
}

pages = 3
start = time.time()
cids = cid_to_cat.keys()
data_total = pd.DataFrame()
for cid in cids:
    start_page = 444
    for i, page in enumerate(range(start_page, start_page + pages)):
        dictionary = {"title": [], "summary": []}
        url = f"https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=25&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}&SearchOption="
        print(f"\n============= {cid_to_cat[cid]} - {page} =============\n")
        driver.get(url)  # 해당 url로 크롬 브라우저 이동
        dictionary = crawling.get_n_books(driver, 25, dictionary)  # 해당 페이지의 도서 25권(전부임 ㅎ) 가져옴
        # 크롤링한 데이터 데이터프레임으로 변환
        data = pd.DataFrame(dictionary)
        data["category"] = cid_to_cat[cid]
        data_total = pd.concat([data_total, data])
        # 소요시간 확인
        print(f"time: {time.time() - start}")

# 저장
today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
data_total.to_csv(
    f"./raw_test_{today}.csv",
    index=False,
)

driver.close()