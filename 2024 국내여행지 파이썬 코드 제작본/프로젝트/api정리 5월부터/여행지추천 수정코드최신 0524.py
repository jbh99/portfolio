import requests
import random

# 초기 지역 코드 데이터 (시/도 단위)
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

# 경기도 하위 지역 관광지 정보
gyeonggi_tourism_info = {
    "4182000000": {  # 가평군
        "name": "가평군",
        "spots": [
            {
                "name": "쁘띠프랑스",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=eadf5f3e-81f9-4da8-9346-5eba291ae970",
                "desc": "프랑스의 정취를 느낄 수 있는 테마파크, 다양한 공연과 체험 프로그램 제공"
            },
            {
                "name": "자라섬",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=d6acd121-1077-4b20-94f7-512cc975b01c",
                "desc": "북한강에 위치한 아름다운 섬, 자라섬 국제재즈페스티벌로 유명"
            }
        ]
    },
    "4165000000": {  # 포천시
        "name": "포천시",
        "spots": [
            {
                "name": "포천 산정호수",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=fed74f79-c3f1-4e3b-86f3-244c82c25306",
                "desc": "아름다운 호수와 주변 산악 경관이 어우러진 관광지"
            },
            {
                "name": "국립수목원(광릉숲)",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=9c864d2b-3fae-4091-8960-0427e441385b",
                "desc": "한반도 식물자원 보존을 위한 연구기관이자 아름다운 수목원"
            }
        ]
    },
    "4180000000": {  # 연천군
        "name": "연천군",
        "spots": [
            {
                "name": "재인폭포 (한탄강 유네스코 세계지질공원)",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=88e97014-89a9-4cb2-82d6-71ca09319cbe",
                "desc": "유네스코 세계지질공원으로 지정된 한탄강의 아름다운 폭포"
            },
            {
                "name": "연천 호로고루",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=19c090e9-3a91-4bf7-9d3d-aa37eaaff273",
                "desc": "고구려 시대의 유적지로 역사적인 의미가 깊은 곳"
            }
        ]
    },
    "4150000000": {  # 이천시
        "name": "이천시",
        "spots": [
            {
                "name": "설봉공원",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=6ac1281a-cce8-4ae1-b1ee-ff27482a3466",
                "desc": "이천시의 대표적인 공원으로 다양한 문화시설이 있는 곳"
            },
            {
                "name": "덕평공룡수목원",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=52d663a5-064d-4222-adbc-b3104254384c",
                "desc": "공룡 테마의 수목원으로 아이들과 함께 가기 좋은 장소"
            }
        ]
    },
    "4146100000": {  # 용인시 처인구
        "name": "용인시 처인구",
        "spots": [
            {
                "name": "호암미술관",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=ddceb6ae-7a32-4838-b5d9-7f4d07c8a4c3",
                "desc": "아름다운 자연 속에 위치한 미술관으로 다양한 전시가 열리는 곳"
            },
            {
                "name": "에버랜드",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=7be6babf-e785-44da-9f4c-f7117f83ab23",
                "desc": "국내 최대 규모의 테마파크로 다양한 놀이기구와 동물원이 있는 곳"
            }
        ]
    },
    "4148000000": {  # 파주시
        "name": "파주시",
        "spots": [
            {
                "name": "헤이리 예술마을",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=82d9a397-b8c5-454e-bb71-dff610fb9bb9",
                "desc": "예술가들이 모여 사는 독특한 마을로 다양한 갤러리와 카페가 있는 곳"
            },
            {
                "name": "퍼스트가든",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=9290abf1-d7ca-4c1d-a4d1-352ec5693726",
                "desc": "유럽식 정원과 다양한 식물들을 볼 수 있는 대형 정원"
            }
        ]
    },
    "4161000000": {  # 광주시
        "name": "광주시",
        "spots": [
            {
                "name": "화담숲",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=d910e258-111d-43f1-8d29-80f4e80ca92a",
                "desc": "사계절 아름다운 경관을 자랑하는 대형 수목원"
            },
            {
                "name": "팔당물안개공원",
                "url": "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=a9b728ea-f910-40b9-8519-9c35957f9ea7",
                "desc": "아름다운 물안개로 유명한 공원으로 사진 찍기 좋은 장소"
            }
        ]
    }
}

def get_region_hierarchy(appkey, parent_code=None):
    """SK Open API로부터 지역 계층 구조를 가져옵니다."""
    base_url = "https://apis.openapi.sk.com/puzzle/travel/meta/districts"
    headers = {'Accept': 'application/json', 'appkey': appkey}
    
    # 코드 길이에 따라 조회 타입 결정
    if parent_code:
        if len(parent_code) >= 8:
            params = {'type': 'ri', 'offset': 0, 'limit': 100}  # 동/리 단위
        else:
            params = {'type': 'sig', 'offset': 0, 'limit': 100}  # 시군구 단위
    else:
        params = {'type': 'sig', 'offset': 0, 'limit': 100}  # 최초 시도 단위
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status']['code'] == '00':
            if parent_code:
                return [item for item in data.get('contents', []) 
                       if item['districtCode'].startswith(parent_code)]
            return data.get('contents', [])
        return []
    except requests.exceptions.RequestException:
        return []

def get_tourist_spots(appkey, region_code):
    """선택한 지역의 관광지 정보를 가져옵니다."""
    base_url = "https://apis.openapi.sk.com/puzzle/travel/places"
    headers = {'Accept': 'application/json', 'appkey': appkey}
    params = {'districtCode': region_code, 'offset': 0, 'limit': 5}  # 상위 5개만 가져옴
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status']['code'] == '00':
            return data.get('contents', [])
        return []
    except requests.exceptions.RequestException:
        return []

def display_region_info(region_code, region_name, spots):
    """지역 정보와 관광지를 표시합니다."""
    print("\n" + "=" * 50)
    print(f"🏆 [{region_name}] 지역 정보 🏆")
    print("=" * 50)
    
    # 경기도 하위 지역인 경우 추가 관광지 정보 표시
    if region_code[:2] == "41" and region_code in gyeonggi_tourism_info:
        extra_info = gyeonggi_tourism_info[region_code]
        print(f"\n📌 {extra_info['name']} 대표 관광지:")
        for spot in extra_info['spots']:
            print(f"- {spot['name']}: {spot['desc']}")
            print(f"  자세히 보기: {spot['url']}")
    
    # API에서 가져온 관광지 정보 표시
    if spots:
        print("\n🌟 API에서 제공하는 관광지:")
        for i, spot in enumerate(spots[:3], 1):  # 상위 3개만 출력
            print(f"{i}. {spot.get('name', '이름 없음')}")
            print(f"   - 주소: {spot.get('address', '주소 없음')}")
            print(f"   - 유형: {spot.get('placeType', '유형 없음')}")
            print(f"   - 설명: {spot.get('description', '설명 없음')[:50]}...")
    else:
        print("\n⚠️ 이 지역의 관광지 정보가 없습니다.")

def main():
    print("🌟 국내 여행지 추천 프로그램 🌟")
    print("=" * 50)
    
    # 1. appKey 입력
    appkey = input("발급 받은 appKey를 입력하세요: ")
    
    # 2. 지역 코드 계층적 탐색
    current_code = None
    regions = []
    region_stack = []  # 이전 단계를 저장하기 위한 스택
    
    while True:
        if not current_code:
            # 최상위 지역 선택
            print("\n[시/도 목록]")
            for code, name in base_region_codes.items():
                print(f"{code}: {name}")
            
            region_code = input("\n추천받을 지역 코드를 입력하세요 (2자리 시/도 코드, 종료: q): ").strip()
            
            if region_code.lower() == 'q':
                return
            if region_code not in base_region_codes:
                print("⚠️ 유효하지 않은 코드입니다. 다시 입력해주세요.")
                continue
            
            regions = get_region_hierarchy(appkey, region_code)
            if not regions:
                print("⚠️ 해당 지역 정보를 가져오지 못했습니다.")
                continue
            
            current_code = region_code
            region_name = base_region_codes[region_code]
            
            # 관광지 정보 가져오기
            spots = get_tourist_spots(appkey, current_code)
            display_region_info(current_code, region_name, spots)
            
            # 현재 상태 저장 (이전 단계로 돌아가기 위해)
            region_stack.append((current_code, regions))
        else:
            # 하위 지역 목록 표시
            print(f"\n[{base_region_codes.get(current_code[:2], '')} 하위 지역 목록]")
            print("~: 이전 단계로 돌아가기")
            print("q: 프로그램 종료")
            
            for i, region in enumerate(regions, 1):
                print(f"{region['districtCode']}: {region['districtName']}")
            
            next_code = input("\n상세 코드를 입력하세요 (전체 코드 입력 또는 Enter로 선택 완료): ").strip()
            
            if next_code.lower() == 'q':
                return
            elif next_code == '~':
                if region_stack:
                    current_code, regions = region_stack.pop()
                    continue
                else:
                    print("⚠️ 더 이상 이전으로 돌아갈 수 없습니다.")
                    continue
            elif not next_code:
                break
                
            # 입력된 코드가 유효한지 확인
            valid_code = False
            for region in regions:
                if region['districtCode'] == next_code:
                    valid_code = True
                    break
            
            if not valid_code:
                print("⚠️ 유효하지 않은 코드입니다. 다시 입력해주세요.")
                continue
                
            new_regions = get_region_hierarchy(appkey, next_code)
            if not new_regions:
                print("⚠️ 해당 지역 정보를 가져오지 못했습니다.")
                continue
            
            # 현재 상태 저장 (이전 단계로 돌아가기 위해)
            region_stack.append((current_code, regions))
            current_code = next_code
            regions = new_regions
            
            # 관광지 정보 가져오기
            spots = get_tourist_spots(appkey, current_code)
            display_region_info(current_code, next_code, spots)
    
    # 3. 최종 선택된 지역의 하위 지역 목록
    destinations = [f"{region['districtCode']}: {region['districtName']}" for region in regions]
    if not destinations:
        print("⚠️ 추천할 여행지가 없습니다.")
        return
    
    # 4. 결과 출력
    print("\n" + "=" * 50)
    print(f"🏆 [{base_region_codes.get(current_code[:2], '')} 지역 목록] 🏆")
    print("=" * 50)
    
    for i, dest in enumerate(destinations[:20], 1):  # 상위 20개만 출력
        print(f"{i}. {dest}")
    
    # 5. 랜덤 추천
    if destinations:
        print("\n" + "=" * 50)
        print("🎲 랜덤 여행지 추천 🎲")
        print("=" * 50)
        random_dest = random.choice(destinations)
        print(f"\n추천 여행지: {random_dest}")
        
        # 경기도 하위 지역인 경우 추가 정보 표시
        if current_code[:2] == "41" and random_dest.split(":")[0] in gyeonggi_tourism_info:
            dest_code = random_dest.split(":")[0]
            extra_info = gyeonggi_tourism_info[dest_code]
            print(f"\n📌 {extra_info['name']} 대표 관광지:")
            for spot in extra_info['spots']:
                print(f"- {spot['name']}: {spot['desc']}")
                print(f"  자세히 보기: {spot['url']}")

if __name__ == "__main__":
    main()