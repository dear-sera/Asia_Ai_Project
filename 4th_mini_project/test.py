import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains

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


def get_n_books(driver: 'selenium webdriver',
                iter: 'iteration number',
                dictionary: 'dict to save result'
                ):
    # 1 ~ 반복횟수 + 1(주로 25번) 반복
    for book_num in range(1, iter + 1):
        try:
            # 도서 리스트에서 book_num번째 책 anchor tag
            book = driver.find_element_by_xpath(
                f'//div[{book_num}][@class="ss_book_box"]//*[@class="ss_book_list"]//li/a')
            book.click()  # book_num번째 도서 클릭

            # 원하는 부분을 로딩하기 위해 근처까지 스크롤
            action = ActionChains(driver)
            action.move_to_element(driver.find_element_by_id('swiper_itemEvent')).perform()

            # 클래스를 통해 1차로 분류한 뒤, 그 중 내용이 '책소개'인 요소의 다음 요소 내용 summary에 저장
            temps = driver.find_elements_by_xpath('//div[@class="Ere_prod_mconts_LS"]')
            for temp in temps:
                if temp.text == '책소개':
                    print(book_num, end=' ')
                    dictionary['summary'].append(
                        temp.find_element_by_xpath('.//following-sibling::div[@class="Ere_prod_mconts_R"]').text)
                    dictionary['title'].append(driver.find_element_by_xpath('//a[@class="Ere_bo_title"]').text)
            # 태그내용(=도서명) title에 저장

            driver.back()

        # 에러 핸들링
        except UnexpectedAlertPresentException:
            print('UnexpectedAlertPresentException')
        except NoSuchElementException:
            print('NoSuchElementException')
    return dictionary  # 결과가 들어있는 dict 반환


pages = int(10000 / 25)  # 크롤링할 페이지 수
# cid = 1  # 이게 카테고리 (ex) 1: 소설/시/희곡, 170: 경제경영 ...
start = time.time()  # 얼마나 걸릴지 궁금

for cid in [1237]:  # 여기에 해당 카테고리의 cid 리스트 작성
    dictionary = {'title': [], 'summary': []}
    start_page = 1
    for page in range(start_page, pages + 1):
        # page를 바꿔가며 반복
        url = f'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=25&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}&SearchOption='
        print(f"\n============= {page} =============\n")
        driver.get(url)  # 해당 url로 크롬 브라우저 이동
        dictionary = get_n_books(driver, 25, dictionary)  # 해당 페이지의 도서 25권(전부임 ㅎ) 가져옴
        # 크롤링한 데이터 데이터프레임으로 변환
        if (page % 100 == 0 and page != 0) or page == pages:
            data = pd.DataFrame(dictionary)
            # 데이터프레임 및 소요시간 확인
            print(f'time: {time.time() - start}')

            # 장-르(정답)_책 수_페이지-범위_오늘 날짜.csv로 저장
            today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            data.to_csv(f'./crawling_data/cid-{cid}_{len(data)}_{start_page}-{page}_{today}.csv', index=False)
            dictionary = {'title': [], 'summary': []}
            start_page = page + 1

# 크롬 드라이버 종료
driver.close()