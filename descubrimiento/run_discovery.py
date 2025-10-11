import os
import json
from typing import Dict, List, Optional

from socrata_discovery import fetch_by_domains, save_json, save_csv, load_app_token
from ckan_client import fetch_ckan_by_config


HERE = os.path.dirname(__file__)
DOMAINS_FILE = os.path.join(HERE, "latam_domains.json")
CONFIG_FILE = os.path.join(HERE, "config.json")
OUTPUT_DIR = os.path.join(HERE, "output")


def load_domains(path: str = DOMAINS_FILE) -> Dict[str, Dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, dict), "latam_domains.json debe ser un objeto JSON {pais: config}"
        return data


def _aggregate_summary(rows: List[dict]) -> List[dict]:
    from collections import Counter
    by_type = Counter(r.get("type") or "unknown" for r in rows)
    by_category = Counter()
    for r in rows:
        cats = (r.get("categories") or "").split(",") if r.get("categories") else []
        for c in cats:
            c = c.strip()
            if c:
                by_category[c] += 1
    summary_rows = []
    for k, v in sorted(by_type.items(), key=lambda x: (-x[1], x[0] or "")):
        summary_rows.append({"metric": "type", "key": k, "count": v})
    for k, v in sorted(by_category.items(), key=lambda x: (-x[1], x[0])):
        summary_rows.append({"metric": "category", "key": k, "count": v})
    return summary_rows


def _parse_date(s: Optional[str]):
    if not s:
        return None
    from datetime import datetime, date
    # Solo formatos de fecha completos (YYYY-MM-DD o con /)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _filter_by_publication_date(rows: List[dict], dfrom: Optional[str], dto: Optional[str]) -> List[dict]:
    if not dfrom and not dto:
        return rows
    from datetime import datetime
    dfrom_d = _parse_date(dfrom)
    dto_d = _parse_date(dto)

    def parse_item_date(item_date: Optional[str]):
        if not item_date:
            return None
        s = item_date.strip()
        # Manejar sufijo Z (UTC) convirtiéndolo a offset ISO compatible
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        # Intentar ISO nativo
        try:
            return datetime.fromisoformat(s).date()
        except Exception:
            pass
        # Intentar patrones comunes sin zona
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(s[:26], fmt).date()
            except ValueError:
                continue
        return None

    out = []
    for r in rows:
        pd = r.get("publication_date")
        dt = parse_item_date(pd) if isinstance(pd, str) else None
        if dfrom_d and (not dt or dt < dfrom_d):
            continue
        if dto_d and (not dt or dt > dto_d):
            continue
        out.append(r)
    return out


def run_for_country(country: str, config: Dict, q: Optional[str] = None, categories: Optional[List[str]] = None,
                    per_domain_limit: int = 1000, published_from: Optional[str] = None, published_to: Optional[str] = None) -> int:
    platform = config.get("platform", "socrata")
    
    if platform == "socrata":
        domains = config.get("domains", [])
        rows = fetch_by_domains(domains, q=q, categories=categories, per_domain_limit=per_domain_limit)
    elif platform == "ckan":
        base_url = config.get("base_url", "https://datos.gob.mx")
        # Convertir categories a groups para CKAN
        groups = categories if categories else None
        rows = fetch_ckan_by_config(base_url=base_url, q=q, groups=groups, per_query_limit=per_domain_limit)
    else:
        print(f"ADVERTENCIA: Plataforma '{platform}' no soportada para {country}")
        rows = []
    
    rows = _filter_by_publication_date(rows, published_from, published_to)
    base = os.path.join(OUTPUT_DIR, f"{country.lower().replace(' ', '_')}_catalog")
    save_json(base + ".json", rows)
    save_csv(base + ".csv", rows)
    # summary
    summary = _aggregate_summary(rows)
    summary_path = os.path.join(OUTPUT_DIR, f"{country.lower().replace(' ', '_')}_summary.csv")
    save_csv(summary_path, summary)
    return len(rows)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inventario de datasets LATAM usando Socrata Discovery API")
    parser.add_argument("--country", help="País a procesar (si se omite, procesa todos)")
    parser.add_argument("--q", help="Término de búsqueda general", default=None)
    parser.add_argument("--categories", nargs="*", help="Filtrar por categorías", default=None)
    parser.add_argument("--limit", type=int, default=1000, help="Límite de items por dominio")
    parser.add_argument("--published-from", dest="published_from", help="Fecha mínima de publicación (YYYY-MM-DD)")
    parser.add_argument("--published-to", dest="published_to", help="Fecha máxima de publicación (YYYY-MM-DD)")
    args = parser.parse_args()

    # Feedback sobre token
    token = load_app_token()
    if token:
        print("Usando X-App-Token (encontrado).")
    else:
        print("ADVERTENCIA: No se encontró App Token. La API puede rate-limitar o fallar.")

    # Cargar config (opcional)
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f) or {}
        except Exception:
            cfg = {}

    # Prioridad: flags CLI > config.json > None
    published_from = args.published_from or cfg.get("published_from")
    published_to = args.published_to or cfg.get("published_to")

    domains_map = load_domains()
    total = 0
    if args.country:
        country_key = None
        # Búsqueda flexible por nombre (case-insensitive)
        for k in domains_map.keys():
            if k.lower() == args.country.lower():
                country_key = k
                break
        if not country_key:
            raise SystemExit(f"País no encontrado en latam_domains.json: {args.country}")
        count = run_for_country(country_key, domains_map[country_key], q=args.q, categories=args.categories,
                                per_domain_limit=args.limit, published_from=published_from, published_to=published_to)
        print(f"{country_key}: {count} registros")
        total += count
    else:
        for country, config in domains_map.items():
            count = run_for_country(country, config, q=args.q, categories=args.categories,
                                    per_domain_limit=args.limit, published_from=published_from, published_to=published_to)
            print(f"{country}: {count} registros")
            total += count
    print(f"Total registros exportados: {total}")
