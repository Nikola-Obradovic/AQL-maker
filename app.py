#!/usr/bin/env python3
"""
AQL Builder Web Application
A Flask-based web UI for building IBM QRadar AQL queries
"""

from flask import Flask, render_template, jsonify, request
from aql_reference import AQLReference
from templates import QueryTemplates
import re

app = Flask(__name__)
reference = AQLReference()
templates = QueryTemplates()


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/reference/event-fields')
def get_event_fields():
    """Get all event fields."""
    fields = []
    for name, (ftype, desc) in reference.EVENT_FIELDS.items():
        fields.append({'name': name, 'type': ftype, 'description': desc})
    return jsonify(fields)


@app.route('/api/reference/flow-fields')
def get_flow_fields():
    """Get all flow fields."""
    fields = []
    for name, (ftype, desc) in reference.FLOW_FIELDS.items():
        fields.append({'name': name, 'type': ftype, 'description': desc})
    return jsonify(fields)


@app.route('/api/reference/functions')
def get_functions():
    """Get all functions organized by category."""
    categories = {
        'Calculation & Formatting': reference.CALC_FUNCTIONS,
        'Aggregation': reference.AGG_FUNCTIONS,
        'Data Retrieval': reference.RETRIEVAL_FUNCTIONS,
        'Geographic': reference.GEO_FUNCTIONS,
        'Reference Data': reference.REFERENCE_FUNCTIONS,
        'Filter': reference.FILTER_FUNCTIONS,
    }

    result = {}
    for cat_name, funcs in categories.items():
        result[cat_name] = []
        for name, (syntax, desc) in funcs.items():
            result[cat_name].append({
                'name': name,
                'syntax': syntax,
                'description': desc
            })
    return jsonify(result)


@app.route('/api/reference/operators')
def get_operators():
    """Get all operators."""
    return jsonify({
        'comparison': [{'op': k, 'desc': v} for k, v in reference.COMPARISON_OPS.items()],
        'string': [{'op': k, 'desc': v} for k, v in reference.STRING_OPS.items()],
        'logical': [{'op': k, 'desc': v} for k, v in reference.LOGICAL_OPS.items()],
    })


@app.route('/api/templates')
def get_templates():
    """Get all query templates."""
    result = {}
    for cat_name, tmpl_list in templates.CATEGORIES.items():
        result[cat_name] = []
        for t in tmpl_list:
            result[cat_name].append({
                'name': t['name'],
                'description': t['description'],
                'query': t['query'],
                'params': t.get('params', [])
            })
    return jsonify(result)


@app.route('/api/validate', methods=['POST'])
def validate_query():
    """Validate an AQL query."""
    data = request.get_json()
    query = data.get('query', '')

    errors = []
    warnings = []
    query_upper = query.upper()

    # Check for SELECT
    if not query_upper.strip().startswith("SELECT"):
        errors.append("Query should start with SELECT")

    # Check for FROM
    if "FROM" not in query_upper:
        errors.append("Query is missing FROM clause")
    else:
        from_match = re.search(r"FROM\s+(\w+)", query_upper)
        if from_match:
            table = from_match.group(1)
            if table not in ["EVENTS", "FLOWS"]:
                errors.append(f"Unknown table '{table}'. Use 'events' or 'flows'")

    # Check for common syntax errors
    if "WHERE" in query_upper:
        if "==" in query:
            errors.append("Use single '=' for equality, not '=='")

        single_quotes = query.count("'")
        if single_quotes % 2 != 0:
            errors.append("Unmatched single quotes detected")

    # Check LIKE usage
    if "LIKE" in query_upper and "%" not in query:
        warnings.append("LIKE clause usually requires % wildcard")

    # Check time clause
    has_time = any(kw in query_upper for kw in ["LAST", "START", "STOP"])
    if not has_time:
        warnings.append("Consider adding a time clause (LAST, START/STOP)")

    # Check clause ordering
    if "LIMIT" in query_upper and "ORDER BY" in query_upper:
        limit_pos = query_upper.find("LIMIT")
        order_pos = query_upper.find("ORDER BY")
        if limit_pos < order_pos:
            errors.append("ORDER BY should come before LIMIT")

    if "LIMIT" in query_upper and "LAST" in query_upper:
        limit_pos = query_upper.find("LIMIT")
        last_pos = query_upper.find("LAST")
        if last_pos < limit_pos:
            errors.append("LIMIT should come before time clause (LAST)")

    # Check GROUP BY with aggregation
    if "GROUP BY" in query_upper:
        agg_funcs = ["COUNT(", "SUM(", "AVG(", "MIN(", "MAX(", "UNIQUECOUNT("]
        has_agg = any(func in query_upper for func in agg_funcs)
        if not has_agg:
            warnings.append("GROUP BY is typically used with aggregate functions")

    return jsonify({
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    })


@app.route('/api/build', methods=['POST'])
def build_query():
    """Build a query from parts."""
    data = request.get_json()

    parts = []

    # SELECT
    select_cols = data.get('select', ['*'])
    if select_cols and select_cols != ['*']:
        parts.append(f"SELECT {', '.join(select_cols)}")
    else:
        parts.append("SELECT *")

    # FROM
    table = data.get('from', 'events')
    parts.append(f"FROM {table}")

    # WHERE
    where_conditions = data.get('where', [])
    if where_conditions:
        parts.append(f"WHERE {' AND '.join(where_conditions)}")

    # GROUP BY
    group_by = data.get('groupBy', [])
    if group_by:
        parts.append(f"GROUP BY {', '.join(group_by)}")

    # HAVING
    having = data.get('having', [])
    if having:
        parts.append(f"HAVING {' AND '.join(having)}")

    # ORDER BY
    order_by = data.get('orderBy', [])
    order_dir = data.get('orderDir', 'DESC')
    if order_by:
        parts.append(f"ORDER BY {', '.join(order_by)} {order_dir}")

    # LIMIT
    limit = data.get('limit')
    if limit:
        parts.append(f"LIMIT {limit}")

    # TIME
    time_clause = data.get('time')
    if time_clause:
        parts.append(time_clause)

    query = "\n".join(parts)

    return jsonify({'query': query})


if __name__ == '__main__':
    print("Starting AQL Builder Web UI...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
