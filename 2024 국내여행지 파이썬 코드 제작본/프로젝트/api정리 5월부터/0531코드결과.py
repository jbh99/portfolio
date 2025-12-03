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

# 하드코딩된 관광지 정보 (경기도)
gyeonggi_spots = {
    "4182000000": "🌟 대표 관광지:\n   - 쁘디프랑스\n   - 자라섬",
    "4165000000": "🌟 대표 관광지:\n   - 포천 산정호수\n   - 국립수목원(광릉숲)",
    "4180000000": "🌟 대표 관광지:\n   - 재인폭포 (한탄강 유네스코 세계지질공원)\n   - 연천 호로고루",
    "4150000000": "🌟 대표 관광지:\n   - 설봉공원\n   - 덕평공룡수목원",
    "4146100000": "🌟 대표 관광지:\n   - 호암미술관\n   - 에버랜드",
    "4148000000": "🌟 대표 관광지:\n   - 헤이리 예술마을\n   - 퍼스트가든",
    "4161000000": "🌟 대표 관광지:\n   - 화담숲\n   - 팔당물안개공원"
}

# 하드코딩된 관광지 정보 (부산)
busan_spots = {
    "2617000000": "🌟 대표 관광지:\n   - 부잔 진시장\n   - 부산 자유도매시장",
    "2644000000": "🌟 대표 관광지:\n   - 맥도생태공원\n   - 신호공원",
    "2671000000": "🌟 대표 관광지:\n   - 아홉산숲\n   - 국립부산과학관",
    "2638000000": "🌟 대표 관광지:\n   - 부산현대미술관\n   - 다대포 꿈의 낙조분수",
    "2614000000": "🌟 대표 관광지:\n   - 송도해수욕장\n   - 송도 구름산책로",
    "2623000000": "🌟 대표 관광지:\n   - 부산어린이대공원\n   - 선암사",
    "2620000000": "🌟 대표 관광지:\n   - 국립해양박물관\n   - 흰여울문화마을",
    "2650000000": "🌟 대표 관광지:\n   - F1963\n   - 광안리해수욕장"
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
    # 경기도 하위 지역인 경우 하드코딩된 데이터 사용
    if region_code in gyeonggi_spots:
        return [{"name": spot.split(":")[0].strip(), "description": spot.split(":")[1].strip()} 
                for spot in gyeonggi_spots[region_code].split("\n")[1:]]
    
    # 부산 하위 지역인 경우 하드코딩된 데이터 사용
    if region_code in busan_spots:
        return [{"name": spot.split(":")[0].strip(), "description": spot.split(":")[1].strip()} 
                for spot in busan_spots[region_code].split("\n")[1:]]
    
    # 그 외 지역은 API 호출
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
    
    if spots:
        print("\n🌟 대표 관광지:")
        for i, spot in enumerate(spots[:3], 1):  # 상위 3개만 출력
            print(f"{i}. {spot.get('name', '이름 없음')}")
            if 'description' in spot:
                print(f"   - {spot['description']}")
            else:
                print(f"   - 설명: {spot.get('description', '설명 없음')[:50]}...")
    else:
        print("\n⚠️ 이 지역의 관광지 정보가 없습니다.")

def display_subregions_with_spots(appkey, regions, parent_name):
    """하위 지역 목록과 관광지를 함께 표시합니다."""
    print("\n" + "=" * 50)
    print(f"🏆 [{parent_name}] 하위 지역 목록 🏆")
    print("=" * 50)
    
    for region in regions:
        region_code = region['districtCode']
        region_name = region['districtName']
        
        # 관광지 정보 가져오기
        spots = get_tourist_spots(appkey, region_code)
        
        print(f"\n📍 {region_code}: {region_name}")
        if spots:
            print("   🌟 대표 관광지:")
            for spot in spots[:3]:  # 상위 3개만 출력
                print(f"      - {spot.get('name', '이름 없음')}")
        else:
            print("   ⚠️ 관광지 정보가 없습니다")

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
            
            # 경기도(41) 또는 부산(26)인 경우 하위 지역과 관광지 함께 출력
            if region_code in ["41", "26"]:
                display_subregions_with_spots(appkey, regions, region_name)
            else:
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
                print(f"{i}. {region['districtCode']}: {region['districtName']}")
            
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
    print(f"🏆 [{base_region_codes.get(current_code[:2], '')} 지역 목록 🏆")
    print("=" * 50)
    
    for i, dest in enumerate(destinations[:20], 1):  # 상위 20개만 출력
        print(f"{i}. {dest}")
    
    # 5. 랜덤 추천
    if destinations:
        print("\n" + "=" * 50)
        random_dest = random.choice(destinations)
        print(f"🎲 무작위 추천 지역: {random_dest}")
            
if __name__ == "__main__":
    main()