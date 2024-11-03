from typing import Callable
import streamlit as st
from sqlalchemy.orm import Session  # ORM 세션
from config import get_db  # 데이터베이스 연결 함수
from model import Quote, Speaker, Category, Reference  # ORM 모델

page = st.radio("페이지 선택", ["명언 추가", "발화자 추가"])

st.markdown(
    """
    <style>
    .box {
        border: 2px solid #4CAF50;  /* 테두리 색상 */
        padding: 20px;              /* 내부 여백 */
        border-radius: 10px;        /* 테두리 둥글기 */
        background-color: #f9f9f9;  /* 배경 색상 */
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# DB 연결 설정
db = next(get_db())

if page == "명언 추가":

    new_quote = {"ko_sentence" : "",
                "en_sentence" : "",
                "category_id" : "",
                "speaker_id" : "",
                "reference_id": ""}
    
    meta = {"category" : "",
            "speaker_name" : "",
            "reference" : "",
            "reference_type" : ""}

    if "new_quote" not in st.session_state:
        st.session_state.new_quote = new_quote
        st.session_state.quote_meta = meta

    # 입력 필드와 관련된 실시간 검색 함수
    def fetch_similar_quotes(query: str, db: Session):
        # 유사한 명언을 찾는 ORM 쿼리 예시
        return db.query(Quote).filter(Quote.ko_sentence.like(f"%{query}%")).limit(5).all()

    def fetch_similar_speaker(speaker: str, db : Session):
        return db.query(Speaker).filter(Speaker.ko_name.like(f"%{speaker}%")).limit(5).all()
    
    def fetch_all_category(db : Session):
        return db.query(Category).all()

    # Streamlit 앱 시작
    st.title("명언 추가")
    quote_input = st.text_input("한글 명언 본문을 입력하세요")

    # 입력 필드가 변경될 때마다 관련된 유사 명언 보여주기
    if quote_input:
        similar_quotes = fetch_similar_quotes(quote_input, db)
        if st.button("한국어 명언 등록") or st.session_state.new_quote["ko_sentence"]:
            st.session_state.new_quote["ko_sentence"] = quote_input
            en_sentence = st.text_input("(선택) 영어 명언을 입력하세요")
            if st.button("영어 등록"):
                st.session_state.new_quote["en_sentence"] = en_sentence

        if similar_quotes and not st.session_state.new_quote["ko_sentence"]:
            container = st.container(border=True)
            container.write("#### 유사한 명언들:")
            for quote in similar_quotes:
                container.write(f"- {quote.ko_sentence} (speak: {quote.speaker.ko_name}, rep.: {quote.reference})")
            
        elif not st.session_state.new_quote["ko_sentence"]:
            container = st.container(border=True)
            container.write("#### 유사한 명언이 없습니다.")
    

    speaker_input = None
    if st.session_state.new_quote["ko_sentence"]:
        "---"
        speaker_input = st.text_input("발화자의 이름을 입력하세요")

    if speaker_input:
        similar_speaker = fetch_similar_speaker(speaker_input, db)
        
        if similar_speaker:
            st.write("#### 발화자 리스트:")
            
            for speaker in similar_speaker:
                if st.button(f"이름 : {speaker.ko_name}, 본명 : {speaker.org_name}, (생몰 : {speaker.born_date} - {speaker.death_date})"):
                    st.session_state.new_quote["speaker_id"] = speaker.speaker_id
                    st.session_state.quote_meta["speaker_name"] = speaker.ko_name
            
            if st.session_state.new_quote["speaker_id"]:
                st.write(f"선택된 발화자 : {st.session_state.quote_meta["speaker_name"]}")
        else:
            st.write("발화자가 없습니다.")

    if st.session_state.new_quote["speaker_id"]:
        "---"
        categorys = fetch_all_category(db)
        
        if categorys:
            st.write("#### 카테고리 리스트:")
            format_func : Callable[[Category], str] = lambda x : x.category
            category : None = st.selectbox("카테고리 선택", categorys, index=None, format_func=format_func, placeholder="카테고리를 선택해주세요")
            if category:
                st.session_state.new_quote["category_id"] = category.category_id
                st.session_state.quote_meta["category"] = category.category
            
            if st.session_state.new_quote["category_id"]:
                st.write(f"선택된 카테고리 : **{st.session_state.quote_meta["category"]}**")
        "---"


    st.markdown(
        f"""
        <style>
        .floating-container {{
            position: fixed;
            bottom: 10%;
            right: 2%;
            width: 300px;
            padding: 20px;
            background-color: #ee4d30;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            z-index: 100;
        }}
        
        p {{
            font-size : 18px;
        }}
        </style>
        <div class="floating-container" style="font-size: 20px;">
            <p>한국어 : {st.session_state.new_quote["ko_sentence"]}</p>
            <p>영어 : {st.session_state.new_quote["en_sentence"]}</p>
            <p>발화자 : {st.session_state.quote_meta["speaker_name"]}</p>
            <p>카테고리 : {st.session_state.quote_meta["category"]}</p>
            <p>레퍼런스 : {st.session_state.quote_meta["reference"]}</p>
        </div>
        """,
        unsafe_allow_html=True
        )
    
    st.session_state.new_quote






elif page=="발화자 추가":
    "여긴 공사중이라네"