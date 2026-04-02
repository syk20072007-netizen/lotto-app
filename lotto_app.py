"""
떼교수님의 행운 교실 - 로또 분석 대시보드
칠판 감성 + 토스 UX 테마
"""

import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="떼교수님의 행운 교실",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════
# 🎨 칠판 + 토스 테마 CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

* { font-family: 'Noto Sans KR', sans-serif; }

/* ── 배경: 칠판 다크 그린 ── */
.stApp { background-color: #1a2e1a; }
section[data-testid="stSidebar"] { background-color: #142314 !important; }
section[data-testid="stSidebar"] * { color: #d4e8c2 !important; }

/* ── 기본 텍스트 밝게 ── */
.stApp, .stMarkdown, p, span, label { color: #e8f0e8; }

/* ── 로또 번호 공 ── */
.ball {
    display: inline-flex; align-items: center; justify-content: center;
    width: 54px; height: 54px; border-radius: 50%;
    color: #fff; font-weight: 800; font-size: 19px; margin: 4px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
    box-shadow: 0 4px 10px rgba(0,0,0,0.4), inset 0 -3px 6px rgba(0,0,0,0.2);
}
.ball-y { background: radial-gradient(circle at 35% 35%, #ffe066, #e6a800); }
.ball-b { background: radial-gradient(circle at 35% 35%, #74b9ff, #0984e3); }
.ball-r { background: radial-gradient(circle at 35% 35%, #ff7675, #d63031); }
.ball-g { background: radial-gradient(circle at 35% 35%, #a8d8a8, #27ae60); }
.ball-k { background: radial-gradient(circle at 35% 35%, #b2bec3, #636e72); }
.ball-bonus { background: radial-gradient(circle at 35% 35%, #c39bd3, #8e44ad); border: 2px dashed #fff; }
.ball-sm {
    display: inline-flex; align-items: center; justify-content: center;
    width: 38px; height: 38px; border-radius: 50%;
    color: #fff; font-weight: 700; font-size: 13px; margin: 2px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}

/* ── 칠판 카드 ── */
.chalk-card {
    background: rgba(255,255,255,0.05);
    border: 1.5px solid rgba(255,255,255,0.15);
    border-radius: 20px; padding: 24px; margin: 10px 0;
    backdrop-filter: blur(4px);
}
.chalk-card-highlight {
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(163,224,163,0.4);
    border-radius: 20px; padding: 24px; margin: 10px 0;
    box-shadow: 0 0 20px rgba(100,200,100,0.1);
}

/* ── 교수님 말풍선 ── */
.bubble {
    background: rgba(255,255,255,0.1);
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 16px 16px 16px 4px;
    padding: 14px 18px; margin: 8px 0 16px 0;
    font-size: 14px; color: #d4e8c2; line-height: 1.7;
    position: relative;
}
.bubble::before {
    content: "🎓 떼교수님";
    display: block; font-size: 12px; font-weight: 700;
    color: #a3e0a3; margin-bottom: 6px;
}

/* ── 강의노트 스타일 ── */
.lecture-note {
    background: rgba(255,230,102,0.08);
    border-left: 4px solid #ffe066;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px; margin: 10px 0;
    font-size: 13px; color: #ffe066;
}

/* ── 토스 스타일 큰 숫자 카드 ── */
.big-stat {
    background: rgba(255,255,255,0.07);
    border-radius: 16px; padding: 20px;
    text-align: center; border: 1px solid rgba(255,255,255,0.12);
}
.big-stat .label { font-size: 13px; color: #a3b8a3; margin-bottom: 6px; }
.big-stat .value { font-size: 32px; font-weight: 800; color: #a3e0a3; }
.big-stat .sub { font-size: 12px; color: #7a9a7a; margin-top: 4px; }

/* ── 추천 메인 카드 ── */
.rec-card {
    background: linear-gradient(135deg, rgba(40,80,40,0.6), rgba(20,50,20,0.8));
    border: 1.5px solid rgba(163,224,163,0.3);
    border-radius: 20px; padding: 22px 28px; margin: 10px 0;
    text-align: center;
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
.rec-card:hover { transform: translateY(-2px); }
.rec-card .tag {
    display: inline-block; background: rgba(163,224,163,0.2);
    color: #a3e0a3; font-size: 12px; font-weight: 700;
    padding: 3px 10px; border-radius: 20px; margin-bottom: 12px;
    border: 1px solid rgba(163,224,163,0.3);
}
.rec-card .stats {
    font-size: 12px; color: #7a9a7a; margin-top: 12px;
}

/* ── 쌍 카드 ── */
.pair-card {
    background: rgba(255,255,255,0.05);
    border-radius: 14px; padding: 14px 18px; margin: 6px 0;
    display: flex; align-items: center; justify-content: space-between;
    border: 1px solid rgba(255,255,255,0.08);
}
.pair-rank { font-size: 18px; font-weight: 800; color: #ffe066; width: 36px; }
.pair-count {
    font-size: 13px; background: rgba(163,224,163,0.15);
    color: #a3e0a3; padding: 3px 10px; border-radius: 20px;
    font-weight: 700;
}

/* ── 요약 배너 ── */
.summary-banner {
    background: linear-gradient(135deg, rgba(163,224,163,0.15), rgba(100,180,100,0.1));
    border: 2px solid rgba(163,224,163,0.4);
    border-radius: 20px; padding: 24px; margin: 16px 0;
    text-align: center;
}
.summary-banner .win-rate {
    font-size: 52px; font-weight: 900; color: #a3e0a3;
    line-height: 1;
}
.summary-banner .win-label { font-size: 14px; color: #7a9a7a; margin-top: 6px; }
.summary-banner .win-detail { font-size: 16px; color: #d4e8c2; margin-top: 10px; }

/* ── 등수 결과 카드 ── */
.rank-card {
    border-radius: 16px; padding: 18px 10px;
    text-align: center; border: 1px solid rgba(255,255,255,0.1);
}
.rank-card .rank-label { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
.rank-card .rank-val { font-size: 28px; font-weight: 900; }
.rank-card .rank-sub { font-size: 11px; color: #7a9a7a; margin-top: 4px; }

/* ── Hot/Cold 번호 박스 ── */
.hc-box {
    border-radius: 16px; padding: 18px; text-align: center;
}
.hc-hot { background: rgba(255,100,100,0.1); border: 1.5px solid rgba(255,100,100,0.3); }
.hc-warm { background: rgba(255,230,100,0.08); border: 1.5px solid rgba(255,230,100,0.2); }
.hc-cold { background: rgba(100,180,255,0.1); border: 1.5px solid rgba(100,180,255,0.3); }
.hc-title { font-size: 15px; font-weight: 800; margin-bottom: 12px; }

/* ── 탭 스타일 ── */
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #7a9a7a !important; border-radius: 8px 8px 0 0;
}
.stTabs [aria-selected="true"] {
    background: rgba(163,224,163,0.15) !important;
    color: #a3e0a3 !important;
}

/* ── 버튼 ── */
.stButton button {
    background: linear-gradient(135deg, #2d6e2d, #1a4a1a) !important;
    color: #a3e0a3 !important; border: 1.5px solid #a3e0a3 !important;
    border-radius: 14px !important; font-weight: 700 !important;
    padding: 10px 24px !important; font-size: 15px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #3a8a3a, #2d6e2d) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(100,200,100,0.3) !important;
}

/* ── 슬라이더 ── */
.stSlider [data-baseweb="slider"] { color: #a3e0a3; }

/* ── 모바일 ── */
@media (max-width: 768px) {
    .ball { width: 40px; height: 40px; font-size: 15px; }
    .ball-sm { width: 30px; height: 30px; font-size: 11px; }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# 📊 데이터 & 업데이트
# ══════════════════════════════════════════════════════════
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lotto_data.csv")
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"


def fetch_round(round_no):
    import requests
    try:
        resp = requests.get(API_URL.format(round_no),
                            headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
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
    except Exception:
        pass
    return None


def auto_update():
    if not os.path.exists(DATA_FILE):
        return 0, 0
    df = pd.read_csv(DATA_FILE)
    last_round = int(df["회차"].max())
    new_count = 0
    for next_round in range(last_round + 1, last_round + 11):
        row = fetch_round(next_round)
        if row is None:
            break
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        new_count += 1
    if new_count > 0:
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    return last_round, new_count


@st.cache_data(ttl=3600)
def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    df = pd.read_csv(DATA_FILE)
    df["번호목록"] = df.apply(
        lambda r: sorted([int(r["번호1"]), int(r["번호2"]), int(r["번호3"]),
                          int(r["번호4"]), int(r["번호5"]), int(r["번호6"])]), axis=1)
    df["회차"] = df["회차"].astype(int)
    df["보너스"] = df["보너스"].astype(int)
    return df.sort_values("회차").reset_index(drop=True)


# ══════════════════════════════════════════════════════════
# 🎱 번호 공 렌더링
# ══════════════════════════════════════════════════════════
def ball_class(n):
    if 1 <= n <= 10:  return "ball-y"
    elif 11 <= n <= 20: return "ball-b"
    elif 21 <= n <= 30: return "ball-r"
    elif 31 <= n <= 40: return "ball-k"
    else:               return "ball-g"


def balls_html(numbers, bonus=None, size="normal"):
    cls = "ball-sm" if size == "sm" else "ball"
    html = ""
    for n in numbers:
        html += f'<span class="{cls} {ball_class(n)}">{n}</span>'
    if bonus is not None:
        html += f' <span style="color:#b2bec3;font-size:18px;vertical-align:middle">＋</span>'
        html += f'<span class="{cls} ball-bonus">{bonus}</span>'
    return html


# ══════════════════════════════════════════════════════════
# 🧮 분석 엔진
# ══════════════════════════════════════════════════════════
class LottoAnalyzer:
    def __init__(self, df):
        self.df = df
        self.all_numbers = [n for nums in df["번호목록"] for n in nums]

    def get_frequency(self):
        freq = Counter(self.all_numbers)
        return {i: freq.get(i, 0) for i in range(1, 46)}

    def get_recent_frequency(self, recent_n=50):
        recent_nums = [n for nums in self.df.tail(recent_n)["번호목록"] for n in nums]
        freq = Counter(recent_nums)
        return {i: freq.get(i, 0) for i in range(1, 46)}

    def get_hot_cold(self, recent_n=50):
        recent_freq = self.get_recent_frequency(recent_n)
        sorted_nums = sorted(range(1, 46), key=lambda x: recent_freq[x], reverse=True)
        return sorted_nums[:15], sorted_nums[15:30], sorted_nums[30:]

    def get_number_gaps(self):
        max_round = self.df["회차"].max()
        gaps = {}
        for num in range(1, 46):
            appeared = self.df[self.df.apply(lambda r: num in r["번호목록"], axis=1)]["회차"]
            gaps[num] = int(max_round - appeared.max()) if len(appeared) > 0 else int(max_round)
        return gaps

    def calculate_weights(self, hot_w=0.4, cold_w=0.3, base_w=0.3):
        rf = self.get_recent_frequency(50)
        tf = self.get_frequency()
        gp = self.get_number_gaps()
        max_rf = max(rf.values()) or 1
        max_gp = max(gp.values()) or 1
        max_tf = max(tf.values()) or 1
        return {n: hot_w*(rf[n]/max_rf) + cold_w*(gp[n]/max_gp) + base_w*(tf[n]/max_tf)
                for n in range(1, 46)}

    def structural_filter(self, numbers):
        total = sum(numbers)
        if not (100 <= total <= 170): return False
        odd = sum(1 for n in numbers if n % 2 == 1)
        if odd < 2 or odd > 4: return False
        s = sorted(numbers)
        for i in range(len(s)-2):
            if s[i+1] == s[i]+1 and s[i+2] == s[i]+2: return False
        if max(Counter([n//10 for n in numbers]).values()) >= 3: return False
        return True

    def generate_numbers(self, n_sets=5, strategy="balanced"):
        hw = {"balanced":0.4,"hot_focused":0.5,"cold_focused":0.3,"expected_value":0.2}
        cw = {"balanced":0.3,"hot_focused":0.2,"cold_focused":0.5,"expected_value":0.2}
        bw = {"balanced":0.3,"hot_focused":0.3,"cold_focused":0.2,"expected_value":0.6}
        weights = self.calculate_weights(hw[strategy], cw[strategy], bw[strategy])
        if strategy == "expected_value":
            for n in range(1, 46):
                if n <= 12:  weights[n] *= 0.7
                if n <= 31:  weights[n] *= 0.85
                if n in [3,7,13,21]: weights[n] *= 0.75
        nums = list(range(1, 46))
        results, attempts = [], 0
        while len(results) < n_sets and attempts < 10000:
            attempts += 1
            w = [weights[n] for n in nums]
            ws = sum(w)
            probs = [wi/ws for wi in w]
            chosen = sorted(list(np.random.choice(nums, 6, replace=False, p=probs)))
            if self.structural_filter(chosen) and chosen not in results:
                results.append(chosen)
        return results

    def simulate_past(self, my_numbers):
        results = {"1등":0,"2등":0,"3등":0,"4등":0,"5등":0,"낙첨":0}
        my_set = set(my_numbers)
        for _, row in self.df.iterrows():
            m = len(my_set & set(row["번호목록"]))
            b = row["보너스"]
            if   m == 6:                    results["1등"] += 1
            elif m == 5 and b in my_set:    results["2등"] += 1
            elif m == 5:                    results["3등"] += 1
            elif m == 4:                    results["4등"] += 1
            elif m == 3:                    results["5등"] += 1
            else:                           results["낙첨"] += 1
        return results

    def get_pair_frequency(self, top_n=15):
        pair_count = Counter()
        for nums in self.df["번호목록"]:
            for pair in combinations(nums, 2):
                pair_count[pair] += 1
        return pair_count.most_common(top_n)

    def get_decade_distribution(self):
        d = {"1~10":0,"11~20":0,"21~30":0,"31~40":0,"41~45":0}
        for n in self.all_numbers:
            if n<=10: d["1~10"]+=1
            elif n<=20: d["11~20"]+=1
            elif n<=30: d["21~30"]+=1
            elif n<=40: d["31~40"]+=1
            else: d["41~45"]+=1
        return d

    def get_sum_distribution(self):
        return [sum(nums) for nums in self.df["번호목록"]]

    def get_odd_even_distribution(self):
        dist = Counter()
        for nums in self.df["번호목록"]:
            odd = sum(1 for n in nums if n%2==1)
            dist[f"홀{odd} 짝{6-odd}"] += 1
        return dict(dist)


# ══════════════════════════════════════════════════════════
# 🖥️ 메인 앱
# ══════════════════════════════════════════════════════════
def main():
    # 자동 업데이트
    if "update_checked" not in st.session_state:
        try:
            last, cnt = auto_update()
            st.session_state["update_checked"] = True
            if cnt > 0:
                st.toast(f"🎉 새 회차 {cnt}개 추가됐어요! ({last+1}~{last+cnt}회)", icon="✅")
                st.cache_data.clear()
        except Exception:
            st.session_state["update_checked"] = True

    df = load_data()
    if df is None:
        st.error("⚠️ lotto_data.csv 파일이 없어요. lotto_crawler.py를 먼저 실행해주세요.")
        return

    analyzer = LottoAnalyzer(df)

    # ── 사이드바 ──
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:16px 0 10px;">
            <div style="font-size:22px;font-weight:900;color:#a3e0a3;letter-spacing:1px;">떼랩 Tte-Lab</div>
            <div style="font-size:13px;color:#7a9a7a;margin-top:2px;">🎓 떼교수님의 로또 연구소</div>
            <div style="font-size:11px;color:#4d6e4d;margin-top:2px;">데이터로 찾는 오늘의 행운</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        menu = st.radio("", [
            "✏️ 이번 주 행운 탐구",
            "📊 데이터 패턴 분석",
            "🎯 나만의 숫자 조합실",
            "📝 과거 당첨 데이터 연구",
            "📈 최신 당첨 추세 전망",
        ], label_visibility="collapsed")

        st.markdown("---")
        last_r = int(df['회차'].max())
        st.markdown(f"""
        <div style="font-size:12px;color:#7a9a7a;line-height:2;">
        📅 최신 회차: <b style="color:#a3e0a3">{last_r}회</b><br>
        📊 분석 데이터: <b style="color:#a3e0a3">{len(df)}회차</b>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 새 회차 업데이트", use_container_width=True):
            with st.spinner("확인 중..."):
                try:
                    last, cnt = auto_update()
                    if cnt > 0:
                        st.success(f"✅ {cnt}회차 추가!")
                        st.cache_data.clear(); st.rerun()
                    else:
                        st.info("이미 최신 데이터예요 👍")
                except Exception as e:
                    st.error(f"연결 실패: {e}")

    # ════════════════════════════════════════════
    # ✏️ 이번 주 행운 탐구
    # ════════════════════════════════════════════
    if menu == "✏️ 이번 주 행운 탐구":
        st.markdown("""
        <h2 style="color:#a3e0a3;margin-bottom:4px;">✏️ 이번 주 행운 탐구</h2>
        <p style="color:#7a9a7a;font-size:14px;margin-bottom:0">
        1~{last_r}회 데이터를 분석해서 통계적으로 균형 잡힌 조합을 뽑아드려요</p>
        """.replace("{last_r}", str(int(df['회차'].max()))), unsafe_allow_html=True)

        st.markdown("""
        <div class="bubble">
        이 조합들은 <b>출현 빈도 · 미출현 기간 · 역대 통계</b>를 종합해서 만들었어요.
        번호 6개의 합이 100~170 사이, 홀짝이 치우치지 않게 필터링도 했답니다.
        로또는 확률 게임이라 보장은 없지만, 통계적으로 가장 "균형 잡힌" 조합이에요! 🍀
        </div>
        """, unsafe_allow_html=True)

        col_btn, col_empty = st.columns([1, 2])
        with col_btn:
            if st.button("🔄 새 조합 뽑기!", use_container_width=True):
                st.session_state.pop("recommended", None)

        if "recommended" not in st.session_state:
            with st.spinner("통계 계산 중..."):
                st.session_state["recommended"] = analyzer.generate_numbers(5, "balanced")

        recommended = st.session_state["recommended"]
        tags = ["🥇 A 조합", "🥈 B 조합", "🥉 C 조합", "🏅 D 조합", "🎯 E 조합"]

        c1, c2 = st.columns(2)
        for i, nums in enumerate(recommended):
            total = sum(nums)
            odd = sum(1 for n in nums if n%2==1)
            card = f"""
            <div class="rec-card">
                <span class="tag">{tags[i]}</span><br>
                <div style="margin:10px 0">{balls_html(nums)}</div>
                <div class="stats">
                    합계 {total} &nbsp;|&nbsp; 홀{odd} 짝{6-odd}
                    &nbsp;|&nbsp; 최소 {min(nums)} 최대 {max(nums)}
                </div>
            </div>"""
            if i % 2 == 0:
                with c1: st.markdown(card, unsafe_allow_html=True)
            else:
                with c2: st.markdown(card, unsafe_allow_html=True)

        # 최근 당첨 번호
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#a3e0a3'>📋 최근 당첨 번호</h4>", unsafe_allow_html=True)
        for _, row in df.tail(5).iloc[::-1].iterrows():
            st.markdown(f"""
            <div class="chalk-card" style="padding:14px 20px;margin:6px 0">
                <span style="color:#7a9a7a;font-size:12px;font-weight:700">제{int(row['회차'])}회</span>
                &nbsp;&nbsp;{balls_html(row['번호목록'], int(row['보너스']), 'sm')}
            </div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # 📊 통계 돋보기
    # ════════════════════════════════════════════
    elif menu == "📊 데이터 패턴 분석":
        st.markdown("<h2 style='color:#a3e0a3'>📊 데이터 패턴 분석</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="bubble">
        1회부터 지금까지 모든 당첨 번호를 분석했어요. 어떤 번호가 자주 나왔는지,
        오래 안 나왔는지, 어떤 번호끼리 자주 같이 나왔는지 한눈에 볼 수 있어요!
        </div>""", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["📈 전체 출현 빈도", "🔥❄️ Hot·Cold 분석", "👫 단짝 번호", "🎯 구간 분포"])

        # ── 탭1: 전체 빈도 ──
        with tab1:
            freq = analyzer.get_frequency()
            freq_df = pd.DataFrame([{"번호": k, "출현횟수": v} for k,v in freq.items()]).sort_values("번호")
            avg = np.mean(list(freq.values()))

            st.markdown(f"""
            <div class="lecture-note">
            📝 <b>강의 노트</b> — 각 번호는 이론적으로 회차당 6/45 = 13.3% 확률로 뽑혀요.
            {len(df)}회 기준 기댓값은 번호당 약 <b>{len(df)*6/45:.0f}회</b>예요.
            막대가 길수록 자주 나온 번호, 색이 진할수록 더 많이 나온 거예요.
            </div>""", unsafe_allow_html=True)

            # 출현 횟수 높을수록 진한 초록색
            fig = px.bar(freq_df, x="번호", y="출현횟수",
                         color="출현횟수",
                         color_continuous_scale=["#0d2b0d", "#2e7d32", "#00e676"],
                         title="번호별 전체 출현 횟수 (진할수록 많이 나온 번호)")
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0.2)",
                font=dict(color="#d4e8c2"),
                title=dict(
                    text="번호별 전체 출현 횟수 (진할수록 많이 나온 번호)",
                    font=dict(color="#a3e0a3", size=15)
                ),
                xaxis=dict(dtick=1, gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,0.05)",
                    title=""
                ),
                coloraxis_showscale=False,
                height=420, margin=dict(t=50, b=20, l=60)
            )
            fig.add_annotation(
                text="횟수", xref="paper", yref="paper",
                x=-0.04, y=1.06, showarrow=False,
                font=dict(color="#d4e8c2", size=12),
                textangle=0, xanchor="center", yanchor="bottom"
            )
            fig.add_hline(y=avg, line_dash="dot", line_color="#ffe066",
                          annotation_text=f"평균 {avg:.0f}회", annotation_font_color="#ffe066")
            st.plotly_chart(fig, use_container_width=True)

            top3 = freq_df.nlargest(3, "출현횟수")
            bot3 = freq_df.nsmallest(3, "출현횟수")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""<div class="chalk-card">
                <div style="color:#a3e0a3;font-weight:700;margin-bottom:10px">🏆 가장 많이 나온 번호</div>
                {"".join([f'<span class="ball {ball_class(int(r["번호"]))}">{int(r["번호"])}</span> <span style="color:#7a9a7a;font-size:13px">{int(r["출현횟수"])}회&nbsp;&nbsp;</span>' for _,r in top3.iterrows()])}
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="chalk-card">
                <div style="color:#e8a0a0;font-weight:700;margin-bottom:10px">📉 가장 적게 나온 번호</div>
                {"".join([f'<span class="ball {ball_class(int(r["번호"]))}">{int(r["번호"])}</span> <span style="color:#7a9a7a;font-size:13px">{int(r["출현횟수"])}회&nbsp;&nbsp;</span>' for _,r in bot3.iterrows()])}
                </div>""", unsafe_allow_html=True)

        # ── 탭2: Hot/Cold ──
        with tab2:
            st.markdown("""
            <div class="bubble">
            <b>🔥 Hot 번호</b>란? → 최근 N회 동안 자주 나온 번호예요.<br>
            <b>❄️ Cold 번호</b>란? → 최근에 통 나오지 않은 번호예요.<br><br>
            아래 슬라이더로 "얼마나 최근"을 기준으로 볼지 조절할 수 있어요.<br>
            예: 50으로 설정하면 가장 최근 50번의 추첨 결과만 보고 Hot·Cold를 판단해요.
            </div>""", unsafe_allow_html=True)

            recent_n = st.slider(
                "📅 최근 몇 회차 기준으로 볼까요?",
                min_value=20, max_value=100, value=50, step=10,
                help="예: 50 = 최근 50번 추첨 결과를 기준으로 Hot/Cold 판단"
            )
            st.caption(f"→ 최근 {recent_n}회 기준으로 분석 중 (전체 {len(df)}회 중)")

            hot, warm, cold = analyzer.get_hot_cold(recent_n)

            st.markdown(f"""
            <div class="lecture-note">
            📝 <b>왜 15개씩일까요?</b> — 로또 번호는 1~45, 총 45개예요.
            이걸 출현 빈도 순으로 줄 세운 뒤 3등분하면 딱 15개씩 나눠져요.
            상위 ⅓ = 🔥, 중간 ⅓ = 🌤️, 하위 ⅓ = ❄️ 이렇게요.
            45 ÷ 3 = <b>15</b>, 그래서 각 그룹이 15개예요!
            </div>""", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class="hc-box hc-hot">
                <div class="hc-title" style="color:#ff7675">🔥 자주 나온 번호<br><span style="font-size:11px;font-weight:400;color:#b2bec3">최근 {recent_n}회 상위 15개</span></div>
                {"".join([f'<span class="ball-sm {ball_class(n)}">{n}</span>' for n in sorted(hot)])}
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="hc-box hc-warm">
                <div class="hc-title" style="color:#ffe066">🌤️ 보통인 번호<br><span style="font-size:11px;font-weight:400;color:#b2bec3">최근 {recent_n}회 중간 15개</span></div>
                {"".join([f'<span class="ball-sm {ball_class(n)}">{n}</span>' for n in sorted(warm)])}
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="hc-box hc-cold">
                <div class="hc-title" style="color:#74b9ff">❄️ 잘 안 나온 번호<br><span style="font-size:11px;font-weight:400;color:#b2bec3">최근 {recent_n}회 하위 15개</span></div>
                {"".join([f'<span class="ball-sm {ball_class(n)}">{n}</span>' for n in sorted(cold)])}
                </div>""", unsafe_allow_html=True)

        # ── 탭3: 번호 쌍 ──
        with tab3:
            st.markdown("""
            <div class="bubble">
            역대 당첨번호에서 <b>두 번호가 같이 뽑힌 횟수</b>를 세어봤어요.
            함께 자주 나오는 "단짝 번호"들이에요.
            단, 이것도 우연의 영역이라 미래를 보장하진 않아요! 참고용으로 활용해보세요 😊
            </div>""", unsafe_allow_html=True)

            pairs = analyzer.get_pair_frequency(15)
            medal = ["🥇","🥈","🥉"] + ["④","⑤","⑥","⑦","⑧","⑨","⑩","⑪","⑫","⑬","⑭","⑮"]

            for i, (pair, count) in enumerate(pairs):
                a, b = pair
                st.markdown(f"""
                <div class="pair-card">
                    <span class="pair-rank">{medal[i]}</span>
                    <span>
                        <span class="ball-sm {ball_class(a)}">{a}</span>
                        <span style="color:#7a9a7a;margin:0 6px;font-size:16px">+</span>
                        <span class="ball-sm {ball_class(b)}">{b}</span>
                    </span>
                    <span class="pair-count">함께 {count}회</span>
                </div>""", unsafe_allow_html=True)

        # ── 탭4: 구간 분포 ──
        with tab4:
            st.markdown("""
            <div class="bubble">
            로또 번호를 10개씩 구간으로 나눴을 때 어느 구간에서 많이 나왔는지 보여줘요.
            번호 선택 시 너무 한 구간에 몰리지 않게 참고하면 좋아요!
            </div>""", unsafe_allow_html=True)

            decade = analyzer.get_decade_distribution()
            total_balls = sum(decade.values())

            COLORS = {"1~10":"#ffe066","11~20":"#74b9ff","21~30":"#ff7675","31~40":"#b2bec3","41~45":"#a3e0a3"}
            for zone, cnt in decade.items():
                pct = cnt / total_balls * 100
                bar_w = int(pct * 3)
                st.markdown(f"""
                <div class="chalk-card" style="padding:16px 20px;margin:6px 0">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                        <span style="color:{COLORS[zone]};font-weight:700;font-size:15px">{zone}번대</span>
                        <span style="color:#a3e0a3;font-weight:800">{pct:.1f}%</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.08);border-radius:6px;height:10px;overflow:hidden">
                        <div style="background:{COLORS[zone]};width:{min(pct*3,100):.0f}%;height:100%;border-radius:6px;transition:width 0.5s"></div>
                    </div>
                    <div style="font-size:12px;color:#7a9a7a;margin-top:6px">총 {cnt:,}번 출현</div>
                </div>""", unsafe_allow_html=True)


    # ════════════════════════════════════════════
    # 🎯 번호 직접 뽑기
    # ════════════════════════════════════════════
    elif menu == "🎯 나만의 숫자 조합실":
        st.markdown("<h2 style='color:#a3e0a3'>🎯 나만의 숫자 조합실</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="bubble">
        전략을 선택하면 그에 맞는 번호를 뽑아드려요.
        전략마다 어떤 번호를 더 중요하게 보는지 달라요!
        </div>""", unsafe_allow_html=True)

        strategies = {
            "balanced":       ("⚖️ 균형 전략",  "최근 자주 나온 번호 + 오래 안 나온 번호를 균형 있게 섞어요. 가장 무난한 선택!"),
            "hot_focused":    ("🔥 Hot 전략",   "요즘 자주 나오는 번호에 집중해요. 흐름을 탄다는 관점이에요."),
            "cold_focused":   ("❄️ Cold 전략",  "오래 안 나온 번호 위주로 뽑아요. 곧 나올 차례라는 관점이에요."),
            "expected_value": ("💰 기대값 전략", "남들이 잘 안 고르는 번호를 뽑아요. 1등이 되면 당첨금을 혼자 가질 확률이 높아요!"),
        }

        c1, c2 = st.columns([2, 1])
        with c1:
            strat_key = st.selectbox("전략 선택", list(strategies.keys()),
                                      format_func=lambda k: strategies[k][0])
        with c2:
            n_sets = st.number_input("조합 수", 1, 20, 5)

        st.markdown(f"""
        <div class="lecture-note">
        💡 <b>{strategies[strat_key][0]}</b> — {strategies[strat_key][1]}
        </div>""", unsafe_allow_html=True)

        if st.button(f"🎲 {strategies[strat_key][0]}으로 뽑기!", use_container_width=True):
            with st.spinner("계산 중..."):
                results = analyzer.generate_numbers(n_sets, strat_key)
            st.session_state["gen_results"] = results

        if "gen_results" in st.session_state:
            c1, c2 = st.columns(2)
            for i, nums in enumerate(st.session_state["gen_results"]):
                total = sum(nums); odd = sum(1 for n in nums if n%2==1)
                card = f"""<div class="rec-card">
                    <span class="tag">조합 {i+1}</span><br>
                    <div style="margin:10px 0">{balls_html(nums)}</div>
                    <div class="stats">합계 {total} | 홀{odd} 짝{6-odd}</div>
                </div>"""
                if i%2==0:
                    with c1: st.markdown(card, unsafe_allow_html=True)
                else:
                    with c2: st.markdown(card, unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # 📝 과거 시험해보기
    # ════════════════════════════════════════════
    elif menu == "📝 과거 당첨 데이터 연구":
        st.markdown("<h2 style='color:#a3e0a3'>📝 과거 당첨 데이터 연구</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="bubble">
        내가 고른 번호 6개를 역대 모든 회차에 제출했다면 어떤 결과가 나왔을까요?
        당첨 규칙 그대로 1~5등, 낙첨을 계산해드려요!
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='chalk-card'><b style='color:#a3e0a3'>번호 6개를 입력하세요 (1~45)</b><br>", unsafe_allow_html=True)
        cols = st.columns(6)
        defaults = [7, 14, 21, 28, 35, 42]
        selected = []
        for i, col in enumerate(cols):
            with col:
                n = st.number_input(f"{i+1}번째", 1, 45, defaults[i], key=f"sim_{i}", label_visibility="visible")
                selected.append(n)
        st.markdown("</div>", unsafe_allow_html=True)

        if len(set(selected)) != 6:
            st.warning("⚠️ 중복 번호가 있어요! 6개 모두 다른 번호로 해주세요.")
        else:
            st.markdown(f"<div style='margin:10px 0'>선택한 번호: {balls_html(sorted(selected))}</div>",
                        unsafe_allow_html=True)

            if st.button("🚀 시뮬레이션 시작!", use_container_width=True):
                with st.spinner(f"역대 {len(df)}회차 전부 대조 중..."):
                    sim = analyzer.simulate_past(sorted(selected))
                st.session_state["sim_result"] = sim

        if "sim_result" in st.session_state:
            sim = st.session_state["sim_result"]
            total_games = len(df)
            total_wins = total_games - sim["낙첨"]
            win_rate = total_wins / total_games * 100

            # 요약 배너를 제일 먼저 크게!
            st.markdown(f"""
            <div class="summary-banner">
                <div class="win-label">역대 {total_games}회차 중</div>
                <div class="win-rate">{total_wins}회 당첨</div>
                <div class="win-detail">당첨률 <b style="color:#ffe066;font-size:24px">{win_rate:.2f}%</b></div>
            </div>""", unsafe_allow_html=True)

            # 등수별 결과
            rank_info = [
                ("1등", "#ff7675", "6개 일치"),
                ("2등", "#e17055", "5개+보너스"),
                ("3등", "#fdcb6e", "5개 일치"),
                ("4등", "#a3e0a3", "4개 일치"),
                ("5등", "#74b9ff", "3개 일치"),
            ]
            cols = st.columns(5)
            for i, (rank, color, desc) in enumerate(rank_info):
                with cols[i]:
                    st.markdown(f"""
                    <div class="rank-card" style="background:rgba(255,255,255,0.05);border:1px solid {color}33">
                        <div class="rank-label" style="color:{color}">{rank}</div>
                        <div class="rank-val" style="color:{color}">{sim[rank]}회</div>
                        <div class="rank-sub">{desc}</div>
                    </div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # 📈 흐름 분석
    # ════════════════════════════════════════════
    elif menu == "📈 최신 당첨 추세 전망":
        st.markdown("<h2 style='color:#a3e0a3'>📈 최신 당첨 추세 전망</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="bubble">
        역대 당첨 번호들의 패턴을 분석해봤어요.
        어떤 합계 범위가 많은지, 홀짝 비율은 어떤지, 번호 히트맵까지 확인해보세요!
        </div>""", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🔢 합계 분포", "홀짝 비율", "🗓 번호 히트맵"])

        with tab1:
            sums = analyzer.get_sum_distribution()
            in_range = sum(1 for s in sums if 100 <= s <= 170)

            st.markdown(f"""
            <div class="lecture-note">
            📝 당첨번호 6개를 더하면 대부분 <b>100~170 사이</b>에 들어와요.
            전체 {len(df)}회 중 <b>{in_range}회 ({in_range/len(df)*100:.1f}%)</b>가 이 구간이에요.
            번호 고를 때 합계를 한번 더해보세요!
            </div>""", unsafe_allow_html=True)

            # 합계별 빈도 집계 → 선그래프
            sum_counts = pd.Series(sums).value_counts().sort_index().reset_index()
            sum_counts.columns = ["합계", "횟수"]
            fig = go.Figure()
            # 면적 채우기 (연한 초록)
            fig.add_trace(go.Scatter(
                x=sum_counts["합계"], y=sum_counts["횟수"],
                mode="lines", fill="tozeroy",
                line=dict(color="#00e676", width=2.5, shape="spline"),
                fillcolor="rgba(0,230,118,0.12)",
                name="합계 빈도"
            ))
            # 추천구간 음영
            fig.add_vrect(x0=100, x1=170, fillcolor="#a3e0a3", opacity=0.08,
                          annotation_text="추천 구간 100~170",
                          annotation_font_color="#a3e0a3",
                          annotation_position="top left")
            # 평균선
            fig.add_vline(x=np.mean(sums), line_dash="dot", line_color="#ffe066",
                          annotation_text=f"평균 {np.mean(sums):.0f}",
                          annotation_font_color="#ffe066")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.2)",
                font=dict(color="#d4e8c2"), height=380,
                margin=dict(t=50, b=20, l=60),
                title=dict(text="당첨번호 6개 합계 분포", font=dict(color="#a3e0a3", size=15)),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=dict(text="합계", font=dict(color="#d4e8c2"))),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,0.05)",
                    title=""
                ),
                showlegend=False
            )
            fig.add_annotation(
                text="횟수", xref="paper", yref="paper",
                x=-0.04, y=1.06, showarrow=False,
                font=dict(color="#d4e8c2", size=12),
                textangle=0, xanchor="center", yanchor="bottom"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            odd_even = analyzer.get_odd_even_distribution()
            sorted_oe = dict(sorted(odd_even.items(), key=lambda x: x[1], reverse=True))
            total_oe = sum(sorted_oe.values())

            st.markdown("""
            <div class="lecture-note">
            📝 6개 번호가 홀수·짝수 몇 개씩인지 분포예요.
            극단적으로 몰린 조합(홀6·짝6 등)은 역대에 거의 안 나왔어요.
            홀2:짝4 ~ 홀4:짝2 사이가 가장 현실적이에요!
            </div>""", unsafe_allow_html=True)

            for ratio, cnt in sorted_oe.items():
                pct = cnt / total_oe * 100
                is_good = any(f"홀{x}" in ratio for x in [2,3,4])
                color = "#a3e0a3" if is_good else "#e8a0a0"
                st.markdown(f"""
                <div class="chalk-card" style="padding:14px 20px;margin:6px 0">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:7px">
                        <span style="color:{color};font-weight:700">{ratio}</span>
                        <span style="color:#a3e0a3;font-weight:800">{pct:.1f}% <span style="color:#7a9a7a;font-size:12px">({cnt}회)</span></span>
                    </div>
                    <div style="background:rgba(255,255,255,0.08);border-radius:6px;height:8px">
                        <div style="background:{color};width:{pct*2:.0f}%;height:100%;border-radius:6px"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        with tab3:
            st.markdown("""
            <div class="lecture-note">
            📝 최근 50회 동안 각 번호가 언제 나왔는지 한눈에 볼 수 있어요.
            녹색 칸이 당첨된 회차예요. 세로로 줄이 많을수록 자주 나온 번호!
            </div>""", unsafe_allow_html=True)

            recent_df = df.tail(50)
            heatmap_data = []
            for _, row in recent_df.iterrows():
                r = [0]*45
                for num in row["번호목록"]: r[num-1] = 1
                heatmap_data.append(r)

            hm_df = pd.DataFrame(heatmap_data,
                                  index=[f"{int(r)}회" for r in recent_df["회차"]],
                                  columns=[str(i) for i in range(1,46)])

            fig3 = px.imshow(hm_df,
                             color_continuous_scale=["#1a2e1a", "#a3e0a3"],
                             aspect="auto",
                             title="최근 50회 번호 히트맵 (초록 = 당첨번호)")
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#d4e8c2"),
                height=560, margin=dict(t=40,b=10),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig3, use_container_width=True)


if __name__ == "__main__":
    main()
