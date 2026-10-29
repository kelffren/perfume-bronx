#!/usr/bin/env python3
"""Discover common perfume questions and create an editorial review queue.

No AI claims, no automatic article publishing, no invented search volumes.
Optional Google Suggest is an exploratory signal, not verified demand.
"""
import argparse
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [
    "como saber si un perfume arabe es original",
    "cuanto dura un perfume arabe",
    "que significa eau de parfum",
    "como aplicar perfume para que dure mas",
    "como elegir un perfume para regalar",
    "a que huele lattafa yara",
    "lattafa khamrah vs asad",
    "como guardar perfumes correctamente",
    "que es la maceracion de perfumes",
    "puedo probar un perfume antes de comprar",
]
EXCLUDE = re.compile(r"(?i)\b(gratis descargar|falsificar|replica exacta|fake reviews)\b")

def suggest(seed):
    query = urlencode({"client": "firefox", "hl": "es", "q": seed})
    req = Request("https://suggestqueries.google.com/complete/search?" + query,
                  headers={"User-Agent": "OudBronxEditorialResearch/1.0"})
    with urlopen(req, timeout=8) as response:
        payload = json.load(response)
    return [x.strip() for x in payload[1] if isinstance(x, str)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Use Google Suggest; requires network")
    parser.add_argument("--output", default="docs/editorial-question-queue.md")
    args = parser.parse_args()
    entries = {}
    for seed in SEEDS:
        entries[seed] = ("seed", seed)
        if args.live:
            try:
                for question in suggest(seed):
                    if len(question) <= 120 and not EXCLUDE.search(question):
                        entries.setdefault(question.casefold(), ("suggestion", question))
            except Exception as error:
                print(f"Suggestion unavailable for {seed}: {type(error).__name__}")
    lines = [
        "# OUD BRONX — Cola editorial de preguntas",
        "",
        f"Generado: {date.today().isoformat()}",
        "",
        "Estas preguntas son hipótesis de contenido, NO datos de volumen de búsqueda.",
        "Las sugerencias externas (si están habilitadas) no prueban popularidad ni intención de compra.",
        "Ningún artículo se publica automáticamente: investigar, contrastar fuentes y aprobar manualmente.",
        "",
        "| Origen | Pregunta o búsqueda | Estado |",
        "|---|---|---|",
    ]
    for origin, question in entries.values():
        safe = question.replace("|", " ").replace("\n", " ")
        lines.append(f"| {origin} | {safe} | Pendiente de revisión |")
    lines += ["", "## Revisión obligatoria antes de publicar", "",
              "- Verificar hechos con fuentes fiables y citar fabricantes cuando corresponda.",
              "- No inventar duración, autenticidad, testimonios, precios, stock ni cobertura.",
              "- Evitar artículos duplicados o creados solo para posicionar palabras clave.",
              "- Aportar respuesta práctica, enlaces internos pertinentes y traducción revisada.",
              "- Aprobar título, texto, enlaces, canonical y hreflang antes del despliegue.", ""]
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved {len(entries)} questions to {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
