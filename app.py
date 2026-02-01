import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="🎬 AI Content Generator - FREE & PRO",
    page_icon="🎬",
    layout="wide"
)

# 세션 상태 초기화
if 'api_keys_saved' not in st.session_state:
    st.session_state.api_keys_saved = False

if 'mode' not in st.session_state:
    st.session_state.mode = 'FREE'

# 타이틀
st.title("🎬 AI Content Generator")
st.markdown("**FREE & PRO 통합 버전**")

# 사이드바 - 모드 선택
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 모드 선택
    mode = st.radio(
        "📂 모드 선택",
        ["FREE (무료, 수동)", "PRO (유료, 자동)"],
        help="FREE: Gemini만 사용 | PRO: 모든 API 사용, 자동 생성"
    )
    
    st.session_state.mode = 'FREE' if 'FREE' in mode else 'PRO'
    
    st.divider()
    
    # API 키 입력
    st.subheader("🔑 API 키 입력")
    
    # Gemini API (필수)
    gemini_key = st.text_input(
        "Gemini API Key (필수)",
        type="password",
        value=st.session_state.get('gemini_api_key', ''),
        help="https://aistudio.google.com/app/apikey"
    )
    
    # PRO 모드 추가 API
    if st.session_state.mode == 'PRO':
        st.warning("⚠️ PRO 모드는 3개 API 키가 모두 필요합니다!")
        
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get('openai_api_key', ''),
            help="음성 생성용"
        )
        
        replicate_key = st.text_input(
            "Replicate API Key",
            type="password",
            value=st.session_state.get('replicate_api_key', ''),
            help="이미지 생성용 (Flux)"
        )
    else:
        openai_key = ''
        replicate_key = ''
    
    # API 키 저장하기
    if st.button("💾 API 키 저장하기", use_container_width=True):
        if gemini_key:
            st.session_state.gemini_api_key = gemini_key
            
            if st.session_state.mode == 'PRO':
                if openai_key and replicate_key:
                    st.session_state.openai_api_key = openai_key
                    st.session_state.replicate_api_key = replicate_key
                    st.session_state.api_keys_saved = True
                    st.success("✅ PRO 모드 API 키 저장 완료!")
                else:
                    st.warning("⚠️ PRO 모드는 3개 API 키가 모두 필요합니다")
            else:
                st.session_state.api_keys_saved = True
                st.success("✅ FREE 모드 API 키 저장 완료!")
        else:
            st.error("❌ Gemini API 키는 필수입니다!")

# 메인 콘텐츠
if not st.session_state.api_keys_saved:
    st.warning("⚠️ 먼저 사이드바에서 API 키를 입력해주세요!")
else:
    # 설정 옵션들
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        language = st.selectbox(
            "🌐 언어",
            ["한국어 (KR)", "영어 (EN)", "일본어 (JP)"]
        )
    
    with col2:
        character_style = st.selectbox(
            "🎭 캐릭터 스타일",
            ["📱 비즈니스맨", "👨‍🏫 선생님", "🎨 크리에이터", "👔 전문가", "🎬 감독", "💼 기업인"]
        )
    
    with col3:
        tone_style = st.selectbox(
            "🗣️ 말투",
            ["😊 친근+유머 (유튜브)", "🎓 교육+설명 (강의)", "💼 전문+신뢰 (리뷰)", "📰 뉴스 (보도)", "🎩 근엄 (공식)"]
        )
    
    with col4:
        voice_style = st.selectbox(
            "🎤 보이스 톤",
            ["🌟 밝고 경쾌한", "🎯 차분한 전문가", "💪 힘있는 리더", "🤗 따뜻한 선생님", "⚡ 에너지 넘치는", "🌙 부드러운"]
        )
    
    col5, col6 = st.columns(2)
    
    with col5:
        aspect_ratio = st.selectbox(
            "📐 화면 비율",
            ["세로형 (9:16)", "가로형 (16:9)", "1:1 (정사각형)"]
        )
    
    # Scene 설정
    st.divider()
    st.subheader("🎬 Scene 설정")
    
    if st.session_state.mode == 'FREE':
        scene_count = st.slider(
            "Scene 개수",
            min_value=3,
            max_value=20,
            value=10,
            help="FREE 모드: 3~20개"
        )
    else:
        # PRO 모드: 롱폼 옵션
        use_longform = st.checkbox("🎥 롱폼 모드 (5~20분)")
        
        if use_longform:
            longform_duration = st.selectbox(
                "롱폼 영상 시간",
                ["5분 (약 30개)", "10분 (약 65개)", "15분 (약 135개)", "20분 (약 200개)"]
            )
            
            duration_map = {"5분": 30, "10분": 65, "15분": 135, "20분": 200}
            scene_count = duration_map[longform_duration.split(" ")[0]]
        else:
            scene_count = st.slider(
                "Scene 개수",
                min_value=30,
                max_value=200,
                value=30,
                help="PRO 모드: 30~200개"
            )
    
    # 기사 내용 입력
    st.divider()
    st.subheader("📝 기사 내용 입력")
    
    article_content = st.text_area(
        "영상으로 만들 기사나 텍스트를 입력하세요",
        height=200,
        placeholder="여기에 기사 내용을 붙여넣으세요..."
    )
    
    # 대본 생성 버튼
    if st.button("🎬 대본 생성하기", type="primary", use_container_width=True):
        if not article_content:
            st.error("❌ 기사 내용을 입력해주세요!")
        else:
            with st.spinner("🎬 AI가 대본을 생성하고 있습니다..."):
                try:
                    # Gemini API 설정 - 최신 방식
                    genai.configure(api_key=st.session_state.gemini_api_key)
                    
                    # 안전한 모델 선택
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                    
                    # 말투 스타일 매핑
                    tone_map = {
                        "😊 친근+유머 (유튜브)": "친근하고 유머러스한 유튜브 톤으로, '여러분~', '대박!', '그죠?' 같은 표현을 자연스럽게 사용하세요.",
                        "🎓 교육+설명 (강의)": "교육적이고 설명하는 강의 톤으로, '~해볼게요', '함께~', '천천히' 같은 표현을 사용하세요.",
                        "💼 전문+신뢰 (리뷰)": "전문적이고 신뢰감 있는 리뷰 톤으로, '~라고 볼 수 있습니다', '~것으로 나타났습니다' 같은 표현을 사용하세요.",
                        "📰 뉴스 (보도)": "격식 있고 전문적인 뉴스 보도 톤으로, '~합니다', '~입니다' 같은 표현을 사용하세요.",
                        "🎩 근엄 (공식)": "권위 있고 진지한 공식 발표 톤으로, '~하십시오', '~하는 바입니다' 같은 표현을 사용하세요."
                    }
                    
                    tone_instruction = tone_map.get(tone_style, tone_map["😊 친근+유머 (유튜브)"])
                    
                    # 프롬프트 생성
                    prompt = f"""
당신은 {character_style} 스타일의 전문 영상 대본 작가입니다.
아래 기사를 {scene_count}개의 Scene으로 나누어 영상 대본을 작성해주세요.

**말투 스타일:**
{tone_instruction}

**설정:**
- 언어: {language}
- 캐릭터: {character_style}
- 보이스: {voice_style}
- 화면비율: {aspect_ratio}

**기사 내용:**
{article_content}

**출력 형식:**
Scene 1: [짧은 제목]
[대본 내용...]

Scene 2: [짧은 제목]
[대본 내용...]

(이하 Scene {scene_count}까지 계속)

**주의사항:**
- 각 Scene은 짧고 임팩트 있게
- 시청자의 흥미를 끌 수 있도록
- {tone_style.split(' ')[1]} 말투를 반영
- 자연스러운 문장 흐름
"""
                    
                    # 대본 생성
                    response = model.generate_content(prompt)
                    script = response.text
                    
                    st.session_state.generated_script = script
                    st.success("✅ 대본 생성 완료!")
                    
                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")
                    st.info("💡 API 키를 확인해주세요!\n\nGemini API Key: https://aistudio.google.com/app/apikey")
    
    # 생성된 대본 표시
    if 'generated_script' in st.session_state:
        st.divider()
        st.success("✅ 대본 생성 완료!")
        
        # 다운로드 버튼들
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                "📝 대본 다운로드 (TXT)",
                st.session_state.generated_script,
                file_name=f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_btn2:
            if st.button("🎨 이미지 프롬프트 생성하기", use_container_width=True):
                with st.spinner("🎨 이미지 프롬프트 생성 중..."):
                    try:
                        model = genai.GenerativeModel('gemini-3-flash-preview')
                        
                        prompt_gen = f"""
아래 대본의 각 Scene에 대해 영어로 이미지 생성 프롬프트를 만들어주세요.

대본:
{st.session_state.generated_script}

각 Scene마다 다음 형식으로:
Scene 1: [영어 이미지 프롬프트]
Scene 2: [영어 이미지 프롬프트]
...
"""
                        
                        response = model.generate_content(prompt_gen)
                        image_prompts = response.text
                        
                        st.session_state.image_prompts = image_prompts
                        st.success("✅ 이미지 프롬프트 생성 완료!")
                        
                    except Exception as e:
                        st.error(f"❌ 오류: {str(e)}")
        
        # 대본 표시
        st.markdown("### 📌 생성된 대본")
        st.text_area(
            "대본",
            st.session_state.generated_script,
            height=400,
            key="script_display"
        )
        
        # 이미지 프롬프트 표시
        if 'image_prompts' in st.session_state:
            st.markdown("### 🎨 이미지 프롬프트")
            st.text_area(
                "프롬프트",
                st.session_state.image_prompts,
                height=300,
                key="prompts_display"
            )
            
            st.download_button(
                "📋 프롬프트 다운로드 (TXT)",
                st.session_state.image_prompts,
                file_name=f"image_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        # 다음 단계 안내
        if st.session_state.mode == 'FREE':
            st.info("""
**📌 FREE 모드 - 다음 단계:**

1. 📝 대본 다운로드 (완료)
2. 🎨 이미지 생성: Leonardo.ai 등에서 수동 생성
3. 🎤 음성 생성: CapCut 또는 ElevenLabs 사용
4. 🎬 영상 편집: 수동 편집
""")
        else:
            st.info("""
**⚡ PRO 모드 - 자동 생성 가능!**

다음 기능 자동 생성 (개발 필요):
1. 🎨 이미지: Replicate Flux로 자동 생성
2. 🎤 음성: OpenAI TTS로 자동 생성  
3. 📥 파일 자동 다운로드

**예상 비용:** 이미지 ~₩1,800 + 음성 ~₩270 ≈ ₩2,100
""")

# 푸터
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
🎬 AI Content Generator | FREE & PRO 통합 버전<br>
어디서든 접속 가능한 웹 기반 도구
</div>
""", unsafe_allow_html=True)
       