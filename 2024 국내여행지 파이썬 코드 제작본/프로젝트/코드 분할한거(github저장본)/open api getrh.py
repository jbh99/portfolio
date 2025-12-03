Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import requests
# 초기 지역 코드 데이터 (시/도 단위)
base_region_codes = {
    "11": "서울특별시",
    "26": "부산광역시",
    "27": "대구광역시",
    "28": "인천광역시",
    "29": "광주광역시",
    "30": "대전광역시",
    "31": "울산광역시",
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
... def get_region_hierarchy(appkey, parent_code=None):
...     """SK Open API로부터 지역 계층 구조를 가져옵니다."""
...     base_url = "https://apis.openapi.sk.com/puzzle/travel/meta/districts"
...     headers = {'Accept': 'application/json', 'appkey': appkey}
...     
...     # 코드 길이에 따라 조회 타입 결정
...     if parent_code:
...         if len(parent_code) >= 8:
...             params = {'type': 'ri', 'offset': 0, 'limit': 100}  # 동/리 단위
...         else:
...             params = {'type': 'sig', 'offset': 0, 'limit': 100}  # 시군구 단위
...     else:
...         params = {'type': 'sig', 'offset': 0, 'limit': 100}  # 최초 시도 단위
...     
...     try:
...         response = requests.get(base_url, headers=headers, params=params)
...         response.raise_for_status()
...         data = response.json()
...         
...         if data['status']['code'] == '00':
...             if parent_code:
...                 return [item for item in data.get('contents', []) 
...                        if item['districtCode'].startswith(parent_code)]
...             return data.get('contents', [])
...         return []
...     except requests.exceptions.RequestException:
...         return []
