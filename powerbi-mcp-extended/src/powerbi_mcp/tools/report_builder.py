"""
MCP tools: PBIR report builder.

PBIR (Power BI Enhanced Report Format) stores reports as a folder of
human-readable JSON files — the format becoming default in Power BI from 2026.

These tools let an AI agent build a complete Power BI report definition
programmatically (no UI required), save it as a PBIR folder structure, and
then open it in Power BI Desktop or deploy it via the Fabric REST API.

PBIR folder layout produced:
    <report_name>/
    ├── .platform              (Fabric/git metadata)
    └── definition/
        ├── report.json        (report-level settings: theme, custom visuals)
        └── pages/
            └── <page_id>/
                ├── page.json  (page name, size, background)
                └── visuals/
                    └── <visual_id>/
                        └── visual.json  (type, position, size, data bindings)

The JSON is kept at the minimum required schema — Power BI Desktop will fill in
defaults for any omitted properties when the file is opened.
"""

import json
import os
import uuid
from pathlib import Path
from typing import Any

from mcp.server import FastMCP


# ── Visual type catalogue ─────────────────────────────────────────────────────

VISUAL_TYPES: dict[str, str] = {
    # Charts
    "bar_chart_clustered": "clusteredBarChart",
    "bar_chart_stacked": "stackedBarChart",
    "bar_chart_100pct": "hundredPercentStackedBarChart",
    "column_chart_clustered": "clusteredColumnChart",
    "column_chart_stacked": "stackedColumnChart",
    "column_chart_100pct": "hundredPercentStackedColumnChart",
    "line_chart": "lineChart",
    "area_chart": "areaChart",
    "area_chart_stacked": "stackedAreaChart",
    "area_chart_100pct": "hundredPercentStackedAreaChart",
    "line_clustered_column": "lineClusteredColumnComboChart",
    "line_stacked_column": "lineStackedColumnComboChart",
    "ribbon_chart": "ribbonChart",
    "waterfall_chart": "waterfallChart",
    "funnel": "funnel",
    "scatter_chart": "scatterChart",
    "bubble_chart": "scatterChart",  # same type, configured differently
    "pie_chart": "pieChart",
    "donut_chart": "donutChart",
    "treemap": "treemap",
    # Maps
    "map": "map",
    "filled_map": "filledMap",
    "azure_map": "azureMap",
    "shape_map": "shapeMap",
    # Tables & Matrices
    "table": "tableEx",
    "matrix": "pivotTable",
    # Cards
    "card": "card",
    "multi_row_card": "multiRowCard",
    "kpi": "kpi",
    # Slicers & Filters
    "slicer": "slicer",
    # AI visuals
    "decomposition_tree": "decompositionTreeVisual",
    "key_influencers": "keyInfluencersVisual",
    "smart_narrative": "smartNarrativeVisual",
    "q_and_a": "qnaVisual",
    # Other
    "gauge": "gauge",
    "text_box": "textbox",
    "image": "image",
    "shape": "basicShape",
    "r_visual": "scriptVisual",
    "python_visual": "pythonVisual",
}


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def get_available_visual_types() -> str:
        """
        Return the full list of supported PBIR visual type keys and their
        internal Power BI visual type names. Use the key (left column) as
        the visual_type argument in add_visual_to_page.
        """
        types = [
            {"key": k, "pbir_type": v}
            for k, v in sorted(VISUAL_TYPES.items())
        ]
        return json.dumps({"visual_types": types, "count": len(types)})

    @mcp.tool()
    def create_report_definition(
        report_name: str,
        dataset_workspace_id: str = "",
        dataset_id: str = "",
        theme: str = "default",
    ) -> str:
        """
        Create a blank PBIR report definition (in-memory JSON structure).
        Returns the JSON you pass to subsequent tools to add pages and visuals,
        and finally to save_report_as_pbir to write it to disk.

        Args:
            report_name: Display name for the report.
            dataset_workspace_id: GUID of the workspace containing the dataset.
                                   Leave empty for a report not yet bound to a dataset.
            dataset_id: GUID of the dataset (semantic model) to bind to.
            theme: Theme name — 'default' or the name of a custom theme.
        """
        definition: dict[str, Any] = {
            "report_name": report_name,
            "report_id": str(uuid.uuid4()),
            "theme": theme,
            "pages": [],
        }
        if dataset_workspace_id and dataset_id:
            definition["dataset"] = {
                "workspace_id": dataset_workspace_id,
                "dataset_id": dataset_id,
            }
        return json.dumps(definition, indent=2)

    @mcp.tool()
    def add_page_to_report(
        report_definition_json: str,
        page_display_name: str,
        width: int = 1280,
        height: int = 720,
        background_color: str = "#FFFFFF",
    ) -> str:
        """
        Add a new page to a report definition created by create_report_definition.
        Returns the updated report definition JSON.

        Args:
            report_definition_json: JSON string from create_report_definition or
                                    a previous add_page_to_report call.
            page_display_name: Human-readable name shown on the page tab.
            width: Page width in pixels (default 1280 = 16:9 widescreen).
            height: Page height in pixels (default 720).
            background_color: Hex color for the page background (default white).
        """
        definition = json.loads(report_definition_json)
        page_id = f"ReportSection{len(definition['pages']) + 1}"
        page: dict[str, Any] = {
            "page_id": page_id,
            "display_name": page_display_name,
            "width": width,
            "height": height,
            "background_color": background_color,
            "visuals": [],
        }
        definition["pages"].append(page)
        return json.dumps(definition, indent=2)

    @mcp.tool()
    def add_visual_to_page(
        report_definition_json: str,
        page_display_name: str,
        visual_type: str,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str = "",
        data_bindings_json: str = "{}",
    ) -> str:
        """
        Add a visual to a specific page in the report definition.
        Returns the updated report definition JSON.

        Args:
            report_definition_json: JSON string from add_page_to_report.
            page_display_name: Name of the target page.
            visual_type: Visual type key from get_available_visual_types,
                         e.g. 'bar_chart_clustered', 'card', 'slicer'.
            x: Left edge position on the page canvas (pixels from left).
            y: Top edge position on the page canvas (pixels from top).
            width: Visual width in pixels.
            height: Visual height in pixels.
            title: Optional visual title shown above the visual.
            data_bindings_json: JSON object mapping field well names to
                                column/measure references. Example:
                                {"category": "Product[Category]",
                                 "values": "Sales[Total Revenue]",
                                 "legend": "Product[Sub-Category]"}
                                Leave empty for visuals without data (text boxes, images).
        """
        definition = json.loads(report_definition_json)
        data_bindings = json.loads(data_bindings_json)

        pbir_type = VISUAL_TYPES.get(visual_type)
        if not pbir_type:
            return json.dumps({
                "error": f"Unknown visual_type '{visual_type}'. "
                         "Call get_available_visual_types() to see valid keys."
            })

        visual_id = str(uuid.uuid4()).replace("-", "")[:16]
        visual: dict[str, Any] = {
            "visual_id": visual_id,
            "visual_type": pbir_type,
            "position": {"x": x, "y": y, "z": 0},
            "dimensions": {"width": width, "height": height},
            "data_bindings": data_bindings,
        }
        if title:
            visual["title"] = title

        # Find the target page
        page = next(
            (p for p in definition["pages"] if p["display_name"] == page_display_name),
            None,
        )
        if page is None:
            return json.dumps({
                "error": f"Page '{page_display_name}' not found. "
                         f"Available pages: {[p['display_name'] for p in definition['pages']]}"
            })

        page["visuals"].append(visual)
        return json.dumps(definition, indent=2)

    @mcp.tool()
    def save_report_as_pbir(
        report_definition_json: str,
        output_directory: str,
    ) -> str:
        """
        Write a report definition to disk as a PBIR folder structure.
        The resulting folder can be opened in Power BI Desktop or committed
        to Git for version control.

        On the Windows machine, use open_pbix_file(output_directory) in the
        powerbi-desktop-mcp server to open the saved report.

        Args:
            report_definition_json: JSON string from add_visual_to_page.
            output_directory: Directory to write the PBIR folder into.
                              The report folder will be created inside this dir.
                              Example: '/tmp/reports' → '/tmp/reports/<report_name>/'
        """
        definition = json.loads(report_definition_json)
        report_name = definition.get("report_name", "report")
        report_root = Path(output_directory) / report_name
        def_dir = report_root / "definition"
        pages_dir = def_dir / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)

        # .platform file (minimal)
        platform = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/platform.json",
            "metadata": {
                "type": "Report",
                "displayName": report_name,
            },
            "config": {
                "version": "1.0",
                "logicalId": definition.get("report_id", str(uuid.uuid4())),
            },
        }
        (report_root / ".platform").write_text(json.dumps(platform, indent=2))

        # definition/report.json
        report_meta: dict[str, Any] = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
            "themeCollection": {"baseTheme": {"name": definition.get("theme", "default")}},
            "sections": [],
        }
        if "dataset" in definition:
            report_meta["datasetReference"] = {
                "byPath": None,
                "byConnection": {
                    "connectionString": None,
                    "pbiServiceModelId": None,
                    "pbiModelVirtualServerName": "sobe_wowvirtualserver",
                    "pbiModelDatabaseName": definition["dataset"]["dataset_id"],
                    "name": "EntityDataSource",
                    "connectionType": "pbiServiceXmlaStyleLive",
                },
            }
        (def_dir / "report.json").write_text(json.dumps(report_meta, indent=2))

        # Pages
        files_written = [str(report_root / ".platform"), str(def_dir / "report.json")]
        for page in definition.get("pages", []):
            page_id = page["page_id"]
            page_dir = pages_dir / page_id
            visuals_dir = page_dir / "visuals"
            visuals_dir.mkdir(parents=True, exist_ok=True)

            # page.json
            page_json: dict[str, Any] = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json",
                "name": page_id,
                "displayName": page["display_name"],
                "displayOption": "FitToPage",
                "width": page["width"],
                "height": page["height"],
            }
            page_path = page_dir / "page.json"
            page_path.write_text(json.dumps(page_json, indent=2))
            files_written.append(str(page_path))

            # visuals
            for vis in page.get("visuals", []):
                vis_dir = visuals_dir / vis["visual_id"]
                vis_dir.mkdir(exist_ok=True)
                visual_json: dict[str, Any] = {
                    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visual/1.0.0/schema.json",
                    "name": vis["visual_id"],
                    "position": {
                        "x": vis["position"]["x"],
                        "y": vis["position"]["y"],
                        "z": vis["position"]["z"],
                        "height": vis["dimensions"]["height"],
                        "width": vis["dimensions"]["width"],
                        "tabOrder": 0,
                    },
                    "visual": {
                        "visualType": vis["visual_type"],
                        "query": _build_query(vis.get("data_bindings", {})),
                        "title": {
                            "show": bool(vis.get("title")),
                            **({"text": {"expr": {"Literal": {"Value": f"'{vis['title']}'"}}}}
                               if vis.get("title") else {}),
                        },
                    },
                }
                vis_path = vis_dir / "visual.json"
                vis_path.write_text(json.dumps(visual_json, indent=2))
                files_written.append(str(vis_path))

        return json.dumps({
            "status": "ok",
            "report_name": report_name,
            "output_path": str(report_root),
            "files_written": files_written,
            "pages": len(definition.get("pages", [])),
            "next_step": (
                f"Open in Power BI Desktop using the powerbi-desktop-mcp tool: "
                f"open_pbix_file('{report_root}')"
            ),
        }, indent=2)

    @mcp.tool()
    def load_pbir_report(pbir_folder_path: str) -> str:
        """
        Read an existing PBIR report folder from disk and return its structure
        as a report definition JSON that can be edited with add_page_to_report
        and add_visual_to_page, then re-saved with save_report_as_pbir.

        Args:
            pbir_folder_path: Path to the report's root folder (contains .platform).
        """
        root = Path(pbir_folder_path)
        if not (root / ".platform").exists():
            return json.dumps({
                "error": f"No .platform file found in {pbir_folder_path}. "
                         "Ensure this is a PBIR report folder."
            })

        platform = json.loads((root / ".platform").read_text())
        report_name = platform.get("metadata", {}).get("displayName", root.name)
        report_id = platform.get("config", {}).get("logicalId", str(uuid.uuid4()))

        definition: dict[str, Any] = {
            "report_name": report_name,
            "report_id": report_id,
            "pages": [],
        }

        pages_dir = root / "definition" / "pages"
        if pages_dir.exists():
            for page_dir in sorted(pages_dir.iterdir()):
                page_json_path = page_dir / "page.json"
                if not page_json_path.exists():
                    continue
                page_data = json.loads(page_json_path.read_text())
                page: dict[str, Any] = {
                    "page_id": page_data.get("name", page_dir.name),
                    "display_name": page_data.get("displayName", page_dir.name),
                    "width": page_data.get("width", 1280),
                    "height": page_data.get("height", 720),
                    "visuals": [],
                }
                vis_dir = page_dir / "visuals"
                if vis_dir.exists():
                    for vis_folder in sorted(vis_dir.iterdir()):
                        vis_path = vis_folder / "visual.json"
                        if vis_path.exists():
                            vis_data = json.loads(vis_path.read_text())
                            pos = vis_data.get("position", {})
                            vis_inner = vis_data.get("visual", {})
                            page["visuals"].append({
                                "visual_id": vis_data.get("name", vis_folder.name),
                                "visual_type": vis_inner.get("visualType", ""),
                                "position": {"x": pos.get("x", 0), "y": pos.get("y", 0), "z": 0},
                                "dimensions": {
                                    "width": pos.get("width", 400),
                                    "height": pos.get("height", 300),
                                },
                                "data_bindings": {},
                            })
                definition["pages"].append(page)

        return json.dumps(definition, indent=2)


# ── Query builder helper ──────────────────────────────────────────────────────

def _build_query(bindings: dict[str, str]) -> dict:
    """
    Build a minimal PBIR query structure from data binding declarations.
    Binding format: {"values": "Sales[Amount]", "category": "Product[Name]"}
    """
    if not bindings:
        return {}

    projections: dict[str, list] = {}
    select: list = []
    for well, field_ref in bindings.items():
        # Parse "Table[Field]" into table/column parts
        if "[" in field_ref and field_ref.endswith("]"):
            table, col = field_ref.rstrip("]").split("[", 1)
            expr = {"Column": {"Expression": {"SourceRef": {"Entity": table}}, "Property": col}}
        else:
            # Treat as a measure name in an unknown table
            expr = {"Measure": {"Expression": {"SourceRef": {"Entity": ""}}, "Property": field_ref}}

        role = f"{well}_{len(select)}"
        select.append({
            "Measure": expr,
            "Name": role,
        })
        projections.setdefault(well, []).append({"queryRef": role})

    return {
        "queryState": {"filters": [], "projections": projections},
        "select": select,
    }
