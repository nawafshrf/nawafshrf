"""
MCP tools: AI-powered Power BI assistant using Claude (claude-opus-4-7).

These tools wrap the Anthropic API to provide intelligent assistance for
Power BI development tasks that benefit from natural-language understanding,
semantic reasoning, and vision analysis:

  - generate_dax_measure       — natural language → valid DAX expression
  - suggest_report_layout      — dataset schema → page/visual layout plan
  - analyze_report_screenshot  — base64 PNG → visual insights (vision)
  - optimize_dax_with_ai       — DAX expression → detailed AI optimization
  - chat_with_data             — natural language Q&A → auto-generated DAX

All tools require ANTHROPIC_API_KEY in the environment.
Power BI context tools (get_dataset_schema, etc.) are called transparently
when a dataset_id is supplied, so callers only need to pass IDs.
"""

import json
import logging
import os

import anthropic

from mcp.server import FastMCP
from .. import client as pbi

logger = logging.getLogger(__name__)

_SYSTEM_DAX = """\
You are an expert Power BI developer and DAX specialist with deep knowledge of:
- DAX language semantics, evaluation contexts, and filter propagation
- Power BI data model design patterns and best practices
- Performance optimization for large datasets (millions of rows)
- PBIR report format and visual configuration

When generating DAX:
1. Prefer variables (VAR/RETURN) to avoid repeated evaluation
2. Use DIVIDE() instead of '/' to handle division by zero safely
3. Prefer REMOVEFILTERS() over ALL() for explicit intent
4. Use CALCULATE sparingly; always justify added filter arguments
5. Format DAX with consistent indentation (4 spaces per level)
6. Return ONLY the DAX expression, followed by a brief explanation prefixed with -- EXPLANATION:
"""

_SYSTEM_LAYOUT = """\
You are a senior Power BI report designer with expertise in:
- UX design patterns for business intelligence dashboards
- Optimal visual type selection for each data shape (categorical, time-series, KPI, etc.)
- PBIR JSON format for programmatic report generation
- Responsive canvas layout (default 1280×720 px canvas)

Respond with a JSON object describing each page's visuals. Follow this schema:
{
  "pages": [
    {
      "name": "<page name>",
      "purpose": "<one-sentence description>",
      "visuals": [
        {
          "type": "<PBIR visual type key from get_available_visual_types>",
          "title": "<display title>",
          "position": {"x": 0, "y": 0, "width": 400, "height": 300},
          "data_bindings": [
            {"role": "<axis|values|legend|category|rows|columns>", "table": "<table>", "field": "<field>"}
          ],
          "rationale": "<why this visual for this data>"
        }
      ]
    }
  ]
}
"""

_SYSTEM_VISION = """\
You are a Power BI expert and data visualization specialist. Analyze Power BI
report screenshots and provide actionable, specific feedback covering:
- Visual type appropriateness for the displayed data
- Layout and spacing issues
- Color usage and accessibility concerns
- Missing context (titles, axis labels, data labels, tooltips)
- Performance red flags (too many visuals, overly complex matrices)
- Specific improvement recommendations

Be concise and prioritize the top 3–5 most impactful observations.
"""

_SYSTEM_OPTIMIZE = """\
You are a DAX performance engineer. Analyze DAX expressions for correctness
and performance. Provide structured feedback:

1. **Summary** — one-sentence assessment (good/needs improvement/critical issues)
2. **Issues Found** — each issue with:
   - Severity: LOW / MEDIUM / HIGH / CRITICAL
   - Pattern: name of the anti-pattern
   - Explanation: why it is a problem
   - Fix: the corrected DAX snippet
3. **Optimized Version** — full rewritten DAX with all fixes applied
4. **Expected Impact** — estimated query time reduction (e.g., "30–50% faster on 10M-row tables")

Reference official DAX best practices from sqlbi.com and Microsoft documentation.
"""

_SYSTEM_CHAT = """\
You are a Power BI data analyst. The user will ask questions about their dataset.
Your job is to:
1. Understand the question intent
2. Write a DAX query (starting with EVALUATE) that answers it
3. Explain what the query does in plain language

Respond in this JSON format:
{
  "dax_query": "<EVALUATE ... DAX query>",
  "explanation": "<plain-language explanation of what the query returns>",
  "usage_note": "<any caveats, e.g., 'run in DAX Studio or via execute_dax_query tool'>"
}
"""


def _make_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Add it to your .env file."
        )
    return anthropic.Anthropic(api_key=api_key)


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def generate_dax_measure(
        description: str,
        dataset_schema_json: str = "",
        dataset_id: str = "",
        workspace_id: str = "",
    ) -> str:
        """
        Generate a DAX measure expression from a natural language description.

        Optionally provide the dataset schema JSON (from get_dataset_schema) or
        a dataset_id so the tool can fetch the schema automatically to give
        Claude the table/column context it needs.

        Args:
            description: Plain-language description, e.g.
                         'Running total of Sales Amount partitioned by Product Category'.
            dataset_schema_json: JSON string of dataset schema (optional).
            dataset_id: Dataset ID to auto-fetch schema (optional).
            workspace_id: Workspace ID for the dataset (optional).
        """
        import asyncio

        schema_context = dataset_schema_json

        if not schema_context and dataset_id:
            try:
                schema_context = asyncio.run(
                    pbi.get_dataset_tables(workspace_id, dataset_id)
                )
                if isinstance(schema_context, dict):
                    schema_context = json.dumps(schema_context)
            except Exception as exc:
                logger.warning("Could not fetch dataset schema: %s", exc)
                schema_context = ""

        prompt_parts = [f"Generate a DAX measure for: {description}"]
        if schema_context:
            prompt_parts.append(
                f"\nDataset schema (tables and columns):\n```json\n{schema_context}\n```"
            )
        prompt_parts.append(
            "\nReturn the DAX expression followed by -- EXPLANATION: <your explanation>."
        )
        prompt = "\n".join(prompt_parts)

        try:
            claude = _make_client()
            response = claude.messages.create(
                model="claude-opus-4-7",
                max_tokens=4096,
                thinking={"type": "adaptive"},
                system=_SYSTEM_DAX,
                messages=[{"role": "user", "content": prompt}],
            )
            text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            return json.dumps({
                "status": "ok",
                "dax_expression": text,
                "model": response.model,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            })
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    def suggest_report_layout(
        report_purpose: str,
        dataset_schema_json: str = "",
        dataset_id: str = "",
        workspace_id: str = "",
        page_count: int = 2,
    ) -> str:
        """
        Generate an optimal Power BI report layout plan from a dataset schema.

        Claude analyzes the schema and report purpose, then returns a structured
        JSON plan describing each page, the recommended visuals, their positions,
        and data bindings — ready to feed into create_report_definition and
        add_visual_to_page from the report_builder tools.

        Args:
            report_purpose: E.g. 'Executive sales dashboard with monthly trends and regional breakdown'.
            dataset_schema_json: JSON schema string (optional if dataset_id provided).
            dataset_id: Dataset ID to auto-fetch schema (optional).
            workspace_id: Workspace ID for the dataset (optional).
            page_count: Number of report pages to design (default 2).
        """
        import asyncio

        schema_context = dataset_schema_json

        if not schema_context and dataset_id:
            try:
                schema_context = asyncio.run(
                    pbi.get_dataset_tables(workspace_id, dataset_id)
                )
                if isinstance(schema_context, dict):
                    schema_context = json.dumps(schema_context)
            except Exception as exc:
                logger.warning("Could not fetch dataset schema: %s", exc)
                schema_context = ""

        prompt = (
            f"Design a {page_count}-page Power BI report for: {report_purpose}\n\n"
        )
        if schema_context:
            prompt += f"Dataset schema:\n```json\n{schema_context}\n```\n\n"
        prompt += (
            "Return ONLY valid JSON matching the schema described in your system prompt. "
            "Choose visual types from the PBIR type keys: clusteredBarChart, lineChart, "
            "pieChart, tableEx, pivotTable, card, multiRowCard, slicer, map, filledMap, "
            "scatterChart, waterfallChart, ribbonChart, treemap, gauge, kpiVisual."
        )

        try:
            claude = _make_client()
            with claude.messages.stream(
                model="claude-opus-4-7",
                max_tokens=8192,
                thinking={"type": "adaptive"},
                system=_SYSTEM_LAYOUT,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                response = stream.get_final_message()

            text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )

            # Attempt to parse as JSON to validate
            try:
                layout = json.loads(text)
                return json.dumps({
                    "status": "ok",
                    "layout": layout,
                    "model": response.model,
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                })
            except json.JSONDecodeError:
                # Return raw text if JSON parse fails (Claude may have wrapped it)
                return json.dumps({
                    "status": "ok",
                    "layout_raw": text,
                    "model": response.model,
                    "note": "Layout returned as raw text (JSON parse failed). Extract the JSON block.",
                })
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    def analyze_report_screenshot(
        screenshot_base64: str,
        analysis_request: str = "Analyze this Power BI report and provide improvement recommendations.",
        media_type: str = "image/png",
    ) -> str:
        """
        Use Claude's vision capability to analyze a Power BI report screenshot.

        Pass the base64-encoded image from screenshot_canvas (powerbi-desktop-mcp)
        or from export_report (PNG format). Claude identifies visual design issues,
        layout problems, accessibility concerns, and improvement opportunities.

        Args:
            screenshot_base64: Base64-encoded PNG/JPEG image string.
            analysis_request: Specific question or focus area for the analysis.
            media_type: Image MIME type — 'image/png' (default) or 'image/jpeg'.
        """
        try:
            claude = _make_client()
            response = claude.messages.create(
                model="claude-opus-4-7",
                max_tokens=4096,
                system=_SYSTEM_VISION,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": screenshot_base64,
                                },
                            },
                            {"type": "text", "text": analysis_request},
                        ],
                    }
                ],
            )
            text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            return json.dumps({
                "status": "ok",
                "analysis": text,
                "model": response.model,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            })
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    def optimize_dax_with_ai(
        measure_expression: str,
        context: str = "",
    ) -> str:
        """
        Send a DAX expression to Claude for deep, context-aware optimization analysis.

        Goes beyond the static suggest_dax_optimizations rules by applying
        reasoning about evaluation context, relationship cardinality, and
        data volume implications. Returns severity-ranked issues, explanations,
        and a fully rewritten optimized version.

        Args:
            measure_expression: The DAX measure or query expression to optimize.
            context: Optional context about the data model (e.g., 'FactSales has 50M rows,
                     partitioned by Year; Products table has 10K rows').
        """
        prompt = f"Analyze and optimize this DAX expression:\n\n```dax\n{measure_expression}\n```"
        if context:
            prompt += f"\n\nData model context:\n{context}"

        try:
            claude = _make_client()
            response = claude.messages.create(
                model="claude-opus-4-7",
                max_tokens=6144,
                thinking={"type": "adaptive"},
                system=_SYSTEM_OPTIMIZE,
                messages=[{"role": "user", "content": prompt}],
            )
            text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            return json.dumps({
                "status": "ok",
                "optimization_report": text,
                "model": response.model,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            })
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    def chat_with_data(
        question: str,
        dataset_schema_json: str = "",
        dataset_id: str = "",
        workspace_id: str = "",
    ) -> str:
        """
        Ask a natural language question about a Power BI dataset.

        Claude analyzes the question, inspects the dataset schema, generates a
        DAX query (starting with EVALUATE) that answers the question, and explains
        what the query returns in plain language. The generated query can be
        executed directly with execute_dax_query.

        Args:
            question: Natural language question, e.g. 'What were the top 5 products by
                      revenue last quarter?'
            dataset_schema_json: JSON schema string (optional if dataset_id provided).
            dataset_id: Dataset ID to auto-fetch schema (optional).
            workspace_id: Workspace ID for the dataset (optional).
        """
        import asyncio

        schema_context = dataset_schema_json

        if not schema_context and dataset_id:
            try:
                schema_context = asyncio.run(
                    pbi.get_dataset_tables(workspace_id, dataset_id)
                )
                if isinstance(schema_context, dict):
                    schema_context = json.dumps(schema_context)
            except Exception as exc:
                logger.warning("Could not fetch dataset schema: %s", exc)
                schema_context = ""

        prompt = f"Question: {question}"
        if schema_context:
            prompt += f"\n\nDataset schema:\n```json\n{schema_context}\n```"

        try:
            claude = _make_client()
            response = claude.messages.create(
                model="claude-opus-4-7",
                max_tokens=4096,
                thinking={"type": "adaptive"},
                system=_SYSTEM_CHAT,
                messages=[{"role": "user", "content": prompt}],
            )
            text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )

            # Parse inner JSON returned by Claude
            try:
                inner = json.loads(text)
            except json.JSONDecodeError:
                inner = {"raw_response": text}

            return json.dumps({
                "status": "ok",
                "model": response.model,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                **inner,
            })
        except Exception as exc:
            return json.dumps({"error": str(exc)})
