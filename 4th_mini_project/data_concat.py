import time
from glob import glob
import re
import pandas as pd

#각 카테고리별 고유 cid번호와 카테고리명을 딕셔너리로 저장
cid_to_cat = {
    '1': 'Novel_Poem',
    '170': 'Economic_Management',
    '1230': 'Home_Cook_Beauty',
    '1237': 'Religion_Mysticism',
    '517': 'Art_Culture',
    '76001': 'reference_book',
    '55890': 'Health_Hobby_Leisure',
    '987': 'Economic'
}
#현재 날짜와 시간 출력하기
today = time.strftime("%Y-%m-%d", time.localtime(time.time()))

#크롤링데이터에 있는 모든 파일의 경로 불러오기
filenames = glob('./crawling_data/*.csv')
get_cid = re.compile('cid-[0-9]+')  #re.compile= 정규식 객체를 리턴해준다 = 경로에서 'cid-숫자'까지 불러온다, cid-다음+는 숫자로 시작하는 단어가 한 개이상으로 된 객체를 가져온다(숫자들로만)
datas = []

for filename in filenames:  #모든 파일의 경로를 하나씩 가져오기
    if today in filename:  #파일 중 오늘 날짜에 해당하는 것만 출력
        print(filename)
        cid = get_cid.search(filename).group()[4:]  #get_cid의 문자열 중 cid-가 4글자여서 [4:]이후인 숫자들로만 가져온다(정규표현식은 객체를 가져오는 거라 group을 사용하여 문자열로 반환해준다)
        df = pd.read_csv(filename)  # 모든 파일을 df 으로 변환
        df['category'] = cid_to_cat[cid]  #위 딕셔너리에서 만들었던 것 중 키에 cid숫자를 넣어서 카테고리 컬럼을 만들어준다(값은 문자가 들어가게)
        datas.append(df)  #각각 파일의 데이터프레임을 하나의 리스트 안으로 합쳐주기

data = pd.concat(datas, ignore_index=True)  #리스트안에 있는 각각의 데이터프레임을 하나로 합쳐준다

print(data.head())
print(data.shape)
print(data['title'].unique().shape)

data.to_csv(f'./data/raw_{len(data)}_{today}.csv', index=False)