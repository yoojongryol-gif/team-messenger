# -*- coding: utf-8 -*-
"""
팀톡 FCM 푸시 릴레이
- Firebase Admin SDK로 Firestore의 새 메시지를 감지해 받는 사람에게 푸시 발송.
- Firebase 무료(Spark) 플랜에서 Cloud Functions(=Blaze 카드 필요) 없이 푸시를 보내기 위한 PC 상주 스크립트.
- FCM 발송 자체는 무료. PC(종합상사 서버)가 켜져 있는 동안 동작.

[준비]
1) Firebase 콘솔 → 프로젝트 설정 → 서비스 계정 → "새 비공개 키 생성" → JSON 다운로드
   → 이 폴더에 serviceAccountKey.json 으로 저장 (또는 환경변수 TEAMTALK_SA_PATH 로 경로 지정)
2) pip install firebase-admin
3) python fcm_relay.py   (백그라운드 상주)
"""
import os, sys, time, threading

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, messaging
except ImportError:
    print("firebase-admin 미설치 → 실행: pip install firebase-admin")
    sys.exit(1)

SA_PATH = os.environ.get("TEAMTALK_SA_PATH") or os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
if not os.path.exists(SA_PATH):
    print(f"[!] 서비스 계정 키가 없습니다: {SA_PATH}")
    print("    Firebase 콘솔 → 프로젝트 설정 → 서비스 계정 → 새 비공개 키 생성")
    sys.exit(1)

firebase_admin.initialize_app(credentials.Certificate(SA_PATH))
db = firestore.client()

START_TS = time.time()
_seen = set()           # 처리한 메시지 id (중복 방지)
_room_cache = {}        # roomId -> room dict (members/memberNames/type/name)

def get_room(room_id):
    r = _room_cache.get(room_id)
    if r is None:
        snap = db.collection("rooms").document(room_id).get()
        r = snap.to_dict() if snap.exists else {}
        _room_cache[room_id] = r
    return r

def user_tokens(uid):
    snap = db.collection("users").document(uid).get()
    if not snap.exists:
        return [], None
    d = snap.to_dict() or {}
    return d.get("fcmTokens", []) or [], d.get("name")

def remove_token(uid, token):
    try:
        db.collection("users").document(uid).update({"fcmTokens": firestore.ArrayRemove([token])})
    except Exception:
        pass

def handle_message(room_id, msg_id, m):
    if msg_id in _seen:
        return
    _seen.add(msg_id)
    # 스크립트 시작 이전 메시지는 무시
    ts = m.get("ts")
    if ts is not None:
        try:
            if ts.timestamp() < START_TS - 5:
                return
        except Exception:
            pass

    room = get_room(room_id)
    members = room.get("members", [])
    sender = m.get("sender")
    sender_name = m.get("senderName", "")
    is_group = room.get("type") == "group"
    room_name = room.get("name", "") if is_group else sender_name

    mtype = m.get("type", "text")
    body = m.get("text", "") if mtype == "text" else {
        "image": "📷 사진", "voice": "🎙 음성메시지", "file": "📎 " + (m.get("fileName") or "파일")
    }.get(mtype, "새 메시지")
    title = f"{room_name} · {sender_name}" if is_group else sender_name

    for uid in members:
        if uid == sender:
            continue
        tokens, _ = user_tokens(uid)
        for tok in tokens:
            try:
                messaging.send(messaging.Message(
                    token=tok,
                    notification=messaging.Notification(title=title, body=body[:120]),
                    data={"roomId": room_id, "title": title, "body": body[:120]},
                    webpush=messaging.WebpushConfig(
                        notification=messaging.WebpushNotification(title=title, body=body[:120], icon="apple-touch-icon.png"),
                        fcm_options=messaging.WebpushFCMOptions(link="./"),
                    ),
                ))
            except messaging.UnregisteredError:
                remove_token(uid, tok)
            except Exception as e:
                print("send err:", e)

def on_snapshot(col_snapshot, changes, read_time):
    for ch in changes:
        if ch.type.name != "ADDED":
            continue
        doc = ch.document
        try:
            room_id = doc.reference.parent.parent.id
        except Exception:
            continue
        handle_message(room_id, doc.id, doc.to_dict() or {})

def invalidate_room_cache():
    # 방 멤버 변경 반영용: 주기적으로 캐시 비움
    while True:
        time.sleep(60)
        _room_cache.clear()

if __name__ == "__main__":
    print(f"[팀톡 FCM 릴레이] 시작 — 새 메시지 감시 중… (키: {SA_PATH})")
    threading.Thread(target=invalidate_room_cache, daemon=True).start()
    # 모든 방의 messages 하위 컬렉션을 collection group 으로 감시
    db.collection_group("messages").on_snapshot(on_snapshot)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("종료")
