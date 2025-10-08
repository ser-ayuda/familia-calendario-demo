self.addEventListener('install', event => {
  self.skipWaiting();
});
self.addEventListener('fetch', event => {
  // Puedes agregar lógica de cache aquí si lo deseas
});
