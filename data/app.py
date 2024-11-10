from typing import Callable
import streamlit as st
from sqlalchemy.orm import Session  # ORM 세션
from config import get_db  # 데이터베이스 연결 함수
from model import Quote, Speaker, Category, Reference, SpeakerCareer, ReferenceType  # ORM 모델

page = st.radio("작업 선택", ["명언 추가", "발화자 추가", "레퍼런스 추가", "발화자 직업 추가", "레퍼런스 타입 추가", "발화자 수정", "명언 수정"])

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
    .floating-container {
        position: fixed;
        bottom: 10%;
        right: 2%;
        width: 300px;
        padding: 20px;
        background-color: #ee4d30;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        z-index: 100;
    }
    
    p {
        font-size : 18px;
        font-weight : 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# DB 연결 설정
db = next(get_db())

def fetch_similar_quotes(query: str, db: Session):
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
    return {k:v for k, v in data.items() if v != "" and v != None}

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
    
    new_quote_meta = {"category" : "",
            "speaker_name" : "",
            "reference" : "",
            "reference_type" : "",
            "ready_create" : False,
            "reference_create" : False}

    if "new_quote" not in st.session_state:
        st.session_state.new_quote = new_quote
        st.session_state.new_quote_meta = new_quote_meta

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
                container.write(f"- {quote.ko_sentence} (speak: {quote.speaker.ko_name})")
            
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
                    st.session_state.new_quote_meta["speaker_name"] = speaker.ko_name
            
            if st.session_state.new_quote["speaker_id"]:
                st.write(f"선택된 발화자 : {st.session_state.new_quote_meta["speaker_name"]}")
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
                st.session_state.new_quote_meta["category"] = category.category
            
            if st.session_state.new_quote["category_id"]:
                st.write(f"선택된 카테고리 : **{st.session_state.new_quote_meta["category"]}**")
    
    
    if st.session_state.new_quote["category_id"]:
        "---"
        
        reference_input = st.text_input("레퍼런스를 입력해주세요")
        
        if reference_input:
            st.write("#### 레퍼런스 리스트:")
            references = fetch_similar_reference(reference_input, db)
            if references:
                for ref in references:
                    if st.button(ref.reference_name):
                        st.session_state.new_quote["reference_id"] = ref.reference_id
                        st.session_state.new_quote_meta["reference"] = ref.reference_name
            else:
                st.write("유사한 레퍼런스가 없습니다.")
                
        if not st.session_state.new_quote_meta["reference"]:
            if st.button("레퍼런스 추가하기!") or st.session_state.new_quote_meta["reference_create"]:
                st.session_state.new_quote_meta["reference_create"] = True
                
                new_reference = {
                    "reference_name" : "",
                    "reference_org_name" : "",
                    "year" : "",
                    "reference_type_id" : "",
                }
                
                ref_meta = {
                    "reference_type" : "",
                    "create_ready" : False
                }
                
                if "new_reference" not in st.session_state:
                    st.session_state.new_reference = new_reference
                    st.session_state.ref_meta = ref_meta
                
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
                            st.session_state.ref_meta["reference_type"] = select_ref.reference_type
                
                if st.session_state.new_reference["reference_type_id"]:
                    
                    if st.button("레퍼런스 추가") or st.session_state.ref_meta["create_ready"]:
                        st.session_state.ref_meta["create_ready"] = True
                        st.session_state.new_reference
                        
                        if st.button("진짤루요?", type="primary"):
                            
                            d = remove_null(st.session_state.new_reference)
                            new_ref = Reference(**d)
                            db.add(new_ref)
                            db.commit()
                            
                            st.write(f"### {reference_input} 추가 완료! 다시 검색해주세요!")
                            
                            st.session_state.new_reference = new_reference
                            st.session_state.ref_meta = ref_meta
                            st.session_state.new_quote_meta["reference_create"] = False

    if (st.session_state.new_quote["ko_sentence"]
        and st.session_state.new_quote["category_id"]):
        
        if st.button("데이터 생성", type="primary") or st.session_state.new_quote_meta["ready_create"]:
            st.session_state.new_quote_meta["ready_create"] = True
            st.session_state.new_quote
            if st.button("진짤루요?", type="primary"):
                d = remove_null(st.session_state.new_quote)
                quote = Quote(**d)
                if data_save(quote, db):
                    st.write(f"{quote_input[-10:]}... 생성 완료!")
                    st.session_state.new_quote = new_quote
                    st.session_state.new_quote_meta = new_quote_meta
            

    if floating == "예":
        st.markdown(
        f"""
        <div class="floating-container" style="font-size: 20px;">
            <h3>명언 추가 </h3>
            <p>한국어 : {st.session_state.new_quote["ko_sentence"]}</p>
            <p>영어 : {st.session_state.new_quote["en_sentence"]}</p>
            <p>발화자 : {st.session_state.new_quote_meta["speaker_name"]}</p>
            <p>카테고리 : {st.session_state.new_quote_meta["category"]}</p>
            <p>레퍼런스 : {st.session_state.new_quote_meta["reference"]}</p>
        </div>
        """,
        unsafe_allow_html=True
        )
    
elif page=="발화자 추가":
    
    new_speaker = {"ko_name" : "",
                   "org_name" : "",
                   "speaker_career_id" : "",
                   "speaker_description" : "",
                   "born_date" : "",
                   "death_date" : ""}
    
    new_speaker_meta = {"career" : "",
            "create_ready": False}
    
    
    if "new_speaker" not in st.session_state or "new_speaker_meta" not in st.session_state:
        st.session_state.new_speaker = new_speaker
        st.session_state.new_speaker_meta = new_speaker_meta
    
    
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
        
        if st.session_state.new_speaker["ko_name"]:
        
            speaker_org_name = st.text_input("발화자의 본명을 입력하세요")
        
            if speaker_org_name:
                
                if st.button("본명 등록"):
                    st.session_state.new_speaker["org_name"] = speaker_org_name
        
        cont = st.container(border=True)
        if st.session_state.new_speaker["org_name"]:
            
            speaker_career = cont.text_input("발화자의 직업을 입력하세요")
            
            
            if speaker_career:
                careers = fetch_similar_speaker_career(speaker_career, db)
                
                if careers:
                    for c in careers:
                        if cont.button(f"{c.speaker_career}"):
                            st.session_state.new_speaker["speaker_career_id"] = c.speaker_career_id
                            st.session_state.new_speaker_meta["career"] = c.speaker_career
                else:
                    cont.write("#### 유사한 직업이 없습니다!")
                            
            
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
                if st.button("생몰연도 등록"):
                    st.session_state.new_speaker["born_date"] = born
                    st.session_state.new_speaker["death_date"] = death
        
        if st.session_state.new_speaker["org_name"]:
            
            if st.button("발화자 등록") or st.session_state.new_speaker_meta["create_ready"]:
                
                st.session_state.new_speaker
                st.session_state.new_speaker_meta["create_ready"] = True
                
                if st.button("진짤루요?", type="primary"):
                    
                    d = st.session_state.new_speaker
                    d = remove_null(d)
                    speaker = Speaker(**d)
                    if st.session_state.new_speaker_meta["create_ready"]:
                        db.add(speaker)
                        db.commit()
                    
                    st.write(f"#### {speaker.ko_name} 생성 완료!")
                    st.session_state.new_speaker = new_speaker
                    st.session_state.new_speaker_meta = new_speaker_meta
                
            
    
    if floating == "예":
        st.markdown(
        f"""
        <div class="floating-container" style="font-size: 20px;">
            <h3>발화자 추가 </h3>
            <p>한글 이름 : {st.session_state.new_speaker["ko_name"]}</p>
            <p>원어 영어 : {st.session_state.new_speaker["org_name"]}</p>
            <p>직업 : {st.session_state.new_speaker_meta["career"]}</p>
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
    
    new_reference_meta = {
        "reference_type" : "",
        "create_ready" : False
    }
    
    if "new_reference" not in st.session_state or "meta" not in st.session_state:
        st.session_state.new_reference = new_reference
        st.session_state.new_reference_meta = new_reference_meta
        
    st.title("레퍼런스 추가")
    
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
                st.session_state.new_reference_meta["reference_type"] = select_ref.reference_type
    
    if st.session_state.new_reference["reference_type_id"]:
        
        if st.button("레퍼런스 추가") or st.session_state.meta["create_ready"]:
            st.session_state.new_reference_meta["create_ready"] = True
            st.session_state.new_reference
            
            if st.button("진짤루요?", type="primary"):
                
                d = remove_null(st.session_state.new_reference)
                new_ref = Reference(**d)
                db.add(new_ref)
                db.commit()
                
                st.write(f"### {reference_input} 추가 완료!")
                
                st.session_state.new_reference = new_reference
                st.session_state.new_reference_meta = new_reference_meta
            
        
    
    if floating == "예":
        st.markdown(
        f"""
        <div class="floating-container" style="font-size: 20px;">
            <h3>레퍼런스 추가 </h3>
            <p>한글 이름 : {st.session_state.new_reference["reference_name"]}</p>
            <p>원어 영어 : {st.session_state.new_reference["reference_org_name"]}</p>
            <p>연도 : {st.session_state.new_reference["year"]}</p>
            <p>타입 : {st.session_state.new_reference_meta["reference_type"]}</p>
        </div>
        """,
        unsafe_allow_html=True
        )

elif page=="발화자 직업 추가":
    
    if 'new_sp_career' not in st.session_state:
        st.session_state.new_sp_career = None
        st.session_state.create = None
        
    st.title("발화자 직업 추가")
    
    career = st.text_input("발화자의 직업을 입력해주세요")
    
    if career and not st.session_state.create:
        
        careers = fetch_similar_speaker_career(career, db)
        
        if careers:
            for career in careers:
                st.button(career.speaker_career)
        elif not st.session_state.create:
            st.write("#### 유사한 직업이 없습니다")
            if st.button("직업 추가하기") or st.session_state.new_sp_career:
                st.session_state.new_sp_career = career
                st.session_state.new_sp_career
                
                if st.button("진짤루요?", type="primary"):
                    new_sp_career = SpeakerCareer(speaker_career = career)
                    db.add(new_sp_career)
                    db.commit()
                    st.session_state.create = True
                    if st.session_state.create:
                        st.write(f"#### {career} 추가 완료!")
                        st.session_state.clear()

elif page=="레퍼런스 타입 추가":

    if 'new_ref_type' not in st.session_state:
        st.session_state.new_ref_type = None
        st.session_state.create = None
        
    st.title("레퍼런스 타입 추가")
    
    new_type = st.text_input("레퍼런스 타입을 입력해주세요")
    
    if new_type and not st.session_state.create:
        
        ref_types = fetch_all_reference_type(db)
        
        if ref_types:
            for ref_type in ref_types:
                st.button(ref_type.reference_type)
        elif not st.session_state.create:
            st.write("#### 유사한 타입이 없습니다")
            if st.button("레퍼런스 타입 추가하기") or st.session_state.new_ref_type:
                st.session_state.new_ref_type = new_type
                st.session_state.new_ref_type
                
                if st.button("진짤루요?", type="primary"):
                    new_ref_type = ReferenceType(reference_type = new_type)
                    db.add(new_ref_type)
                    db.commit()
                    st.session_state.create = True
                    if st.session_state.create:
                        st.write(f"#### {new_ref_type} 추가 완료!")
                        st.session_state.clear()

elif page=="명언 수정":
    
    modify_quote = {
        "quote_id" : None,
        "ko_sentence" : "",
        "en_sentence" : "",
        "category_id" : "",
        "speaker_id" : "",
        "reference_id": ""}
    
    modify_quote_meta = {
        "category" : "",
        "category_change": False,
        "speaker_name" : "",
        "speaker_change" : False,
        "reference" : "",
        "reference_type" : "",
        "ready_modify" : False,
        "reference_change" : False}
    
    if "modify_quote" not in st.session_state:
        st.session_state.modify_quote = modify_quote
        st.session_state.modify_quote_meta = modify_quote_meta
    
    modify_quote_input = st.text_input("한글 명언을 입력해주세요")
    
    if modify_quote_input:
        
        quotes : list[Quote] = fetch_similar_quotes(modify_quote_input, db)
        
        if quotes:
            for quote in quotes:
                if st.button(f"{quote.ko_sentence}"):
                    q = {"quote_id" : quote.quote_id,
                         "ko_sentence" : quote.ko_sentence,
                         "en_sentence" : quote.en_sentence,
                         "category_id" : quote.category_id,
                         "speaker_id" : quote.speaker_id,
                         "reference_id": quote.reference_id}
                    st.session_state.modify_quote = q
                    m = {"category" : quote.category.category,
                         "category_change": False,
                         "speaker_name" : quote.speaker.ko_name if quote.speaker_id else None,
                         "speaker_change" : False,
                         "reference" : quote.reference.reference_name if quote.reference_id else None,
                         "reference_type" : quote.reference.reference_type.reference_type if quote.reference else None,
                         "ready_modify" : False,
                         "reference_change" : False}
                    st.session_state.modify_quote_meta = m
        
        if st.session_state.modify_quote["ko_sentence"]:
            new_ko_sentence =st.text_input("한글 명언", value=st.session_state.modify_quote["ko_sentence"])
            if st.button("한글 명언 수정"):
                st.session_state.modify_quote["ko_sentence"] = new_ko_sentence
        
        if st.session_state.modify_quote["ko_sentence"]:
            new_en_sentence = st.text_input("영어 명언", value=st.session_state.modify_quote["en_sentence"])
            if st.button("영어 명언 수정"):
                st.session_state.modify_quote["en_sentence"] = new_en_sentence
        
        if st.session_state.modify_quote["ko_sentence"]:
            new_speaker = st.text_input("발화자 이름", value=f"{st.session_state.modify_quote_meta["speaker_name"]}")
            if new_speaker:
                speakers = fetch_similar_speaker(new_speaker, db)
                
                if speakers:
                    for speaker in speakers:
                        if st.button(f"{speaker.ko_name}"):
                            st.session_state.modify_quote["speaker_id"] = speaker.speaker_id
                            st.session_state.modify_quote_meta["speaker_name"] = speaker.ko_name
                            
        st.write(f"선택된 발화자 : {st.session_state.modify_quote_meta["speaker_name"]}")
            
        if st.session_state.modify_quote["ko_sentence"]:
            categorys = fetch_all_category(db)
            if categorys:
                st.write("#### 카테고리 리스트:")
                format_func : Callable[[Category], str] = lambda x : x.category
                category : None = st.selectbox("카테고리 선택", categorys, index=False, format_func=format_func, placeholder="카테고리를 선택해주세요")
                if category:
                    st.session_state.modify_quote["category_id"] = category.category_id
                    st.session_state.modify_quote_meta["category"] = category.category
                    st.session_state.modify_quote_meta["category_change"] = True
                
                if st.session_state.modify_quote_meta["category_change"]:
                    st.write(f"수정된 카테고리 : **{st.session_state.modify_quote_meta["category"]}**")
        
        if st.session_state.modify_quote["ko_sentence"]:
            new_reference = st.text_input("레퍼런스", value=st.session_state.modify_quote_meta["reference"])
            
            if st.button("레퍼런스 없이 기입"):
                st.session_state.modify_quote_meta["reference"] = "없음"
                st.session_state.modify_quote["reference_id"] = 1
            
            if new_reference:
                references = fetch_similar_reference(new_reference, db)
            
                if references:
                    for reference in references:
                        if st.button(f"{reference.reference_name}"):
                            st.session_state.modify_quote["reference_id"] = reference.reference_id
                            st.session_state.modify_quote_meta["reference"] = reference.reference_name
                            st.session_state.modify_quote_meta["reference_change"] = True
                
                if st.session_state.modify_quote_meta["reference_change"]:
                    st.write(f"수정된 레퍼런스 : {st.session_state.modify_quote_meta["reference"]}")
        
        if st.session_state.modify_quote["ko_sentence"]:
            
            if st.button("수정하기") or st.session_state.modify_quote_meta["ready_modify"]:
                st.session_state.modify_quote_meta["ready_modify"] = True
                st.session_state.modify_quote
                st.session_state.modify_quote_meta
                if st.button("진짤루요?"):
                    d = remove_null(st.session_state.modify_quote)
                    quote = Quote(**d)
                    db.merge(quote)
                    db.commit()
                    st.session_state.modify_quote = modify_quote
                    st.session_state.modify_quote_meta = modify_quote_meta
                    st.write("## 수정 완료!")
    
    if floating == "예":
        st.markdown(
        f"""
        <div class="floating-container" style="font-size: 20px;">
            <h3>명언 수정 </h3>
            <p>한국어 : {st.session_state.modify_quote["ko_sentence"]}</p>
            <p>영어 : {st.session_state.modify_quote["en_sentence"]}</p>
            <p>발화자 : {st.session_state.modify_quote_meta["speaker_name"]}</p>
            <p>카테고리 : {st.session_state.modify_quote_meta["category"]}</p>
            <p>레퍼런스 : {st.session_state.modify_quote_meta["reference"]}</p>
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
        
        if st.button("발화자 수정하기!") or st.session_state.s_meta["modify_ready"]:
            st.session_state.s_meta["modify_ready"] = True
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
                
                st.session_state.s_meta["modify_ready"] = False
                st.write("수정 완료!")
                st.session_state.speaker = before_speaker
                st.session_state.s_meta = speaker_meta
    
    if floating == "예":
        st.markdown(
        f"""
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
        
        