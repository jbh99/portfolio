import tkinter as tk
from tkinter import ttk, messagebox
import requests
base_region_codes = {
    "11": "서울특별시",
    "26": "부산광역시",
    "27": "대구광역시",
    "28": "인천광역시",
    "29": "광주광역시",
    "30": "대전광역시",
    "31": "울산광역시",
    "36": "세종특별자치시",
    "41": "경기도",
    "42": "강원도",
    "43": "충청북도",
    "44": "충청남도",
    "45": "전라북도",
    "46": "전라남도",
    "47": "경상북도",
    "48": "경상남도",
    "50": "제주특별자치도"
}
tourist_spots = {
    # 서울특별시 하위 지역
    "1111000000": [
        ["경복궁", "조선 시대의 정궁으로 1395년에 완공. 광화문, 근정전 등 주요 건물들이 잘 보존되어 있음"],
        ["청와대", "대한민국 대통령의 관저로 1991년 완공. 본관, 영빈관, 춘추관 등 한옥 스타일의 건물이 특징"]
    ],
    "1114000000": [
        ["남산타워", "서울의 전경을 한눈에 볼 수 있는 랜드마크 타워. 1969년 개장, 높이 236.7m의 서울 대표 관광지"],
        ["명동", "쇼핑과 음식으로 유명한 서울의 대표적인 상업지구. 명동거리, 명동성당 등이 주요 관광 포인트"]
    ],
    "1117000000": [
        ["홍대", "젊음과 예술이 공존하는 문화의 거리. 공연, 갤러리, 독특한 카페들이 밀집해 있는 지역"],
        ["합정역", "힙한 분위기의 카페와 맛집들이 모여있는 곳. 특히 합정동 망리단길이 유명"]
    ],
    
    # 부산광역시 하위 지역
    "2614000000": [
        ["송도해수욕장", "부산에서 가장 오래된 인공 해수욕장. 1913년 개장, 송도암반산책로와 함께 즐길 수 있음"],
        ["송도 구름산책로", "바다 위를 걷는 듯한 느낌을 주는 산책로. 2015년 개장, 총 길이 365m의 아름다운 코스"]
    ],
    "2617000000": [
        ["부잔 진시장", "부산 최대의 전통시장. 1946년 개장, 신선한 해산물과 다양한 먹거리로 유명"],
        ["부산 자유도매시장", "신선한 농수산물을 저렴하게 구입할 수 있는 대형 시장. 새벽 장이 특히 유명"]
    ],
    "2620000000": [
        ["국립해양박물관", "한국 해양문화를 한눈에 볼 수 있는 박물관. 2012년 개관, 다양한 체험 프로그램 제공"],
        ["흰여울문화마을", "부산의 산토리니라고 불리는 컬러풀한 마을. 영화 '변호인' 촬영지로 유명"]
    ],
    "2623000000": [
        ["부산어린이대공원", "동물원과 놀이시설이 함께 있는 대공원. 1971년 개원, 가족 단위 관광객에게 인기"],
        ["선암사", "부산 기장군에 위치한 천년고찰. 통일신라시대 창건, 부산의 대표적인 사찰 중 하나"]
    ],
    "2638000000": [
        ["부산현대미술관", "현대미술 작품을 전시하는 미술관. 1998년 개관, 다양한 기획전시가 열림"],
        ["다대포 꿈의 낙조분수", "해질녘 아름다운 노을과 분수가 어우러지는 명소. 높이 55m의 분수쇼"]
    ],
    "2644000000": [
        ["맥도생태공원", "도심 속 생태공원. 습지생태원과 다양한 식물들을 관찰할 수 있음"],
        ["신호공원", "부산진구에 위치한 휴식공간. 아기자기한 정원과 산책로가 잘 조성되어 있음"]
    ],
    "2650000000": [
        ["F1963", "옛 와이어공장을 리모델링한 문화공간. 카페, 서점, 갤러리 등이 입점해 있음"],
        ["광안리해수욕장", "부산 대표 해수욕장. 1.4km의 백사장과 광안대교 야경이 유명"]
    ],
    "2671000000": [
        ["아홉산숲", "도심 속 휴식처. 9개의 작은 산으로 이루어진 울창한 숲"],
        ["국립부산과학관", "체험형 과학관. 다양한 과학 원리를 체험하며 배울 수 있는 시설"]
    ],
    
    # 대구광역시 하위 지역
    "2711000000": [
        ["대구약령시", "한방약재 전문 시장. 조선시대부터 이어온 전통시장으로 다양한 한약재 판매"],
        ["대구근대골목", "대구의 근대문화유산이 모여있는 거리. 근대건축물과 박물관이 많음"]
    ],
    "2714000000": [
        ["동화사", "대구 팔공산에 위치한 사찰. 통일신라시대 창건, 보물 제246호 동화사극락전이 유명"],
        ["팔공산", "대구의 진산. 높이 1,192m, 등산로와 동화사 등 사찰이 많음"]
    ],
    "2717000000": [
        ["수성못", "대구 수성구의 인공호수. 1925년 조성, 주변에 산책로와 문화시설이 잘 갖춰져 있음"],
        ["수성알파시티", "대구의 첨단 도시공간. 고층 건물과 쇼핑몰, 문화시설이 밀집"]
    ],
    "2720000000": [
        ["앞산공원", "대구 시내를 내려다볼 수 있는 공원. 등산로와 전망대가 잘 정비되어 있음"],
        ["대구스타디움", "대구 월드컵경기장. 2001년 완공, 66,422석 규모의 대형 경기장"]
    ],
    "2723000000": [
        ["이월드", "대구의 대표적인 테마파크. 83타워와 다양한 놀이기구, 계절별 축제로 유명"],
        ["두류공원", "대구 달서구의 대형 공원. 분수쇼와 산책로, 체육시설이 잘 갖춰져 있음"]
    ],
    "2771000000": [
        ["대구삼성라이온즈파크", "프로야구 삼성 라이온즈의 홈구장. 2016년 개장, 24,000석 규모"],
        ["대구과학관", "체험형 과학문화시설. 다양한 과학 전시물과 교육 프로그램 운영"]
    ],
    
    # 인천광역시 하위 지역
    "2817000000": [
        ["인천대교", "인천을 상징하는 현수교. 총 길이 21.38km, 야간 조명이 아름다운 명소"],
        ["을왕리해수욕장", "인천의 대표적인 해수욕장. 얕은 수심과 넓은 백사장이 특징"]
    ],
    "2818500000": [
        ["차이나타운", "한국 최대의 차이나타운. 중식당과 중국풍 건물들이 밀집해 있음"],
        ["자유공원", "한국 최초의 서양식 공원. 1888년 개원, 인천 시내를 내려다볼 수 있는 전망대"]
    ],
    
    # 광주광역시 하위 지역
    "2917000000": [
        ["무등산", "광주의 진산. 높이 1,187m, 기암괴석과 억새평원이 유명"],
        ["국립광주박물관", "호남지역의 문화유산을 전시. 1978년 개관, 다양한 고고미술품 소장"]
    ],
    "2920000000": [
        ["광주광역시립미술관", "현대미술 작품을 전시하는 미술관. 1992년 개관, 기획전시가 활발"],
        ["518민주묘지", "5·18 민주화운동의 역사적 현장. 추모공원과 기념관으로 구성"]
    ],
    "2953000000": [
        ["양림동 역사문화마을", "근대역사문화거리. 옛 가옥과 박물관, 갤러리가 모여있는 지역"],
        ["광주예술의거리", "예술가들이 모여드는 거리. 공연장과 갤러리, 공방이 밀집"]
    ],
    
    # 대전광역시 하위 지역
    "3017000000": [
        ["엑스포과학공원", "1993년 대전엑스포 개최지. 과학관과 체험시설, 한빛탑이 유명"],
        ["대전오월드", "동물원과 식물원이 결합한 테마파크. 다양한 동물과 아름다운 정원"]
    ],
    "3020000000": [
        ["유성온천", "대전의 대표 온천지구. 다양한 온천시설과 호텔이 밀집해 있음"],
        ["계족산", "대전의 명산. 높이 429m, 억새밭과 전망대가 유명"]
    ],
    "3023000000": [
        ["대청호", "대전의 대표적인 인공호수. 수상레포츠와 드라이브 코스로 유명"],
        ["보문산", "대전 시내를 내려다볼 수 있는 산. 높이 457m, 등산로가 잘 정비되어 있음"]
    ],
    
    # 울산광역시 하위 지역
    "3117000000": [
        ["간절곶", "울산의 동쪽 끝. 해돋이 명소로 유명한 절경"],
        ["대왕암공원", "울산의 대표적인 해안공원. 기암절벽과 산책로가 아름다움"]
    ],
    "3120000000": [
        ["태화강국가정원", "도심 속 생태공원. 철새도래지와 십리대숲이 유명"],
        ["울산대공원", "울산의 대표 공원. 동물원과 식물원, 다양한 휴식공간"]
    ],
    "3171000000": [
        ["울산바위", "울산의 상징적인 바위. 기암괴석과 전설이 어우러진 명소"],
        ["신불산", "울산의 명산. 높이 1,209m, 등산로와 자연경관이 뛰어남"]
    ],
    
    # 세종특별자치시 하위 지역
    "3611000000": [
        ["세종호수공원", "세종시의 중심공원. 넓은 호수와 산책로, 분수쇼가 유명"],
        ["국립세종도서관", "국립중앙도서관 세종분관. 2013년 개관, 대규모 장서 보유"]
    ],
    
    # 경기도 하위 지역
    "4146100000": [
        ["호암미술관", "한국 근현대 미술품을 전시하는 사립미술관. 1982년 개관"],
        ["에버랜드", "국내 최대 규모의 테마파크. 다양한 놀이기구와 동물원으로 유명"]
    ],
    "4148000000": [
        ["헤이리 예술마을", "예술가들이 모여 사는 마을. 갤러리와 카페, 공방이 밀집"],
        ["퍼스트가든", "유럽식 정원과 실내정원이 어우러진 대형 정원"]
    ],
    "4150000000": [
        ["설봉공원", "이천의 대표 공원. 등산로와 전망대, 문화시설이 잘 갖춰져 있음"],
        ["덕평공룡수목원", "공룡 테마의 수목원. 다양한 식물과 공룡 모형 전시"]
    ],
    "4161000000": [
        ["화담숲", "자연과 인공이 조화된 수목원. 4계절 아름다운 풍경을 즐길 수 있음"],
        ["팔당물안개공원", "팔당호를 배경으로 한 공원. 물안개 분수와 산책로가 유명"]
    ],
    "4165000000": [
        ["포천 산정호수", "아름다운 호수와 주변 경관으로 유명한 관광지"],
        ["국립수목원(광릉숲)", "한국을 대표하는 수목원. 다양한 식물자원 보유"]
    ],
    "4180000000": [
        ["재인폭포 (한탄강 유네스코 세계지질공원)", "한탄강의 아름다운 폭포. 지질학적 가치가 높음"],
        ["연천 호로고루", "고구려 시대의 유적지. 역사적 가치가 높은 명소"]
    ],
    "4182000000": [
        ["쁘디프랑스", "프랑스 마을을 테마로 한 관광지. 유럽풍 건물과 문화체험"],
        ["자라섬", "남한강의 아름다운 섬. 국제재즈페스티벌 개최지로 유명"]
    ],
    
    # 강원도 하위 지역
    "4211000000": [
        ["남이섬", "자연과 예술이 어우러진 섬. 겨울에는 눈꽃축제로 유명"],
        ["강촌레일파크", "폐철도를 활용한 레일바이크. 아름다운 강원도 풍경을 즐길 수 있음"]
    ],
    "4213000000": [
        ["설악산", "한국의 대표적인 명산. 울산바위와 비룡폭포 등 절경이 많음"],
        ["속초해수욕장", "동해안의 대표적인 해수욕장. 맑은 물과 넓은 백사장이 특징"]
    ],
    "4215000000": [
        ["정동진", "해돋이로 유명한 동해안 마을. 정동진역과 해안절경이 아름다움"],
        ["강릉커피거리", "커피와 문화가 어우러진 거리. 다양한 카페와 갤러리 밀집"]
    ],
    "4217000000": [
        ["양양서피비치", "청정해변으로 유명한 해수욕장. 서핑하기 좋은 조건을 갖춤"],
        ["낙산사", "동해안에 위치한 사찰. 해송과 바다가 어우러진 절경"]
    ],
    "4219000000": [
        ["평창알펜시아", "2018 평창동계올림픽 개최지. 리조트와 콘도시설이 잘 갖춰져 있음"],
        ["대관령스키장", "국내 최고의 스키장. 다양한 슬로프와 시설을 자랑"]
    ],
    "4221000000": [
        ["철원DMZ", "비무장지대 일원. 평화전망대와 제3땅굴 등 역사적 현장"],
        ["고석정", "한탄강의 절경. 기암절벽과 맑은 강물이 어우러진 명소"]
    ],
    "4223000000": [
        ["화천산나물축제", "화천군의 대표 축제. 산나물 체험과 다양한 행사 진행"],
        ["파로호", "화천의 아름다운 인공호수. 수상레포츠와 드라이브 코스로 유명"]
    ],
    
    # 충청북도 하위 지역
    "4311000000": [
        ["청주상당산성", "백제 시대의 산성. 역사적 가치가 높은 문화재"],
        ["청주공예비엔날레", "국제공예전시회. 2년마다 개최되는 대형 문화행사"]
    ],
    "4313000000": [
        ["수안보온천", "충북의 대표 온천지구. 다양한 온천시설과 숙박시설"],
        ["충주호", "한국 최대의 인공호수. 수상레포츠와 관광명소"]
    ],
    "4315000000": [
        ["단양팔경", "단양군의 8대 절경. 고수동굴, 도담삼봉 등이 포함"],
        ["도담삼봉", "남한강의 상징적인 경관. 세 개의 바위가 강 중앙에 우뚝 솟아 있음"]
    ],
    "4372000000": [
        ["보은속리산", "충북의 명산. 법주사와 함께 유명한 등산코스"],
        ["법주사", "속리산에 위치한 사찰. 국보 제55호 쌍사자석등이 유명"]
    ],
    "4374000000": [
        ["옥천레일바이크", "폐철도를 활용한 레일바이크. 아름다운 농촌 풍경을 즐길 수 있음"],
        ["이화사", "옥천군에 위치한 사찰. 아름다운 자연경관과 어우러진 절"]
    ],
    
    # 충청남도 하위 지역
    "4413000000": [
        ["아산스파비스", "대형 온천리조트. 다양한 테마의 온천시설을 갖춤"],
        ["온양온천", "한국 최고(最古)의 온천. 1300년의 역사를 가진 온천지구"]
    ],
    "4415000000": [
        ["공주공산성", "백제 시대의 산성. 역사적 가치가 높은 문화재"],
        ["무령왕릉", "백제 무령왕과 왕비의 무덤. 1971년 발견된 중요한 고고학적 유적"]
    ],
    "4418000000": [
        ["부여낙화암", "백제 멸망의 전설이 깃든 절벽. 아름다운 경관과 역사적 의미"],
        ["백제문화단지", "백제 문화를 재현한 테마파크. 역사체험과 문화행사 진행"]
    ],
    "4420000000": [
        ["서산해미읍성", "조선 시대의 읍성. 잘 보존된 성곽과 역사적 분위기"],
        ["간월암", "서해안의 아름다운 암자. 바다와 어우러진 절경"]
    ],
    "4421000000": [
        ["태안안면도", "서해안의 아름다운 섬. 해수욕장과 등대가 유명"],
        ["꽃지해변", "태안군의 대표적인 해수욕장. 아름다운 일몰로 유명"]
    ],
    "4471000000": [
        ["예산수덕사", "충남 예산군의 사찰. 대한불교조계종 제6교구 본사"],
        ["삽교천", "예산군을 흐르는 강. 아름다운 강변 풍경과 생태공원"]
    ],
    
    # 전라북도 하위 지역
    "4511000000": [
        ["전주한옥마을", "전통 한옥이 밀집한 지역. 한옥체험과 맛집으로 유명"],
        ["경기전", "조선 태조의 어진을 모신 사당. 전주 한옥마을 내에 위치"]
    ],
    "4513000000": [
        ["군산근대역사박물관", "군산의 근대문화유산을 전시. 옛 일본식 건물을 리모델링"],
        ["군산철새도래지", "새들이 모여드는 습지. 다양한 철새를 관찰할 수 있음"]
    ],
    "4514000000": [
        ["익산미륵사지", "백제 시대의 사찰 유적. 미륵사지석탑(국보 제11호)이 유명"],
        ["익산타워", "익산의 랜드마크. 전망대와 문화시설을 갖춘 타워"]
    ],
    "4518000000": [
        ["정읍내장산", "전북의 명산. 가을 단풍이 특히 아름다운 곳"],
        ["내장산국립공원", "내장사를 비롯한 아름다운 자연경관. 등산로와 절경"]
    ],
    "4519000000": [
        ["남원광한루원", "춘향전의 배경이 된 정자. 아름다운 정원과 연못"],
        ["지리산", "한국의 대표적인 명산. 천왕봉과 반야봉 등 높은 봉우리"]
    ],
    "4571000000": [
        ["순창장류박물관", "전통 장류문화를 소개하는 박물관. 순창은 전통 간장, 된장으로 유명"],
        ["순창메밀꽃축제", "메밀꽃이 피는 계절에 열리는 축제. 아름다운 풍경과 체험행사"]
    ],
    
    # 전라남도 하위 지역
    "4611000000": [
        ["목포해상케이블카", "바다 위를 건너는 케이블카. 유달산과 달동네를 연결"],
        ["목포근대역사관", "목포의 근대역사를 전시. 옛 일본식 건물을 리모델링"]
    ],
    "4613000000": [
        ["여수엑스포", "2012년 세계박람회 개최지. 빅오와 스카이타워 등이 유명"],
        ["오동도", "여수의 아름다운 섬. 동백나무와 해안절경으로 유명"]
    ],
    "4615000000": [
        ["순천만습지", "자연생태계가 잘 보존된 습지. 멸종위기종 서식지"],
        ["순천드라마촬영장", "드라마 촬영지로 사용된 장소. 다양한 세트장과 체험시설"]
    ],
    "4617000000": [
        ["보성녹차밭", "국내 최대 규모의 녹차 재배단지. 아름다운 계단식 밭 풍경"],
        ["대한다원", "보성의 대표적인 차밭. 녹차 체험과 시음 가능"]
    ],
    "4623000000": [
        ["해남대둔산", "호남의 소금산. 정상에서 바라보는 풍경이 장관"],
        ["코스모스공원", "가을이면 코스모스가 만발하는 공원. 아름다운 꽃길"]
    ],
    "4671000000": [
        ["담양메타세쿼이아길", "거대한 메타세쿼이아 나무길. 아름다운 숲길 산책로"],
        ["담양대나무밭", "대나무가 우거진 아름다운 풍경. 죽녹원이 유명"]
    ],
    "4672000000": [
        ["화순세량제", "화순의 대표적인 저수지. 아름다운 호수 풍경"],
        ["화순스파랜드", "온천과 워터파크가 결합된 복합휴양시설"]
    ],
    
    # 경상북도 하위 지역
    "4711000000": [
        ["경주불국사", "신라 시대의 대표적인 사찰. 석가탑과 다보탑(국보)이 유명"],
        ["경주월정교", "신라 시대의 다리를 재현. 야간 조명이 아름다운 명소"]
    ],
    "4713000000": [
        ["포항호미곶", "한반도 동쪽 끝. 해돋이 명소로 유명한 곳"],
        ["영일대해수욕장", "포항의 대표적인 해수욕장. 넓은 백사장과 얕은 수심"]
    ],
    "4715000000": [
        ["김천직지사", "세계 최초의 금속활자 직지심체요절을 간행한 사찰"],
        ["김천프로방스마을", "프랑스 프로방스 지방을 테마로 한 관광지"]
    ],
    "4717000000": [
        ["안동하회마을", "한국 전통마을. 세계문화유산으로 지정된 중요 문화재"],
        ["봉정사", "안동의 고찰. 국내 최고(最古)의 목조건물인 극락전(국보)이 있음"]
    ],
    "4719000000": [
        ["구미금오산", "경북의 명산. 높이 977m, 등산로와 자연경관이 뛰어남"],
        ["인동도장길", "인동의 아름다운 길. 벚꽃과 단풍이 유명한 산책로"]
    ],
    "4721000000": [
        ["영주부석사", "신라 시대의 사찰. 무량수전(국보)을 비롯한 문화재가 많음"],
        ["소백산", "한국의 명산. 높이 1,439m, 아름다운 자연경관"]
    ],
    "4723000000": [
        ["문경새재", "옛 남북을 연결하는 고개. 역사 박물관과 체험시설"],
        ["문경석탄박물관", "한국 광업의 역사를 보여주는 박물관. 지하 갱신 체험 가능"]
    ],
    "4725000000": [
        ["예천콘도미니엄", "예천의 대표적인 휴양시설. 자연 속에서 휴식하기 좋음"],
        ["예천금당실솔밭", "아름다운 소나무 숲. 휴양과 산책하기 좋은 장소"]
    ],
    "4728000000": [
        ["청도운문사", "청도군의 고찰. 운문산 자락에 위치한 아름다운 사찰"],
        ["청도반시축제", "청도 특산물 반시(감)를 주제로 한 축제. 다양한 체험행사"]
    ],
    
    # 경상남도 하위 지역
    "4812000000": [
        ["창원마산합포구", "역사적인 항구 도시. 다양한 문화유산과 근대건축물"],
        ["진해군항제", "지난 1952년 4월 13일, 우리나라 최초로 충무공 이순신 장군의 동상을 북원로터리에 세우고 추모제를 거행하여 온 것이 계기가 된 축제"]
    ],
    "4817000000": [
        ["진주성", "임진왜란 때 큰 전투가 있었던 성. 역사적 의미가 깊은 곳"],
        ["진주남강유등축제", "남강에 등불을 띄우는 축제. 아름다운 야간 경관"]
    ],
    "4822000000": [
        ["통영산림문화수련원", "통영의 자연학습장. 다양한 산림 체험 프로그램"],
        ["통영한산도", "이순신 장군의 한산도대첩이 있었던 섬. 역사적 의미"]
    ],
    "4824000000": [
        ["사천바다케이블카", "바다를 건너는 케이블카. 아름다운 해안 풍경"],
        ["사천공룡박물관", "공룡 화석과 모형을 전시하는 박물관. 체험시설"]
    ],
    "4825000000": [
        ["김해가야테마파크", "가야 문화를 테마로 한 공원. 역사 체험 시설"],
        ["김해수로왕릉", "가야 수로왕의 무덤. 김해의 대표적인 역사 유적"]
    ],
    "4827000000": [
        ["밀양영남루", "조선 시대의 대표적인 누각. 아름다운 강변 풍경"],
        ["밀양아리랑박물관", "밀양 아리랑을 주제로 한 박물관. 전통 음악 체험"]
    ],
    "4831000000": [
        ["거제바람의언덕", "거제도의 아름다운 전망대. 바다와 어우러진 풍경"],
        ["거제외도보타니아", "아름다운 정원이 있는 섬. 다양한 식물과 꽃길"]
    ],
    "4833000000": [
        ["남해상주해수욕장", "남해안의 대표적인 해수욕장. 맑은 물과 백사장"],
        ["남해독일마을", "독일풍의 건물과 문화를 체험할 수 있는 테마마을"]
    ],
    "4872000000": [
        ["함양상림공원", "함양군의 대표 공원. 아름다운 숲과 산책로"],
        ["함양메밀꽃축제", "메밀꽃이 피는 계절에 열리는 축제. 아름다운 풍경"]
    ],
    "4873000000": [
        ["거창월성계곡", "거창의 아름다운 계곡. 여름철 피서지로 인기"],
        ["거창대성동계곡", "깨끗한 물과 울창한 숲이 어우러진 계곡"]
    ],
    
    # 제주특별자치도 하위 지역
    "5011000000": [
        ["성산일출봉", "제주 동쪽의 상징적인 봉우리. 해돋이 명소"],
        ["섭지코지", "성산일출봉 근처의 아름다운 해안 절경"]
    ],
    "5013000000": [
        ["한라산", "제주의 상징. 높이 1,950m의 한국 최고봉"],
        ["협재해수욕장", "맑은 에메랄드빛 바다와 백사장으로 유명한 해수욕장"]
    ]
}
class TravelRecommendation:
    def __init__(self, root):
        self.root = root
        self.root.title("국내 여행지추천 파이썬코드")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # appKey 저장 변수
        self.appkey = ""
        
        # 현재 선택된 지역 정보
        self.current_code = None
        self.regions = []
        self.region_stack = []
        self.search_results = []
        self.is_search_mode = False
        
        # UI 초기화
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 상단 프레임 (appKey 입력)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(top_frame, text="API 접속 키:").pack(side=tk.LEFT)
        self.appkey_entry = ttk.Entry(top_frame, width=50)
        self.appkey_entry.pack(side=tk.LEFT, padx=5)
        
        self.connect_btn = ttk.Button(top_frame, text="연결", command=self.connect_api)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        # 검색 프레임
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="지역 검색:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_region())
        
        self.search_btn = ttk.Button(search_frame, text="검색", command=self.search_region)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_search_btn = ttk.Button(search_frame, text="검색 초기화", command=self.clear_search)
        self.clear_search_btn.pack(side=tk.LEFT, padx=5)
        self.clear_search_btn.config(state=tk.DISABLED)
        
        # 중간 프레임 (트리뷰와 상세 정보)
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        # 트리뷰 프레임 (지역 목록)
        tree_frame = ttk.Frame(middle_frame, width=250)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        self.tree = ttk.Treeview(tree_frame, columns=("code"), height=25)
        self.tree.heading("#0", text="지역명")
        self.tree.heading("code", text="코드")
        self.tree.column("code", width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 상세 정보 프레임
        detail_frame = ttk.Frame(middle_frame)
        detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 상세 정보 라벨
        self.detail_label = ttk.Label(detail_frame, text="상세 정보", font=('Arial', 10, 'bold'))
        self.detail_label.pack(anchor=tk.W)
        
        # 상세 정보 텍스트 박스
        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD, state=tk.DISABLED, padx=10, pady=10)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # 
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.back_btn = ttk.Button(bottom_frame, text="← 이전", command=self.go_back, state=tk.DISABLED)
        self.back_btn.pack(side=tk.LEFT, padx=5)
           
        # 상태바
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(bottom_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, expand=True, padx=5)
        
        # 초기 상태 설정
        self.load_top_regions()
        self.update_status("시/도를 선택해주세요.")
        
    def display_region_info(self, region_code, region_name, spots):
        """지역 정보와 관광지를 UI에 표시합니다."""
        detail_content = f"[{region_name}] 지역 정보\n\n"
        
        if spots:
            detail_content += "대표 관광지:\n"
            for i, spot in enumerate(spots, 1):
                name = spot[0] if isinstance(spot, list) and len(spot) > 0 else '이름 없음'
                desc = spot[1] if isinstance(spot, list) and len(spot) > 1 else '설명 없음'
                detail_content += f"{i}. {name}\n   - {desc}\n\n"
        else:
            detail_content += " 이 지역의 관광지 정보가 없습니다.\n"
            
        self.update_detail(detail_content)

    def connect_api(self):
        self.appkey = self.appkey_entry.get().strip()
        if not self.appkey:
            messagebox.showwarning("경고", "appKey를 입력해주세요.")
            return
        
        try:
            test_url = "https://apis.openapi.sk.com/puzzle/travel/meta/districts"
            headers = {'Accept': 'application/json', 'appkey': self.appkey}
            response = requests.get(test_url, headers=headers, params={'type': 'sig', 'offset': 0, 'limit': 1})
            response.raise_for_status()
            
            messagebox.showinfo("성공", "API에 성공적으로 연결되었습니다.")
            self.load_top_regions()
        except Exception as e:
            messagebox.showerror("오류", f"API 연결 실패: {str(e)}")
        
    def update_status(self, message):
        self.status_var.set(message)
        
    def load_top_regions(self):
        """최상위 지역(시/도)을 로드합니다."""
        self.is_search_mode = False
        self.clear_search_btn.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        
        for code, name in base_region_codes.items():
            self.tree.insert("", "end", text=name, values=(code))
        
        self.current_code = None
        self.regions = []
        self.region_stack = []
        self.back_btn.config(state=tk.DISABLED)
        self.update_detail("")
        self.update_status("시/도 목록이 로드되었습니다. 원하는 지역을 선택하세요.")
        
    def search_region(self):
        """지역을 검색합니다."""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("경고", "검색어를 입력해주세요.")
            return
            
        self.search_results = []
        for code, name in base_region_codes.items():
            if query in name:
                self.search_results.append((code, name))
        
        if not self.search_results:
            messagebox.showinfo("검색 결과", "일치하는 지역이 없습니다.")
            return
            
        self.is_search_mode = True
        self.clear_search_btn.config(state=tk.NORMAL)
        self.tree.delete(*self.tree.get_children())
        
        for code, name in self.search_results:
            self.tree.insert("", "end", text=name, values=(code))
            
        self.current_code = None
        self.regions = []
        self.region_stack = []
        self.back_btn.config(state=tk.DISABLED)
        self.update_detail("")
        self.update_status(f"'{query}'에 대한 검색 결과 {len(self.search_results)}건이 있습니다.")
        
    def clear_search(self):
        """검색 결과를 초기화하고 최상위 지역 목록으로 돌아갑니다."""
        self.search_entry.delete(0, tk.END)
        self.load_top_regions()
        
    def update_detail(self, content):
        """상세 정보 텍스트 박스를 업데이트합니다."""
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, content)
        self.detail_text.config(state=tk.DISABLED)
        
    def go_back(self):
        """이전 단계로 돌아갑니다."""
        if self.region_stack:
            self.current_code, self.regions = self.region_stack.pop()
            self.display_regions()
            
        if not self.region_stack:
            self.back_btn.config(state=tk.DISABLED)
            self.update_status("최상위 지역 목록입니다.")
        else:
            self.update_status(f"{base_region_codes.get(self.current_code[:2], '알 수 없는 지역')}의 하위 지역 목록입니다.")
        
    def display_regions(self):
        """지역 목록을 표시합니다."""
        self.tree.delete(*self.tree.get_children())
        
        if not self.current_code:
            # 최상위 지역 표시
            for code, name in base_region_codes.items():
                self.tree.insert("", "end", text=name, values=(code))
        else:
            # 하위 지역 표시
            for region in self.regions:
                code = region.get('districtCode', '')
                name = region.get('districtName', '이름 없음')
                self.tree.insert("", "end", text=name, values=(code))
                
            # 관광지 정보 표시
            spots = get_tourist_spots(self.current_code)
            region_name = base_region_codes.get(self.current_code[:2], '알 수 없는 지역')
            self.display_region_info(self.current_code, region_name, spots)
    
    def on_tree_select(self, event):
        """트리뷰에서 항목을 선택했을 때 호출됩니다."""
        selected_item = self.tree.focus()
        if not selected_item:
            return
            
        item_data = self.tree.item(selected_item)
        region_name = item_data["text"]
        region_code = item_data["values"][0]
        
        if self.is_search_mode:
            # 검색 모드에서는 선택 시 바로 관광지 정보 표시
            spots = get_tourist_spots(region_code)
            self.display_region_info(region_code, region_name, spots)
            self.update_status(f"'{region_name}'의 관광지 정보를 표시합니다.")
        else:
            # 일반 모드에서는 하위 지역 탐색
            if not self.current_code:
                # 최상위 지역 선택
                self.regions = get_region_hierarchy(self.appkey, region_code)
                if not self.regions:
                    messagebox.showerror("오류", "해당 지역 정보를 가져오지 못했습니다.")
                    return
                    
                self.region_stack.append((self.current_code, self.regions))
                self.current_code = region_code
                self.back_btn.config(state=tk.NORMAL)
                self.display_regions()
                self.update_status(f"{region_name}의 하위 지역 목록입니다.")
            else:
                # 하위 지역 선택 시 관광지 정보 표시
                spots = get_tourist_spots(region_code)
                self.display_region_info(region_code, region_name, spots)
                self.update_status(f"'{region_name}'의 관광지 정보를 표시합니다.")

def get_region_hierarchy(appkey, parent_code=None):
    """SK Open API로부터 지역 계층 구조를 가져옵니다."""
    base_url = "https://apis.openapi.sk.com/puzzle/travel/meta/districts"
    headers = {'Accept': 'application/json', 'appkey': appkey}
    
    try:
        params = {'type': 'sig', 'offset': 0, 'limit': 100}
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status', {}).get('code') == '00':
            contents = data.get('contents', [])
            if parent_code:
                return [item for item in contents if str(item.get('districtCode', '')).startswith(str(parent_code))]
            return contents
        return []
    except Exception as e:
        print(f"지역 정보 가져오기 오류: {str(e)}")       
    return []

def get_tourist_spots(region_code):
    """관광지 정보를 가져옵니다."""
    return tourist_spots.get(region_code, [])

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelRecommendation(root)
    app.tree.bind("<<TreeviewSelect>>", app.on_tree_select)
    root.mainloop()