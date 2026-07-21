const CACHE_NAME = "clippy-v1";

const FILES_TO_CACHE = [
    "/",
    "/lang=mobile",
    "/conta",
    "/login",
    "/sobre",
    "/historico",
    "/shorts",
    "/aovivo",
    "{{ static_url }}"
    "{{ static_url }}/story.png"
];

// Instalação
self.addEventListener("install", (event) => {
    console.log("[Offline] Instalando...");

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(FILES_TO_CACHE))
    );

    self.skipWaiting();
});

// Ativação
self.addEventListener("activate", (event) => {
    console.log("[Offline] Ativado");

    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        })
    );

    self.clients.claim();
});

// Intercepta requisições
self.addEventListener("fetch", (event) => {

    // Ignora métodos diferentes de GET
    if (event.request.method !== "GET") {
        return;
    }

    event.respondWith(

        fetch(event.request)
            .then(response => {

                const responseClone = response.clone();

                caches.open(CACHE_NAME)
                    .then(cache => {
                        cache.put(event.request, responseClone);
                    });

                return response;
            })

            .catch(() => {

                return caches.match(event.request)
                    .then(cached => {

                        if (cached) {
                            return cached;
                        }

                        // Página offline
                        if (
                            event.request.headers.get("accept") &&
                            event.request.headers.get("accept").includes("text/html")
                        ) {
                            return caches.match("/");
                        }

                        return new Response(
                            "Sem conexão.",
                            {
                                status: 503,
                                statusText: "Offline"
                            }
                        );
                    });
            })
    );
});