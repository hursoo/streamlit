import streamlit as st
import pandas as pd
# from konlpy.tag import Okt  <- 이 부분을 주석 처리하거나 삭제
from kiwipiepy import Kiwi   # <- Kiwi를 임포트합니다.
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="나만의 텍스트 분석기 (Kiwi)", page_icon="🥝")

st.title("🥝 나만의 텍스트 분석 도우미 (Kiwi ver.)")
st.write("가지고 있는 텍스트 파일을 업로드하고 간단한 분석을 수행해보세요!")

# --- Kiwi 객체 생성 ---
# 이 객체는 한 번만 만들어두고 재사용하는 것이 좋습니다.
@st.cache_resource
def get_kiwi():
    return Kiwi()

kiwi = get_kiwi()
# ----------------------

uploaded_file = st.file_uploader("분석할 텍스트 파일(txt)을 선택하세요.", type="txt")

if uploaded_file is not None:
    try:
        raw_text = uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        raw_text = uploaded_file.read().decode('cp949')

    st.subheader("📝 원본 텍스트")
    st.text_area("내용", raw_text, height=200)

    # --- 텍스트 분석 로직 (Kiwi 사용) ---
    # kiwi.tokenize()를 사용해 텍스트를 분석합니다.
    # NNG(보통 명사), NNP(고유 명사)만 추출합니다.
    result = kiwi.analyze(raw_text)
    nouns = [token.form for token in result[0][0] if token.tag in ['NNG', 'NNP']]
    words = [n for n in nouns if len(n) > 1] # 1글자 단어 제외
    # ------------------------------------

    count = Counter(words)
    most_common_words = count.most_common(30)

    st.subheader("📊 단어 빈도 분석 (상위 30개)")
    df = pd.DataFrame(most_common_words, columns=['단어', '빈도수'])
    st.dataframe(df)

    st.subheader("☁️ 워드클라우드")
    font_path = 'c:/Windows/Fonts/malgun.ttf'
    try:
        wc = WordCloud(font_path=font_path, background_color='white', width=800, height=600)
        cloud = wc.generate_from_frequencies(dict(most_common_words))
        fig, ax = plt.subplots()
        ax.imshow(cloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except FileNotFoundError:
        st.error("워드클라우드를 위한 한글 폰트를 찾을 수 없습니다. 코드 내의 `font_path`를 확인해주세요.")
