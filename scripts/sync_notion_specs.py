#!/usr/bin/env python3
"""
Sync Notion Specifications to Local Workspace.
Migrates spec documents under Notion "GTA / 프로젝트 개발" to local folders:
- requirement-specs/
- functional-specs/
- domain-specs/
- api-specs/

Reads NOTION_TOKEN from environment variables or local .env file.
"""

import os
import sys
import json
import shutil
import urllib.request
import urllib.error
from pathlib import Path

# Project Root Directory
REPO_ROOT = Path(__file__).resolve().parent.parent

# --- Helper to load .env file if present ---
def load_dotenv():
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v

load_dotenv()

# --- Configuration & Authentication ---

def get_notion_token():
    token = os.environ.get("NOTION_TOKEN")
    if token:
        return token
    openapi_headers = os.environ.get("OPENAPI_MCP_HEADERS")
    if openapi_headers:
        try:
            parsed = json.loads(openapi_headers)
            auth = parsed.get("Authorization", "")
            if auth.startswith("Bearer "):
                return auth.split("Bearer ")[1].strip()
        except Exception:
            pass
    return None

NOTION_TOKEN = get_notion_token()

if not NOTION_TOKEN:
    print("❌ Error: NOTION_TOKEN is missing!", flush=True)
    print("Please set NOTION_TOKEN in your environment or in a .env file.", flush=True)
    print("Example: export NOTION_TOKEN='ntn_your_notion_token_here'", flush=True)
    sys.exit(1)

BASE_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

# Notion Database IDs (Configurable via ENV or defaults)
DB_REQ = os.environ.get("NOTION_DB_REQ", "ef9d79a391fa43a78eb58c6a71fc4ef9")      # 요구사항 정의서
DB_FUN = os.environ.get("NOTION_DB_FUN", "e0df11516e6a44319e5ca51e1e25c913")      # 기능 명세서
DB_DOM = os.environ.get("NOTION_DB_DOM", "3911d7341cda801a9858c8a1bc7dca12")      # 데이터 및 도메인 정의서
DB_API_FB = os.environ.get("NOTION_DB_API_FB", "3911d7341cda807a9590d2f496218c70")   # API 명세서 FE - BE
DB_API_BA = os.environ.get("NOTION_DB_API_BA", "3911d7341cda807a8361e4d48e51ed39")   # API 명세서 BE - AI


# --- Helper Functions for Notion API ---

def query_database(db_id):
    """Query all pages from a Notion database with pagination."""
    url = f"{BASE_URL}/databases/{db_id}/query"
    results = []
    has_more = True
    start_cursor = None

    while has_more:
        body = {"page_size": 100}
        if start_cursor:
            body["start_cursor"] = start_cursor
        
        req = urllib.request.Request(
            url,
            headers=HEADERS,
            data=json.dumps(body).encode("utf-8"),
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error querying database {db_id}: {e.code} - {e.read().decode('utf-8')}", flush=True)
            sys.exit(1)
        except Exception as e:
            print(f"Error querying database {db_id}: {e}", flush=True)
            sys.exit(1)

    return results


def fetch_child_blocks(block_id):
    """Fetch all child blocks of a Notion block/page with pagination."""
    url = f"{BASE_URL}/blocks/{block_id}/children?page_size=100"
    results = []
    has_more = True
    start_cursor = None

    while has_more:
        req_url = f"{url}&start_cursor={start_cursor}" if start_cursor else url
        req = urllib.request.Request(req_url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
        except Exception as e:
            print(f"Warning: Failed to fetch blocks for block_id={block_id}: {e}", flush=True)
            break

    return results


def rich_text_to_md(rich_texts):
    """Convert Notion rich text array to Markdown string."""
    if not rich_texts:
        return ""
    md_parts = []
    for rt in rich_texts:
        text = rt.get("plain_text", "")
        if not text:
            continue
        ann = rt.get("annotations", {})
        if ann.get("code"):
            text = f"`{text}`"
        if ann.get("bold"):
            text = f"**{text}**"
        if ann.get("italic"):
            text = f"*{text}*"
        if ann.get("strikethrough"):
            text = f"~~{text}~~"
        if rt.get("href"):
            text = f"[{text}]({rt['href']})"
        md_parts.append(text)
    return "".join(md_parts)


def get_prop_text(props, prop_name):
    """Extract plain text from a property in properties dict."""
    prop = props.get(prop_name)
    if not prop:
        return ""
    ptype = prop.get("type")
    if ptype == "title":
        return rich_text_to_md(prop.get("title", []))
    elif ptype == "rich_text":
        return rich_text_to_md(prop.get("rich_text", []))
    elif ptype == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    elif ptype == "multi_select":
        sels = prop.get("multi_select", [])
        return ", ".join([s.get("name", "") for s in sels if s.get("name")])
    elif ptype == "number":
        val = prop.get("number")
        return str(val) if val is not None else ""
    elif ptype == "checkbox":
        return "Y" if prop.get("checkbox") else "N"
    elif ptype == "relation":
        rels = prop.get("relation", [])
        return f"{len(rels)}개 연동" if rels else ""
    return ""


def convert_blocks_to_md(blocks, indent_level=0):
    """Recursively convert Notion block list into clean Markdown text."""
    lines = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        btype = b.get("type")
        has_children = b.get("has_children", False)
        block_id = b.get("id")

        if btype == "paragraph":
            text = rich_text_to_md(b["paragraph"].get("rich_text", []))
            lines.append(f"{text}\n" if text else "\n")

        elif btype in ("heading_1", "heading_2", "heading_3"):
            level = int(btype[-1])
            text = rich_text_to_md(b[btype].get("rich_text", []))
            lines.append(f"\n{'#' * level} {text}\n")

        elif btype == "bulleted_list_item":
            text = rich_text_to_md(b["bulleted_list_item"].get("rich_text", []))
            lines.append(f"{'  ' * indent_level}- {text}")

        elif btype == "numbered_list_item":
            text = rich_text_to_md(b["numbered_list_item"].get("rich_text", []))
            lines.append(f"{'  ' * indent_level}1. {text}")

        elif btype == "to_do":
            checked = "x" if b["to_do"].get("checked") else " "
            text = rich_text_to_md(b["to_do"].get("rich_text", []))
            lines.append(f"{'  ' * indent_level}- [{checked}] {text}")

        elif btype == "code":
            lang = b["code"].get("language", "")
            text = rich_text_to_md(b["code"].get("rich_text", []))
            lines.append(f"```{lang}\n{text}\n```\n")

        elif btype == "quote":
            text = rich_text_to_md(b["quote"].get("rich_text", []))
            lines.append(f"> {text}\n")

        elif btype == "callout":
            text = rich_text_to_md(b["callout"].get("rich_text", []))
            lines.append(f"> 💡 {text}\n")

        elif btype == "divider":
            lines.append("\n---\n")

        elif btype == "table":
            table_children = fetch_child_blocks(block_id)
            table_rows = []
            for tr in table_children:
                if tr.get("type") == "table_row":
                    cells = [rich_text_to_md(cell) for cell in tr["table_row"].get("cells", [])]
                    table_rows.append(cells)
            if table_rows:
                header_row = table_rows[0]
                lines.append("| " + " | ".join(header_row) + " |")
                lines.append("| " + " | ".join([":---"] * len(header_row)) + " |")
                for row in table_rows[1:]:
                    lines.append("| " + " | ".join(row) + " |")
                lines.append("")

        elif btype == "toggle":
            text = rich_text_to_md(b["toggle"].get("rich_text", []))
            lines.append(f"<details><summary>{text}</summary>\n")
            if has_children:
                child_blocks = fetch_child_blocks(block_id)
                lines.append(convert_blocks_to_md(child_blocks, indent_level))
            lines.append("</details>\n")

        if has_children and btype not in ("table", "toggle"):
            child_blocks = fetch_child_blocks(block_id)
            lines.append(convert_blocks_to_md(child_blocks, indent_level + 1))

        i += 1

    return "\n".join(lines)


INDEX_FILES = {"requirement.md", "functional.md", "domain.md", "api.md"}


def clean_directory(dir_path):
    """Clean files in directory except preserved index markdown files."""
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        return

    for item in dir_path.iterdir():
        if item.is_file():
            if item.name not in INDEX_FILES:
                item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


# --- Sync Functions ---

def sync_requirement_specs():
    print("🔄 Syncing requirement-specs...", flush=True)
    target_dir = REPO_ROOT / "requirement-specs"
    clean_directory(target_dir)

    pages = query_database(DB_REQ)
    items = []
    used_ids = set()

    for p in pages:
        explicit_id = get_prop_text(p["properties"], "ID").strip()
        if explicit_id:
            used_ids.add(explicit_id)

    fallback_num = 1
    for p in pages:
        props = p["properties"]
        req_id = get_prop_text(props, "ID").strip()
        if not req_id:
            while f"REQ-{fallback_num}" in used_ids:
                fallback_num += 1
            req_id = f"REQ-{fallback_num}"
            used_ids.add(req_id)

        title = get_prop_text(props, "요구사항 명")
        description = get_prop_text(props, "설명")
        ac = get_prop_text(props, "Acceptance Criteria")

        blocks = fetch_child_blocks(p["id"])
        body_md = convert_blocks_to_md(blocks).strip()

        file_name = f"{req_id}.md"
        file_path = target_dir / file_name

        content = f"# [{req_id}] {title}\n\n"
        content += "## 상세 요구사항\n\n"
        if description:
            content += f"{description}\n\n"
        if body_md:
            content += f"{body_md}\n\n"
        
        if ac:
            content += "## Acceptance Criteria\n\n"
            content += f"{ac}\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        items.append({
            "id": req_id,
            "title": title,
            "description": description,
            "ac": ac,
            "filename": file_name
        })

    def get_sort_key(item):
        num_str = item["id"].replace("REQ-", "").strip()
        return int(num_str) if num_str.isdigit() else 999

    items.sort(key=get_sort_key)

    index_path = target_dir / "requirement.md"
    idx_content = "# 요구사항 정의서 목록\n\n"
    idx_content += "이 문서는 Yeolo 프로젝트의 요구사항 요약 목록입니다. 상세한 설명 및 관련 인수 기준 세부는 각 요구사항 ID 링크의 개별 문서에서 확인할 수 있습니다.\n\n"
    idx_content += "---\n\n"
    idx_content += "| 요구사항 ID | 요구사항 명 | 설명 | 인수기준 |\n"
    idx_content += "| :--- | :--- | :--- | :--- |\n"

    for item in items:
        link_id = f"[{item['id']}](./{item['filename']})"
        desc = item["description"].replace("\n", " ")
        ac = item["ac"].replace("\n", " ")
        idx_content += f"| {link_id} | {item['title']} | {desc} | {ac} |\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

    print(f"✅ requirement-specs synced ({len(items)} items).", flush=True)


def sync_functional_specs():
    print("🔄 Syncing functional-specs...", flush=True)
    target_dir = REPO_ROOT / "functional-specs"
    clean_directory(target_dir)

    pages = query_database(DB_FUN)
    items = []
    used_ids = set()

    for p in pages:
        raw_id = get_prop_text(p["properties"], "기능 ID").strip()
        if raw_id:
            used_ids.add(raw_id.upper())

    fallback_num = 1
    for p in pages:
        props = p["properties"]
        raw_fun_id = get_prop_text(props, "기능 ID").strip()
        if raw_fun_id:
            fun_id = raw_fun_id.upper()
        else:
            while f"FUN-{fallback_num}" in used_ids:
                fallback_num += 1
            fun_id = f"FUN-{fallback_num}"
            used_ids.add(fun_id)

        title = get_prop_text(props, "기능 명")
        scope = get_prop_text(props, "구현 범위")
        screens = get_prop_text(props, "연결된 UI 화면")
        details = get_prop_text(props, "상세 내용 및 예외 처리")
        req_str = get_prop_text(props, "관련 요구사항") or "-"

        blocks = fetch_child_blocks(p["id"])
        body_md = convert_blocks_to_md(blocks).strip()

        file_name = f"{fun_id}.md"
        file_path = target_dir / file_name

        content = f"# [{fun_id}] {title}\n\n"
        content += "## 기능 개요\n\n"
        content += f"- **구현 범위**: {scope or '-'}\n"
        content += f"- **연결된 UI 화면**: {screens or '-'}\n"
        content += f"- **관련 요구사항**: {req_str}\n\n"
        content += "## 상세 내용 및 예외 처리\n\n"
        if details:
            content += f"{details}\n\n"
        if body_md:
            content += f"{body_md}\n\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        items.append({
            "id": fun_id,
            "title": title,
            "scope": scope,
            "screens": screens,
            "req_str": req_str,
            "details": details,
            "filename": file_name
        })

    def get_sort_key(item):
        num_str = item["id"].replace("FUN-", "").strip()
        return int(num_str) if num_str.isdigit() else 999

    items.sort(key=get_sort_key)

    index_path = target_dir / "functional.md"
    idx_content = "# 기능 명세서 목록\n\n"
    idx_content += "이 문서는 Yeolo 프로젝트의 기능 명세 요약 목록입니다. 상세한 비즈니스 로직 및 예외 처리는 각 기능 ID 링크의 개별 문서에서 확인할 수 있습니다.\n\n"
    idx_content += "---\n\n"
    idx_content += "| 기능 ID | 기능 명 | 구현 범위 | 연결된 UI 화면 | 관련 요구사항 |\n"
    idx_content += "| :--- | :--- | :--- | :--- | :--- |\n"

    for item in items:
        link_id = f"[{item['id']}](./{item['filename']})"
        idx_content += f"| {link_id} | {item['title']} | {item['scope']} | {item['screens']} | {item['req_str']} |\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

    print(f"✅ functional-specs synced ({len(items)} items).", flush=True)


def sync_domain_specs():
    print("🔄 Syncing domain-specs...", flush=True)
    target_dir = REPO_ROOT / "domain-specs"
    clean_directory(target_dir)

    pages = query_database(DB_DOM)
    items = []
    used_ids = set()

    for p in pages:
        dom_id = get_prop_text(p["properties"], "Domain ID").strip()
        if dom_id:
            used_ids.add(dom_id.upper())

    fallback_num = 1
    for p in pages:
        props = p["properties"]
        dom_id = get_prop_text(props, "Domain ID").strip().upper()
        if not dom_id:
            while f"DOM-{fallback_num}" in used_ids:
                fallback_num += 1
            dom_id = f"DOM-{fallback_num}"
            used_ids.add(dom_id)

        title = get_prop_text(props, "도메인 명")

        blocks = fetch_child_blocks(p["id"])
        body_md = convert_blocks_to_md(blocks).strip()

        file_name = f"{dom_id}.md"
        file_path = target_dir / file_name

        content = f"# [{dom_id}] {title}\n\n"
        if body_md:
            content += f"{body_md}\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        items.append({
            "id": dom_id,
            "title": title,
            "filename": file_name
        })

    def get_sort_key(item):
        num_str = item["id"].replace("DOM-", "").strip()
        return int(num_str) if num_str.isdigit() else 999

    items.sort(key=get_sort_key)

    index_path = target_dir / "domain.md"
    idx_content = "# 데이터 및 도메인 정의서 목록\n\n"
    idx_content += "이 문서는 Yeolo 프로젝트의 도메인 모델 요약 목록입니다. 상세 컬럼 스펙, Enum 정의 및 JSON 스키마는 각 도메인 ID 링크의 개별 문서에서 확인할 수 있습니다.\n\n"
    idx_content += "---\n\n"
    idx_content += "| 도메인 ID | 도메인 명 |\n"
    idx_content += "| :--- | :--- |\n"

    for item in items:
        link_id = f"[{item['id']}](./{item['filename']})"
        idx_content += f"| {link_id} | {item['title']} |\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

    print(f"✅ domain-specs synced ({len(items)} items).", flush=True)


def sync_api_specs():
    print("🔄 Syncing api-specs...", flush=True)
    target_dir = REPO_ROOT / "api-specs"
    clean_directory(target_dir)

    pages_fb = query_database(DB_API_FB)
    pages_ba = query_database(DB_API_BA)

    items_fb = []
    items_ba = []

    def process_api_page(p, title_key, prefix):
        props = p["properties"]
        api_id = get_prop_text(props, "API ID").strip()
        title = get_prop_text(props, title_key)
        method = get_prop_text(props, "Method")
        endpoint = get_prop_text(props, "Endpoint")
        comm_type = get_prop_text(props, "통신 방식")
        auth_req = get_prop_text(props, "인증 필요")
        header = get_prop_text(props, "Header")
        path_params = get_prop_text(props, "Path Params")
        query_params = get_prop_text(props, "Query Params")
        req_body = get_prop_text(props, "Request Body")
        success_status = get_prop_text(props, "Success Status")
        success_resp = get_prop_text(props, "성공 응답")
        error_codes = get_prop_text(props, "Error Codes")
        fail_resp = get_prop_text(props, "실패 응답")

        if not api_id:
            safe_title = title.replace(" ", "_")
            api_id = f"{prefix}-{safe_title}"

        blocks = fetch_child_blocks(p["id"])
        body_md = convert_blocks_to_md(blocks).strip()

        file_name = f"{api_id}.md"
        file_path = target_dir / file_name

        content = f"# [{api_id}] {title}\n\n"
        content += "## 1. 기본 정보\n\n"
        content += f"- **Method**: `{method or '-'}`\n"
        content += f"- **Endpoint**: `{endpoint or '-'}`\n"
        content += f"- **통신 방식**: {comm_type or '-'}\n"
        content += f"- **인증 필요**: {auth_req or '-'}\n"
        if success_status:
            content += f"- **Success Status**: `{success_status}`\n"
        content += "\n## 2. Request 사양\n\n"
        if header:
            content += f"### Header\n{header}\n\n"
        if path_params:
            content += f"### Path Params\n{path_params}\n\n"
        if query_params:
            content += f"### Query Params\n{query_params}\n\n"
        if req_body:
            content += f"### Request Body\n```json\n{req_body}\n```\n\n"

        content += "## 3. Response 사양\n\n"
        if success_resp:
            status_label = f" (Status {success_status})" if success_status else ""
            content += f"### 성공 응답{status_label}\n```json\n{success_resp}\n```\n\n"
        if error_codes:
            content += f"### Error Codes\n{error_codes}\n\n"
        if fail_resp:
            content += f"### 실패 응답\n```json\n{fail_resp}\n```\n\n"

        if body_md:
            content += f"## 4. 상세 내용 및 예외 케이스\n\n{body_md}\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "id": api_id,
            "title": title,
            "method": method,
            "endpoint": endpoint,
            "filename": file_name
        }

    for p in pages_fb:
        item = process_api_page(p, "API명", "API-FB")
        items_fb.append(item)

    for p in pages_ba:
        item = process_api_page(p, "설명", "API-BA")
        items_ba.append(item)

    items_fb.sort(key=lambda x: x["id"])
    items_ba.sort(key=lambda x: x["id"])

    index_path = target_dir / "api.md"
    idx_content = "# API 명세 목록\n\n"
    idx_content += "이 문서는 Yeolo 프로젝트의 백엔드 서비스(FE-BE) 및 AI 엔진(BE-AI) 간의 API 요약 목록입니다. 상세한 호출 규격(Request/Response, JSON Schema, Error Codes)은 각 API ID 링크의 개별 문서에서 확인할 수 있습니다.\n\n"
    idx_content += "---\n\n"
    idx_content += "## 1. Frontend - Backend (FE-BE) API\n\n"
    idx_content += "| API ID | API 명 | HTTP Method | Endpoint |\n"
    idx_content += "| :--- | :--- | :--- | :--- |\n"

    for item in items_fb:
        link_id = f"[{item['id']}](./{item['filename']})"
        idx_content += f"| {link_id} | {item['title']} | `{item['method']}` | `{item['endpoint']}` |\n"

    idx_content += "\n---\n\n"
    idx_content += "## 2. Backend - AI (BE-AI) 내부 API\n\n"
    idx_content += "| API ID | API 명 | HTTP Method | Endpoint |\n"
    idx_content += "| :--- | :--- | :--- | :--- |\n"

    for item in items_ba:
        link_id = f"[{item['id']}](./{item['filename']})"
        idx_content += f"| {link_id} | {item['title']} | `{item['method']}` | `{item['endpoint']}` |\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

    print(f"✅ api-specs synced ({len(items_fb)} FE-BE APIs, {len(items_ba)} BE-AI APIs).", flush=True)


def main():
    print("🚀 Starting Notion Specifications Sync...", flush=True)
    print(f"📂 Repository Root: {REPO_ROOT}", flush=True)
    sync_requirement_specs()
    sync_functional_specs()
    sync_domain_specs()
    sync_api_specs()
    print("🎉 Sync completed successfully!", flush=True)


if __name__ == "__main__":
    main()
