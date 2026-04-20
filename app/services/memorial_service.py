import re
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from app.schemas.memorial import (
    MemorialItemOut,
    MemorialResponseOut,
    MemorialSectionOut,
)

JRA_URL = "https://www.jra.go.jp/datafile/kiroku/"
NANKAN_URL = "https://www.nankankeiba.com/memorial/memorial.do"


# ----------------------------
# 共通
# ----------------------------
def _fetch_html(url: str) -> str:
    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; KeibaApp/1.0)"
        },
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding
    return response.text


def _make_soup(url: str) -> BeautifulSoup:
    html = _fetch_html(url)
    return BeautifulSoup(html, "html.parser")


def _normalize_text(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_lines_from_soup(soup: BeautifulSoup) -> List[str]:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    lines: List[str] = []
    for s in soup.stripped_strings:
        line = _normalize_text(str(s))
        if line:
            lines.append(line)

    return _dedupe_keep_order(lines)


def _dedupe_keep_order(lines: List[str]) -> List[str]:
    seen = set()
    result = []
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        result.append(line)
    return result


def _extract_as_of_text(lines: List[str]) -> Optional[str]:
    patterns = [
        r".*現在.*",
        r".*終了現在.*",
        r".*更新予定.*",
        r".*日現在.*",
    ]
    for line in lines[:150]:
        for pattern in patterns:
            if re.search(pattern, line):
                return line
    return None


def _make_detail(parts: List[str]) -> Optional[str]:
    cleaned = [p for p in parts if p]
    if not cleaned:
        return None
    return " / ".join(cleaned)


# ----------------------------
# JRA
# ----------------------------
_JRA_SECTION_TITLES = {
    "達成間近な記録",
    "GⅠレース勝利数",
    "重賞勝利数",
    "通算勝利数",
    "騎手",
    "調教師",
}

def _looks_like_jra_name_with_affiliation(line: str) -> bool:
    return bool(re.match(r"^[^\d]{1,20}（(?:美浦|栗東)）$", line))


def _split_jra_name_affiliation(line: str) -> tuple[str, str]:
    m = re.match(r"^(?P<name>.+?)（(?P<aff>美浦|栗東)）$", line)
    if not m:
        return line, ""
    return _normalize_text(m.group("name")), m.group("aff")


def _is_jra_record_line(line: str) -> bool:
    return (
        "あと" in line
        or "勝まで" in line
        or "回まで" in line
        or "メートルまで" in line
        or "mまで" in line
        or "獲得まで" in line
    )


def _is_jra_explanatory_line(line: str) -> bool:
    bad_prefixes = ["原則として", "※", "注"]
    return any(line.startswith(prefix) for prefix in bad_prefixes)


def _find_jra_record_in_window(lines: List[str], start_idx: int, window: int = 6) -> Optional[str]:
    """
    人名行の後ろ数行を探索して record 行を見つける。
    次の人名行や次の section に当たったら探索終了。
    """
    end = min(len(lines), start_idx + 1 + window)

    for i in range(start_idx + 1, end):
        line = lines[i]

        if line in _JRA_SECTION_TITLES:
            break

        if _looks_like_jra_name_with_affiliation(line):
            break

        if _is_jra_explanatory_line(line):
            continue

        if _is_jra_record_line(line):
            return line

    return None


def _parse_jra_sections(lines: List[str]) -> List[MemorialSectionOut]:
    sections: List[MemorialSectionOut] = []

    current_section = "達成間近な記録"
    current_role: Optional[str] = None
    current_items: List[MemorialItemOut] = []

    def flush():
        nonlocal current_items
        if current_items:
            sections.append(
                MemorialSectionOut(
                    title=current_section,
                    items=current_items,
                )
            )
        current_items = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # セクション切り替え
        if line in _JRA_SECTION_TITLES:
            if line in {"騎手", "調教師"}:
                current_role = line
            else:
                flush()
                current_section = line
            i += 1
            continue

        # 人名 + 所属
        if _looks_like_jra_name_with_affiliation(line):
            name, affiliation = _split_jra_name_affiliation(line)

            # この人名の後ろを広めに探索
            record_line = None
            for j in range(i + 1, min(len(lines), i + 10)):
                next_line = lines[j]

                # 次のセクションや次の人名で探索打ち切り
                if next_line in _JRA_SECTION_TITLES:
                    break
                if _looks_like_jra_name_with_affiliation(next_line):
                    break
                if _is_jra_explanatory_line(next_line):
                    continue
                if _is_jra_record_line(next_line):
                    record_line = next_line
                    break

            if record_line:
                subtitle_parts = []
                if current_role:
                    subtitle_parts.append(current_role)
                subtitle_parts.append(affiliation)

                subtitle = " / ".join(subtitle_parts)

                current_items.append(
                    MemorialItemOut(
                        title=name,
                        subtitle=subtitle,
                        detail=record_line,
                        status="達成間近",
                    )
                )

        i += 1

    flush()

    # 重複除去
    deduped_sections: List[MemorialSectionOut] = []
    for section in sections:
        seen = set()
        items: List[MemorialItemOut] = []

        for item in section.items:
            key = (item.title, item.subtitle, item.detail)
            if key in seen:
                continue
            seen.add(key)
            items.append(item)

        if items:
            deduped_sections.append(
                MemorialSectionOut(
                    title=section.title,
                    items=items,
                )
            )

    return deduped_sections

def _is_jra_role_title(line: str) -> bool:
    return line in {"騎手", "調教師"}


def _is_jra_section_title(line: str) -> bool:
    return line in {"GⅠレース勝利数", "重賞勝利数", "通算勝利数"}


def _collect_jra_dom_lines(soup: BeautifulSoup) -> List[str]:
    """
    JRA ページ全体からテキストを順序付きで収集。
    lines ベースよりも DOM 順序を保ちやすい。
    """
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    lines: List[str] = []
    for text in soup.stripped_strings:
        line = _normalize_text(str(text))
        if line:
            lines.append(line)

    return lines


def _parse_jra_sections_dom(soup: BeautifulSoup) -> List[MemorialSectionOut]:
    lines = _collect_jra_dom_lines(soup)

    sections: List[MemorialSectionOut] = []
    current_section: Optional[str] = None
    current_role: Optional[str] = None
    current_items: List[MemorialItemOut] = []

    def flush():
        nonlocal current_items, current_section
        if current_section and current_items:
            sections.append(
                MemorialSectionOut(
                    title=current_section,
                    items=current_items,
                )
            )
        current_items = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if _is_jra_section_title(line):
            flush()
            current_section = line
            i += 1
            continue

        if _is_jra_role_title(line):
            current_role = line
            i += 1
            continue

        if _looks_like_jra_name_with_affiliation(line):
            name, affiliation = _split_jra_name_affiliation(line)

            record_line = None
            # DOM順の近傍をやや広めに探索
            for j in range(i + 1, min(len(lines), i + 15)):
                next_line = lines[j]

                if _is_jra_section_title(next_line):
                    break

                if _looks_like_jra_name_with_affiliation(next_line):
                    break

                if _is_jra_role_title(next_line):
                    continue

                if _is_jra_explanatory_line(next_line):
                    continue

                if _is_jra_record_line(next_line):
                    record_line = next_line
                    break

            if record_line and current_section:
                subtitle_parts = []
                if current_role:
                    subtitle_parts.append(current_role)
                subtitle_parts.append(affiliation)

                current_items.append(
                    MemorialItemOut(
                        title=name,
                        subtitle=" / ".join(subtitle_parts),
                        detail=record_line,
                        status="達成間近",
                    )
                )

        i += 1

    flush()

    # 重複除去
    deduped_sections: List[MemorialSectionOut] = []
    for section in sections:
        seen = set()
        items: List[MemorialItemOut] = []
        for item in section.items:
            key = (item.title, item.subtitle, item.detail)
            if key in seen:
                continue
            seen.add(key)
            items.append(item)

        if items:
            deduped_sections.append(
                MemorialSectionOut(
                    title=section.title,
                    items=items,
                )
            )

    return deduped_sections

# ----------------------------
# NANKAN 共通補助
# ----------------------------
_NANKAN_IGNORE_LINES = {
    "サイトマップ",
    "リーチ",
    "地方競馬 通算最多勝利",
    "地方競馬通算最多勝利",
    "地方競馬累計最多勝利",
    "メモリアル達成・達成間近",
    "メモリアル達成！",
    "達成間近",
    "騎手",
    "調教師",
    "トップ",
    "メニュー",
}

def _looks_like_nankan_person_name(line: str) -> bool:
    if not line or len(line) > 20:
        return False
    if line in _NANKAN_IGNORE_LINES:
        return False
    if "勝" in line or "あと" in line or "年" in line or "月" in line or "日" in line:
        return False
    if "現在" in line or "所属" in line:
        return False
    return bool(re.match(r"^[ぁ-んァ-ヶ一-龥々・ー\s]+$", line))


def _looks_like_nankan_affiliation(line: str) -> bool:
    return line in {"大井", "船橋", "川崎", "浦和"}


def _looks_like_win_line(line: str) -> bool:
    return bool(re.match(r"^\d+勝$", line))


def _looks_like_target_line(line: str) -> bool:
    return bool(re.match(r"^あと\d+勝$", line))


def _looks_like_date_line(line: str) -> bool:
    return bool(re.search(r"\d{4}年\d{1,2}月\d{1,2}日", line))


def _looks_like_birth_line(line: str) -> bool:
    return bool(re.match(r"^\d{4}年\d{1,2}月\d{1,2}日生$", line))


def _extract_wins_int(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    m = re.search(r"(\d+)\s*勝", _normalize_text(text))
    if not m:
        return None
    return int(m.group(1))


def _next_hundred_milestone(wins: int) -> int:
    return ((wins // 100) + 1) * 100


def _remaining_to_next_hundred(wins: int) -> int:
    return _next_hundred_milestone(wins) - wins


def _build_nankan_detail_and_status_from_wins(
    wins_text: Optional[str],
    date_text: Optional[str] = None,
) -> tuple[Optional[str], str]:
    wins = _extract_wins_int(wins_text)
    if wins is None:
        return _make_detail([wins_text or "", date_text or ""]), "記録"

    remaining = _remaining_to_next_hundred(wins)

    if remaining <= 10:
        base = f"{wins}勝 / あと{remaining}勝"
        status = "達成間近"
    else:
        base = f"{wins}勝"
        status = "記録"

    detail_parts = [base]
    if date_text:
        detail_parts.append(date_text)

    return _make_detail(detail_parts), status


def _force_clean_nankan_detail(detail: Optional[str]) -> Optional[str]:
    if not detail:
        return detail

    text = _normalize_text(detail)
    text = text.replace("あー", "あと")
    text = text.replace("阿", "あと")
    text = re.sub(r"/\s*あ(\d+勝)", r"/ あと\1", text)
    text = re.sub(r"\s*/\s*", " / ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _guess_nankan_role(current_section: str, current_role: Optional[str], affiliation: Optional[str]) -> Optional[str]:
    if current_section in {"地方競馬 通算最多勝利", "地方競馬通算最多勝利", "地方競馬累計最多勝利"}:
        return "騎手"
    if current_role in {"騎手", "調教師"}:
        return current_role
    return None


# ----------------------------
# NANKAN fallback（従来の line ベース）
# ----------------------------
def _parse_nankan_sections_fallback(lines: List[str]) -> List[MemorialSectionOut]:
    sections: List[MemorialSectionOut] = []
    current_section = "メモリアル"
    current_role: Optional[str] = None
    current_items: List[MemorialItemOut] = []

    section_titles = {
        "地方競馬 通算最多勝利",
        "地方競馬通算最多勝利",
        "地方競馬累計最多勝利",
        "メモリアル達成！",
        "達成間近",
    }

    def flush():
        nonlocal current_items
        if current_items:
            sections.append(
                MemorialSectionOut(
                    title=current_section,
                    items=current_items,
                )
            )
        current_items = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if line in section_titles:
            flush()
            current_section = line
            i += 1
            continue

        if line in {"騎手", "調教師"}:
            current_role = line
            i += 1
            continue

        if _looks_like_nankan_person_name(line):
            name = line
            affiliation = None
            wins = None
            date_text = None
            birth_text = None

            j = i + 1
            consumed = 1

            if j < len(lines) and _looks_like_nankan_affiliation(lines[j]):
                affiliation = lines[j]
                j += 1
                consumed += 1

            if j < len(lines) and _looks_like_win_line(lines[j]):
                wins = lines[j]
                j += 1
                consumed += 1

            if j < len(lines) and _looks_like_target_line(lines[j]):
                j += 1
                consumed += 1

            if j < len(lines) and _looks_like_date_line(lines[j]):
                if _looks_like_birth_line(lines[j]):
                    birth_text = lines[j]
                else:
                    date_text = lines[j]
                j += 1
                consumed += 1

            if birth_text and not (wins or date_text):
                i += consumed
                continue

            if affiliation or wins or date_text:
                role = _guess_nankan_role(current_section, current_role, affiliation)

                subtitle_parts = []
                if role:
                    subtitle_parts.append(role)
                if affiliation:
                    subtitle_parts.append(affiliation)

                subtitle = " / ".join(subtitle_parts) if subtitle_parts else None
                detail, status = _build_nankan_detail_and_status_from_wins(wins, date_text)
                detail = _force_clean_nankan_detail(detail)

                current_items.append(
                    MemorialItemOut(
                        title=name,
                        subtitle=subtitle,
                        detail=detail,
                        status=status,
                    )
                )
                i += consumed
                continue

        i += 1

    flush()
    return [s for s in sections if s.items]


# ----------------------------
# NANKAN table直読み（優先）
# ----------------------------
def _parse_nankan_summary_table(table, section_title: str) -> List[MemorialItemOut]:
    items: List[MemorialItemOut] = []

    tbody = table.find("tbody")
    if not tbody:
        return items

    for tr in tbody.find_all("tr", recursive=False):
        tds = tr.find_all("td", recursive=False)
        if not tds:
            continue

        classes = []
        for td in tds:
            classes.extend(td.get("class") or [])

        if "is-title" in classes or "is-full" in classes or "is-empty" in classes:
            continue

        cells = [_normalize_text(td.get_text(" ", strip=True)) for td in tds]
        cells = [c for c in cells if c]

        if len(cells) < 3:
            continue

        name = cells[0]
        affiliation = cells[1] if len(cells) >= 2 else None
        wins_text = cells[2] if len(cells) >= 3 else None
        date_text = cells[3] if len(cells) >= 4 else None

        if not _looks_like_nankan_person_name(name):
            continue

        if affiliation and not _looks_like_nankan_affiliation(affiliation):
            affiliation = None

        role = None
        thead = table.find("thead")
        if thead:
            head_text = _normalize_text(thead.get_text(" ", strip=True))
            if "騎手" in head_text:
                role = "騎手"
            elif "調教師" in head_text:
                role = "調教師"

        if not role:
            role = _guess_nankan_role(section_title, None, affiliation)

        subtitle_parts = []
        if role:
            subtitle_parts.append(role)
        if affiliation:
            subtitle_parts.append(affiliation)

        subtitle = " / ".join(subtitle_parts) if subtitle_parts else None

        detail, status = _build_nankan_detail_and_status_from_wins(
            wins_text,
            date_text,
        )
        detail = _force_clean_nankan_detail(detail)

        items.append(
            MemorialItemOut(
                title=name,
                subtitle=subtitle,
                detail=detail,
                status=status,
            )
        )

    return items


def _parse_nankan_sections_from_tables(soup: BeautifulSoup) -> List[MemorialSectionOut]:
    sections: List[MemorialSectionOut] = []

    table_max = soup.find("table", attrs={"summary": "地方競馬通算最多勝利一覧"})
    if table_max:
        items = _parse_nankan_summary_table(table_max, "地方競馬通算最多勝利")
        if items:
            sections.append(
                MemorialSectionOut(
                    title="地方競馬通算最多勝利",
                    items=items,
                )
            )

    table_kis = soup.find("table", attrs={"summary": "メモリアル達成・達成間近騎手一覧"})
    if table_kis:
        items = _parse_nankan_summary_table(table_kis, "メモリアル達成・達成間近")
        if items:
            sections.append(
                MemorialSectionOut(
                    title="メモリアル達成・達成間近（騎手）",
                    items=items,
                )
            )

    table_cho = soup.find("table", attrs={"summary": "メモリアル達成・達成間近調教師一覧"})
    if table_cho:
        items = _parse_nankan_summary_table(table_cho, "メモリアル達成・達成間近")
        if items:
            sections.append(
                MemorialSectionOut(
                    title="メモリアル達成・達成間近（調教師）",
                    items=items,
                )
            )

    return sections


def _parse_nankan_sections_safe(soup: BeautifulSoup, lines: List[str]) -> List[MemorialSectionOut]:
    try:
        sections = _parse_nankan_sections_from_tables(soup)
        if sections:
            return sections
    except Exception as e:
        print(f"[memorial] nankan table parse failed, fallback to line parse: {e}")

    return _parse_nankan_sections_fallback(lines)


# ----------------------------
# Public functions
# ----------------------------
def get_jra_memorial() -> MemorialResponseOut:
    soup = _make_soup(JRA_URL)
    lines = _extract_lines_from_soup(soup)

    sections: List[MemorialSectionOut] = []

    try:
        sections = _parse_jra_sections_dom(soup)
    except Exception as e:
        print(f"[memorial] jra dom parse failed, fallback to line parse: {e}")

    if not sections:
        sections = _parse_jra_sections(lines)

    return MemorialResponseOut(
        source="jra",
        source_label="中央競馬",
        source_url=JRA_URL,
        as_of_text=_extract_as_of_text(lines),
        sections=sections,
    )


def get_nankan_memorial() -> MemorialResponseOut:
    soup = _make_soup(NANKAN_URL)
    lines = _extract_lines_from_soup(soup)

    return MemorialResponseOut(
        source="nankan",
        source_label="地方競馬",
        source_url=NANKAN_URL,
        as_of_text=_extract_as_of_text(lines),
        sections=_parse_nankan_sections_safe(soup, lines),
    )