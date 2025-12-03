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

def main():
    print("🌟 국내 여행지 추천 프로그램 🌟")
    print("=" * 50)
    
    # 1. appKey 입력
    appkey = input("발급 받은 appKey를 입력하세요: ")
    
    # 2. 지역 코드 계층적 탐색
    current_code = None
    regions = []
    while True:
        if not current_code:
            # 최상위 지역 선택
            print("\n[시/도 목록]")
            for code, name in base_region_codes.items():
                print(f"{code}: {name}")
            
            region_code = input("\n추천받을 지역 코드를 입력하세요 (2자리 시/도 코드): ")[:2]
            if region_code not in base_region_codes:
                print("⚠️ 유효하지 않은 코드입니다.")
                continue
            
            regions = get_region_hierarchy(appkey, region_code)
            if not regions:
                print("⚠️ 해당 지역 정보를 가져오지 못했습니다.")
                return
            
            current_code = region_code
            region_name = base_region_codes[region_code]
        else:
            # 하위 지역 목록 표시
            print(f"\n[{base_region_codes.get(current_code[:2], '')} 하위 지역 목록]")
            for i, region in enumerate(regions, 1):
                print(f"{region['districtCode']}: {region['districtName']}")
            
            next_code = input("\n상세 코드를 입력하세요 (전체 코드 입력 또는 Enter로 선택 완료): ").strip()
            if not next_code:
                break
                
            regions = get_region_hierarchy(appkey, next_code)
            if not regions:
                print("⚠️ 해당 지역 정보를 가져오지 못했습니다.")
                return
            current_code = next_code
    
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
        print("=" * 50)

if __name__ == "__main__":
    main()