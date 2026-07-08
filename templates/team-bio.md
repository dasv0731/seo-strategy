# Plantilla — Bio E-E-A-T (equipo / persona)

La autoridad se ancla en humanos verificables. Cada bio alimenta un nodo `Person`. **Nunca inventar credenciales.**

```
FOTO: [real, 800×800, en contexto profesional]
NOMBRE: ...
CARGO / TÍTULO EXACTO: ...
ESPECIALIDADES (chips): [áreas → knowsAbout]

BIO (3 párrafos):
  P1 — quién es + años de experiencia + foco
  P2 — trayectoria / sectores / tipos de proyecto o caso
  P3 — enfoque / filosofía de trabajo

FORMACIÓN:
  - Título universitario (universidad → alumniOf, año)
  - Posgrados / formaciones

CREDENCIALES / REGISTROS (verificables → hasCredential):
  - Registro profesional del país (p.ej. SENESCYT/MSP en EC, cédula profesional en MX, colegiado en ES / nº) // CONFIRMAR vigente
  - Certificaciones (con ImageObject si se muestran)
  - Membresías (→ memberOf)

EXPERIENCIA DESTACADA: [proyectos / casos / años]

CONTACTO / sameAs:
  - LinkedIn público
  - [directorio sectorial del mercado (p.ej. Doctoralia en salud)]
  - email profesional

→ Mapea a schema Person:
  name, jobTitle, image, alumniOf, hasCredential, knowsAbout, memberOf, sameAs, worksFor
```
