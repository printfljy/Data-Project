import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI.csv")
    return df

df = load_data()

# --- UI 제목 ---
st.title("🌎 MBTI 성향별 국가 분포 분석 (E/I, N/S, T/F, P/J)")
st.markdown("""
MBTI를 구성하는 4가지 축 중 하나를 선택하면,  
각 국가의 해당 성향(E, I 등) 비율을 계산해 **표와 지도**로 시각화합니다.
""")

# --- 선택창 ---
options = ["E vs I", "N vs S", "T vs F", "P vs J"]
selected_option = st.selectbox("분석할 축을 선택하세요:", options)

# --- 각 축별 MBTI 그룹 ---
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

# --- 선택한 축에 따른 분류 ---
if selected_option == "E vs I":
    group_a, group_b = "E", "I"
elif selected_option == "N vs S":
    group_a, group_b = "N", "S"
elif selected_option == "T vs F":
    group_a, group_b = "T", "F"
else:
    group_a, group_b = "P", "J"

# --- 각 그룹 비율 계산 ---
df[group_a] = df[mbti_groups[group_a]].sum(axis=1)
df[group_b] = df[mbti_groups[group_b]].sum(axis=1)
df["Diff"] = df[group_a] - df[group_b]

# --- 정렬 (group_a가 높은 순) ---
df_sorted = df.sort_values(by="Diff", ascending=False).reset_index(drop=True)

# --- 우리나라(South Korea) 찾기 ---
korea_row = df_sorted[df_sorted["Country"].str.lower() == "south korea"]

if not korea_row.empty:
    korea_index = korea_row.index[0] + 1  # 순위는 1부터 시작
    korea_a = float(korea_row[group_a])
    korea_b = float(korea_row[group_b])
    st.markdown(f"""
    ### 🇰🇷 한국의 {selected_option} 분포
    우리나라는 **{group_a} {korea_a*100:.2f}%**, **{group_b} {korea_b*100:.2f}%**로  
    **{group_a} 성향이 높은 국가 중 {korea_index}위**에 해당해요.
    """)
else:
    st.warning("⚠️ 데이터에 'South Korea' 항목이 없습니다. CSV 파일의 국가명을 확인해 주세요.")

# --- 표 출력 ---
st.subheader(f"📋 {selected_option} 분포 표")
st.markdown(f"**{group_a} 성향이 강한 국가 → {group_b} 성향이 강한 국가 순**으로 정렬되었습니다.")
st.dataframe(df_sorted[["Country", group_a, group_b, "Diff"]].style.format({
    group_a: "{:.2%}",
    group_b: "{:.2%}",
    "Diff": "{:.2%}"
}))

# --- 지도 시각화 ---
st.subheader("🗺️ 세계 지도 시각화")

geolocator = Nominatim(user_agent="mbti_axis_map")
m = folium.Map(location=[20, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(m)

for _, row in df_sorted.iterrows():
    country = row["Country"]
    val_a = row[group_a] * 100
    val_b = row[group_b] * 100
    diff = row["Diff"] * 100

    try:
        location = geolocator.geocode(country)
        if location:
            color = "red" if diff > 0 else "blue"
            popup_html = f"""
            <b>{country}</b><br>
            {group_a}: {val_a:.2f}%<br>
            {group_b}: {val_b:.2f}%<br>
            차이({group_a} - {group_b}): {diff:.2f}%
            """
            folium.CircleMarker(
                location=[location.latitude, location.longitude],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                popup=popup_html,
                tooltip=country
            ).add_to(marker_cluster)
    except:
        pass

# --- 지도 표시 ---
st_folium(m, width=800, height=500)
