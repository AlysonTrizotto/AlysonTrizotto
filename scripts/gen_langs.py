"""Gera langs.svg e langs.json: linguagens por bytes agregados nos repos do usuário (API de linguagens do GitHub).

Env: GH_USER (obrigatória), GH_TOKEN (opcional; sem ela só repos públicos).
Bytes vêm do linguist do GitHub, que já ignora vendor/lockfiles/generated.
"""
import json
import logging
import os
import re
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import escape

API = "https://api.github.com"
TIMEOUT = 30
TOP = 8
# Cores do tema "radical" já usado nos cards atuais
BG, TITLE, TEXT, BAR_BG = "#141321", "#fe428e", "#a9fef7", "#2a2840"
PALETTE = ["#fe428e", "#a9fef7", "#f8d847", "#9d7bff", "#ff8a4c", "#4cc9f0", "#7bd88f", "#c0c0d8"]

log = logging.getLogger("gen_langs")


def get(url: str, token: str | None) -> tuple[object, str]:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r), r.headers.get("Link", "")


def list_repos(user: str, token: str | None) -> list[dict]:
    # /user/repos inclui privados do dono do token; /users/{u}/repos só públicos
    url = f"{API}/user/repos?affiliation=owner&per_page=100" if token else f"{API}/users/{user}/repos?per_page=100"
    repos: list[dict] = []
    while url:
        page, link = get(url, token)
        repos += page
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = m.group(1) if m else ""
    return [r for r in repos if not r["fork"]]


def aggregate(repos: list[dict], token: str | None) -> Counter:
    total: Counter = Counter()
    for r in repos:
        try:
            langs, _ = get(r["languages_url"], token)
            total.update(langs)
        except Exception:
            # um repo falhando não derruba o card inteiro
            log.exception("languages_failed", extra={"repo_id": r["id"]})
    return total


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def render(total: Counter, n_repos: int, stars: int) -> str:
    grand = sum(total.values()) or 1
    top = total.most_common(TOP)
    rest = grand - sum(b for _, b in top)
    if rest > 0:
        top.append(("Outras", rest))
    w, row_h, y0 = 420, 26, 92
    h = y0 + row_h * len(top) + 14
    rows = []
    for i, (name, b) in enumerate(top):
        y, pct = y0 + i * row_h, b / grand * 100
        color = PALETTE[i % len(PALETTE)]
        rows.append(
            f'<text x="20" y="{y}" class="t">{escape(name)}</text>'
            f'<rect x="130" y="{y - 10}" width="190" height="8" rx="4" fill="{BAR_BG}"/>'
            f'<rect x="130" y="{y - 10}" width="{max(pct / 100 * 190, 2):.1f}" height="8" rx="4" fill="{color}"/>'
            f'<text x="400" y="{y}" class="t" text-anchor="end">{pct:.1f}% · {human(b)}</text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="Linguagens por bytes">'
        f'<style>.h{{font:600 18px "Segoe UI",Ubuntu,sans-serif;fill:{TITLE}}}'
        f'.t{{font:400 12px "Segoe UI",Ubuntu,sans-serif;fill:{TEXT}}}'
        f'.s{{font:400 11px "Segoe UI",Ubuntu,sans-serif;fill:#8a88a8}}</style>'
        f'<rect width="{w}" height="{h}" rx="6" fill="{BG}"/>'
        f'<text x="20" y="32" class="h">Linguagens (bytes)</text>'
        f'<text x="20" y="54" class="s">{n_repos} repos próprios · {stars} ★ · {human(grand)} de código</text>'
        f'{"".join(rows)}</svg>'
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}')
    user, token = os.environ["GH_USER"], os.environ.get("GH_TOKEN")
    repos = list_repos(user, token)
    total = aggregate(repos, token)
    if not total:
        sys.exit("nenhuma linguagem coletada; mantendo langs.svg anterior")
    stars = sum(r["stargazers_count"] for r in repos)
    with open("langs.svg", "w", encoding="utf-8") as f:
        f.write(render(total, len(repos), stars))
    # consumido pelo portfólio (fetch do raw.githubusercontent.com); só números agregados, sem nomes de repo
    with open("langs.json", "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "repos": len(repos),
                   "stars": stars, "total": sum(total.values()),
                   "languages": [{"name": n, "bytes": b} for n, b in total.most_common()]}, f)
    log.info("done repos=%d languages=%d", len(repos), len(total))


if __name__ == "__main__":
    main()
