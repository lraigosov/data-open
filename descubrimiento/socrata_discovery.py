import os
import json
from typing import Dict, Any, Generator, List, Optional

import requests


DISCOVERY_BASE = os.environ.get("SOCRATA_DISCOVERY_BASE", "https://api.us.socrata.com/api/catalog/v1")


def load_app_token(secret_file: str = os.path.join(os.path.dirname(__file__), "..", "secretos.json")) -> Optional[str]:
    """
    Carga el App Token desde variables de entorno o un archivo secretos.json.
    Precedencia: env(SOCRATA_APP_TOKEN) > secretos.json[AppToken|APIKeyID].
    """
    token = os.environ.get("SOCRATA_APP_TOKEN")
    if token:
        return token

    try:
        with open(os.path.abspath(secret_file), "r", encoding="utf-8") as f:
            # El archivo podría ser JSON o estilo .env antiguo; intentamos JSON primero
            text = f.read().strip()
            try:
                data = json.loads(text)
                for k in ("AppToken", "APIKeyID", "APIKeyId", "api_key", "token"):
                    if isinstance(data, dict) and k in data and data[k]:
                        return str(data[k])
            except json.JSONDecodeError:
                # Formato clave=valor
                for line in text.splitlines():
                    if not line or line.strip().startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() in ("AppToken", "APIKeyID"):
                            return v.strip()
    except FileNotFoundError:
        pass
    return None


def query_catalog(domain: Optional[str] = None,
                  q: Optional[str] = None,
                  categories: Optional[List[str]] = None,
                  limit: int = 100,
                  max_pages: int = 50,
                  app_token: Optional[str] = None) -> Generator[Dict[str, Any], None, None]:
    """
    Generador que recorre la Discovery API devolviendo items del catálogo.
    - domain: restringe por dominio (e.g. "www.datos.gov.co").
    - q: término de búsqueda.
    - categories: lista de categorías para filtrar.
    - limit: tamaño de página (<= 100 recomendado por la API).
    - max_pages: tope de páginas a recorrer para evitar loops infinitos.
    - app_token: token opcional para cabecera X-App-Token.
    """
    headers = {}
    token = app_token or load_app_token()
    if token:
        headers["X-App-Token"] = token

    params: Dict[str, Any] = {
        "limit": max(1, min(limit, 100)),
        "offset": 0,
    }
    if domain:
        params["domains"] = domain
    if q:
        params["q"] = q
    if categories:
        # La API acepta categories como lista repetida o CSV; probamos CSV
        params["categories"] = ",".join(categories)

    for page in range(max_pages):
        try:
            resp = requests.get(DISCOVERY_BASE, params=params, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 404:
                # Dominio no encontrado en Discovery API, omitir silenciosamente
                print(f"ADVERTENCIA: Dominio '{domain}' no encontrado en Discovery API (404)")
                break
            else:
                raise e
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Fallo al consultar dominio '{domain}': {e}")
            break

        results = data.get("results", [])
        if not results:
            break
        for item in results:
            yield item
        params["offset"] += params["limit"]


def normalize_result(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrae campos útiles en un dict plano.
    """
    resource = item.get("resource", {})
    classification = item.get("classification", {})
    metadata = item.get("metadata", {})

    return {
        "name": resource.get("name"),
        "id": resource.get("id"),
        "type": resource.get("type"),
        "description": resource.get("description"),
        "domain": metadata.get("domain"),
        "permalink": item.get("permalink"),
        "link": item.get("link"),
        "domain_category": classification.get("domain_category"),
        "categories": ",".join(classification.get("categories", []) or []),
        "tags": ",".join(classification.get("tags", []) or []),
        "download_count": item.get("view",
                                     {}).get("download_count") or item.get("download_count"),
        "publication_date": item.get("view", {}).get("publication_date") or resource.get("publication_date"),
    }


def fetch_by_domains(domains: List[str], q: Optional[str] = None, categories: Optional[List[str]] = None,
                     per_domain_limit: int = 500, app_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Consulta el catálogo para una lista de dominios y devuelve una lista de resultados normalizados.
    Limita el total por dominio para evitar respuestas enormes por defecto.
    """
    all_rows: List[Dict[str, Any]] = []
    for domain in domains:
        count = 0
        for item in query_catalog(domain=domain, q=q, categories=categories, limit=100, max_pages=100, app_token=app_token):
            all_rows.append(normalize_result(item))
            count += 1
            if count >= per_domain_limit:
                break
    return all_rows


def save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    import csv
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not rows:
        # Crear CSV vacío con cabeceras mínimas
        headers = ["name", "id", "type", "domain", "permalink", "domain_category"]
    else:
        # Unir todas las claves para columnas completas
        headers = sorted({k for row in rows for k in row.keys()})
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    # Prueba rápida: leer dominios desde arg o usar Colombia por defecto
    import argparse
    parser = argparse.ArgumentParser(description="Consultar Discovery API de Socrata por dominios")
    parser.add_argument("--domains", nargs="*", help="Lista de dominios a consultar")
    parser.add_argument("--q", help="Término de búsqueda", default=None)
    parser.add_argument("--categories", nargs="*", help="Categorías a filtrar", default=None)
    parser.add_argument("--limit", type=int, default=300, help="Límite por dominio")
    parser.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "output", "preview_colombia"),
                        help="Ruta base de salida (sin extensión)")
    args = parser.parse_args()

    domains = args.domains or ["www.datos.gov.co"]
    rows = fetch_by_domains(domains, q=args.q, categories=args.categories, per_domain_limit=args.limit)
    save_json(args.out + ".json", rows)
    save_csv(args.out + ".csv", rows)
    print(f"Guardado: {args.out}.json y {args.out}.csv ({len(rows)} filas)")
