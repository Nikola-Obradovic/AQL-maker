# AQL Builder

An intuitive tool for creating IBM QRadar AQL (Ariel Query Language) queries. Available as both a CLI tool and a web-based UI.

## Quick Start

### Web UI (Recommended)

```bash
# Install Flask
pip install flask

# Run the web application
python3 app.py
```

Then open **http://localhost:5000** in your browser.

### CLI Version

```bash
python3 aql_builder.py
```

## Web UI Features

### Query Builder Tab
- **Visual query construction** - Build queries step-by-step
- **Quick-add buttons** - Common fields and WHERE conditions
- **Real-time validation** - Errors and warnings as you type
- **One-click copy** - Copy query to clipboard

### Templates Tab
- **25+ pre-built queries** for common security scenarios
- **Categories**: Authentication, Network, Threat Detection, Windows Events, Investigation
- **Customizable** - Load templates and modify them

### Reference Tab
- **Event Fields** - All available event table columns
- **Flow Fields** - All available flow table columns
- **Functions** - Calculation, aggregation, retrieval, geo, filter functions
- **Operators** - Comparison, string, logical operators
- **Time Clauses** - LAST, START/STOP, PARSEDATETIME syntax

### Validator Tab
- Paste any AQL query to check for errors
- Identifies syntax issues and common mistakes
- Suggestions for improvements

## Template Categories

| Category | Queries |
|----------|---------|
| Authentication & Access | Failed logins, brute force, privileged accounts |
| Network & Traffic | Top talkers, RDP, SSH, suspicious ports |
| Threat Detection | High magnitude, LOLBins, DNS tunneling |
| System Monitoring | Events by source, category analysis |
| Windows Events | 4624, 4688, 4740 events |
| Investigation | Activity by IP/user, offense events |

## Quick Reference

### Basic Query Structure
```sql
SELECT <columns>
FROM <events|flows>
[WHERE <conditions>]
[GROUP BY <columns>]
[HAVING <conditions>]
[ORDER BY <columns> [ASC|DESC]]
[LIMIT <number>]
[LAST <time> | START '<datetime>' STOP '<datetime>']
```

### Common Functions
```sql
LOGSOURCENAME(logsourceid)    -- Log source name
QIDNAME(qid)                  -- Event name
CATEGORYNAME(category)        -- Category name
DATEFORMAT(starttime, 'fmt')  -- Format timestamp
COUNT(*), SUM(), AVG()        -- Aggregations
INCIDR('10.0.0.0/8', ip)      -- CIDR matching
```

### Common Operators
```sql
=, !=, <, >, <=, >=           -- Comparison
LIKE, ILIKE                   -- Pattern match (% wildcard)
MATCHES, IMATCHES             -- Regex match
AND, OR, NOT                  -- Logical
IN (val1, val2)               -- List
BETWEEN x AND y               -- Range
```

### Time Clauses
```sql
LAST 1 HOURS                  -- Relative time
LAST 24 HOURS
LAST 7 DAYS
START '2024-01-01 00:00'      -- Absolute time
START '2024-01-01' STOP '2024-01-02'
```

## Requirements

- Python 3.6+
- Flask (for web UI): `pip install flask`
- Optional: `xclip` or `xsel` for CLI clipboard support

## File Structure

```
AQL-maker/
├── app.py              # Flask web application
├── aql_builder.py      # CLI application
├── aql_reference.py    # AQL reference data
├── query_builder.py    # Query building logic
├── templates.py        # Pre-built query templates
├── templates/
│   └── index.html      # Web UI template
└── requirements.txt    # Python dependencies
```

## License

MIT
