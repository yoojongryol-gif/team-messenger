# 팀톡 — 업무용 전용 메신저 + 사내 인트라넷

**주소: https://yoojongryol-gif.github.io/team-messenger/**
폰 브라우저로 열고 "홈 화면에 추가"하면 앱처럼 설치됩니다.

> ✅ Firebase 셋업(프로젝트 teamtalk-efb25, 로그인·DB·저장소·보안규칙)은 **이미 완료**되어 있습니다.
> 직원들은 위 주소에서 **가입(이름·이메일·비번 + 회사 초대 코드)** 하면 바로 서로 대화·공지·일정 사용 가능합니다.
> ⚠️ **초대 코드가 있어야 가입됩니다** — 사장님이 직원에게 별도로 코드를 전달해 주세요(이 문서에는 코드 값을 적지 않습니다. 코드는 firestore.rules 파일 상단 주석에서 관리자가 직접 확인).

---

## 기능
**💬 채팅**
- 1:1 / 그룹 실시간 채팅, 읽음 표시, 안 읽음 뱃지
- 사진 · 파일 · 음성 메시지
- PDF · Word · Excel · PPT **앱 안에서 바로 열람**

**📢 공지사항** — 공지 올리기, 상단 고정(📌), 읽음 표시, 작성자 삭제
**👥 조직도 · 주소록** — 부서별 그룹, 전화·메일·대화 바로가기. 각자 ✏️로 부서·직급·전화번호 입력
**📅 팀 일정** — 월간 캘린더, 일정 추가/수정/삭제 공유

**🔒 보안** — 앱 잠금(암호 + Face ID/지문), 로그인한 직원만 접근

---

## 직원 온보딩 (각자 1분)
1. https://yoojongryol-gif.github.io/team-messenger/ 접속
2. "가입하기" → 이름·이메일·비번 + **회사에서 받은 초대 코드** 입력 (코드 없으면 가입 거부됨)
3. 조직도 탭 → ✏️ → 부서·직급·전화번호 입력 (선택)
4. 끝. 채팅·공지·일정 바로 사용

> 초대 코드를 모르면 사장님/관리자에게 문의하세요. 코드가 틀리면 "초대 코드가 올바르지 않습니다" 오류가 뜹니다.

---

## 남은 선택 작업
### 푸시 알림 (앱 꺼져 있어도 알림) — 선택
앱이 켜져 있을 땐 알림이 오지만, 완전히 꺼진 상태 푸시는 아래가 필요:
1. Firebase 콘솔 → 프로젝트 설정 → 클라우드 메시징 → 웹 푸시 인증서 → 키 생성 → 복사
2. 앱 ⚙️서버설정의 VAPID 칸에 붙여넣기 (또는 index.html의 `EMBEDDED_VAPID`)
3. 콘솔 → 프로젝트 설정 → 서비스 계정 → 키 생성 → `serviceAccountKey.json` 저장 → `pip install firebase-admin` → `python fcm_relay.py` (PC 상주)

---

## 관리자 메모 (사장님/개발용)
- Firebase 프로젝트: **teamtalk-efb25** (계정 scjulsan250212). 요금제 Blaze(예산알림 1만원). Storage=US-EAST1 무료위치.
- 설정값은 index.html `EMBEDDED_CONFIG`에 내장(웹 config는 공개용, 보안은 규칙으로).
- 데이터: Firestore(서울) — users / rooms+messages / notices / events. Storage: chat/{roomId}/...
- 배포: GitHub Pages (repo yoojongryol-gif/team-messenger, 로컬 C:\Users\NHNE\team-messenger). 푸시하면 자동 반영.
- 가입: 초대 코드 게이트 있음(firestore.rules `inviteOK()`). 코드는 firestore.rules 파일 상단 주석에만 존재(원문은 앱/이 문서 어디에도 없음).
- **알려진 제한 — HWP 파일 인앱 미리보기 (2026-07-26 실측)**: 원인은 hwp.js 라이브러리 문제가 아니라 **Firebase Storage 버킷에 CORS 설정이 없어서** 파일 바이트를 직접 받아오는(`fetch()`) 방식이 전부 브라우저에서 CORS 차단됨. PDF·docx는 fetch 없이 여는 방식(iframe/오피스뷰어)으로 우회했지만, HWP는 마땅한 우회 뷰어가 없어 여전히 "미리보기 실패 + 다운로드 버튼" 폴백만 동작. **진짜 해결하려면**(선택) 아래 명령 1회 실행 필요(gcloud/gsutil 설치 + teamtalk-efb25 프로젝트 소유자 계정 로그인 필요, 사장님 액션):
  ```
  gsutil cors set cors.json gs://teamtalk-efb25.firebasestorage.app
  ```
  cors.json 예시: `[{"origin":["https://yoojongryol-gif.github.io"],"method":["GET"],"maxAgeSeconds":3600,"responseHeader":["Content-Type","Range"]}]`
  적용 후엔 HWP도 기존 hwp.js 인앱 렌더가 정상 동작할 것으로 예상(코드는 이미 있음, 인프라 설정만 없는 상태).

## 파일
| 파일 | 용도 |
|---|---|
| index.html | 앱 본체 (채팅·공지·조직도·일정·앱잠금) |
| manifest.json / sw.js | PWA(설치·자동 업데이트) |
| firebase-messaging-sw.js | 백그라운드 푸시 수신 |
| fcm_relay.py | 푸시 발송 릴레이 (PC 상주) |
| firestore.rules / storage.rules | 보안 규칙 (이미 콘솔에 게시됨) |
