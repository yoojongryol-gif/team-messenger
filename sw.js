/* 팀톡 PWA 서비스워커 — 앱 셸 캐시 + 자동 업데이트 */
const VER = "teamtalk-v1.0.0";
const SHELL = ["./","./index.html","./manifest.json","./apple-touch-icon.png"];

self.addEventListener("install", e=>{
  self.skipWaiting();
  e.waitUntil(caches.open(VER).then(c=>c.addAll(SHELL).catch(()=>{})));
});
self.addEventListener("activate", e=>{
  e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==VER).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener("fetch", e=>{
  const req=e.request;
  if(req.method!=="GET") return;
  const url=new URL(req.url);
  // 같은 출처의 앱 셸만 캐시. Firebase/외부는 항상 네트워크.
  if(url.origin!==location.origin) return;
  // index.html 류는 network-first (최신 우선)
  if(req.mode==="navigate" || url.pathname.endsWith("index.html") || url.pathname.endsWith("/")){
    e.respondWith(fetch(req).then(r=>{const cp=r.clone();caches.open(VER).then(c=>c.put(req,cp));return r;}).catch(()=>caches.match(req).then(m=>m||caches.match("./index.html"))));
    return;
  }
  // 그 외 정적 자원은 cache-first
  e.respondWith(caches.match(req).then(m=>m||fetch(req).then(r=>{const cp=r.clone();caches.open(VER).then(c=>c.put(req,cp));return r;})));
});
