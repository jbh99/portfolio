Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
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
...             
...             regions = get_region_hierarchy(appkey, region_code)
...             if not regions:
...                 print("⚠️ 해당 지역 정보를 가져오지 못했습니다.")
...                 return
...             
...             current_code = region_code
...             region_name = base_region_codes[region_code]
...         else:
...             # 하위 지역 목록 표시
...             print(f"\n[{base_region_codes.get(current_code[:2], '')} 하위 지역 목록]")
...             for i, region in enumerate(regions, 1):
...                 print(f"{region['districtCode']}: {region['districtName']}")
...             
...             next_code = input("\n상세 코드를 입력하세요 (전체 코드 입력 또는 Enter로 선택 완료): ").strip()
...             if not next_code:
...                 break
...                 
...             regions = get_region_hierarchy(appkey, next_code)
...             if not regions:
...                 print("⚠️ 해당 지역 정보를 가져오지 못했습니다.")
...                 return
...             current_code = next_code
...     
...     # 3. 최종 선택된 지역의 하위 지역 목록
...     destinations = [f"{region['districtCode']}: {region['districtName']}" for region in regions]
...     if not destinations:
...         print("⚠️ 추천할 여행지가 없습니다.")
...         return
...     
...     # 4. 결과 출력
...     print("\n" + "=" * 50)
...     print(f"🏆 [{base_region_codes.get(current_code[:2], '')} 지역 목록 🏆")
...     print("=" * 50)
...     
...     for i, dest in enumerate(destinations[:20], 1):  # 상위 20개만 출력
