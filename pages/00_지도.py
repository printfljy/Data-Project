import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광명소 지도", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울 주요 관광지 Top 10")
st.write("서울을 찾는 외국인들이 많이 방문하는 인기 관광지를 지도에 표시했습니다!")

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]

# 외국인 인기 관광지 Top 10
locations = [
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770, "desc": "조선의 법궁으로 역사와 전통의 중심지"},
    {"name": "명동", "lat": 37.5636, "lon": 126.9827, "desc": "쇼핑과 음식, 패션의 거리"},
    {"name": "남산타워(N서울타워)", "lat": 37.5512, "lon": 126.9882, "desc": "서울의 랜드마크, 야경 명소"},
    {"name": "홍대", "lat": 37.5563, "lon": 126.9220, "desc": "젊음과 예술, 자유분방한 거리"},
    {"name": "인사동", "lat": 37.5740, "lon": 126.9849, "desc": "전통 문화와 예술의 거리"},
    {"name": "북촌 한옥마을", "lat": 37.5826, "lon": 126.9830, "desc": "전통 한옥과 골목길의 매력"},
    {"name": "롯데월드타워", "lat": 37.5131, "lon": 127.1028, "desc": "123층 초고층 랜드마크"},
    {"name": "동대문 디자인 플라자(DDP)", "lat": 37.5663, "lon": 127.0094, "desc": "현대적인 건축물과 전시 공간"},
    {"name": "청계천", "lat": 37.5700, "lon": 126.9784, "desc": "도심 속 자연 휴식 공간"},
    {"name": "이태원", "lat": 37.5348, "lon": 126.9946, "desc": "다문화 거리, 글로벌 레스토랑과 바"}
]

# 지도 생성
m = folium.Map(location=seoul_center, zoom_start=12)

# 마커 추가
for loc in locations:
    folium.Marker(
        [loc["lat"], loc["lon"]],
        popup=f"<b>{loc['name']}</b><br>{loc['desc']}",
        tooltip=loc["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Streamlit에 Folium 지도 표시
st_folium(m, width=800, height=600)
