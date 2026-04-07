"""
GitHub Actions에서 실행되는 로또 데이터 자동 업데이트 스크립트
매주 토요일 추첨 후 새 회차 데이터를 lotto_data.csv에 추가
"""
import requests
import pandas as pd
import os

API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"
DATA_FILE = "lotto_data.csv"


def fetch_round(round_no):
    try:
        resp = requests.get(
            API_URL.format(round_no),
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            timeout=15
        )
        data = resp.json()
        if data.get("returnValue") == "success":
            return {
                "회차": data["drwNo"],
                "번호1": data["drwtNo1"], "번호2": data["drwtNo2"],
                "번호3": data["drwtNo3"], "번호4": data["drwtNo4"],
                "번호5": data["drwtNo5"], "번호6": data["drwtNo6"],
                "보너스": data["bnusNo"],
                "1등당첨금": data.get("firstWinamnt", 0),
                "1등당첨자수": data.get("firstPrzwnerCo", 0),
            }
    except Exception as e:
        print(f"  오류: {e}")
    return None


def main():
    if not os.path.exists(DATA_FILE):
        print(f"오류: {DATA_FILE} 없음")
        return

    df = pd.read_csv(DATA_FILE)
    last_round = int(df["회차"].max())
    print(f"현재 최신 회차: {last_round}회")

    new_count = 0
    for next_round in range(last_round + 1, last_round + 20):
        print(f"  {next_round}회 확인 중...")
        row = fetch_round(next_round)
        if row is None:
            print(f"  {next_round}회 데이터 없음 → 종료")
            break
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        new_count += 1
        print(f"  {next_round}회 추가 완료!")

    if new_count > 0:
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
        print(f"\n총 {new_count}회차 추가. 최신: {int(df['회차'].max())}회")
    else:
        print("\n새로운 회차 없음.")


if __name__ == "__main__":
    main()
