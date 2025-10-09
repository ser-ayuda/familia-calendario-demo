Removed local/real data before creating a portfolio-friendly package

Fecha: 2025-10-09

Este directorio contiene información sobre archivos que han sido eliminados o movidos
para evitar incluir datos personales reales en el paquete de portfolio.

Acciones realizadas:
- `db.sqlite3` local: eliminado del repositorio y del paquete.
- Backups y archivos con datos reales: reubicados en `removed_for_portfolio/backup_import_*/` (no están incluidos en el paquete público).

Si necesitas recuperar datos reales para pruebas, mantén una copia local fuera del repositorio.
