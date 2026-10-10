# CotizaFlow

**Cotizaciones y propuestas comerciales — by MARRSO.**

CotizaFlow reúne las herramientas y plantillas del proceso comercial de MARRSO S.A.C. Es la base de un futuro producto web para preparar cotizaciones, propuestas y documentos comerciales.

## Estado actual

El entorno local funciona mediante skills para Codex, plantillas Markdown/HTML y un script de exportación a PDF. La versión pública incluye documentación y el exportador. Todavía no incluye una aplicación web, un servidor ni una base de datos.

## Contenido

- `scripts/generate_pdf.py`: exportación de documentos HTML a PDF con Playwright.
- `requirements.txt`: dependencias del exportador.
- Las skills, plantillas y recursos específicos de MARRSO permanecen en `.agents/` únicamente en el entorno local.

La marca del producto es **CotizaFlow**. MARRSO conserva su identidad como empresa emisora de los documentos. Los nombres de las skills se mantienen para conservar sus referencias.

## Uso del generador de PDF

Requiere Python 3.10 o superior, Playwright y Chrome/Edge, o el Chromium de Playwright.

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
python scripts/generate_pdf.py propuestas/ejemplo.html propuestas/ejemplo.pdf --cliente "Cliente"
```

El documento HTML debe existir previamente. El generador valida las fuentes de marca; su carga puede requerir acceso a Internet.

## Configuración privada

El repositorio público excluye toda la carpeta `.agents/`, propuestas de clientes, historial comercial, configuración financiera interna, paquetes de skills y copias de respaldo.

Para utilizar el flujo comercial completo en otro equipo, se debe transferir de forma privada la carpeta `.agents/`. Entre sus archivos privados se encuentran:

- `pricing-engine.md`: reglas de cálculo y parámetros financieros del negocio.
- `proposal-registry.md`: registro de propuestas y numeración.
- `company-profile.md`: identidad, trayectoria y datos de la empresa.

Estos archivos permanecen disponibles en el entorno original, pero no se publican en Git. Sin esa configuración, el repositorio contiene el exportador, pero no permite ejecutar el flujo de cotización completo.

## Dirección del producto

La futura app web podrá incorporar gestión de clientes, partidas y precios, edición de propuestas, exportación a PDF y seguimiento de estados. Estas capacidades están previstas y todavía no están implementadas.

Repositorio: [martirspe/cotizaflow](https://github.com/martirspe/cotizaflow).
