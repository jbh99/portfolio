Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>>  # 5. 랜덤 추천
...     if destinations:
...         print("\n" + "=" * 50)
...         random_dest = random.choice(destinations)
...         print(f"🎲 무작위 추천 지역: {random_dest}")
...         print("=" * 50)
... 
... if __name__ == "__main__":
