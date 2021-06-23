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


def get_book(driver, book_num, dictionary):
    """권 단위 크롤링"""
    try:
        # 도서 리스트에서 book_num번째 책 anchor tag
        book = driver.find_element_by_xpath(  #해당 anchor tag의 xpath경로에서 해당 element를 찾음
            f'//div[{book_num}][@class="ss_book_box"]//*[@class="ss_book_list"]//li/a')
        book.click()  # click = book_num번째 도서(위에 해당하는 엘리먼트를) 클릭

        # 원하는 부분을 로딩하기 위해 근처까지 스크롤
        # 책소개는 엘리먼트가 없어서 근처인 이벤트 엘리먼트로 스크롤한 것('swiper_itemEvent')
        action = ActionChains(driver)  # ActionChains = 여러 개의 동작을 체인으로 묶어서 저장하고 실행
        action.move_to_element(driver.find_element_by_id('swiper_itemEvent')).perform()  #move_to_element = element로 마우스 이동(드래그), perform= action객체 실행 할 때 사용

        # 클래스를 통해 1차로 분류한 뒤, 그 중 내용이 '책소개'인 요소의 다음 요소 내용 summary에 저장(문단 전체가 통으로 클래스로 묶여서)
        # 태그내용(=도서명) title에 저장
        temps = driver.find_elements_by_xpath('//div[@class="Ere_prod_mconts_LS"]')  #클래스 안에 있는 여러 엘리먼트를 찾아옴
        for temp in temps:
            if temp.text == '책소개':  #temp의 글이 책소개면 책의 번호를 출력, summary컬럼에 내용저장
                print(book_num, end=' ')
                dictionary['summary'].append(
                    temp.find_element_by_xpath('.//following-sibling::div[@class="Ere_prod_mconts_R"]').text)
                dictionary['title'].append(driver.find_element_by_xpath('//a[@class="Ere_bo_title"]').text)  #타이틀커럼에 책 이름 저장


        driver.back()  # 페이지 속에 크롤링이 끝나면 전페이지로 돌아가기
    # 에러 핸들링
    except UnexpectedAlertPresentException: #청소년불가 책은 로그인알림창이 뜨는데 이창이 뜰 경우 그냥 무시
        print('UnexpectedAlertPresentException')
    except NoSuchElementException:  #해당되는 엘리먼트가 없으면 무시
        print('NoSuchElementException')

    return dictionary  # 결과가 들어있는 dict 반환


def get_n_books(driver: 'selenium webdriver', # 함수 생성 시 변수에 콜론을 붙여 문자열을 적으면 주석과 같은 기능 (함수 변수를 설명)
                iter: 'iteration number',  #iter = 반복할 수
                dictionary: 'dict to save result'
                ):
    """페이지 단위 크롤링"""
    # 페이지당 25권의 책이 있어서 25권을 반복해준다
    for book_num in range(1, iter + 1):
        get_book(driver, book_num, dictionary)

    return dictionary  # 결과가 들어있는 dict 반환


if __name__=='__main__':  # 이 py파일을 직접 돌릴 때만 실행이 가능하게 해준다(다른 파일해서 import해도 실행이 되지 않는다)
    # 드라이버 경로
    chromedriver = './chromedriver.exe'

    # selenium webdriver에 크롬 드라이버 연동
    driver = webdriver.Chrome(chromedriver, options=options)
    driver.implicitly_wait(10)

    pages = int(10000 / 25)  # 크롤링할 페이지 수 (만개의 데이터가 목표라서 페이지당 25개의 권 수로 나눠준다)
    # cid = 1  # 이게 카테고리 (ex) 1: 소설/시/희곡, 170: 경제경영 ...
    start = time.time()  # 얼마나 걸릴지 궁금

    for cid in [170]:  # 여기에 해당 카테고리의 cid 리스트 작성
        dictionary = {'title': [], 'summary': []}  #딕셔너리 생성하여 초기화
        start_page = 1  #기본 페이지 설정
        for page in range(start_page, pages + 1):
            # page를 바꿔가며 반복(cid에는 카테고리 고유 숫자가 들어가게)
            url = f'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=25&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}&SearchOption='
            print(f"\n============= {page} =============\n")  #f = 에프스트링을 사용하여 중괄호안에 변수값을 대입해준다
            driver.get(url)  # 해당 url로 크롬 브라우저 이동
            dictionary = get_n_books(driver, 25, dictionary)  # 해당 페이지의 도서 25권(전부) 가져옴(25=iter)
            if (page % 100 == 0 and page != 0) or page == pages:  #페이지가 100으로 나눠지는 수에 도달하면 데이터프레임으로 변환 후 저장 (100, 200, 300, 400 페이지 당)
                # 크롤링한 데이터 데이터프레임으로 변환
                data = pd.DataFrame(dictionary)
                # 소요시간 확인
                print(f'time: {time.time() - start}')

                # 장-르(정답)_책 수_페이지-범위_오늘 날짜.csv로 저장
                today = time.strftime("%Y-%m-%d", time.localtime(time.time()))  #strftime=날짜와 시간을 문자열로 변환, time.time=현재 시간을 반환, localtime= time에서 반환한 값을 현재시간대에 맞춰서 출력
                data.to_csv(f'./crawling_data/cid-{cid}_{len(data)}_{start_page}-{page}_{today}.csv', index=False)  #index=False => 인덱스를 만들지 않는다 (이걸 안하고 그냥 만들면 인덱스가 자동으로 생성되어 'Unnamed: 0' 이 만들어진다)
                # 위에서 만들어져서 100페이지가 추가된 딕셔너리가 데이터프레임으로 만들어진 뒤 저장을 하면 다시 101페이지부터 돌 떄 딕셔너리를 기존껄로 덮혀쓰는 걸 막기위해 새로 초기화
                dictionary = {'title': [], 'summary': []}
                start_page = page + 1  #저장할 때 데이터 이름에 start_page가 들어가서 새로 100페이지를 저장해줄 때

    # 크롬 드라이버 종료
    driver.close()