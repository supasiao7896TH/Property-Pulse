/* Property Pulse PWA — Service Worker */
const CACHE = 'property-pulse-v1';
const APP_SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon.svg',
];

/* ── Install: cache the app shell ── */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

/* ── Activate: purge old caches ── */
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

/* ── Fetch: cache-first for app shell, network-first + cache for CDN ── */
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isCDN = ['cdn.tailwindcss.com', 'cdn.jsdelivr.net', 'unpkg.com',
                  'fonts.googleapis.com', 'fonts.gstatic.com'].some(h => url.hostname.includes(h));

  if (isCDN) {
    /* Network-first, fall back to cache (CDN resources) */
    event.respondWith(
      fetch(event.request)
        .then(res => {
          if (res && res.ok) {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(event.request, clone));
          }
          return res;
        })
        .catch(() => caches.match(event.request))
    );
  } else {
    /* Cache-first for same-origin (app shell, data URIs, blobs) */
    event.respondWith(
      caches.match(event.request).then(cached => {
        const networkFetch = fetch(event.request).then(res => {
          if (res && res.ok) {
            caches.open(CACHE).then(c => c.put(event.request, res.clone()));
          }
          return res;
        }).catch(() => null);
        return cached || networkFetch;
      })
    );
  }
});
