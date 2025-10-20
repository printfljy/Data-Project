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

# --- 제목 및 설명 ---
st.title("🌍 MBTI별 세계 분포 지도")
st.markdown("선호하는 MBTI 유형을 선택하면, 해당 유형의 비율이 가장 높은 **Top10 국가**를 지도에서 확인할 수 있습니다.")

# --- MBTI 선택창 ---
mbti_list = [col for col in df.columns if col != "Country"]
selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_list)

# --- Top10 국가 추출 ---
top10 = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10).reset_index(drop=True)

# --- 지도 생성 ---
st.write(f"### 🌐 {selected_mbti} 유형 비율이 높은 Top10 국가")
geolocator = Nominatim(user_agent="mbti_map")

m = folium.Map(location=[20, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(m)

for i, row in top10.iterrows():
    country = row["Country"]
    mbti_value = row[selected_mbti] * 100  # 퍼센트 단위로 표시
    try:
        location = geolocator.geocode(country)
        if location:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=f"<b>{country}</b><br>{selected_mbti} 비율: {mbti_value:.2f}%",
                tooltip=country,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(marker_cluster)
    except:
        pass

# --- 지도 표시 ---
st_data = st_folium(m, width=800, height=500)

# --- 데이터 테이블 표시 ---
st.write("#### 📊 Top10 국가 데이터")
st.dataframe(top10.style.format({selected_mbti: "{:.2%}"}))
