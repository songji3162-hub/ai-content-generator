import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="AI Content Generator - FREE & PRO",
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
st.markdown("### FREE & PRO 통합 버전")

# 사이드바 - 모드 선택
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 모드 선택
    mode = st.radio(
        "모드 선택",
        ["FREE (무료, 수동)", "PRO (유료, 자동)"],
        help="FREE: Gemini만 사용, 수동 생성 | PRO: 모든 API 사용, 자동 생성"
    )
    
    st.session_state.mode = 'FREE' if 'FREE' in mode else 'PRO'
    
    st.divider()
    
    # API 키 입력
    st.subheader("🔑 API 키")
    
    # Gemini API (필수)
    gemini_key = st.text_input(
        "Gemini API Key (필수)",
        type="password",
        value=st.session_state.get('gemini_api_key', ''),
        help="https://aistudio.google.com/app/apikey"
    )
    
    # PRO 모드 전용 API
    if st.session_state.mode == 'PRO':
        st.markdown("**PRO 모드 전용:**")
        
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
    
    # API 키 저장
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
            st.error("❌ Gemini API Key는 필수입니다!")
    
    st.divider()
    
    # 현재 모드 상태 표시
    if st.session_state.mode == 'FREE':
        st.info("""
        **🆓 FREE 모드**
        - Gemini API만 사용
        - Scene: 3~20개
        - 수동 이미지/음성 생성
        - 완전 무료
        """)
    else:
        st.info("""
        **💎 PRO 모드**
        - API 3개 모두 사용
        - Scene: 30~200개
        - 자동 이미지/음성 생성
        - 롱폼 모드 지원
        - 15분 영상 → 20분 완성
        """)

# 메인 콘텐츠
if not st.session_state.api_keys_saved:
    st.warning("⚠️ 왼쪽 사이드바에서 API 키를 입력하고 저장해주세요!")
    st.stop()

# 기본 설정
col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "언어 선택",
        ["한국어", "English", "日本語"]
    )

with col2:
    character_style = st.selectbox(
        "캐릭터 스타일",
        ["👔 비즈니스맨", "👨‍🏫 선생님", "🎨 크리에이터", "💼 전문가", 
         "🌟 인플루언서", "📰 뉴스 앵커", "🎭 엔터테이너", "🔬 과학자",
         "👨‍💻 개발자", "📚 교수"]
    )

col3, col4 = st.columns(2)

with col3:
    voice_style = st.selectbox(
        "보이스 스타일",
        ["부드럽고 신뢰감 있는 남성", "명랑하고 친근한 여성", "차분하고 전문적인 남성",
         "활기차고 에너제틱한 여성", "진지하고 무게감 있는 남성"]
    )

with col4:
    aspect_ratio = st.selectbox(
        "화면 비율",
        ["16:9 (유튜브)", "9:16 (쇼츠)", "1:1 (인스타그램)"]
    )

# Scene 설정
st.divider()
st.subheader("📝 Scene 설정")

if st.session_state.mode == 'FREE':
    scene_count = st.slider(
        "Scene 개수",
        min_value=3,
        max_value=20,
        value=10,
        help="FREE 모드: 최대 20개"
    )
else:
    # PRO 모드: 롱폼 옵션
    use_longform = st.checkbox("🎬 롱폼 모드 사용하기")
    
    if use_longform:
        longform_duration = st.selectbox(
            "영상 길이",
            ["5분", "10분", "15분", "20분"]
        )
        
        duration_map = {"5분": 30, "10분": 65, "15분": 135, "20분": 200}
        scene_count = duration_map[longform_duration]
        
        st.info(f"📊 {longform_duration} 영상 = 약 {scene_count}장 이미지 생성")
    else:
        scene_count = st.slider(
            "Scene 개수",
            min_value=30,
            max_value=200,
            value=50,
            help="PRO 모드: 최대 200개"
        )

# 기사 내용 입력
st.divider()
st.subheader("📄 기사 내용 입력")

article_content = st.text_area(
    "영상으로 만들 기사나 텍스트를 입력하세요",
    height=300,
    placeholder="여기에 기사 내용을 붙여넣으세요..."
)

# 대본 생성 버튼
if st.button("🎬 대본 생성하기", type="primary", use_container_width=True):
    if not article_content:
        st.error("❌ 기사 내용을 입력해주세요!")
    else:
        with st.spinner("🔄 AI가 대본을 생성하고 있습니다..."):
            try:
                # Gemini API 설정 - 최신 방식
                genai.configure(api_key=st.session_state.gemini_api_key)
                
                # 안전한 모델 선택
                model = genai.GenerativeModel('gemini-2.0-flash-exp')
                
                # 프롬프트 생성
                prompt = f"""
당신은 전문 영상 대본 작가입니다.
아래 기사를 {scene_count}개의 Scene으로 나누어 영상 대본을 작성해주세요.

**설정:**
- 언어: {language}
- 캐릭터: {character_style}
- 보이스 톤: {voice_style}
- Scene 수: {scene_count}개

**기사 내용:**
{article_content}

**출력 형식:**
Scene 1: [대본 내용]
Scene 2: [대본 내용]
...

각 Scene은 자연스럽게 연결되어야 하며, {character_style}의 톤으로 작성해주세요.
"""
                
                # 대본 생성
                response = model.generate_content(prompt)
                script = response.text
                
                st.session_state.script = script
                st.success("✅ 대본 생성 완료!")
                
                # 대본 표시
                st.subheader("📝 생성된 대본")
                st.text_area("대본", script, height=400, key="script_display")
                
                # 대본 다운로드
                st.download_button(
                    "💾 대본 다운로드 (TXT)",
                    script,
                    file_name=f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
                # 이미지 프롬프트 생성 버튼
                if st.button("🎨 이미지 프롬프트 생성하기", key="gen_prompts"):
                    with st.spinner("🔄 이미지 프롬프트 생성 중..."):
                        prompt_gen = f"""
위 대본의 각 Scene에 맞는 이미지 생성 프롬프트를 영어로 작성해주세요.

**형식:**
Scene 1: [영어 프롬프트]
Scene 2: [영어 프롬프트]
...

각 프롬프트는:
- 구체적이고 상세하게
- 시각적 요소 강조
- {aspect_ratio} 비율에 적합하게
- {character_style} 스타일 반영

대본:
{script}
"""
                        
                        img_response = model.generate_content(prompt_gen)
                        image_prompts = img_response.text
                        
                        st.session_state.image_prompts = image_prompts
                        
                        st.subheader("🎨 이미지 프롬프트")
                        st.text_area("프롬프트", image_prompts, height=400, key="prompts_display")
                        
                        # 다운로드
                        st.download_button(
                            "💾 이미지 프롬프트 다운로드",
                            image_prompts,
                            file_name=f"image_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="download_prompts"
                        )
                        
                        # 다음 단계 안내
                        if st.session_state.mode == 'FREE':
                            st.info("""
**🆓 FREE 모드 - 다음 단계:**

1. **이미지 생성** (수동):
   - Leonardo.ai 접속: https://leonardo.ai
   - 위 프롬프트를 복사해서 이미지 생성
   - 각 Scene별 이미지 다운로드

2. **음성 생성** (수동):
   - CapCut 또는 ElevenLabs 사용
   - 대본을 음성으로 변환
   - MP3 파일 다운로드

3. **영상 편집**:
   - CapCut, Premiere Pro 등 사용
   - 이미지 + 음성 조합
   - 최종 영상 완성!
                            """)
                        else:
                            st.info("""
**💎 PRO 모드 - 자동 생성 준비 완료!**

다음 기능이 자동으로 실행됩니다:
1. ✅ Replicate Flux로 이미지 자동 생성
2. ✅ OpenAI TTS로 음성 자동 생성
3. ✅ 파일 자동 다운로드

⚠️ **주의**: 실제 API 비용이 발생합니다!
- 이미지: 약 ₩1,800
- 음성: 약 ₩270
- 총: 약 ₩2,100

*현재 데모 버전에서는 자동 생성 기능이 비활성화되어 있습니다.*
*실제 사용을 원하시면 별도로 요청해주세요!*
                            """)
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
                st.info("💡 API 키를 확인해주세요!\n\nGemini API Key: https://aistudio.google.com/app/apikey")

# 푸터
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🎬 AI Content Generator | FREE & PRO 통합 버전</p>
    <p>어디서든 접속 가능한 웹 버전</p>
</div>
""", unsafe_allow_html=True)
