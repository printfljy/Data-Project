import streamlit as st
import pandas as pd

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI.csv")
    return df

df = load_data()

# --- 한국 데이터 추출 ---
korea_data = df[df["Country"].str.lower() == "south korea"]
if korea_data.empty:
    st.error("⚠️ 데이터에 'South Korea'가 없습니다. CSV 파일에서 국가명을 확인해 주세요.")
    st.stop()

korea_data = korea_data.iloc[0]
mbti_types = [col for col in df.columns if col != "Country"]

# --- MBTI 선택 ---
st.title("🇰🇷 한국 내 MBTI 순위 & 직업 추천")
st.markdown("자신의 MBTI를 선택하면, 한국에서 얼마나 흔한지와 추천 직업을 확인할 수 있습니다.")

selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_types)

# --- 한국 내 순위 계산 ---
sorted_mbti = sorted(
    [(mbti, korea_data[mbti]) for mbti in mbti_types],
    key=lambda x: x[1],
    reverse=True
)
rank = [mbti for mbti, _ in sorted_mbti].index(selected_mbti) + 1
percentage = korea_data[selected_mbti]
population_estimate = 51150000 * percentage  # 한국 인구 5,115만 기준

# --- 결과 출력 ---
st.subheader("📊 한국 내 분포 결과")
st.markdown(f"""
**{selected_mbti}** 유형은 한국에서 **{rank}번째로 흔한 MBTI**입니다.  
한국 인구 **약 5,115만 명** 기준으로 보면,  
👉 약 **{population_estimate:,.0f}명 ({percentage*100:.2f}%)** 정도가 {selected_mbti} 유형이에요.
""")

# --- 직업 추천 데이터 ---
career_recommendations = {
    "INTJ": [
        ("데이터 과학자", "논리적 사고와 전략적 접근을 선호하기 때문에 복잡한 문제를 분석하는 일에 강점이 있습니다."),
        ("전략 컨설턴트", "큰 그림을 보고 체계적으로 해결책을 제시하는 능력이 뛰어납니다."),
    ],
    "INFP": [
        ("작가", "감정과 상상을 표현하는 능력이 뛰어나며, 자신만의 세계관을 글로 풀어내는 데 적합합니다."),
        ("심리상담사", "타인의 감정을 깊이 이해하고 공감할 수 있어 사람을 돕는 직업에 잘 어울립니다."),
    ],
    "ENTJ": [
        ("경영 컨설턴트", "목표 지향적이며 리더십이 강해 팀을 이끌고 전략을 설계하는 데 능숙합니다."),
        ("프로젝트 매니저", "조직을 효율적으로 운영하며 결과 중심으로 추진하는 성향이 강합니다."),
    ],
    "ISFP": [
        ("디자이너", "섬세한 감성과 미적 감각이 뛰어나 시각적 창의력을 발휘합니다."),
        ("사진작가", "감정과 분위기를 예술적으로 포착하는 능력이 뛰어납니다."),
    ],
    "ENFP": [
        ("마케팅 기획자", "창의적이고 사람을 잘 이해하여 새로운 아이디어를 내는 데 탁월합니다."),
        ("콘텐츠 크리에이터", "열정과 표현력이 풍부하여 다양한 매체에서 영향력을 발휘합니다."),
    ],
    "ISTJ": [
        ("회계사", "정확성과 책임감이 뛰어나 체계적인 업무를 수행하는 데 강점이 있습니다."),
        ("공무원", "규칙과 절차를 중시하며 안정적인 환경에서 꾸준히 성과를 내는 스타일입니다."),
    ],
    "ESFJ": [
        ("교사", "사람들과의 관계를 중요하게 생각하며 타인을 도와주는 데 만족을 느낍니다."),
        ("인사 담당자", "조직 내 사람들의 조화를 유지하고 소통을 중시합니다."),
    ],
    "INFJ": [
        ("상담사", "깊이 있는 통찰과 공감을 바탕으로 타인의 성장과 치유를 돕습니다."),
        ("작가", "자신의 내면세계를 표현하고 의미 있는 메시지를 전하는 일에 적합합니다."),
    ],
}

# --- 기본 추천 (없을 경우 대체) ---
if selected_mbti in career_recommendations:
    recs = career_recommendations[selected_mbti]
else:
    recs = [
        ("연구원", "깊이 있는 사고력과 분석력을 발휘할 수 있는 분야입니다."),
        ("기획자", "체계적이고 창의적인 접근을 모두 요구하는 직업에 잘 맞습니다."),
    ]

# --- 직업 추천 표시 ---
st.subheader("💼 추천 직업 & 이유")
for job, reason in recs:
    st.markdown(f"**- {job}**: {reason}")
