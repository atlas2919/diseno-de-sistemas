# PSet 1 — ReservaU

Plataforma de reservas de espacios universitarios. Diseño completo del sistema: requerimientos,
modelo de dominio, casos de uso e implementación con una simulación ejecutable.

## Estructura

```
psets/pset-01/
├── README.md
├── 01-requerimientos.pdf
├── 02-modelo-dominio.pdf
├── 03-casos-de-uso.pdf
└── implementacion/
    ├── *.py
    ├── simulacion.py
    └── Dockerfile
```

## Ejecución

Desde `implementacion/`:

```bash
docker build -t reservau .
docker run reservau
```

La salida reproduce, en orden, los flujos documentados en `04-flujos-casos-de-uso.pdf`.
