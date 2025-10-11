## Paquete listo para publicar en LinkedIn — texto, imágenes y checklist

1) Texto largo (ideal para post principal en LinkedIn — voz personal y técnica)

Hoy comparto un proyecto que he preparado para mi portafolio: Familia Calendario — una app web para planificar tareas y eventos compartidos en el hogar.

La demo pública está desplegada en Render y puedes probarla en: https://familia-calendario-demo.onrender.com/gestion/ (credenciales: demo/demo)

Aspectos técnicos destacados:
- Stack: Python 3.13, Django 5.2.7, Django REST Framework
- Despliegue: Render (Docker opcional), Postgres en producción
- Automatización: pruebas unitarias, generación de capturas con Playwright y packaging para portafolio
- Seguridad & privacidad: fixtures anonimizados y checklist COMPLIANCE.md para asegurar que no se exponen datos personales

Si te interesa ver el código o que lo despleguemos juntos en 15 minutos, escríbeme. El repositorio y la guía están aquí: https://github.com/ser-ayuda/familia-calendario-demo

2) Texto corto (preview / titular)

Familia Calendario — demo pública desplegada en Render. Planifica tareas del hogar con una interfaz sencilla. Prueba: https://familia-calendario-demo.onrender.com/gestion/ • Código: https://github.com/ser-ayuda/familia-calendario-demo

3) Publicación técnica (primera respuesta o sección técnica)

Ficha rápida:
- Lenguaje y framework: Python 3.13 + Django 5.2.7
- API: Django REST Framework
- Base de datos: SQLite (dev) / Postgres (prod)
- Infraestructura: Render (PAAS), Dockerfile incluido
- Testing: Django tests; capturas automatizadas con Playwright

4) Orden y uso de las imágenes (recomendado)
- Imagen 1 (principal): `assets/social.png` — composición vertical/rectangular con título del proyecto (usa para el primer slot en LinkedIn)
- Imagen 2: captura de la UI (home o gestión) — `demo_screenshots/home.png` o `demo_screenshots/gestion.png`
- Imagen 3: captura del admin o del flujo técnico — `demo_screenshots/admin.png`

Alt text sugerido (accesibilidad)
- Imagen 1: "Familia Calendario — portada del proyecto, app para planificar tareas y eventos del hogar"
- Imagen 2: "Vista principal de la app Familia Calendario mostrando la lista de tareas"
- Imagen 3: "Panel de administración mostrando gestión de miembros y tareas"

5) Hashtags sugeridos
#Django #Python #WebDev #DevOps #Render #OpenSource #Portfolio

6) Checklist antes de publicar
- [ ] Confirmar que `README_demo.md` apunta a la demo correcta y que las credenciales demo aparecen documentadas.
- [ ] Verificar que `portfolio_minimal.zip` creado para la release contiene solo fixtures anonimizados.
- [ ] Comprobar que no quedan secretos (usar `git grep` o herramientas de scanning).
- [ ] Revisar que la URL de la demo responde correctamente y SSL está activo si está publicada.
- [ ] Subir `assets/social.png` y elegir orden de imágenes.

7) Tamaños recomendados para imágenes
- Imagen principal (social): 1200 x 628 px (landscape) o 1080 x 1350 px (portrait) según formato preferido
- Capturas: 1200 px ancho (mantener relación de aspecto para no recortar información)

8) CTA sugerida al final del post
"¿Te interesa que lo despleguemos juntos en una llamada de 15 minutos? Mándame un mensaje y lo hacemos." 

---

Si quieres, puedo:
- Generar automáticamente una versión PNG optimizada para LinkedIn desde `assets/social.svg` (si existe).
- Crear la primera respuesta automática en formato corto con enlaces listos para pegar.
