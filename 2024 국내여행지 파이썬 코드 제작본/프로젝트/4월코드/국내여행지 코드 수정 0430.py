Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> KeyboardInterrupt
>>> import requests
... import random
... 
... # 행정표준코드 (시/도 단위)
... region_codes = {
...     "11": "서울특별시",
...     "26": "부산광역시",
...     "27": "대구광역시",
...     "28": "인천광역시",
...     "29": "광주광역시",
...     "30": "대전광역시",
...     "31": "울산광역시",
...     "36": "세종특별자치시",
...     "41": "경기도",
...     "42": "강원도",
...     "43": "충청북도",
...     "44": "충청남도",
...     "45": "전라북도",
...     "46": "전라남도",
...     "47": "경상북도",
...     "48": "경상남도",
...     "50": "제주특별자치도"
... }
... 
... def get_travel_recommendations(region_code, appkey):
...     """SK Open API로부터 여행지 목록을 가져옵니다."""
...     base_url = "https://apis.openapi.sk.com/puzzle/travel/meta/districts"
...     headers = {'Accept': 'application/json', 'appkey': appkey}
...     params = {'type': 'sig', 'offset': 0, 'limit': 20}  # 시/군/구 단위로 20개 조회
...     
...     try:
...         response = requests.get(base_url, headers=headers, params=params)
...         response.raise_for_status()
...         data = response.json()
...         
...         if data['status']['code'] == '00':
            return [item['districtName'] for item in data.get('contents', []) 
                   if item['districtCode'].startswith(region_code)]
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def calculate_score(destination, preferences):
    """선호도에 따른 여행지 점수 계산 (예시 로직)"""
    # 각 여행지의 특성 (임의 설정)
    destination_attrs = {
        "서울특별시": {"budget": 3, "activity": 4, "culture": 5, "food": 5},
        "부산광역시": {"budget": 3, "activity": 4, "culture": 4, "food": 5},
        "제주특별자치도": {"budget": 4, "activity": 5, "culture": 3, "food": 4},
        # ... 다른 지역 추가 가능
    }
    
    # 기본값 (없는 지역은 평균값 적용)
    attrs = destination_attrs.get(destination, {"budget": 3, "activity": 3, "culture": 3, "food": 3})
    
    # 점수 계산 (5점 만점 차이 감점)
    score = 0
    for key in ['budget', 'activity', 'culture', 'food']:
        score += 5 - abs(preferences[key] - attrs[key])
    return score

def main():
    print("🌟 국내 여행지 추천 프로그램 🌟")
    print("=" * 50)
    
    # 1. 사용자 선호도 입력
    print("\n[여행 스타일 설문] (1-5점)")
    preferences = {
        'budget': int(input("예산 (1: 저예산 ~ 5: 고예산): ")),
        'activity': int(input("활동성 (1: 휴식 ~ 5: 모험): ")),
        'culture': int(input("문화/역사 관심도 (1: 낮음 ~ 5: 높음): ")),
        'food': int(input("음식 관심도 (1: 낮음 ~ 5: 높음): "))
    }
    
    # 2. SK Open API 연결
    appkey = input("\n발급 받은 appKey를 입력하세요: ")
    print("\n[지역 목록]")
    for code, name in region_codes.items():
        print(f"{code}: {name}")
    region_code = input("\n추천받을 지역 코드를 입력하세요 (예: 11, 50): ")
    
    if region_code not in region_codes:
        print("⚠️ 유효하지 않은 코드입니다.")
        return
    
    # 3. API에서 여행지 목록 가져오기
    destinations = get_travel_recommendations(region_code, appkey)
    if not destinations:
        print("⚠️ 해당 지역의 여행지 정보를 가져오지 못했습니다.")
        return
    
    # 4. 선호도 기반 점수 계산
    scored_destinations = []
    for dest in destinations:
        score = calculate_score(dest, preferences)
        scored_destinations.append((dest, score))
    
    # 5. 결과 정렬 및 출력
    scored_destinations.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "=" * 50)
    print(f"🏆 [{region_codes[region_code]}] 여행지 추천 🏆")
    print("=" * 50)
    for i, (dest, score) in enumerate(scored_destinations[:5], 1):  # 상위 5개
        print(f"\n{i}위: {dest} (적합도: {score}/20)")
    
    # 6. 랜덤 추천 (재미 요소)
    print("\n" + "=" * 50)
    print(f"🎲 오늘의 숨은 명소: {random.choice(destinations)}")
    print("=" * 50)

if __name__ == "__main__":
