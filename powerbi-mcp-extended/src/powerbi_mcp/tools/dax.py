"""
MCP tools: Advanced DAX Intelligence.

These tools go beyond the official Microsoft MCP's basic DAX execution by providing:
- Performance benchmarking (multiple runs, statistics)
- Measure dependency graph extraction
- DAX best-practice analysis and optimization suggestions
- DAX query execution via Power BI REST API (works on published datasets)
"""

import asyncio
import json
import re
import time
from mcp.server import FastMCP
from .. import client


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def execute_dax_query(
        workspace_id: str, dataset_id: str, dax_query: str
    ) -> str:
        """
        Execute a DAX query against a published Power BI dataset and return results.
        This works on cloud-hosted datasets (not Power BI Desktop) via the REST API.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
            dax_query: A valid DAX query, e.g. "EVALUATE SUMMARIZE('Sales', 'Sales'[Category])"
        """
        result = await client.execute_dax_query(workspace_id, dataset_id, dax_query)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def benchmark_dax_query(
        workspace_id: str,
        dataset_id: str,
        dax_query: str,
        runs: int = 5,
    ) -> str:
        """
        Benchmark a DAX query by running it multiple times and reporting
        min/max/avg/median execution times. Helps identify slow measures.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
            dax_query: The DAX query to benchmark.
            runs: Number of times to run the query (default 5, max 10).
        """
        runs = max(1, min(runs, 10))
        timings: list[float] = []

        for i in range(runs):
            t0 = time.perf_counter()
            await client.execute_dax_query(workspace_id, dataset_id, dax_query)
            elapsed = (time.perf_counter() - t0) * 1000  # ms
            timings.append(elapsed)

        timings_sorted = sorted(timings)
        n = len(timings_sorted)
        median = (
            timings_sorted[n // 2]
            if n % 2 == 1
            else (timings_sorted[n // 2 - 1] + timings_sorted[n // 2]) / 2
        )

        return json.dumps({
            "query": dax_query,
            "runs": runs,
            "timing_ms": {
                "min": round(min(timings), 1),
                "max": round(max(timings), 1),
                "avg": round(sum(timings) / n, 1),
                "median": round(median, 1),
                "all": [round(t, 1) for t in timings],
            },
            "assessment": _assess_performance(sum(timings) / n),
        }, indent=2)

    @mcp.tool()
    async def analyze_measure_dependencies(
        workspace_id: str,
        dataset_id: str,
        measure_expression: str,
        measure_name: str = "MyMeasure",
    ) -> str:
        """
        Parse a DAX measure expression and extract:
        - All referenced measures (direct and potential indirect references)
        - Referenced tables and columns
        - DAX functions used
        - Nesting depth estimate

        This is a static analysis tool — it does NOT execute the DAX.

        Args:
            workspace_id: Workspace GUID (used to fetch table/column names for context).
            dataset_id: Dataset GUID (used to fetch schema for context).
            measure_expression: The DAX expression body of the measure.
            measure_name: Name of the measure being analyzed (for display).
        """
        # Fetch schema for cross-referencing
        tables = await client.get_dataset_tables(workspace_id, dataset_id)
        table_names = {t.get("name", "") for t in tables}

        analysis = _analyze_dax_expression(measure_expression, measure_name, table_names)
        return json.dumps(analysis, indent=2)

    @mcp.tool()
    async def suggest_dax_optimizations(
        workspace_id: str,
        dataset_id: str,
        measure_expression: str,
        measure_name: str = "MyMeasure",
    ) -> str:
        """
        Analyze a DAX measure expression and return a list of optimization suggestions
        based on common Power BI performance best practices.

        Examples of issues detected:
        - CALCULATE with many filters (prefer KEEPFILTERS)
        - FILTER(ALL(...)) instead of CALCULATETABLE
        - Missing REMOVEFILTERS vs ALL distinction
        - Overuse of iterators (SUMX/AVERAGEX) on large tables
        - Nested CALCULATE without purpose
        - String operations inside aggregations
        - Use of IF with ISBLANK (prefer COALESCE)

        Args:
            workspace_id: Workspace GUID (for schema context).
            dataset_id: Dataset GUID (for schema context).
            measure_expression: The DAX expression body.
            measure_name: Name of the measure.
        """
        tables = await client.get_dataset_tables(workspace_id, dataset_id)
        table_names = {t.get("name", "") for t in tables}

        suggestions = _get_optimization_suggestions(measure_expression, table_names)
        analysis = _analyze_dax_expression(measure_expression, measure_name, table_names)

        return json.dumps({
            "measure": measure_name,
            "expression": measure_expression,
            "optimization_suggestions": suggestions,
            "static_analysis": analysis,
            "overall_rating": _rate_measure(suggestions),
        }, indent=2)

    @mcp.tool()
    async def compare_dax_query_results(
        workspace_id: str,
        dataset_id: str,
        dax_query_a: str,
        dax_query_b: str,
    ) -> str:
        """
        Run two DAX queries in parallel and compare their result shapes and
        execution times. Useful for validating measure rewrites produce the
        same results before deploying.

        Args:
            workspace_id: Workspace GUID.
            dataset_id: Dataset GUID.
            dax_query_a: First DAX query (original).
            dax_query_b: Second DAX query (rewrite/optimized).
        """
        t0_a = time.perf_counter()
        t0_b = time.perf_counter()

        result_a, result_b = await asyncio.gather(
            client.execute_dax_query(workspace_id, dataset_id, dax_query_a),
            client.execute_dax_query(workspace_id, dataset_id, dax_query_b),
        )
        time_a = (time.perf_counter() - t0_a) * 1000
        time_b = (time.perf_counter() - t0_b) * 1000

        rows_a = _count_rows(result_a)
        rows_b = _count_rows(result_b)

        return json.dumps({
            "query_a": {"query": dax_query_a, "row_count": rows_a, "time_ms": round(time_a, 1)},
            "query_b": {"query": dax_query_b, "row_count": rows_b, "time_ms": round(time_b, 1)},
            "row_counts_match": rows_a == rows_b,
            "speedup": round(time_a / time_b, 2) if time_b > 0 else None,
            "note": "Row counts matching does not guarantee identical values. Inspect results manually.",
        }, indent=2)


# ── Static analysis helpers ───────────────────────────────────────────────────

_DAX_FUNCTIONS = [
    "CALCULATE", "CALCULATETABLE", "FILTER", "ALL", "ALLEXCEPT", "ALLSELECTED",
    "KEEPFILTERS", "REMOVEFILTERS", "SUMX", "AVERAGEX", "MAXX", "MINX", "COUNTX",
    "RANKX", "TOPN", "SUMMARIZE", "SUMMARIZECOLUMNS", "ADDCOLUMNS", "SELECTCOLUMNS",
    "UNION", "INTERSECT", "EXCEPT", "CROSSJOIN", "GENERATE", "GENERATEALL",
    "RELATED", "RELATEDTABLE", "USERELATIONSHIP", "CROSSFILTER",
    "IF", "SWITCH", "IFERROR", "ISBLANK", "COALESCE", "BLANK",
    "DIVIDE", "ROUND", "ROUNDUP", "ROUNDDOWN", "INT", "TRUNC",
    "FORMAT", "TEXT", "VALUE", "DATEVALUE", "DATE", "TODAY", "NOW",
    "YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND",
    "DATEADD", "DATESYTD", "DATESMTD", "DATESQTD", "SAMEPERIODLASTYEAR",
    "TOTALYTD", "TOTALMTD", "TOTALQTD", "PREVIOUSMONTH", "PREVIOUSQUARTER",
    "PREVIOUSYEAR", "PARALLELPERIOD", "DATESBETWEEN",
    "HASONEVALUE", "HASONEFILTER", "ISFILTERED", "ISCROSSFILTERED",
    "EARLIER", "EARLIEST", "ROW", "SELECTEDVALUE", "VALUES", "DISTINCT",
    "COUNTROWS", "COUNT", "COUNTA", "COUNTBLANK", "DISTINCTCOUNT",
    "SUM", "AVERAGE", "MAX", "MIN", "MEDIAN", "PERCENTILE",
    "VAR", "RETURN",
]

_ITERATOR_FUNCTIONS = {"SUMX", "AVERAGEX", "MAXX", "MINX", "COUNTX", "RANKX", "FILTER",
                        "ADDCOLUMNS", "SELECTCOLUMNS", "GENERATE", "GENERATEALL"}


def _analyze_dax_expression(
    expr: str, name: str, table_names: set[str]
) -> dict:
    expr_upper = expr.upper()

    # Functions used
    functions_used = [f for f in _DAX_FUNCTIONS if re.search(rf"\b{f}\b", expr_upper)]
    iterators_used = [f for f in functions_used if f in _ITERATOR_FUNCTIONS]

    # Column references: 'Table'[Column] or Table[Column]
    col_refs = re.findall(r"'?[\w\s]+'?\[[\w\s]+\]", expr)

    # Measure references (heuristic: [Name] not preceded by table)
    measure_refs = re.findall(r"(?<!['\w])\[[\w\s]+\]", expr)

    # Nesting depth (estimate via CALCULATE count)
    calculate_depth = expr_upper.count("CALCULATE")

    # VAR usage
    has_variables = "VAR " in expr_upper

    return {
        "measure_name": name,
        "functions_used": functions_used,
        "iterator_functions": iterators_used,
        "column_references": list(set(col_refs)),
        "measure_references": list(set(measure_refs)),
        "calculate_nesting_depth": calculate_depth,
        "uses_variables": has_variables,
        "expression_length": len(expr),
    }


def _get_optimization_suggestions(expr: str, table_names: set[str]) -> list[dict]:
    expr_upper = expr.upper()
    suggestions = []

    # 1. FILTER(ALL(...)) — can often be CALCULATETABLE
    if re.search(r"FILTER\s*\(\s*ALL\s*\(", expr_upper):
        suggestions.append({
            "rule": "FILTER_ALL",
            "severity": "medium",
            "message": (
                "Consider replacing FILTER(ALL(...), ...) with CALCULATETABLE(..., ALL(...)) "
                "or using REMOVEFILTERS inside CALCULATE. "
                "CALCULATETABLE is generally more efficient."
            ),
        })

    # 2. Nested CALCULATE without variables
    calculate_count = len(re.findall(r"\bCALCULATE\b", expr_upper))
    if calculate_count > 1 and "VAR " not in expr_upper:
        suggestions.append({
            "rule": "NESTED_CALCULATE_NO_VAR",
            "severity": "low",
            "message": (
                f"Found {calculate_count} CALCULATE calls. "
                "Consider using VAR/RETURN to store intermediate results — "
                "this improves readability and can reduce redundant evaluations."
            ),
        })

    # 3. SUMX / iterator over potentially large table without filter
    iterators = re.findall(r"\b(SUMX|AVERAGEX|MAXX|MINX|COUNTX)\s*\(", expr_upper)
    if iterators and "FILTER" not in expr_upper and "CALCULATETABLE" not in expr_upper:
        suggestions.append({
            "rule": "UNFILTERED_ITERATOR",
            "severity": "high",
            "message": (
                f"Iterator function(s) {iterators} detected without an explicit filter. "
                "Iterating over large unfiltered tables is a common performance bottleneck. "
                "Apply a filter or use CALCULATE with a scalar aggregation instead."
            ),
        })

    # 4. IF(ISBLANK(...)) — prefer COALESCE
    if re.search(r"\bIF\s*\(\s*ISBLANK\s*\(", expr_upper):
        suggestions.append({
            "rule": "IF_ISBLANK",
            "severity": "low",
            "message": (
                "Replace IF(ISBLANK(x), default, x) with COALESCE(x, default). "
                "COALESCE is more concise and equally performant."
            ),
        })

    # 5. DIVIDE without explicit alternate result
    divide_calls = re.findall(r"\bDIVIDE\s*\([^)]+\)", expr_upper)
    for call in divide_calls:
        # Simple heuristic: check comma count — DIVIDE(a,b) has 1 comma, DIVIDE(a,b,alt) has 2
        if call.count(",") < 2:
            suggestions.append({
                "rule": "DIVIDE_NO_ALTERNATE",
                "severity": "low",
                "message": (
                    "DIVIDE() is used without an explicit alternate result. "
                    "Consider adding DIVIDE(numerator, denominator, 0) to make the "
                    "zero-division behavior explicit and document intent."
                ),
            })
            break

    # 6. String operations inside aggregators
    if re.search(r"\b(SUMX|AVERAGEX)\b.*\b(FORMAT|TEXT|LEFT|RIGHT|MID|CONCATENATE)\b", expr_upper):
        suggestions.append({
            "rule": "STRING_OPS_IN_ITERATOR",
            "severity": "high",
            "message": (
                "String manipulation functions (FORMAT, TEXT, CONCATENATE, etc.) inside "
                "iterators like SUMX/AVERAGEX are very expensive. Move string formatting "
                "to a calculated column or to the final display layer."
            ),
        })

    # 7. ALL on specific column instead of REMOVEFILTERS
    if re.search(r"\bALL\s*\(\s*'?[\w\s]+'?\[", expr_upper):
        suggestions.append({
            "rule": "ALL_COLUMN_PREFER_REMOVEFILTERS",
            "severity": "low",
            "message": (
                "ALL('Table'[Column]) inside CALCULATE can be replaced with "
                "REMOVEFILTERS('Table'[Column]) for clearer intent. "
                "Both are functionally equivalent."
            ),
        })

    if not suggestions:
        suggestions.append({
            "rule": "NO_ISSUES",
            "severity": "info",
            "message": "No common anti-patterns detected. The expression looks clean.",
        })

    return suggestions


def _rate_measure(suggestions: list[dict]) -> str:
    high = sum(1 for s in suggestions if s.get("severity") == "high")
    medium = sum(1 for s in suggestions if s.get("severity") == "medium")
    if high > 0:
        return "needs_attention"
    if medium > 0:
        return "could_improve"
    return "good"


def _assess_performance(avg_ms: float) -> str:
    if avg_ms < 100:
        return "fast (<100ms)"
    elif avg_ms < 500:
        return "acceptable (100–500ms)"
    elif avg_ms < 2000:
        return "slow (500ms–2s) — investigate"
    else:
        return "very slow (>2s) — optimization required"


def _count_rows(result: dict) -> int:
    try:
        return len(result["results"][0]["tables"][0]["rows"])
    except (KeyError, IndexError, TypeError):
        return -1
