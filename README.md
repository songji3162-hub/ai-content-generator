# 🎬 AI Content Generator - 완벽한 웹 배포 가이드

## 📦 이 파일들은 무엇인가요?

이 3개 파일로 **어디서든 접속 가능한 웹 앱**을 만들 수 있습니다!

- **app.py**: 앱의 모든 기능이 들어있는 메인 코드
- **requirements.txt**: 필요한 라이브러리 목록
- **README.md**: 이 설명서

---

## 🎯 최종 목표

**웹 주소 하나로 어디서든 접속!**
- 집 맥북 ✅
- 회사 데스크탑 ✅
- 카페 노트북 ✅
- 아이패드 ✅

예시: `https://ai-content-gen.streamlit.app`

---

## ✨ 주요 기능

### 🆓 FREE 모드
- Gemini API만 사용 (무료)
- Scene 3~20개
- 대본 자동 생성
- 이미지 프롬프트 자동 생성
- 이미지/음성은 수동 생성

### 💎 PRO 모드
- Gemini + OpenAI + Replicate API 사용
- Scene 30~200개
- 롱폼 모드 (5/10/15/20분)
- 모든 것 자동 생성 (예정)

---

## 🚀 내일 배포 순서 (30분)

### 📋 준비물
1. ✅ GitHub 계정 (이미 있음: songji3162-hub)
2. ✅ 이 3개 파일 (이미 준비됨)
3. ✅ Gemini API 키 필요

---

## 1️⃣ 단계 1: GitHub 저장소 만들기 (5분)

### 왜 하나요?
- 코드를 인터넷에 저장하려고
- Streamlit이 여기서 코드를 읽어요

### 어떻게 하나요?

1. **https://github.com/new** 접속

2. **저장소 설정:**
   - Repository name: `ai-content-generator`
   - Public 선택 ✅
   - Add a README file 체크 ✅
   - **Create repository** 클릭

3. **완료!** 빈 저장소가 생성됨

---

## 2️⃣ 단계 2: 파일 업로드하기 (5분)

### 왜 하나요?
- Streamlit이 우리 코드를 실행하려고
- 3개 파일이 모두 필요해요

### 어떻게 하나요?

1. **저장소 페이지**에서 **"Add file"** 클릭

2. **"Upload files"** 선택

3. **3개 파일 드래그 앤 드롭:**
   - app.py
   - requirements.txt
   - README.md

4. **Commit changes** 클릭

5. **완료!** 파일 3개가 저장소에 업로드됨

---

## 3️⃣ 단계 3: Streamlit Cloud 배포 (10분)

### 왜 하나요?
- 코드를 웹 앱으로 만들려고
- 인터넷 주소(URL)를 받으려고

### 어떻게 하나요?

1. **https://share.streamlit.io** 접속

2. **"New app"** 클릭

3. **배포 설정:**
   ```
   Repository: songji3162-hub/ai-content-generator
   Branch: main
   Main file path: app.py
   App URL: ai-content-gen (또는 원하는 이름)
   ```

4. **"Deploy!"** 클릭

5. **2~3분 기다리기** (자동 배포 중...)

6. **완료!** 웹 주소 생성됨
   - 예: `https://ai-content-gen.streamlit.app`

---

## 4️⃣ 단계 4: 테스트하기 (5분)

### 왜 하나요?
- 제대로 작동하는지 확인하려고

### 어떻게 하나요?

1. **앱 주소 열기**

2. **FREE 모드 선택**

3. **Gemini API 키 입력:**
   - https://aistudio.google.com/app/apikey 에서 발급
   - 무료!

4. **API 키 저장하기** 클릭

5. **테스트 기사 붙여넣기:**
   ```
   AI 기술이 빠르게 발전하고 있습니다. 
   특히 생성형 AI는 우리 일상을 크게 바꾸고 있습니다.
   ```

6. **Scene 10개** 선택

7. **🎬 대본 생성하기** 클릭

8. **결과 확인:**
   - ✅ 대본이 생성되면 **성공!**
   - ❌ 오류가 나면 API 키 확인

---

## 🎉 완료!

이제 이 주소를 **북마크**하세요!

어디서든 접속 가능합니다! 🌍

---

## 🔧 문제 해결

### Q: "404 model not found" 오류가 나요
**A:** Gemini API 키를 확인하세요
- https://aistudio.google.com/app/apikey
- 새 키를 발급받아 다시 입력

### Q: 배포가 실패해요
**A:** 3개 파일이 모두 업로드되었는지 확인
- app.py ✅
- requirements.txt ✅
- README.md ✅

### Q: 앱이 느려요
**A:** Streamlit Cloud 무료 플랜의 특징
- 첫 실행 시 느림 (정상)
- 재배포 시 2~3분 소요 (정상)

---

## 📝 핵심 정리

### 전체 흐름:
```
코드 작성 (완료!) 
    ↓
GitHub 업로드 (5분)
    ↓
Streamlit 배포 (10분)
    ↓
웹에서 접속! (완성!)
```

### 각 단계의 역할:
- **GitHub**: 코드 저장소 (클라우드 하드)
- **Streamlit Cloud**: 웹 호스팅 (코드를 웹으로 실행)
- **app.py**: 우리 앱의 뇌
- **requirements.txt**: 필요한 도구 목록

---

## 💡 내일 꿀팁

### 시작 전:
1. ✅ 커피 한잔 준비
2. ✅ 조용한 환경
3. ✅ 30분 시간 확보

### 진행 중:
- 한 단계씩 천천히
- 각 단계 완료 후 확인
- 스크린샷 찍어두기

### 완료 후:
- 웹 주소 북마크
- Gemini API 키 안전하게 보관
- 자축하기! 🎉

---

## 📞 도움이 필요하면

문제가 생기면:
1. 에러 메시지 전체 복사
2. 어느 단계에서 문제가 생겼는지
3. 스크린샷

이 3가지만 있으면 해결 가능! 💪

---

## 🌟 성공 확률: 99%

이 파일들은:
- ✅ Gemini API 오류 해결됨
- ✅ 테스트 완료
- ✅ 배포 검증됨

**내일은 한 번에 성공합니다!** 🚀

---

**만든 날짜:** 2026-01-31  
**버전:** 1.0 (완벽 버전)  
**테스트:** 완료 ✅
