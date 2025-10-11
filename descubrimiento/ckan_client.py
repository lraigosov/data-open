import os
import json
from typing import Dict, Any, Generator, List, Optional
from datetime import datetime

import requests


def query_ckan_catalog(base_url: str = "https://datos.gob.mx",
                       q: Optional[str] = None,
                       organization: Optional[str] = None,
                       groups: Optional[List[str]] = None,
                       start: int = 0,
                       rows: int = 100,
                       max_pages: int = 50) -> Generator[Dict[str, Any], None, None]:
    """
    Generador que recorre la API CKAN package_search devolviendo packages (datasets).
    - base_url: URL base del portal CKAN (ej. "https://datos.gob.mx").
    - q: término de búsqueda.
    - organization: filtrar por organización específica.
    - groups: lista de grupos/categorías para filtrar.
    - start: índice de inicio (paginación).
    - rows: tamaño de página (<= 1000 típicamente).
    - max_pages: tope de páginas a recorrer.
    """
    endpoint = f"{base_url}/api/3/action/package_search"
    
    params: Dict[str, Any] = {
        "start": start,
        "rows": min(rows, 1000),  # CKAN típicamente limita a 1000
    }
    
    if q:
        params["q"] = q
    if organization:
        params["fq"] = f"organization:{organization}"
    if groups:
        # CKAN usa 'groups' como filtro adicional
        group_filter = " OR ".join(f"groups:{g}" for g in groups)
        if "fq" in params:
            params["fq"] += f" AND ({group_filter})"
        else:
            params["fq"] = f"({group_filter})"
    
    for page in range(max_pages):
        try:
            resp = requests.get(endpoint, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get("success", False):
                print(f"ADVERTENCIA: CKAN API retornó success=false para {base_url}")
                break
            
            result = data.get("result", {})
            results = result.get("results", [])
            count = result.get("count", 0)
            
            if not results:
                break
                
            for item in results:
                yield item
                
            # Verificar si hay más páginas
            if params["start"] + params["rows"] >= count:
                break
                
            params["start"] += params["rows"]
            
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Fallo al consultar CKAN {base_url}: {e}")
            break


def normalize_ckan_result(item: Dict[str, Any], base_url: str = "https://datos.gob.mx") -> Dict[str, Any]:
    """
    Extrae campos útiles de un package CKAN en un dict plano compatible con Socrata.
    """
    # Obtener tags como lista de strings
    tags = [tag.get("display_name", tag.get("name", "")) for tag in item.get("tags", [])]
    
    # Obtener grupos/categorías
    groups = [group.get("display_name", group.get("title", group.get("name", ""))) 
              for group in item.get("groups", [])]
    
    # Organización
    org = item.get("organization", {}) or {}
    org_title = org.get("title", org.get("name", ""))
    
    return {
        "name": item.get("title", item.get("name", "")),
        "id": item.get("id", ""),
        "type": "dataset",  # CKAN packages son típicamente datasets
        "description": item.get("notes", ""),
        "domain": None,  # CKAN no tiene concepto de dominio como Socrata
        "permalink": f"{item.get('ckan_url', base_url)}/dataset/{item.get('name', '')}",
        "link": f"{item.get('ckan_url', base_url)}/dataset/{item.get('name', '')}",
        "domain_category": org_title,
        "categories": ",".join(groups),
        "tags": ",".join(tags),
        "download_count": None,  # CKAN no siempre expone download count en package_search
        "publication_date": item.get("metadata_created", ""),
        "num_resources": item.get("num_resources", 0),
        "license": item.get("license_title", item.get("license_id", "")),
        "organization": org_title,
    }


def fetch_ckan_by_config(base_url: str = "https://datos.gob.mx",
                         q: Optional[str] = None,
                         groups: Optional[List[str]] = None,
                         per_query_limit: int = 1000) -> List[Dict[str, Any]]:
    """
    Consulta CKAN y devuelve una lista de resultados normalizados.
    Limita el total por consulta para evitar respuestas enormes.
    """
    all_rows: List[Dict[str, Any]] = []
    count = 0
    
    for item in query_ckan_catalog(base_url=base_url, q=q, groups=groups, rows=100, max_pages=100):
        all_rows.append(normalize_ckan_result(item, base_url))
        count += 1
        if count >= per_query_limit:
            break
    
    return all_rows


if __name__ == "__main__":
    # Prueba rápida con México
    import argparse
    parser = argparse.ArgumentParser(description="Consultar CKAN API de México")
    parser.add_argument("--base-url", default="https://datos.gob.mx", help="URL base CKAN")
    parser.add_argument("--q", help="Término de búsqueda", default=None)
    parser.add_argument("--groups", nargs="*", help="Grupos/categorías a filtrar", default=None)
    parser.add_argument("--limit", type=int, default=100, help="Límite de resultados")
    parser.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "output", "preview_mexico"),
                        help="Ruta base de salida (sin extensión)")
    args = parser.parse_args()
    
    from socrata_discovery import save_json, save_csv
    
    rows = fetch_ckan_by_config(base_url=args.base_url, q=args.q, groups=args.groups, per_query_limit=args.limit)
    save_json(args.out + ".json", rows)
    save_csv(args.out + ".csv", rows)
    print(f"Guardado: {args.out}.json y {args.out}.csv ({len(rows)} filas)")