const CACHE_NAME = 'raylib-odin-pwa-v1';

// Cài đặt Service Worker
self.addEventListener('install', event => {
    self.skipWaiting(); // Ép buộc SW mới hoạt động ngay lập tức
});

self.addEventListener('activate', event => {
    event.waitUntil(clients.claim());
});

// Cache chiến lược Stale-While-Revalidate (Lấy từ Cache, ngầm tải mạng cập nhật lại Cache)
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            const networkFetch = fetch(event.request).then(response => {
                // Chỉ cache các request HTTP thành công
                if (response && response.status === 200 && response.type === 'basic') {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            }).catch(() => {
                // Bỏ qua lỗi fetch khi offline
            });

            // Trả về cache nếu có, nếu không thì lấy từ mạng
            return cachedResponse || networkFetch;
        })
    );
});
