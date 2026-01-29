#!/usr/bin/env python3
"""
AQL Reference - Comprehensive reference for AQL fields, functions, and operators
Based on IBM QRadar documentation
"""

class AQLReference:
    """Comprehensive AQL reference data and display methods."""

    # Event fields
    EVENT_FIELDS = {
        # Core identification
        "qid": ("INTEGER", "QRadar event ID (use with QIDNAME function)"),
        "qidEventId": ("INTEGER", "Original event ID from the log source"),
        "category": ("INTEGER", "Low-level category ID (use with CATEGORYNAME)"),
        "logsourceid": ("INTEGER", "Log source ID (use with LOGSOURCENAME)"),
        "devicetype": ("INTEGER", "Device type ID (use with LOGSOURCETYPENAME)"),

        # Network fields
        "sourceip": ("IP", "Source IP address"),
        "destinationip": ("IP", "Destination IP address"),
        "sourceport": ("INTEGER", "Source port number"),
        "destinationport": ("INTEGER", "Destination port number"),
        "sourcemac": ("STRING", "Source MAC address"),
        "destinationmac": ("STRING", "Destination MAC address"),
        "protocolid": ("INTEGER", "Protocol ID (use with PROTOCOLNAME)"),

        # User and identity
        "username": ("STRING", "Username associated with the event"),
        "identityip": ("IP", "Identity IP address"),
        "identityhostname": ("STRING", "Identity hostname"),

        # Time fields
        "starttime": ("TIMESTAMP", "Event start time (milliseconds since epoch)"),
        "endtime": ("TIMESTAMP", "Event end time"),
        "devicetime": ("TIMESTAMP", "Time reported by the device"),

        # Event metadata
        "eventcount": ("INTEGER", "Number of events aggregated"),
        "magnitude": ("INTEGER", "Event magnitude (1-10)"),
        "severity": ("INTEGER", "Event severity (1-10)"),
        "credibility": ("INTEGER", "Event credibility (1-10)"),
        "relevance": ("INTEGER", "Event relevance (1-10)"),

        # Payload and content
        "payload": ("BLOB", "Raw event payload (use UTF8 function to read)"),
        "utf8payload": ("STRING", "UTF-8 decoded payload"),

        # Source information
        "sourcev6": ("IPv6", "Source IPv6 address"),
        "destinationv6": ("IPv6", "Destination IPv6 address"),
        "sourcegeographiclocation": ("STRING", "Source geographic location"),
        "destinationgeographiclocation": ("STRING", "Destination geographic location"),

        # Processing information
        "processorid": ("INTEGER", "Event processor ID"),
        "collectorid": ("INTEGER", "Event collector ID"),
        "domainid": ("INTEGER", "Domain ID"),

        # Rule and offense
        "ruleid": ("INTEGER", "Rule ID that triggered"),
        "hasoffense": ("BOOLEAN", "Whether event is part of an offense"),
    }

    # Flow fields
    FLOW_FIELDS = {
        # Core identification
        "sourcebytes": ("LONG", "Bytes sent from source"),
        "destinationbytes": ("LONG", "Bytes sent to destination"),
        "sourcepackets": ("LONG", "Packets from source"),
        "destinationpackets": ("LONG", "Packets to destination"),
        "totalbytes": ("LONG", "Total bytes transferred"),
        "totalpackets": ("LONG", "Total packets transferred"),

        # Network fields
        "sourceip": ("IP", "Source IP address"),
        "destinationip": ("IP", "Destination IP address"),
        "sourceport": ("INTEGER", "Source port number"),
        "destinationport": ("INTEGER", "Destination port number"),
        "protocolid": ("INTEGER", "Protocol ID"),

        # Application
        "applicationid": ("INTEGER", "Application ID (use with APPLICATIONNAME)"),
        "applicationname": ("STRING", "Application name"),

        # ASN fields
        "sourceasn": ("INTEGER", "Source Autonomous System Number"),
        "destinationasn": ("INTEGER", "Destination Autonomous System Number"),

        # Payload
        "sourcepayload": ("BLOB", "Source payload data"),
        "destinationpayload": ("BLOB", "Destination payload data"),

        # Time
        "starttime": ("TIMESTAMP", "Flow start time"),
        "endtime": ("TIMESTAMP", "Flow end time"),
        "firstpackettime": ("TIMESTAMP", "Time of first packet"),
        "lastpackettime": ("TIMESTAMP", "Time of last packet"),

        # Geographic
        "sourcegeographiclocation": ("STRING", "Source geographic location"),
        "destinationgeographiclocation": ("STRING", "Destination geographic location"),

        # Processing
        "flowdirection": ("STRING", "Flow direction (L2L, L2R, R2L, R2R)"),
        "flowsourceid": ("INTEGER", "Flow source ID"),
        "processorid": ("INTEGER", "Processor ID"),
        "domainid": ("INTEGER", "Domain ID"),
    }

    # Calculation and formatting functions
    CALC_FUNCTIONS = {
        "BASE64": ("BASE64(value)", "Returns Base64 encoded string of binary data"),
        "CONCAT": ("CONCAT(str1, str2, ...)", "Concatenates multiple strings into one"),
        "DATEFORMAT": ("DATEFORMAT(timestamp, 'format')", "Formats timestamp to readable form. Format: yyyy-MM-dd HH:mm:ss"),
        "DOUBLE": ("DOUBLE(value)", "Converts value to double data type"),
        "LONG": ("LONG(value)", "Converts value to long integer"),
        "LOWER": ("LOWER(string)", "Returns lowercase version of string"),
        "UPPER": ("UPPER(string)", "Returns uppercase version of string"),
        "NOW": ("NOW()", "Returns current time in milliseconds since epoch"),
        "PARSEDATETIME": ("PARSEDATETIME('time reference')", "Parses time reference (e.g., '1 hour ago', 'now')"),
        "PARSETIMESTAMP": ("PARSETIMESTAMP('datetime', 'format')", "Converts datetime string to UNIX epoch"),
        "REPLACEALL": ("REPLACEALL(string, 'regex', 'replacement')", "Replace all regex matches"),
        "REPLACEFIRST": ("REPLACEFIRST(string, 'regex', 'replacement')", "Replace first regex match"),
        "STR": ("STR(value)", "Converts any value to string"),
        "STRLEN": ("STRLEN(string)", "Returns length of string"),
        "STRPOS": ("STRPOS(string, 'substring')", "Returns position of substring (0-indexed, -1 if not found)"),
        "SUBSTRING": ("SUBSTRING(string, start, length)", "Extracts substring from string"),
        "UTF8": ("UTF8(payload)", "Converts byte array to UTF-8 string"),
    }

    # Aggregation functions
    AGG_FUNCTIONS = {
        "COUNT": ("COUNT(*) or COUNT(field)", "Returns count of rows"),
        "SUM": ("SUM(field)", "Returns sum of numeric field"),
        "AVG": ("AVG(field)", "Returns average of numeric field"),
        "MIN": ("MIN(field)", "Returns minimum value"),
        "MAX": ("MAX(field)", "Returns maximum value"),
        "FIRST": ("FIRST(field)", "Returns first value in aggregate"),
        "LAST": ("LAST(field)", "Returns last value in aggregate"),
        "UNIQUECOUNT": ("UNIQUECOUNT(field)", "Returns count of unique values"),
        "STDEV": ("STDEV(field)", "Returns sample standard deviation"),
        "STDEVP": ("STDEVP(field)", "Returns population standard deviation"),
    }

    # Data retrieval functions
    RETRIEVAL_FUNCTIONS = {
        "ASSETHOSTNAME": ("ASSETHOSTNAME(ip)", "Returns hostname for IP from asset database"),
        "ASSETPROPERTY": ("ASSETPROPERTY('property', ip)", "Returns asset property value"),
        "ASSETUSER": ("ASSETUSER(ip)", "Returns username associated with IP"),
        "NETWORKNAME": ("NETWORKNAME(ip)", "Returns network name from hierarchy"),
        "FULLNETWORKNAME": ("FULLNETWORKNAME(ip)", "Returns full network path from hierarchy"),
        "APPLICATIONNAME": ("APPLICATIONNAME(applicationid)", "Returns application name"),
        "CATEGORYNAME": ("CATEGORYNAME(category)", "Returns category name"),
        "DOMAINNAME": ("DOMAINNAME(domainid)", "Returns domain name"),
        "HOSTNAME": ("HOSTNAME(processorid)", "Returns processor hostname"),
        "LOGSOURCENAME": ("LOGSOURCENAME(logsourceid)", "Returns log source name"),
        "LOGSOURCETYPENAME": ("LOGSOURCETYPENAME(devicetype)", "Returns log source type name"),
        "PROCESSORNAME": ("PROCESSORNAME(processorid)", "Returns processor name"),
        "PROTOCOLNAME": ("PROTOCOLNAME(protocolid)", "Returns protocol name (TCP, UDP, etc.)"),
        "QIDNAME": ("QIDNAME(qid)", "Returns event name for QID"),
        "QIDDESCRIPTION": ("QIDDESCRIPTION(qid)", "Returns event description for QID"),
        "RULENAME": ("RULENAME(ruleid)", "Returns rule name"),
    }

    # Geographic functions
    GEO_FUNCTIONS = {
        "GEO::LOOKUP": ("GEO::LOOKUP(ip, 'property')", "Returns MaxMind location data as JSON"),
        "GEO::LOOKUP_TEXT": ("GEO::LOOKUP_TEXT(ip, 'property')", "Returns location data as text. Properties: city_name, country_name, continent_name"),
        "GEO::DISTANCE": ("GEO::DISTANCE(ip1, ip2)", "Returns distance between IPs in kilometers"),
    }

    # Reference data functions
    REFERENCE_FUNCTIONS = {
        "REFERENCESETCONTAINS": ("REFERENCESETCONTAINS('SetName', value)", "Returns true if value is in reference set"),
        "REFERENCEMAP": ("REFERENCEMAP('MapName', key)", "Returns value from reference map"),
        "REFERENCETABLE": ("REFERENCETABLE('TableName', 'column', key)", "Returns column value from reference table"),
    }

    # Filter functions
    FILTER_FUNCTIONS = {
        "INCIDR": ("INCIDR('cidr', ip)", "Returns true if IP is in CIDR range. Example: INCIDR('192.168.0.0/16', sourceip)"),
        "INOFFENSE": ("INOFFENSE(offenseid)", "Returns true if event belongs to specified offense"),
        "OFFENSE_TIME": ("OFFENSE_TIME(offenseid)", "Limits query to offense timeframe"),
    }

    # Comparison operators
    COMPARISON_OPS = {
        "=": "Equal to",
        "!=": "Not equal to",
        "<>": "Not equal to (alternate)",
        "<": "Less than",
        ">": "Greater than",
        "<=": "Less than or equal to",
        ">=": "Greater than or equal to",
        "BETWEEN": "Between two values. Syntax: field BETWEEN value1 AND value2",
        "IN": "In a list of values. Syntax: field IN (value1, value2, ...)",
        "IS NULL": "Is null value",
        "IS NOT NULL": "Is not null value",
    }

    # String operators
    STRING_OPS = {
        "LIKE": "Pattern matching (case-sensitive). Wildcards: % (any chars), _ (single char)",
        "ILIKE": "Pattern matching (case-insensitive). Same wildcards as LIKE",
        "MATCHES": "Regular expression matching (case-sensitive)",
        "IMATCHES": "Regular expression matching (case-insensitive)",
    }

    # Logical operators
    LOGICAL_OPS = {
        "AND": "Both conditions must be true",
        "OR": "Either condition must be true",
        "NOT": "Negates the condition",
    }

    # Time clause examples
    TIME_CLAUSES = {
        "LAST": [
            ("LAST 5 MINUTES", "Last 5 minutes"),
            ("LAST 1 HOURS", "Last 1 hour"),
            ("LAST 24 HOURS", "Last 24 hours"),
            ("LAST 7 DAYS", "Last 7 days"),
            ("LAST 30 DAYS", "Last 30 days"),
        ],
        "START/STOP": [
            ("START '2024-01-01 00:00' STOP '2024-01-02 00:00'", "Specific date range"),
            ("START '2024-01-01 09:00:00' STOP '2024-01-01 17:00:00'", "Specific time range"),
        ],
        "PARSEDATETIME": [
            ("START PARSEDATETIME('1 hour ago') STOP PARSEDATETIME('now')", "Dynamic time range"),
            ("START PARSEDATETIME('1 day ago')", "From 1 day ago to now"),
        ],
    }

    def _print_table(self, headers: list, rows: list, col_widths: list = None):
        """Print a formatted table."""
        if col_widths is None:
            col_widths = [max(len(str(row[i])) for row in [headers] + rows) + 2 for i in range(len(headers))]

        # Header
        header_line = "".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_line)
        print("-" * sum(col_widths))

        # Rows
        for row in rows:
            line = "".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
            print(line)

    def show_fields(self):
        """Display field reference."""
        print("\033[2J\033[H", end="")
        print("=" * 70)
        print("                    AQL FIELD REFERENCE")
        print("=" * 70)
        print("\n1. Event Fields")
        print("2. Flow Fields")
        print("3. Back to main menu")
        print()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            self._show_event_fields()
        elif choice == "2":
            self._show_flow_fields()

    def _show_event_fields(self):
        """Display event fields."""
        print("\033[2J\033[H", end="")
        print("=" * 80)
        print("                         EVENT FIELDS")
        print("=" * 80)
        print()

        categories = {
            "Network": ["sourceip", "destinationip", "sourceport", "destinationport",
                       "sourcemac", "destinationmac", "protocolid", "sourcev6", "destinationv6"],
            "Identity": ["username", "identityip", "identityhostname"],
            "Time": ["starttime", "endtime", "devicetime"],
            "Event Info": ["qid", "qidEventId", "category", "logsourceid", "devicetype",
                          "eventcount", "magnitude", "severity", "credibility", "relevance"],
            "Payload": ["payload", "utf8payload"],
            "Geographic": ["sourcegeographiclocation", "destinationgeographiclocation"],
            "Processing": ["processorid", "collectorid", "domainid", "ruleid", "hasoffense"],
        }

        for cat_name, fields in categories.items():
            print(f"\n{cat_name.upper()}")
            print("-" * 70)
            for field in fields:
                if field in self.EVENT_FIELDS:
                    ftype, desc = self.EVENT_FIELDS[field]
                    print(f"  {field:<35} {ftype:<12} {desc}")

        input("\n\nPress Enter to continue...")

    def _show_flow_fields(self):
        """Display flow fields."""
        print("\033[2J\033[H", end="")
        print("=" * 80)
        print("                          FLOW FIELDS")
        print("=" * 80)
        print()

        categories = {
            "Traffic Volume": ["sourcebytes", "destinationbytes", "sourcepackets",
                              "destinationpackets", "totalbytes", "totalpackets"],
            "Network": ["sourceip", "destinationip", "sourceport", "destinationport", "protocolid"],
            "Application": ["applicationid", "applicationname"],
            "ASN": ["sourceasn", "destinationasn"],
            "Payload": ["sourcepayload", "destinationpayload"],
            "Time": ["starttime", "endtime", "firstpackettime", "lastpackettime"],
            "Geographic": ["sourcegeographiclocation", "destinationgeographiclocation"],
            "Processing": ["flowdirection", "flowsourceid", "processorid", "domainid"],
        }

        for cat_name, fields in categories.items():
            print(f"\n{cat_name.upper()}")
            print("-" * 70)
            for field in fields:
                if field in self.FLOW_FIELDS:
                    ftype, desc = self.FLOW_FIELDS[field]
                    print(f"  {field:<35} {ftype:<12} {desc}")

        input("\n\nPress Enter to continue...")

    def show_functions(self):
        """Display function reference."""
        print("\033[2J\033[H", end="")
        print("=" * 80)
        print("                      AQL FUNCTION REFERENCE")
        print("=" * 80)
        print("""
1. Calculation & Formatting Functions
2. Aggregation Functions
3. Data Retrieval Functions
4. Geographic Functions
5. Reference Data Functions
6. Filter Functions
7. Back to main menu
""")

        choice = input("Enter choice: ").strip()

        func_map = {
            "1": ("CALCULATION & FORMATTING", self.CALC_FUNCTIONS),
            "2": ("AGGREGATION", self.AGG_FUNCTIONS),
            "3": ("DATA RETRIEVAL", self.RETRIEVAL_FUNCTIONS),
            "4": ("GEOGRAPHIC", self.GEO_FUNCTIONS),
            "5": ("REFERENCE DATA", self.REFERENCE_FUNCTIONS),
            "6": ("FILTER", self.FILTER_FUNCTIONS),
        }

        if choice in func_map:
            title, functions = func_map[choice]
            self._show_function_category(title, functions)

    def _show_function_category(self, title: str, functions: dict):
        """Display a category of functions."""
        print("\033[2J\033[H", end="")
        print("=" * 90)
        print(f"                    {title} FUNCTIONS")
        print("=" * 90)
        print()

        for name, (syntax, desc) in functions.items():
            print(f"  {name}")
            print(f"    Syntax: {syntax}")
            print(f"    {desc}")
            print()

        input("\nPress Enter to continue...")

    def show_operators(self):
        """Display operator reference."""
        print("\033[2J\033[H", end="")
        print("=" * 80)
        print("                      AQL OPERATOR REFERENCE")
        print("=" * 80)

        print("\nCOMPARISON OPERATORS")
        print("-" * 60)
        for op, desc in self.COMPARISON_OPS.items():
            print(f"  {op:<15} {desc}")

        print("\n\nSTRING OPERATORS")
        print("-" * 60)
        for op, desc in self.STRING_OPS.items():
            print(f"  {op:<15} {desc}")

        print("\n\nLOGICAL OPERATORS")
        print("-" * 60)
        for op, desc in self.LOGICAL_OPS.items():
            print(f"  {op:<15} {desc}")

        print("\n\nEXAMPLES:")
        print("-" * 60)
        print("  WHERE sourceip = '192.168.1.1'")
        print("  WHERE magnitude >= 7 AND severity > 5")
        print("  WHERE username LIKE 'admin%'")
        print("  WHERE payload ILIKE '%error%'")
        print("  WHERE sourceip MATCHES '192\\.168\\..*'")
        print("  WHERE sourceport IN (22, 23, 3389)")
        print("  WHERE eventcount BETWEEN 10 AND 100")
        print("  WHERE username IS NOT NULL")

        input("\n\nPress Enter to continue...")

    def show_time_clauses(self):
        """Display time clause reference."""
        print("\033[2J\033[H", end="")
        print("=" * 80)
        print("                      AQL TIME CLAUSES")
        print("=" * 80)

        print("\nLAST CLAUSE (Relative Time)")
        print("-" * 60)
        print("  Syntax: LAST <number> <unit>")
        print("  Units: MINUTES, HOURS, DAYS")
        print()
        for example, desc in self.TIME_CLAUSES["LAST"]:
            print(f"  {example:<40} # {desc}")

        print("\n\nSTART/STOP CLAUSE (Absolute Time)")
        print("-" * 60)
        print("  Syntax: START '<datetime>' [STOP '<datetime>']")
        print("  Format: yyyy-MM-dd HH:mm or yyyy-MM-dd HH:mm:ss")
        print("  Note: STOP is optional (defaults to now)")
        print()
        for example, desc in self.TIME_CLAUSES["START/STOP"]:
            print(f"  {example}")
            print(f"    # {desc}")
            print()

        print("\nPARSEDATETIME (Dynamic Time)")
        print("-" * 60)
        print("  Syntax: START PARSEDATETIME('time reference')")
        print("  References: 'now', '1 hour ago', '1 day ago', etc.")
        print()
        for example, desc in self.TIME_CLAUSES["PARSEDATETIME"]:
            print(f"  {example}")
            print(f"    # {desc}")
            print()

        print("\nIMPORTANT NOTES:")
        print("-" * 60)
        print("  - Time clauses must come AFTER LIMIT clause if both are used")
        print("  - Example: SELECT * FROM events LIMIT 100 LAST 1 HOURS")

        input("\n\nPress Enter to continue...")

    def get_all_event_fields(self) -> list:
        """Return list of all event field names."""
        return list(self.EVENT_FIELDS.keys())

    def get_all_flow_fields(self) -> list:
        """Return list of all flow field names."""
        return list(self.FLOW_FIELDS.keys())

    def get_all_functions(self) -> dict:
        """Return all functions merged."""
        all_funcs = {}
        all_funcs.update(self.CALC_FUNCTIONS)
        all_funcs.update(self.AGG_FUNCTIONS)
        all_funcs.update(self.RETRIEVAL_FUNCTIONS)
        all_funcs.update(self.GEO_FUNCTIONS)
        all_funcs.update(self.REFERENCE_FUNCTIONS)
        all_funcs.update(self.FILTER_FUNCTIONS)
        return all_funcs
