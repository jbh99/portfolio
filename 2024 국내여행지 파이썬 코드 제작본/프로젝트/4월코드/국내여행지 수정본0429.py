import random
import requests

def get_travel_destinations():
    """SK Open API에서 여행지 정보 가져오기"""
    url = "https://apis.openapi.sk.com/puzzle/travel/meta/districts?type=ri"
    headers = {
        'appkey': 'BpVxtzDwzsa4CSZDvpfZy9yXrU6uK99e6KZDjAcC'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
        
        data = response.json()
        return data.get('data', [])
    
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return []

def travel_recommender():
    print("🌟 국내 여행지 추천 프로그램 🌟")
    print("=" * 50)
    
    # API에서 여행지 데이터 가져오기
    api_destinations = get_travel_destinations()
    
    # 기본 여행지 데이터 (API가 실패할 경우를 대비해 기본 데이터 포함)
    default_destinations = {
        "서울": {
            "budget": 3, "activity": 4, "culture": 5, "food": 5,
            "desc": "한국의 수도로 현대적 도시와 전통문화가 공존하는 도시"
        },
        "부산": {
            "budget": 3, "activity": 4, "culture": 4, "food": 5,
            "desc": "바다와 어우러진 활기찬 항구도시, 해운대와 광안리가 유명"
        },
        "제주도": {
            "budget": 4, "activity": 5, "culture": 3, "food": 4,
            "desc": "아름다운 자연경관과 독특한 문화를 가진 섬"
        },
        "경주": {
            "budget": 3, "activity": 2, "culture": 5, "food": 4,
            "desc": "신라 문화의 유적이 가득한 역사 도시"
        },
        "전주": {
            "budget": 2, "activity": 3, "culture": 5, "food": 5,
            "desc": "한옥마을과 맛있는 한식으로 유명한 도시"
        }
    }
    
    # API에서 가져온 데이터가 있으면 병합
    destinations = default_destinations.copy()
    
    if api_destinations:
        for dest in api_destinations:
            name = dest.get('districtName', '')
            if name and name not in destinations:
                destinations[name] = {
                    "budget": random.randint(2, 4),
                    "activity": random.randint(2, 5),
                    "culture": random.randint(2, 5),
                    "food": random.randint(2, 5),
                    "desc": dest.get('description', '추가 정보 없음')
                }
    
    # 사용자 선호도 조사
    print("\n여행 스타일을 선택해주세요 (1-5):")
    
    def get_preference(prompt):
        while True:
            try:
                value = int(input(prompt))
                if 1 <= value <= 5:
                    return value
                print("1에서 5 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("숫자를 입력해주세요.")
    
    budget = get_preference("예산 (1: 저예산 ~ 5: 고예산): ")
    activity = get_preference("활동성 (1: 휴식 ~ 5: 모험): ")
    culture = get_preference("문화/역사 관심도 (1: 낮음 ~ 5: 높음): ")
    food = get_preference("음식 관심도 (1: 낮음 ~ 5: 높음): ")
    
    # 선호도 점수 계산
    recommendations = []
    for dest, attrs in destinations.items():
        score = 0
        score += 5 - abs(budget - attrs["budget"])
        score += 5 - abs(activity - attrs["activity"])
        score += 5 - abs(culture - attrs["culture"])
        score += 5 - abs(food - attrs["food"])
        recommendations.append((dest, score, attrs["desc"]))
    
    # 상위 3개 추천
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "=" * 50)
    print("🏆 당신을 위한 최고의 여행지 추천 🏆")
    print("=" * 50)
    
    for i, (dest, score, desc) in enumerate(recommendations[:3], 1):
        print(f"\n{i}위: {dest} (적합도: {score}/20)")
        print(f"📌 {desc}")
    
    # 랜덤 추천 (재미 요소)
    if destinations:
        random_dest, random_attrs = random.choice(list(destinations.items()))
        print("\n" + "=" * 50)
        print(f"🎲 오늘의 랜덤 추천: {random_dest}")
        print(f"📌 {random_attrs['desc']}")
        print("=" * 50)
    else:
        print("\n추천할 여행지 정보가 없습니다.")

if __name__ == "__main__":
    travel_recommender()