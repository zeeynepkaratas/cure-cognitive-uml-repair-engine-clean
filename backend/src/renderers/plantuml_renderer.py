"""
PlantUML render helpers.

The project can later switch this module to a PlantUML server or local jar.
For the checkpoint delivery we keep rendering deterministic and offline: the
API returns a valid SVG preview plus a valid PNG placeholder data URI, while
the original PlantUML source remains the authoritative diagram definition.
"""
import base64
import html
import re
from typing import Dict, List, Tuple

try:
    from utils.plantuml_parser import parse_relationships, parse_classes
    from plantuml_runtime import render_with_plantuml
except ModuleNotFoundError:  # package import path: src.renderers.plantuml_renderer
    from src.utils.plantuml_parser import parse_relationships, parse_classes
    from src.plantuml_runtime import render_with_plantuml


TRANSPARENT_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def _parse_classes(plantuml_code: str) -> List[str]:
    # PlantUML icindeki class tanimlarini render yerlesimi icin cikarir.
    return sorted(parse_classes(plantuml_code))


def _parse_relations(plantuml_code: str) -> List[Tuple[str, str]]:
    # En yaygin iliski oklarini yakalar; SVG'de kutular arasina cizgi cizmek icin kullanilir.
    return sorted(parse_relationships(plantuml_code))


def render_plantuml_svg(plantuml_code: str) -> str:
    """Create a compact SVG preview from PlantUML class declarations."""
    classes = _parse_classes(plantuml_code)
    relations = _parse_relations(plantuml_code)

    # Dinamik yukseklik: sinif sayisi arttikca SVG tasmasin diye boyut buyur.
    width = 760
    row_height = 76
    height = max(180, 90 + (len(classes) * row_height) + 40)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        ".bg{fill:#f8fafc}.box{fill:#ffffff;stroke:#2563eb;stroke-width:2}.title{font:600 16px Arial;fill:#0f172a}.meta{font:12px Arial;fill:#64748b}.line{stroke:#334155;stroke-width:1.6;marker-end:url(#arrow)}",
        "</style>",
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#334155"/></marker></defs>',
        f'<rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="0"/>',
        '<text class="title" x="32" y="38">CURE UML Diagram</text>',
        f'<text class="meta" x="32" y="60">{len(classes)} class, {len(relations)} relation</text>',
    ]

    positions: Dict[str, Tuple[int, int]] = {}
    for index, class_name in enumerate(classes):
        # Siniflar iki sutunlu basit bir grid ile yerlestirilir.
        x = 48 + (index % 2) * 360
        y = 92 + (index // 2) * row_height
        positions[class_name] = (x, y)
        safe_name = html.escape(class_name)
        svg_parts.extend([
            f'<rect class="box" x="{x}" y="{y}" width="280" height="52" rx="6"/>',
            f'<text class="title" x="{x + 16}" y="{y + 31}">{safe_name}</text>',
        ])

    for source, target in relations:
        # Sadece SVG'de koordinati bilinen siniflar arasindaki iliskiler cizilir.
        if source not in positions or target not in positions:
            continue
        sx, sy = positions[source]
        tx, ty = positions[target]
        svg_parts.append(
            f'<line class="line" x1="{sx + 280}" y1="{sy + 26}" x2="{tx}" y2="{ty + 26}"/>'
        )

    if not classes:
        svg_parts.append('<text class="meta" x="32" y="110">No class declarations found.</text>')

    svg_parts.append("</svg>")
    return "".join(svg_parts)


def render_plantuml(plantuml_code: str) -> dict:
    """Return SVG text and PNG data URI in the API response format."""
    runtime_render = render_with_plantuml(plantuml_code)
    if runtime_render.get("successful"):
        svg = runtime_render["svg"]
        svg_base64 = runtime_render["svg_base64"]
        render_source = "plantuml_runtime"
    else:
        svg = render_plantuml_svg(plantuml_code)
        svg_base64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        render_source = "fallback_svg_preview"
    return {
        "svg": svg,
        "svg_base64": svg_base64,
        # PNG alani frontend kontrati icin vardir; asil okunabilir gorsel SVG'dir.
        "png_base64": TRANSPARENT_PNG_BASE64,
        "png_data_uri": f"data:image/png;base64,{TRANSPARENT_PNG_BASE64}",
        "formatlar": ["svg", "png"],
        "render_source": render_source,
        "plantuml_runtime": {
            key: value for key, value in runtime_render.items() if key not in {"svg", "svg_base64"}
        },
    }
