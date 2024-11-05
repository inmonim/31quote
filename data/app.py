from typing import Callable
import streamlit as st
from sqlalchemy.orm import Session  # ORM 세션
from config import get_db  # 데이터베이스 연결 함수
from model import Quote, Speaker, Category, Reference, SpeakerCareer, ReferenceType  # ORM 모델

page = st.radio("페이지 선택", ["명언 추가", "발화자 추가", "레퍼런스 추가", "발화자 수정"])

floating = st.radio("플로팅 띄우기", ["예", "아니오"])

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

# 입력 필드와 관련된 실시간 검색 함수
def fetch_similar_quotes(query: str, db: Session):
    # 유사한 명언을 찾는 ORM 쿼리 예시
    return db.query(Quote).filter(Quote.ko_sentence.like(f"%{query}%")).limit(5).all()

def fetch_similar_speaker(speaker: str, db : Session):
    return db.query(Speaker).filter(Speaker.ko_name.like(f"%{speaker}%")).limit(5).all()

def fetch_similar_reference(reference: str, db : Session):
    return db.query(Reference).filter(Reference.reference_name.like(f"%{reference}%")).limit(5).all()

def fetch_similar_speaker_career(career: str, db : Session):
    return db.query(SpeakerCareer).filter(SpeakerCareer.speaker_career.like(f"%{career}%")).limit(5).all()

def fetch_all_category(db : Session):
    return db.query(Category).all()

def fetch_all_reference_type(db : Session):
    return db.query(ReferenceType).all()

def remove_null(data : dict):
    return {k:v for k, v in data.items() if v != "" or v != None}

def data_save(data, db : Session):
    db.add(data)
    db.commit()
    return True

if page == "명언 추가":

    new_quote = {"ko_sentence" : "",
                "en_sentence" : "",
                "category_id" : "",
                "speaker_id" : "",
                "reference_id": ""}
    
    meta = {"category" : "",
            "speaker_name" : "",
            "reference" : "",
            "reference_type" : "",
            "ready_create" : 0}

    if "new_quote" not in st.session_state:
        st.session_state.new_quote = new_quote
        st.session_state.quote_meta = meta

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
    
    
    if st.session_state.new_quote["category_id"]:
        "---"
        
        reference_input = st.text_input("레퍼런스를 입력해주세요")
        
        if reference_input:
            st.write("#### 레퍼런스 리스트:")
            references = fetch_similar_reference(reference_input, db)
            if references:
                for ref in references:
                    st.button(ref.reference_name)
            else:
                st.write("유사한 레퍼런스가 없습니다.")
        
    if (st.session_state.new_quote["ko_sentence"]
        and st.session_state.new_quote["category_id"]):
        
        if st.button("데이터 생성", type="primary") or st.session_state.quote_meta["ready_create"]:
            st.session_state.quote_meta["ready_create"] = 1
            st.session_state.new_quote
            if st.button("정말로 생성합니다", type="primary"):
                d = remove_null(st.session_state.new_quote)
                quote = Quote(**d)
                if data_save(quote, db):
                    st.write("생성 완료!")
            

    if floating == "예":
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
            font-weight : 600;
        }}
        </style>
        <div class="floating-container" style="font-size: 20px;">
            <h3>명언 추가 </h3>
            <p>한국어 : {st.session_state.new_quote["ko_sentence"]}</p>
            <p>영어 : {st.session_state.new_quote["en_sentence"]}</p>
            <p>발화자 : {st.session_state.quote_meta["speaker_name"]}</p>
            <p>카테고리 : {st.session_state.quote_meta["category"]}</p>
            <p>레퍼런스 : {st.session_state.quote_meta["reference"]}</p>
        </div>
        """,
        unsafe_allow_html=True
        )
    
elif page=="발화자 추가":
    
    new_speaker = {"ko_name" : "",
                   "org_name" : "",
                   "career" : "",
                   "speaker_description" : "",
                   "born_date" : "",
                   "death_date" : ""}
    
    speaker_meta = {"career" : ""}
    
    
    if "new_speaker" not in st.session_state:
        st.session_state.new_speaker = new_speaker
        st.session_state.speaker_meta = speaker_meta
    
    
    st.title("발화자 추가")
    
    speaker_kname = st.text_input("발화자의 한글 이름을 입력하세요")
    
    if speaker_kname:
        
        find_speaker = fetch_similar_speaker(speaker=speaker_kname, db=db)
        
        if find_speaker:
            container = st.container(border=True)
            container.write("#### 유사한 발화자 목록:")
            for speaker in find_speaker:
                n = speaker.ko_name
                s = n.index(speaker_kname)
                e = s + len(speaker_kname)
                d = f"{n[:s]}*{n[s:e]}*{n[e:]}"
                container.button(f"ko: {d}, org: {speaker.org_name}")

        else:
            st.write("### 유사한 발화자가 없습니다")
    
    if st.button("한글 이름 등록"):
        st.session_state.new_speaker["ko_name"] = speaker_kname
        st.write(f"#### 등록된 이름 : {st.session_state.new_speaker["ko_name"]}")
    
    "---"
    
    if st.session_state.new_speaker["ko_name"]:
    
        speaker_org_name = st.text_input("발화자의 본명을 입력하세요")
    
        if speaker_org_name:
            
            if st.button("본명 등록"):
                st.session_state.new_speaker["org_name"] = speaker_org_name
    
    cont = st.container(border=True)
    if st.session_state.new_speaker["org_name"]:
        
        speaker_career = cont.text_input("발화자의 직업을 입력하세요")
        
        careers = fetch_similar_speaker_career(speaker_career, db)
        
        if speaker_career:
            
            if careers:
                for c in careers:
                    if cont.button(f"{c.speaker_career}"):
                        st.session_state.new_speaker["career"] = c.speaker_career_id
                        st.session_state.speaker_meta["career"] = c.speaker_career
                    
        
    if st.session_state.new_speaker["org_name"]:
        
        speaker_desc = cont.text_input("발화자의 설명을 입력하세요")
        
        if speaker_desc:
            
            if cont.button("발화자 설명 등록"):
                st.session_state.new_speaker["speaker_description"] = speaker_desc
    
    if st.session_state.new_speaker["org_name"]:
        
        st.write("#### 생몰연도를 입력해주세요")
        
        col1, col2 = st.columns(2)
        
        born = col1.text_input("생년")
        death = col2.text_input("몰년")
        
        if born:
            bd = st.button("생몰연도 등록")
            st.session_state.new_speaker["born_date"] = born
            st.session_state.new_speaker["death_date"] = death
    
    if floating == "예":
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
            font-weight : 600;
        }}
        </style>
        <div class="floating-container" style="font-size: 20px;">
            <h3>발화자 추가 </h3>
            <p>한글 이름 : {st.session_state.new_speaker["ko_name"]}</p>
            <p>원어 영어 : {st.session_state.new_speaker["org_name"]}</p>
            <p>직업 : {st.session_state.speaker_meta["career"]}</p>
            <p>설명 : {st.session_state.new_speaker["speaker_description"]}</p>
            <p>생몰 년도 : {st.session_state.new_speaker["born_date"]} ~ {st.session_state.new_speaker["death_date"]}</p>
        </div>
        """,
        unsafe_allow_html=True
        )
    
elif page=="레퍼런스 추가":
    
    new_reference = {
        "reference_name" : "",
        "reference_org_name" : "",
        "year" : "",
        "reference_type_id" : "",
    }
    
    reference_meta = {
        "reference_type" : ""
    }
    
    if "new_reference" not in st.session_state:
        st.session_state.new_reference = new_reference
        st.session_state.reference_meta = reference_meta
    
    reference_input = st.text_input("레퍼런스의 한글 이름을 입력하세요")
    
    if reference_input:
        
        references = fetch_similar_reference(reference_input, db)
        cont1 = st.container(border=True)
        cont1.write("#### 유사한 레퍼런스:")
        if references:
            for ref in references:
                cont1.button(ref.reference_name)
        
        else:
            cont1.write("#### 유사한 레퍼런스가 없습니다.")
    
        if st.button("레퍼런스 등록"):
            
            st.session_state.new_reference["reference_name"] = reference_input
        
    cont2 = st.container(border=True)
    if st.session_state.new_reference["reference_name"]:
        
        reference_org_name = cont2.text_input("레퍼런스의 원어 이름을 입력하세요")
        
        if reference_org_name:
            cont2.button("원어 레퍼런스 등록")
            st.session_state.new_reference["reference_org_name"] = reference_org_name
    
    if st.session_state.new_reference["reference_name"]:
        
        year = cont2.text_input("연도를 입력하세요")
        if year and cont2.button("연도 등록"):
            st.session_state.new_reference["year"] = year
    
    
    if st.session_state.new_reference["reference_name"]:
        
        reference_type = fetch_all_reference_type(db)
        
        ref_func = lambda x : x.reference_type
        
        if reference_type:
            select_ref : None = st.selectbox("레퍼런스 타입을 선택해주세요",
                                             reference_type,
                                             index=None,
                                             format_func=ref_func,
                                             placeholder="레퍼런스 타입")
            if select_ref:
                st.session_state.new_reference["reference_type_id"] = select_ref.reference_type_id
                st.session_state.reference_meta["reference_type"] = select_ref.reference_type
            
        
    
    if floating == "예":
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
            font-weight : 600;
        }}
        </style>
        <div class="floating-container" style="font-size: 20px;">
            <h3>레퍼런스 추가 </h3>
            <p>한글 이름 : {st.session_state.new_reference["reference_name"]}</p>
            <p>원어 영어 : {st.session_state.new_reference["reference_org_name"]}</p>
            <p>연도 : {st.session_state.new_reference["year"]}</p>
            <p>타입 : {st.session_state.reference_meta["reference_type"]}</p>
        </div>
        """,
        unsafe_allow_html=True
        )

elif page=="발화자 수정":
    
    before_speaker = {
        "speaker_id" : "",
        "ko_name" : "",
        "org_name" : "",
        "speaker_career_id" : "",
        "speaker_description" : "",
        "born_date" : "",
        "death_date" : ""
        }
    
    speaker_meta = {
    "speaker_career" : "",
    "modify_ready" : ""
    }
    
    if "speaker" not in st.session_state:
        st.session_state.speaker = before_speaker
        st.session_state.s_meta = speaker_meta

    st.title("발화자 수정")
    
    speaker_name = st.text_input("수정할 발화자를 입력해주세용")
    
    if speaker_name:
        speakers = fetch_similar_speaker(speaker_name, db)
        
        if speakers:
            for s in speakers:
                if st.button(f"{s.ko_name} {s.org_name}"):                                     
                    st.session_state.speaker = {
                        "speaker_id" : s.speaker_id,
                        "ko_name" : s.ko_name,
                        "org_name" : s.org_name,
                        "speaker_career_id" : s.speaker_career.speaker_career_id if s.speaker_career else None,
                        "speaker_description" : s.speaker_description,
                        "born_date" : s.born_date,
                        "death_date" : s.death_date
                        }
                    
                    st.session_state.s_meta["speaker_career"] = s.speaker_career.speaker_career if s.speaker_career else None,
        else:
            st.write("유사한 발화자가 없습니다!")
    
    if st.session_state.speaker["speaker_id"]:

        new_ko_name = st.text_input("발화자의 이름을 수정하세요", value=st.session_state.speaker["ko_name"])
        if new_ko_name:
            st.session_state.speaker["ko_name"] = new_ko_name
        
        new_org_name = st.text_input("발화자의 원어 이름을 수정하세요", value=st.session_state.speaker["org_name"])
        if new_org_name:
            st.session_state.speaker["org_name"] = new_org_name
        
        new_speaker_career = st.text_input("발화자의 직업 수정", value=st.session_state.s_meta["speaker_career"])
        
        if new_speaker_career:
            careers = fetch_similar_speaker_career(new_speaker_career, db)
            
            if new_speaker_career:
                
                if careers:
                    for c in careers:
                        if st.button(f"{c.speaker_career}"):
                            st.session_state.speaker["speaker_career_id"] = c.speaker_career_id
                            st.session_state.s_meta["speaker_career"] = c.speaker_career
                        
            
        new_speaker_description = st.text_input("발화자의 설명 수정", value=st.session_state.speaker["speaker_description"])
        
        if new_speaker_description:
            st.session_state.speaker["speaker_description"] = new_speaker_description
        
        col1, col2 = st.columns(2)
        
        born = col1.text_input("생년", value=st.session_state.speaker["born_date"])
        if born:
            st.session_state.speaker["born_date"] = born
        death = col2.text_input("몰년", value=st.session_state.speaker["death_date"])
        if death:
            st.session_state.speaker["death_date"] = death
    
    if st.session_state.speaker["ko_name"]:
        
        if st.button("발화자 수정하기!") or st.session_state.s_meta["modify_ready"] == 1:
            st.session_state.s_meta["modify_ready"] = 1
            st.session_state.speaker
            
            if st.button("진짤루요?", type="primary"):
                d = st.session_state.speaker
                bf : Speaker = db.query(Speaker).get(d["speaker_id"])
                
                bf.ko_name = d["ko_name"]
                bf.org_name = d["org_name"]
                bf.speaker_career_id = d["speaker_career_id"]
                bf.born_date = d["born_date"]
                bf.death_date = d["death_date"]
                bf.speaker_description = d["speaker_description"]
                
                db.commit()
                
                st.session_state.s_meta["modify_ready"] = 2
        
        if st.session_state.s_meta["modify_ready"] == 2:
            st.write("수정 완료!")
    
    if floating == "예":
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
            font-weight : 600;
        }}
        </style>
        <div class="floating-container" style="font-size: 20px;">
            <h3>발화자 추가 </h3>
            <p>ID : {st.session_state.speaker["speaker_id"]}</p>
            <p>한글 이름 : {st.session_state.speaker["ko_name"]}</p>
            <p>원어 영어 : {st.session_state.speaker["org_name"]}</p>
            <p>직업 : {st.session_state.s_meta["speaker_career"]}, {st.session_state.speaker["speaker_career_id"]}</p>
            <p>설명 : {st.session_state.speaker["speaker_description"]}</p>
            <p>생몰 년도 : {st.session_state.speaker["born_date"]} ~ {st.session_state.speaker["death_date"]}</p>
        </div>
        """,
        unsafe_allow_html=True
        )