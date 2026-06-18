# 팀톡 셋업 가이드 (사장님용 · 약 5~10분)

업무용 전용 메신저. 단일 HTML PWA + Firebase(무료). 기존 마이플래너/식단운동 앱과 같은 방식.

---

## 1단계. Firebase 프로젝트 만들기 (무료)

1. https://console.firebase.google.com 접속 (구글 로그인: scjulsan250212 등)
2. **프로젝트 추가** → 이름 `teamtalk` (또는 아무거나) → 만들기
   - Google 애널리틱스는 꺼도 됨
3. 만들어지면 그대로 다음 단계

## 2단계. 웹 앱 등록 → 설정값 복사

1. 프로젝트 개요 화면에서 **`</>` (웹) 아이콘** 클릭
2. 앱 닉네임 `teamtalk-web` 입력 → 등록
3. 화면에 나오는 **`firebaseConfig = { ... }`** 객체 전체를 복사
   (apiKey, authDomain, projectId, storageBucket, messagingSenderId, appId)

## 3단계. 3가지 기능 켜기 (콘솔 좌측 메뉴)

- **빌드 → Authentication** → 시작하기 → **이메일/비밀번호** 사용 설정 ON
- **빌드 → Firestore Database** → 데이터베이스 만들기 → 위치 `asia-northeast3(서울)` → **테스트 모드**로 시작
- **빌드 → Storage** → 시작하기 → 위치 동일 → 테스트 모드로 시작

> 테스트 모드는 30일 후 막힙니다. 아래 6단계에서 보안 규칙을 넣으면 영구 사용 가능.

## 4단계. 앱에 설정값 넣기

1. 배포된 앱 주소를 폰/PC 브라우저로 엽니다 (배포 후 주소 안내)
2. 로그인 화면 아래 **⚙️ 서버 설정** 클릭
3. 2단계에서 복사한 `firebaseConfig` 객체를 붙여넣고 **저장**
4. 자동 새로고침되면 준비 끝 → **가입하기**로 직원 계정 생성

> 직원들은 각자 앱 주소 접속 → 가입(이름·이메일·비번)만 하면 서로 대화 가능.
> (설정값을 매번 넣기 싫으면 index.html 상단 `EMBEDDED_CONFIG`에 박아 배포해도 됨)

---

## 5단계. 푸시 알림 (선택, 앱 꺼져 있어도 알림)

### 5-1. VAPID 키
- 콘솔 → 프로젝트 설정 → **클라우드 메시징** 탭 → "웹 푸시 인증서" → 키 쌍 생성 → 키 복사
- 앱 ⚙️ 서버 설정의 **VAPID 키** 칸에 붙여넣고 저장

### 5-2. 푸시 발송 릴레이 (PC 상주)
무료 플랜은 Cloud Functions에 카드 등록이 필요하므로, PC에서 도는 파이썬으로 무료 처리:
- 콘솔 → 프로젝트 설정 → **서비스 계정** → "새 비공개 키 생성" → JSON 다운로드
- 이 폴더에 `serviceAccountKey.json` 으로 저장
- `pip install firebase-admin`
- `python fcm_relay.py` 실행 (PC 켜져 있는 동안 새 메시지마다 푸시 발송)

> 릴레이 없이도 **앱이 켜져 있을 때는 알림이 옵니다**. 앱 완전히 꺼진 상태 푸시만 릴레이 필요.

---

## 6단계. 보안 규칙 적용 (30일 후 잠김 방지 · 중요)

- **Firestore Database → 규칙** 탭 → `firestore.rules` 내용 붙여넣기 → 게시
- **Storage → 규칙** 탭 → `storage.rules` 내용 붙여넣기 → 게시

이러면 로그인한 직원만 접근, 본인 메시지만 작성 가능하게 잠깁니다.

---

## 파일 구성
| 파일 | 용도 |
|---|---|
| index.html | 앱 본체 (로그인·채팅·실시간·파일·문서뷰어·앱잠금) |
| manifest.json / sw.js | PWA(설치·자동 업데이트) |
| firebase-messaging-sw.js | 백그라운드 푸시 수신 |
| fcm_relay.py | 푸시 발송 릴레이 (PC 상주) |
| firestore.rules / storage.rules | 보안 규칙 |
| apple-touch-icon.png | 앱 아이콘 |

## 기능
- 1:1 / 그룹 채팅, 실시간 전송, 읽음 표시, 안 읽음 뱃지
- 사진 · 파일 · 음성 메시지
- **PDF · Word · Excel · PPT 앱 내 미리보기** (Office/구글 뷰어)
- 푸시 알림 (FCM)
- 앱 잠금 (암호 + Face ID/지문)
- 폰 홈화면 설치, 자동 업데이트
