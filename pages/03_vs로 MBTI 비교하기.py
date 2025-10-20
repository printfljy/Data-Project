import streamlit as st
import pandas as pd

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI.csv")
    return df

df = load_data()

st.title("🌍 MBTI 성향별 대륙 비교 분석")
st.markdown("""
MBTI의 주요 네 축 중 하나를 선택하면,  
**대륙별 평균 성향 비율**을 계산해 비교합니다.
""")

# --- 선택창 ---
options = ["E vs I", "N vs S", "T vs F", "P vs J"]
selected_option = st.selectbox("비교할 성향 축을 선택하세요:", options)

# --- MBTI 그룹 정의 ---
mbti_groups = {
    "E": ["ENFJ", "ENFP", "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP"],
    "I": ["INFJ", "INFP", "INTJ", "INTP", "ISFJ", "ISFP", "ISTJ", "ISTP"],
    "N": ["ENFJ", "ENFP", "ENTJ", "ENTP", "INFJ", "INFP", "INTJ", "INTP"],
    "S": ["ESFJ", "ESFP", "ESTJ", "ESTP", "ISFJ", "ISFP", "ISTJ", "ISTP"],
    "T": ["ENTJ", "ENTP", "ESTJ", "ESTP", "INTJ", "INTP", "ISTJ", "ISTP"],
    "F": ["ENFJ", "ENFP", "ESFJ", "ESFP", "INFJ", "INFP", "ISFJ", "ISFP"],
    "P": ["ENFP", "ENTP", "ESFP", "ESTP", "INFP", "INTP", "ISFP", "ISTP"],
    "J": ["ENFJ", "ENTJ", "ESFJ", "ESTJ", "INFJ", "INTJ", "ISFJ", "ISTJ"]
}

# --- 대륙 분류 (간단 매핑 예시) ---
continent_map = {
    "South Korea": "Asia",
    "Japan": "Asia",
    "China": "Asia",
    "India": "Asia",
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Brazil": "South America",
    "Argentina": "South America",
    "Chile": "South America",
    "Germany": "Europe",
    "France": "Europe",
    "United Kingdom": "Europe",
    "Italy": "Europe",
    "Spain": "Europe",
    "Russia": "Europe",
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "South Africa": "Africa",
    "Egypt": "Africa",
    "Nigeria": "Africa",
}
df["Continent"] = df["Country"].map(continent_map).fillna("Other")

# --- 선택한 축에 따른 그룹 선택 ---
if selected_option == "E vs I":
    group_a, group_b = "E", "I"
elif selected_option == "N vs S":
    group_a, group_b = "N", "S"
elif selected_option == "T vs F":
    group_a, group_b = "T", "F"
else:
    group_a, group_b = "P", "J"

# --- 각 성향 비율 계산 ---
df[group_a] = df[mbti_groups[group_a]].sum(axis=1)
df[group_b] = df[mbti_groups[group_b]].sum(axis=1)

# --- 대륙별 평균 계산 ---
continent_avg = df.groupby("Continent")[[group_a, group_b]].mean().reset_index()
continent_avg["Diff"] = continent_avg[group_a] - continent_avg[group_b]

# --- 표 출력 ---
st.subheader(f"📊 대륙별 {selected_option} 평균 비율")
st.dataframe(continent_avg.style.format({
    group_a: "{:.2%}",
    group_b: "{:.2%}",
    "Diff": "{:.2%}"
}))

# --- 성향별로 높은 대륙 찾기 ---
a_higher = continent_avg.loc[continent_avg["Diff"] > 0, "Continent"].tolist()
b_higher = continent_avg.loc[continent_avg["Diff"] < 0, "Continent"].tolist()

# --- 한국 정보 ---
korea_row = df[df["Country"].str.lower() == "south korea"]
if not korea_row.empty:
    korea_a = float(korea_row[group_a])
    korea_b = float(korea_row[group_b])
    korea_diff = korea_a - korea_b
    st.markdown(f"""
    ### 🇰🇷 한국의 {selected_option} 분포
    한국은 **{group_a} {korea_a*100:.2f}%**, **{group_b} {korea_b*100:.2f}%** 입니다.
    """)

# --- 요약 문장 출력 ---
st.subheader("🧭 분석 요약")
a_str = ", ".join(a_higher) if a_higher else "없음"
b_str = ", ".join(b_higher) if b_higher else "없음"
st.markdown(f"""
평균적으로 **{group_a} 성향 비율이 더 높은 대륙**은 👉 **{a_str}**,  
**{group_b} 성향 비율이 더 높은 대륙**은 👉 **{b_str}** 예요.
""")
