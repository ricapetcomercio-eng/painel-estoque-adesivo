#!/usr/bin/env python3
"""Regenera catalog.json a partir da constante CATALOG embutida em estoque.html.

catalog.json é lido pelo painel-entrega-turbo (lib/estoqueSaldo.js,
importarContagemFisica) pra saber TODOS os produto/cor/tamanho existentes
-- inclusive os que nunca foram contados fisicamente ainda -- e não só os
que já têm alguma contagem salva no JSONBin. Sem isso, o saldo automático
fica bem menor que o catálogo completo (e que a planilha "Estoque Ricapet",
que sempre lista o catálogo inteiro).

Rode isto sempre que CATALOG for editado em estoque.html (novo produto,
cor, tamanho, produto removido/renomeado etc.) e faça commit do
catalog.json atualizado junto.

Uso:
    python scripts/gerar_catalog_json.py
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ESTOQUE_HTML = RAIZ / "estoque.html"
CATALOG_JSON = RAIZ / "catalog.json"


def main():
    texto = ESTOQUE_HTML.read_text(encoding="utf-8")
    m = re.search(r"const CATALOG = (\{.*?\});", texto)
    if not m:
        raise SystemExit("Não encontrei 'const CATALOG = {...};' em estoque.html")
    catalog = json.loads(m.group(1))

    combos = sum(len(tamanhos) for cores in catalog.values() for tamanhos in cores.values())
    CATALOG_JSON.write_text(
        json.dumps(catalog, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    print(f"catalog.json atualizado: {len(catalog)} produtos, {combos} combinações produto/cor/tamanho.")


if __name__ == "__main__":
    main()
