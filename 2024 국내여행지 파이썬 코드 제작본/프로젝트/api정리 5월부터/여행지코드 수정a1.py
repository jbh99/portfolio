Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import requests
import pandas as pd
import random
from collections import defaultdict

def get_travel_list(appkey, dongtype):
    """SK Open API에서 여행지 리스트 가져오기"""
    url = f"https://apis.openapi.sk.com/puzzle/travel?type={dongtype}"
    headers = {"accept": "application/json", "appkey": appkey}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        return pd.DataFrame(result['contents'])
    except Exception as e:
        print(f"API 호출 오류: {e}, 기본 데이터를 사용합니다.")
        return None

def load_default_destinations():
    """기본 여행지 데이터 로드 (API 실패시 사용)"""
    destinations = {
        "서울": {
            "budget": 3, "activity": 4, "culture": 5, "food": 5, "nature": 2,
            "desc": "한국의 수도로 현대적 도시와 전통문화가 공존하는 도시",
            "districtName": "서울특별시"
        },
        "부산": {
            "budget": 3, "activity": 4, "culture": 4, "food": 5, "nature": 3,
            "desc": "바다와 어우러진 활기찬 항구도시, 해운대와 광안리가 유명",
            "districtName": "부산광역시"
        },
        "제주도": {
            "budget": 4, "activity": 5, "culture": 3, "food": 4, "nature": 5,
            "desc": "아름다운 자연경관과 독특한 문화를 가진 섬",
            "districtName": "제주특별자치도"
        },
        "경주": {
            "budget": 3, "activity": 2, "culture": 5, "food": 4, "nature": 3,
            "desc": "신라 문화의 유적이 가득한 역사 도시",
            "districtName": "경상북도 경주시"
        },
        "전주": {
            "budget": 2, "activity": 3, "culture": 5, "food": 5, "nature": 2,
            "desc": "한옥마을과 맛있는 한식으로 유명한 도시",
            "districtName": "전라북도 전주시"
        },
        "강릉": {
            "budget": 3, "activity": 3, "culture": 4, "food": 4, "nature": 4,
            "desc": "동해안의 아름다운 해변과 커피거리가 있는 도시",
            "districtName": "강원도 강릉시"
        },
        "춘천": {
            "budget": 2, "activity": 4, "culture": 3, "food": 3, "nature": 4,
            "desc": "호수와 자연이 어우러진 레저 스포츠 천국",
            "districtName": "강원도 춘천시"
        },
        "여수": {
            "budget": 3, "activity": 3, "culture": 4, "food": 5, "nature": 4,
            "desc": "아름다운 해안선과 신선한 해산물이 풍부한 도시",
            "districtName": "전라남도 여수시"
        },
        "대구": {
            "budget": 2, "activity": 3, "culture": 4, "food": 5, "nature": 2,
            "desc": "맛있는 음식과 따뜻한 정서가 있는 대표적인 내륙도시",
            "districtName": "대구광역시"
        },
        "인천": {
            "budget": 3, "activity": 3, "culture": 4, "food": 4, "nature": 3,
            "desc": "국제적인 항구도시이자 차이나타운이 있는 도시",
            "districtName": "인천광역시"
        }
    }
    return pd.DataFrame.from_dict(destinations, orient='index')

def get_travel_data(appkey):
    """API 또는 기본 데이터로부터 여행지 정보 가져오기"""
    # 시/군 단위 여행지 가져오기 시도
    df_sig = get_travel_list(appkey, 'sig')
    
    # 리 단위 여행지 가져오기 시도
    df_ri = get_travel_list(appkey, 'ri')
    
    # API 실패시 기본 데이터 사용
    if df_sig is None or df_ri is None:
        print("API 호출에 실패하여 기본 여행지 데이터를 사용합니다.")
        return load_default_destinations()
    
    # API 성공시 데이터 병합
    df_combined = pd.concat([df_sig, df_ri], ignore_index=True)
    
    # API 데이터에 기본 평가 요소 추가 (임의값 부여)
    destinations = {}
    for _, row in df_combined.iterrows():
        name = row['districtName'].split()[-1]  # 지역명만 추출 (예: '서울특별시' -> '서울')
        if name.endswith('시') or name.endswith('군') or name.endswith('구'):
            name = name[:-1]
        
        destinations[name] = {
            "budget": random.randint(1, 5),  # 임의 예산 점수
            "activity": random.randint(1, 5),  # 임의 활동성 점수
            "culture": random.randint(1, 5),  # 임의 문화 점수
            "food": random.randint(1, 5),  # 임의 음식 점수
            "nature": random.randint(1, 5),  # 임의 자연 점수
            "desc": f"{name} 지역의 아름다운 여행지",
            "districtName": row['districtName']
        }
    
    return pd.DataFrame.from_dict(destinations, orient='index')
... 
... def travel_recommender(appkey):
...     """여행지 추천 메인 함수"""
...     print("🌟 국내 여행지 추천 프로그램 🌟")
...     print("=" * 50)
...     
...     # 여행지 데이터 로드
...     destinations_df = get_travel_data(appkey)
...     destinations = destinations_df.to_dict('index')
...     
...     # 사용자 선호도 조사
...     print("\n여행 스타일을 선택해주세요 (1-5):")
...     budget = int(input("예산 (1: 저예산 ~ 5: 고예산): "))
...     activity = int(input("활동성 (1: 휴식 ~ 5: 모험): "))
...     culture = int(input("문화/역사 관심도 (1: 낮음 ~ 5: 높음): "))
...     food = int(input("음식 관심도 (1: 낮음 ~ 5: 높음): "))
...     nature = int(input("자연 경관 관심도 (1: 낮음 ~ 5: 높음): "))
...     
...     # 선호도 점수 계산
...     recommendations = []
...     for dest, attrs in destinations.items():
...         score = 0
...         score += 5 - abs(budget - attrs["budget"])
...         score += 5 - abs(activity - attrs["activity"])
...         score += 5 - abs(culture - attrs["culture"])
...         score += 5 - abs(food - attrs["food"])
...         score += 5 - abs(nature - attrs["nature"])
...         recommendations.append((dest, score, attrs["desc"], attrs["districtName"]))
...     
...     # 상위 3개 추천
...     recommendations.sort(key=lambda x: x[1], reverse=True)
...     
...     print("\n" + "=" * 50)
...     print("🏆 당신을 위한 최고의 여행지 추천 🏆")
...     print("=" * 50)
...     
...     for i, (dest, score, desc, district) in enumerate(recommendations[:3], 1):
...         print(f"\n{i}위: {dest} (적합도: {score}/25)")
...         print(f"📍 위치: {district}")
        print(f"📌 {desc}")
    
    # 랜덤 추천 (재미 요소)
    random_rec = random.choice(list(destinations.items()))
    print("\n" + "=" * 50)
    print(f"🎲 오늘의 랜덤 추천: {random_rec[0]}")
    print(f"📍 위치: {random_rec[1]['districtName']}")
    print(f"📌 {random_rec[1]['desc']}")
    print("=" * 50)

if __name__ == "__main__":
    # 사용자 AppKey 입력 (없으면 빈 문자열로 두면 기본 데이터 사용)
    appkey = input("SK Open API AppKey를 입력하세요 (없으면 Enter 키를 누르세요): ").strip()
