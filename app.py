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

# 기본 설정 - 4열 레이아웃
col1, col2, col3, col4 = st.columns(4)

with col1:
    language = st.selectbox(
        "🌐 언어 선택",
        ["한국어", "English", "日本語"]
    )

with col2:
    character_style = st.selectbox(
        "🎭 캐릭터 스타일",
        ["🦸 귀여운 히어로", "💊 알약 캐릭터", "🔷 도형 얼굴", "🧍 졸라맨",
         "🐻 귀여운 곰돌이", "🐱 일본 복 고양이 (마네키네코)", "🦊 영리한 여우", 
         "🐰 상냥한 토끼", "🐶 친근한 강아지", "🦅 당당한 독수리",
         "👔 비즈니스맨", "🎨 크리에이터"]
    )

with col3:
    tone_style = st.selectbox(
        "🗣️ 말투 선택",
        ["😊 친근+유머 (유튜브 기본)", 
         "🎓 교육+설명 (강의/튜토리얼)", 
         "💼 전문+신뢰 (리뷰/분석)", 
         "📰 뉴스 (보도)", 
         "🎩 근엄 (공식/발표)"]
    )

with col4:
    voice_style = st.selectbox(
        "🎤 보이스 스타일",
        ["부드럽고 신뢰감 있는 남성", "명랑하고 친근한 여성", 
         "차분하고 전문적인 남성", "활기차고 에너제틱한 여성", 
         "진지하고 무게감 있는 남성"]
    )

# 두 번째 줄: 화면 비율과 Scene 설정
col5, col6 = st.columns([1, 3])

with col5:
    aspect_ratio = st.selectbox(
        "📐 화면 비율",
        ["16:9 (유튜브)", "9:16 (쇼츠)", "1:1 (인스타그램)"]
    )

with col6:
    # Scene 설정
    if st.session_state.mode == 'FREE':
        scene_count = st.slider(
            "🎬 Scene 개수",
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
                "🎬 Scene 개수",
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
    height=200,
    placeholder="여기에 기사 내용을 붙여넣으세요..."
)

# 대본 생성 버튼
if st.button("🎬 대본 생성하기", type="primary", use_container_width=True):
    if not article_content:
        st.error("❌ 기사 내용을 입력해주세요!")
    else:
        with st.spinner("🔄 AI가 대본을 생성하고 있습니다..."):
            try:
                # Gemini API 설정
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-3-flash-preview')
                
                # 말투 스타일 매핑
                tone_map = {
                    "😊 친근+유머 (유튜브 기본)": """
                    - '여러분', '대박', '진짜', '그죠?' 같은 친근한 표현 사용
                    - 감탄사 자주 사용 ('와!', '어머!', '헐!')
                    - 질문형으로 시청자 참여 유도
                    - 유머러스하고 밝은 톤
                    - 예시: "여러분, 이거 진짜 대박이에요! 믿을 수 있나요?"
                    """,
                    "🎓 교육+설명 (강의/튜토리얼)": """
                    - '자, 이제', '함께', '천천히' 등 교육적 표현
                    - 단계별로 차근차근 설명
                    - '~해볼까요?', '~해보세요' 유도형 문장
                    - 예시: "자, 이제 함께 알아볼까요? 천천히 따라오세요!"
                    """,
                    "💼 전문+신뢰 (리뷰/분석)": """
                    - 전문적이면서도 이해하기 쉬운 표현
                    - 객관적 데이터와 분석 포함
                    - '~것으로 평가됩니다', '~할 수 있습니다'
                    - 예시: "이 제품은 가성비가 뛰어난 것으로 평가됩니다."
                    """,
                    "📰 뉴스 (보도)": """
                    - 격식 있는 표준어 사용
                    - 사실 중심, 객관적 서술
                    - '~입니다', '~했습니다' 뉴스 톤
                    - 예시: "오늘 전해드릴 소식은 다음과 같습니다."
                    """,
                    "🎩 근엄 (공식/발표)": """
                    - 매우 격식 있는 표현
                    - 존댓말 최상급 사용
                    - 진지하고 무게감 있는 톤
                    - 예시: "이제부터 말씀드릴 내용을 주목하시기 바랍니다."
                    """
                }
                
                tone_instruction = tone_map.get(tone_style, tone_map["😊 친근+유머 (유튜브 기본)"])
                
                # 프롬프트 생성
                prompt = f"""
당신은 전문 유튜브 영상 대본 작가입니다.
아래 기사를 {scene_count}개의 Scene으로 나누어 영상 대본을 작성해주세요.

**설정:**
- 언어: {language}
- 캐릭터: {character_style} (이 캐릭터의 성격을 대본에 반영하세요)
- 말투: {tone_style}
{tone_instruction}
- 보이스 톤: {voice_style}
- Scene 수: {scene_count}개

**기사 내용:**
{article_content}

**출력 형식:**
Scene 1: [제목]
[대본 내용]

Scene 2: [제목]
[대본 내용]

...

**중요:**
- 각 Scene은 자연스럽게 연결
- {character_style}의 성격과 {tone_style} 말투를 일관되게 유지
- Scene별로 명확히 구분
- 시청자가 몰입할 수 있도록 스토리텔링
"""
                
                # 대본 생성
                response = model.generate_content(prompt)
                script = response.text
                
                st.session_state.script = script
                
                # 이미지 프롬프트도 자동 생성
                with st.spinner("🎨 이미지 프롬프트도 자동 생성 중..."):
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
- {character_style} 캐릭터 스타일 반영
- 배경, 색감, 분위기 포함

대본:
{script}
"""
                    
                    img_response = model.generate_content(prompt_gen)
                    image_prompts = img_response.text
                    
                    st.session_state.image_prompts = image_prompts
                
                st.success("✅ 대본 & 이미지 프롬프트 생성 완료!")
                
                # 상단 다운로드 버튼
                st.divider()
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    st.download_button(
                        "📝 대본 다운로드 (TXT)",
                        script,
                        file_name=f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col_btn2:
                    st.download_button(
                        "🎨 이미지 프롬프트 다운로드 (TXT)",
                        image_prompts,
                        file_name=f"image_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col_btn3:
                    combined = f"=== 대본 ===\n\n{script}\n\n=== 이미지 프롬프트 ===\n\n{image_prompts}"
                    st.download_button(
                        "📦 전체 다운로드 (TXT)",
                        combined,
                        file_name=f"all_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                # Scene별 대본과 프롬프트 함께 표시
                st.divider()
                st.subheader("📋 생성된 대본 & 이미지 프롬프트")
                
                # Scene 분리
                script_lines = script.split('\n')
                prompt_lines = image_prompts.split('\n')
                
                current_scene = None
                scene_script = ""
                scene_prompt = ""
                scene_dict = {}
                
                # 대본 파싱
                for line in script_lines:
                    if line.strip().startswith('Scene'):
                        if current_scene and scene_script:
                            scene_dict[current_scene] = {'script': scene_script.strip()}
                        current_scene = line.strip()
                        scene_script = ""
                    else:
                        scene_script += line + "\n"
                
                if current_scene and scene_script:
                    scene_dict[current_scene] = {'script': scene_script.strip()}
                
                # 프롬프트 파싱
                current_scene = None
                scene_prompt = ""
                
                for line in prompt_lines:
                    if line.strip().startswith('Scene'):
                        if current_scene and scene_prompt:
                            if current_scene in scene_dict:
                                scene_dict[current_scene]['prompt'] = scene_prompt.strip()
                        current_scene = line.strip().split(':')[0].strip()
                        scene_prompt = line.strip().split(':', 1)[1].strip() if ':' in line else ""
                    else:
                        scene_prompt += line + "\n"
                
                if current_scene and scene_prompt:
                    if current_scene in scene_dict:
                        scene_dict[current_scene]['prompt'] = scene_prompt.strip()
                
                # Scene별 표시
                for scene_name, content in scene_dict.items():
                    with st.expander(f"🎬 {scene_name}", expanded=True):
                        st.markdown("**📝 대본:**")
                        st.info(content.get('script', ''))
                        
                        st.markdown("**🎨 이미지 프롬프트:**")
                        st.success(content.get('prompt', ''))
                        
                        st.divider()
                
                # 다음 단계 안내
                st.divider()
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

*현재 데모 버전에서는 자동 생성 기능이 비활성화되어 있습니다.*
                    """)
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
                st.info("💡 API 키를 확인해주세요!\n\nGemini API Key: https://aistudio.google.com/app/apikey")

# 푸터
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🎬 AI Content Generator | FREE & PRO 통합 버전</p>
    <p>귀여운 캐릭터와 함께하는 유튜브 대본 생성기</p>
</div>
""", unsafe_allow_html=True)
            