import random

def travel_recommender():
    print("🌟 국내 여행지 추천 프로그램 🌟")
    print("=" * 50)
    
    # 사용자 선호도 조사
    print("\n여행 스타일을 선택해주세요 (1-5):")
    budget = int(input("예산 (1: 저예산 ~ 5: 고예산): "))
    activity = int(input("활동성 (1: 휴식 ~ 5: 모험): "))
    culture = int(input("문화/역사 관심도 (1: 낮음 ~ 5: 높음): "))
    food = int(input("음식 관심도 (1: 낮음 ~ 5: 높음): "))
       
    # 여행지 데이터베이스
    destinations = {
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
        },
        "강릉": {
            "budget": 3, "activity": 3, "culture": 4, "food": 4,
            "desc": "동해안의 아름다운 해변과 커피거리가 있는 도시"
        },
        "춘천": {
            "budget": 2, "activity": 4, "culture": 3, "food": 3,
            "desc": "호수와 자연이 어우러진 레저 스포츠 천국"
        },
        "여수": {
            "budget": 3, "activity": 3, "culture": 4, "food": 5,
            "desc": "아름다운 해안선과 신선한 해산물이 풍부한 도시"
        },
        "대구": {
            "budget": 2, "activity": 3, "culture": 4, "food": 5,
            "desc": "맛있는 음식과 따뜻한 정서가 있는 대표적인 내륙도시"
        },
        "인천": {
            "budget": 3, "activity": 3, "culture": 4, "food": 4,
            "desc": "국제적인 항구도시이자 차이나타운이 있는 도시"
        }
    }
    
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
    random_rec = random.choice(list(destinations.items()))
    print("\n" + "=" * 50)
    print(f"🎲 오늘의 랜덤 추천: {random_rec[0]}")
    print(f"📌 {random_rec[1]['desc']}")
    print("=" * 50)

if __name__ == "__main__":
    travel_recommender()