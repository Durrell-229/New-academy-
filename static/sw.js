// Service Worker simple pour PWA
const CACHE_NAME = 'academie-ia-v1';
const urlsToCache = [
    '/app/',
    '/showcase/',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache).catch(err => console.log('PWA: Cache skipping some files'));
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
