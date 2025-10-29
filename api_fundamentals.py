# -*- coding: utf-8 -*-
"""
CLI para CRUD con Directus.
- Autenticación por token o login (opcional).
- Menú con acciones CRUD sobre una colección.
- Visualización con 'tabulate'.
- Exportación a CSV del último listado.
Código en inglés; comentarios explicativos en español (ADSO - SENA).
"""

import csv
import os
import sys
import json
from typing import Any, Dict, List, Optional, Tuple

import requests
from tabulate import tabulate
from dotenv import load_dotenv

# -----------------------------
# Config & Auth
# -----------------------------

load_dotenv()

BASE_URL = os.getenv("DIRECTUS_URL", "").rstrip("/")
STATIC_TOKEN = os.getenv("DIRECTUS_TOKEN", "")
LOGIN_EMAIL = os.getenv("DIRECTUS_EMAIL", "")
LOGIN_PASSWORD = os.getenv("DIRECTUS_PASSWORD", "")
DEFAULT_COLLECTION = os.getenv("DIRECTUS_DEFAULT_COLLECTION", "articles")

SESSION = requests.Session()
SESSION.headers.update({"Accept": "application/json"})

# Almacena último listado para exportar
_LAST_LIST_CACHE: List[Dict[str, Any]] = []


def ensure_base_url():
    # Validación temprana de la URL base
    if not BASE_URL:
        print("❌ Missing DIRECTUS_URL in .env")
        sys.exit(1)


def authenticate_if_needed() -> None:
    """
    Autenticación:
    - Si hay STATIC_TOKEN, usarlo.
    - Si no, intenta login con email/password para obtener token.
    """
    if STATIC_TOKEN:
        SESSION.headers["Authorization"] = f"Bearer {STATIC_TOKEN}"
        return

    if LOGIN_EMAIL and LOGIN_PASSWORD:
        auth_url = f"{BASE_URL}/auth/login"
        payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
        try:
            resp = SESSION.post(auth_url, json=payload, timeout=30)
            data = resp.json()
            if resp.ok and data.get("data", {}).get("access_token"):
                token = data["data"]["access_token"]
                SESSION.headers["Authorization"] = f"Bearer {token}"
            else:
                print("❌ Login failed. Check DIRECTUS_EMAIL / DIRECTUS_PASSWORD.")
                sys.exit(1)
        except requests.RequestException as e:
            print(f"❌ Auth error: {e}")
            sys.exit(1)
    else:
        print("❌ Provide DIRECTUS_TOKEN or DIRECTUS_EMAIL + DIRECTUS_PASSWORD in .env")
        sys.exit(1)


# -----------------------------
# Utilidades de API
# -----------------------------


def api_request(
    method: str, path: str, *, params=None, json=None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Envoltura para peticiones a Directus.
    Retorna (ok, data_dict). Si hay error, intenta formatearlo.
    """
    url = f"{BASE_URL}{path}"
    try:
        resp = SESSION.request(method, url, params=params, json=json, timeout=60)
        payload = {}
        try:
            payload = resp.json()
        except ValueError:
            payload = {"raw": resp.text}

        if resp.ok:
            return True, payload
        else:
            # Directus suele responder con {errors: [...]}
            err = payload.get("errors") or payload
            return False, {"status": resp.status_code, "errors": err}
    except requests.RequestException as e:
        return False, {"status": 0, "errors": str(e)}


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", sep: str = "."
) -> Dict[str, Any]:
    """
    Aplana diccionarios anidados para mostrarlos en tabla.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def print_table(rows: List[Dict[str, Any]], max_cols: int = 12) -> None:
    """
    Muestra filas en tabla con tabulate.
    Limita columnas si son demasiadas para una vista rápida.
    """
    if not rows:
        print("∅ No data")
        return
    # Determinar columnas (hasta max_cols) basadas en la unión de llaves
    all_keys = []
    for r in rows:
        for k in r.keys():
            if k not in all_keys:
                all_keys.append(k)
    header = all_keys[:max_cols]
    table = [[r.get(c, "") for c in header] for r in rows]
    print(tabulate(table, headers=header, tablefmt="github"))


def export_csv(rows: List[Dict[str, Any]], filename: str) -> None:
    """
    Exporta filas a CSV. Calcula cabeceras por unión de llaves.
    """
    if not rows:
        print("∅ Nothing to export")
        return
    headers = []
    for r in rows:
        for k in r.keys():
            if k not in headers:
                headers.append(k)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow({h: r.get(h, "") for h in headers})
    print(f"✅ CSV exported → {filename}")


# -----------------------------
# Operaciones Directus
# -----------------------------


def get_collection_fields(collection: str) -> List[Dict[str, Any]]:
    """
    Obtiene metadatos de campos para una colección.
    Filtra algunas propiedades de sistema de solo lectura.
    """
    ok, data = api_request("GET", f"/fields/{collection}")
    if not ok:
        print(f"⚠️ Could not fetch fields: {data}")
        return []

    fields = data.get("data", [])
    # Excluir campos técnicos comunes (ajusta según tu proyecto)
    exclude = {"date_created", "date_updated", "user_created", "user_updated"}
    filtered = [f for f in fields if f.get("field") not in exclude]
    return filtered


def list_items(
    collection: str, limit: int = 10, page: int = 1, query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Lista items con soporte básico de paginación.
    `query` puede contener filtros Directus (ejemplo simple).
    """
    params = {
        "limit": limit,
        "page": page,
    }
    if query:
        # Nota: Los filtros de Directus pueden ser complejos; aquí aceptamos 'filter' crudo en JSON
        try:
            params["filter"] = json.loads(query)
        except Exception:
            print(
                '⚠️ Ignoring invalid filter JSON. Example: {"status": {"_eq": "published"}}'
            )

    ok, data = api_request("GET", f"/items/{collection}", params=params)
    if not ok:
        print(f"❌ List error: {data}")
        return []

    items = data.get("data", [])
    # Aplanar para impresión
    rows = [flatten_dict(it) for it in items]
    # Guarda en caché para exportación
    global _LAST_LIST_CACHE
    _LAST_LIST_CACHE = rows
    return rows


def get_item(collection: str, item_id: Any) -> Optional[Dict[str, Any]]:
    ok, data = api_request("GET", f"/items/{collection}/{item_id}")
    if not ok:
        print(f"❌ Get error: {data}")
        return None
    item = data.get("data", {})
    return flatten_dict(item)


def create_item(collection: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ok, data = api_request("POST", f"/items/{collection}", json=payload)
    if not ok:
        print(f"❌ Create error: {data}")
        return None
    return flatten_dict(data.get("data", {}))


def update_item(
    collection: str, item_id: Any, payload: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    ok, data = api_request("PATCH", f"/items/{collection}/{item_id}", json=payload)
    if not ok:
        print(f"❌ Update error: {data}")
        return None
    return flatten_dict(data.get("data", {}))


def delete_item(collection: str, item_id: Any) -> bool:
    ok, data = api_request("DELETE", f"/items/{collection}/{item_id}")
    if not ok:
        print(f"❌ Delete error: {data}")
        return False
    return True


# -----------------------------
# CLI Interactivo
# -----------------------------


def prompt_collection(default_name: str) -> str:
    name = input(f"Collection name [{default_name}]: ").strip()
    return name or default_name


def prompt_int(msg: str, default: int) -> int:
    val = input(f"{msg} [{default}]: ").strip()
    if not val:
        return default
    try:
        return int(val)
    except ValueError:
        print("⚠️ Invalid number; using default.")
        return default


def build_payload_from_fields(
    fields: List[Dict[str, Any]], mode: str = "create"
) -> Dict[str, Any]:
    """
    Pregunta por valores campo a campo usando metadatos de Directus.
    'mode' puede ser 'create' o 'update'.
    Evita pedir 'id' en create si está autoincrementado.
    """
    payload: Dict[str, Any] = {}
    for f in fields:
        field_name = f.get("field")
        interface = f.get("interface")
        required = f.get("required", False)
        readonly = f.get("readonly", False)
        hidden = f.get("hidden", False)
        special = f.get("special") or []

        # Saltar campos solamente de lectura o escondidos
        if readonly or hidden:
            continue

        # Si estamos creando y el id es autogenerado, evitar pedirlo
        if mode == "create" and (
            field_name == "id" or "uuid" in special or "primaryKey" in special
        ):
            continue

        placeholder = ""
        if interface:
            placeholder = f" ({interface})"
        req_mark = "*" if required else ""
        raw = input(f" - {field_name}{placeholder}{req_mark}: ").strip()
        if raw == "" and required:
            print("  ⚠️ This field is required; leaving empty may cause an error.")
        # Conversión simple: JSON si parece JSON, si no, string
        try:
            # Permite ingresar objetos/arrays como JSON
            value = (
                json.loads(raw) if raw.startswith("{") or raw.startswith("[") else raw
            )
        except Exception:
            value = raw
        payload[field_name] = value  # type: ignore
    return payload


def main_loop():
    ensure_base_url()
    authenticate_if_needed()

    collection = DEFAULT_COLLECTION
    print("\n🔗 Directus CLI ready.")
    print(f"Base URL: {BASE_URL}")
    print(f"Default collection: {collection}\n")

    while True:
        print("\n==== MENU ====")
        print("1) List items")
        print("2) Get item by ID")
        print("3) Create item")
        print("4) Update item")
        print("5) Delete item")
        print("6) Change collection")
        print("7) Export last list to CSV")
        print("0) Exit")
        choice = input("> Choose: ").strip()

        if choice == "0":
            print("Bye! 👋")
            break

        elif choice == "6":
            collection = prompt_collection(collection)

        elif choice == "1":
            limit = prompt_int("Limit", 10)
            page = prompt_int("Page", 1)
            print(
                'Optional filter as JSON (Directus "filter"), e.g. {"status":{"_eq":"published"}}'
            )
            query = input("Filter JSON (or empty): ").strip() or None
            rows = list_items(collection, limit=limit, page=page, query=query)
            print_table(rows)

        elif choice == "2":
            item_id = input("Item ID: ").strip()
            row = get_item(collection, item_id)
            print_table([row] if row else [])

        elif choice == "3":
            fields = get_collection_fields(collection)
            payload = build_payload_from_fields(fields, mode="create")
            created = create_item(collection, payload)
            print_table([created] if created else [])

        elif choice == "4":
            item_id = input("Item ID to update: ").strip()
            fields = get_collection_fields(collection)
            payload = build_payload_from_fields(fields, mode="update")
            updated = update_item(collection, item_id, payload)
            print_table([updated] if updated else [])

        elif choice == "5":
            item_id = input("Item ID to delete: ").strip()
            confirm = input(f"Type 'YES' to confirm deletion of {item_id}: ")
            if confirm == "YES":
                ok = delete_item(collection, item_id)
                print("✅ Deleted" if ok else "❌ Delete failed")
            else:
                print("Deletion cancelled.")

        elif choice == "7":
            if not _LAST_LIST_CACHE:
                print("∅ No previous list to export. Run 'List items' first.")
            else:
                fname = input("CSV filename [export.csv]: ").strip() or "export.csv"
                export_csv(_LAST_LIST_CACHE, fname)
        else:
            print("⚠️ Invalid option.")


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")
