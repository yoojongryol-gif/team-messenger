# 팀톡 — 업무용 전용 메신저 + 사내 인트라넷

**주소: https://yoojongryol-gif.github.io/team-messenger/**
폰 브라우저로 열고 "홈 화면에 추가"하면 앱처럼 설치됩니다.

> ✅ Firebase 셋업(프로젝트 teamtalk-efb25, 로그인·DB·저장소·보안규칙)은 **이미 완료**되어 있습니다.
> 직원들은 그냥 위 주소에서 **가입(이름·이메일·비번)만** 하면 바로 서로 대화·공지·일정 사용 가능합니다.

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
2. "가입하기" → 이름·이메일·비번 입력
3. 조직도 탭 → ✏️ → 부서·직급·전화번호 입력 (선택)
4. 끝. 채팅·공지·일정 바로 사용

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

## 파일
| 파일 | 용도 |
|---|---|
| index.html | 앱 본체 (채팅·공지·조직도·일정·앱잠금) |
| manifest.json / sw.js | PWA(설치·자동 업데이트) |
| firebase-messaging-sw.js | 백그라운드 푸시 수신 |
| fcm_relay.py | 푸시 발송 릴레이 (PC 상주) |
| firestore.rules / storage.rules | 보안 규칙 (이미 콘솔에 게시됨) |
