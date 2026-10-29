"""Gera langs.svg, metrics.svg e langs.json: linguagens por bytes agregados nos repos do usuário (API de linguagens do GitHub).

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
# Tokens do portfólio (alysontrizotto.vercel.app): fundo escuro, acento ciano-menta + índigo
BG, TITLE, TEXT, MUTED, BAR_BG, LINE = "#07080b", "#5eead4", "#e8eaf0", "#7d8394", "#1b1f2a", "#1b1f2a"
ACC, ACC2 = "#5eead4", "#818cf8"
PALETTE = ["#5eead4", "#6ee0d6", "#7fd0e0", "#93bcea", "#818cf8", "#7a82e6", "#6f78cc", "#5a6178"]
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
# Fallback das métricas de downloads se a API falhar (mesmos valores do portfólio)
DL_FALLBACK = (1100, 2300)
PACKAGIST = "https://packagist.org/packages/alysontrizotto/laravel-ddl-crud.json"
OPEN_VSX = "https://open-vsx.org/api/alysontrizotto/ruby-nav"

log = logging.getLogger("gen_langs")


def get(url: str, token: str | None) -> tuple[object, str]:
    # Accept do GitHub só para a API do GitHub; Packagist/Open VSX respondem 406 a ele
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"} if url.startswith(API) else {})
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
    own = [r for r in repos if not r["fork"]]
    # diagnóstico: token ausente/limitado aparece aqui como poucos repos e zero privados
    log.info("repos_listed token=%s total=%d forks=%d private=%d kept=%d", bool(token), len(repos),
             len(repos) - len(own), sum(r["private"] for r in own), len(own))
    return own


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
            f'<rect x="130" y="{y - 10}" width="150" height="8" rx="4" fill="{BAR_BG}"/>'
            f'<rect x="130" y="{y - 10}" width="{max(pct / 100 * 150, 2):.1f}" height="8" rx="4" fill="{color}"/>'
            f'<text x="400" y="{y}" class="t" text-anchor="end">{pct:.1f}% · {human(b)}</text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="Linguagens por bytes">'
        f'<style>.h{{font:700 17px system-ui,-apple-system,"Segoe UI",sans-serif;fill:{TEXT}}}'
        f'.t{{font:500 12px {MONO};fill:{TEXT}}}'
        f'.s{{font:400 11px {MONO};fill:{MUTED}}}</style>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{BG}" stroke="{LINE}"/>'
        f'<text x="20" y="32" class="h">Linguagens <tspan fill="{ACC}">(bytes)</tspan></text>'
        f'<text x="20" y="54" class="s">{n_repos} repos próprios · {stars} ★ · {human(grand)} de código</text>'
        f'{"".join(rows)}</svg>'
    )


def downloads() -> tuple[int, int]:
    """Totais vivos (Packagist, Open VSX); cai no fallback por métrica se a API falhar."""
    out = []
    for (url, pick), fb in zip(((PACKAGIST, lambda d: d["package"]["downloads"]["total"]),
                                (OPEN_VSX, lambda d: d["downloadCount"])), DL_FALLBACK):
        try:
            out.append(pick(get(url, None)[0]) or fb)
        except Exception:
            log.exception("downloads_failed")
            out.append(fb)
    return out[0], out[1]


def render_metrics(dl: tuple[int, int]) -> str:
    cells = [("-73%", "latência da busca"), ("-47%", "memória em produção"),
             (f"{dl[0]:,}+".replace(",", "."), "downloads · ddl-crud"),
             (f"{dl[1]:,}+".replace(",", "."), "downloads · ruby-nav")]
    w, h, cw = 840, 110, 210
    parts = []
    for i, (num, label) in enumerate(cells):
        x = i * cw + 24
        if i:
            parts.append(f'<line x1="{i * cw}" y1="18" x2="{i * cw}" y2="{h - 18}" stroke="{LINE}"/>')
        parts.append(f'<text x="{x}" y="58" class="n">{num}</text><text x="{x}" y="82" class="l">{escape(label)}</text>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Métricas">'
        f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC2}"/></linearGradient></defs>'
        f'<style>.n{{font:700 32px {MONO};fill:url(#g)}}.l{{font:400 12px {MONO};fill:{MUTED}}}</style>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{BG}" stroke="{LINE}"/>{"".join(parts)}</svg>'
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
    with open("metrics.svg", "w", encoding="utf-8") as f:
        f.write(render_metrics(downloads()))
    # consumido pelo portfólio (fetch do raw.githubusercontent.com); só números agregados, sem nomes de repo
    with open("langs.json", "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "repos": len(repos),
                   "stars": stars, "total": sum(total.values()),
                   "languages": [{"name": n, "bytes": b} for n, b in total.most_common()]}, f)
    log.info("done repos=%d languages=%d", len(repos), len(total))


if __name__ == "__main__":
    main()
