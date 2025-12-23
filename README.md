# etl-end-to-end-api
 bronze/
│   │   └── (archivos crudos diarios .json/.csv/)
│   ├── silver/
│   │   └── (archivos limpios/normalizados)
│   └── gold/
│       └── (archivos listos para analítica/dashboard


Prefijo (Tipo)	Descripción	Ejemplo
feat:	Nueva funcionalidad.	feat: Añadir soporte para archivos CSV en la ingesta
fix:	Corrección de un error.	fix: Corregir error de desbordamiento de buffer en parseo
docs:	Cambios solo en la documentación.	docs: Actualizar README con instrucciones de setup
style:	Cambios de formato (sin cambio de código).	style: Formatear código según las guías PEP8
refactor:	Refactorización de código sin cambio de funcionalidad.	refactor: Extraer lógica de validación a un nuevo módulo
test:	Añadir o corregir pruebas.	test: Añadir prueba unitaria para la función de conexión