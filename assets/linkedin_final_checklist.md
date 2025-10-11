# Checklist final — publicar proyecto en LinkedIn

Antes de publicar
- [ ] Revocar tokens temporales utilizados para subir artefactos (si corresponde).
- [ ] Confirmar que `README_demo.md` apunta a la URL de demo correcta.
- [ ] Verificar que `portfolio_minimal.zip` contiene fixtures anonimizados y no incluye `db.sqlite3` con datos reales.
- [ ] Ejecutar `python manage.py check --deploy` localmente para confirmar que no hay warnings críticos (DEBUG=false recomendado).
- [ ] Revisar que las imágenes `assets/social_linkedin_landscape.png` y capturas se muestran correctamente en la vista previa.
- [ ] Comprobar certificados SSL y que la demo en Render responde por HTTPS (si aplica).

Durante la publicación
- [ ] Subir `assets/social_linkedin_landscape.png` como imagen principal.
- [ ] Añadir capturas adicionales en el orden recomendado (UI -> Admin).
- [ ] Pegar la descripción (ES o EN) y revisar enlaces. En el campo de enlace principal añade la demo en Render: https://familia-calendario-demo.onrender.com/gestion/ (o https://familia-calendario-demo.onrender.com si prefieres la raíz del sitio).
- [ ] Añadir aptitudes sugeridas y seleccionar la opción de notificar a la red si deseas visibilidad.

Tras publicar
- [ ] Comprobar que el post se renderiza bien en móvil y desktop.
- [ ] Responder al primer comentario con la ficha técnica (usar `assets/linkedin_post_detailed.md` como guía).
- [ ] Monitorizar interacciones y responder mensajes de networking.

Notas técnicas
- Si quieres publicar `/portfolio_minimal.zip` en Releases, asegúrate de que el asset descargado tiene el SHA256 publicado.
- Para autores de código: añade un GitHub Actions que valide `manage.py test` y `manage.py check --deploy` en `main`.
