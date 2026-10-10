"""Genera el PDF de una propuesta CotizaFlow a partir de su HTML.

Uso:
    python scripts/generate_pdf.py <archivo.html> [salida.pdf] [--cliente "Nombre"] [--sin-paginacion]

--sin-paginacion: para el one-pager (una sola hoja, sin footer de página).
Si no se pasa --cliente, se toma del <title> ("Título — Cliente | CotizaFlow").
Requiere: python -m pip install playwright (usa el Chrome/Edge instalado; CHROME_PATH para otra ruta;
si no hay ninguno, usa el Chromium de Playwright: python -m playwright install chromium).
"""

import argparse
import asyncio
import html
import os
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

CANDIDATOS = [
    os.environ.get("CHROME_PATH"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
]

FOOTER_TEMPLATE_HTML = """
<div style="width:100%;padding:0 14mm;display:flex;justify-content:space-between;
            font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:8px;color:#5C6570;">
  <span>{pie}</span>
  <span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>
</div>
"""


async def generar(html_path: Path, pdf_path: Path, cliente: str | None, sin_paginacion: bool) -> None:
    executable = next((p for p in CANDIDATOS if p and Path(p).exists()), None)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(executable_path=executable)
        except Exception as e:
            raise RuntimeError(
                "No se pudo abrir Chrome/Edge ni el Chromium de Playwright. "
                "Define CHROME_PATH o ejecuta `python -m playwright install chromium`."
            ) from e
        try:
            page = await browser.new_page()
            await page.goto(html_path.as_uri(), wait_until="networkidle")
            await page.wait_for_function("document.fonts.ready.then(() => true)")

            fonts_ok = await page.evaluate("""
              document.fonts.check("16px 'DM Sans'") &&
              document.fonts.check("16px 'Space Grotesk'") &&
              document.fonts.check("16px 'IBM Plex Sans'")
            """)
            if not fonts_ok:
                raise RuntimeError(
                    "Fuentes de marca no cargaron (posible falta de acceso a fonts.googleapis.com). "
                    "El PDF saldría con tipografía y tamaños distintos al HTML — no generar así."
                )

            if cliente is None:
                match = re.search(r"—\s*(.+?)\s*\|", await page.title())
                cliente = match.group(1) if match else ""

            match = re.search(r"(COT|MARRSO)-\d{4}-\d{3}", await page.evaluate(
                "document.querySelector('.proposal-id')?.textContent ?? ''"
            ))
            if match:
                tipo = "Cotización" if match.group(1) == "COT" else "Propuesta"
                pie = f"{cliente} — {tipo} {match.group(0)}"
            else:
                pie = cliente

            await page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=not sin_paginacion,
                header_template="<span></span>",
                footer_template="<span></span>" if sin_paginacion
                else FOOTER_TEMPLATE_HTML.format(pie=html.escape(pie)),
                margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"} if sin_paginacion
                else {"top": "14mm", "bottom": "16mm", "left": "0mm", "right": "0mm"},
            )
        finally:
            await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el PDF de una propuesta CotizaFlow.")
    parser.add_argument("html")
    parser.add_argument("pdf", nargs="?")
    parser.add_argument("--cliente")
    parser.add_argument("--sin-paginacion", action="store_true")
    args = parser.parse_args()

    html_path = Path(args.html).resolve()
    pdf_path = Path(args.pdf).resolve() if args.pdf else html_path.with_suffix(".pdf")
    try:
        asyncio.run(generar(html_path, pdf_path, args.cliente, args.sin_paginacion))
    except RuntimeError as e:
        sys.exit(str(e))
    except PermissionError:
        sys.exit(f"No se pudo escribir {pdf_path.name}: ciérralo en el editor o visor de PDF y vuelve a intentar.")
    print(f"PDF generado: {pdf_path}")


if __name__ == "__main__":
    main()
