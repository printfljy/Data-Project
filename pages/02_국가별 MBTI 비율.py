import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI.csv")
    return df

df = load_data()

# --- UI 제목 ---
st.title("📊 국가별 MBTI 비율 시각화 (Plotly)")
st.markdown("국가를 선택하면 해당 국가의 MBTI 분포를 **내림차순 정렬된 인터랙티브 막대그래프**로 확인할 수 있습니다.")

# --- 국가 선택창 ---
countries = sorted(df["Country"].unique())
selected_country = st.selectbox("국가를 선택하세요:", countries)

# --- 선택된 국가 데이터 추출 ---
country_data = df[df["Country"] == selected_country].iloc[0]
mbti_types = [col for col in df.columns if col != "Country"]
values = [country_data[mbti] for mbti in mbti_types]

# --- 데이터프레임으로 묶고 내림차순 정렬 ---
data_sorted = pd.DataFrame({
    "MBTI": mbti_types,
    "Value": values
}).sort_values(by="Value", ascending=False)

# --- 색상 설정 (최대값은 빨간색, 나머지는 파란색 그라데이션) ---
max_value = data_sorted["Value"].max()
colors = [
    "red" if v == max_value else f"rgba(0, 100, 255, {0.4 + 0.6*(v/max_value)})"
    for v in data_sorted["Value"]
]

# --- Plotly 막대그래프 생성 ---
fig = go.Figure(data=[
    go.Bar(
        x=data_sorted["MBTI"],
        y=data_sorted["Value"],
        marker_color=colors,
        text=[f"{v*100:.2f}%" for v in data_sorted["Value"]],
        textposition="outside",
    )
])

fig.update_layout(
    title=f"{selected_country}의 MBTI 비율 (내림차순)",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    yaxis_tickformat=".0%",
    template="plotly_white",
    showlegend=False,
    height=500,
)

# --- 그래프 표시 ---
st.plotly_chart(fig, use_container_width=True)

# --- 데이터 표시 ---
st.write("#### 📋 내림차순 정렬된 세부 데이터")
st.dataframe(
    data_sorted.assign(비율=(data_sorted["Value"] * 100).round(2).astype(str) + "%")
    .rename(columns={"MBTI": "MBTI 유형", "Value": "비율(소수)"})
)
