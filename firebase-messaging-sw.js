/* 팀톡 FCM 백그라운드 메시지 수신 서비스워커
   설정값은 등록 시 URL 쿼리스트링으로 전달받음 (SW는 localStorage 접근 불가) */
importScripts("https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js");

const params = new URL(location).searchParams;
const cfg = {
  apiKey: params.get("apiKey"),
  authDomain: params.get("authDomain"),
  projectId: params.get("projectId"),
  storageBucket: params.get("storageBucket"),
  messagingSenderId: params.get("messagingSenderId"),
  appId: params.get("appId")
};

try{
  if(cfg.apiKey){
    firebase.initializeApp(cfg);
    const messaging = firebase.messaging();
    messaging.onBackgroundMessage(payload=>{
      const n = payload.notification || {};
      const d = payload.data || {};
      self.registration.showNotification(n.title || d.title || "새 메시지", {
        body: n.body || d.body || "",
        icon: "apple-touch-icon.png",
        badge: "apple-touch-icon.png",
        tag: d.roomId || "teamtalk",
        data: { roomId: d.roomId || "" }
      });
    });
  }
}catch(e){ /* noop */ }

self.addEventListener("notificationclick", e=>{
  e.notification.close();
  e.waitUntil(clients.matchAll({type:"window",includeUncontrolled:true}).then(list=>{
    for(const c of list){ if("focus" in c) return c.focus(); }
    if(clients.openWindow) return clients.openWindow("./");
  }));
});
