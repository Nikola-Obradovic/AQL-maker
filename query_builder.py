#!/usr/bin/env python3
"""
Query Builder - Interactive step-by-step AQL query construction
"""

import re
from typing import Optional, List, Dict
from aql_reference import AQLReference


class QueryBuilder:
    """Interactive AQL query builder."""

    def __init__(self):
        self.reference = AQLReference()
        self.query_parts = {}
        self.reset()

    def reset(self):
        """Reset query parts."""
        self.query_parts = {
            "select": [],
            "from": "events",
            "where": [],
            "group_by": [],
            "having": [],
            "order_by": [],
            "order_dir": "DESC",
            "limit": None,
            "time": None,
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")

    def print_current_query(self):
        """Print the current query being built."""
        print("\n" + "=" * 60)
        print("CURRENT QUERY:")
        print("-" * 60)
        query = self.build_query()
        if query:
            # Format for readability
            formatted = self._format_query(query)
            print(formatted)
        else:
            print("  (empty)")
        print("=" * 60 + "\n")

    def _format_query(self, query: str) -> str:
        """Format query for display."""
        # Add newlines before major clauses
        clauses = ["FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT", "LAST", "START"]
        formatted = query
        for clause in clauses:
            formatted = formatted.replace(f" {clause} ", f"\n{clause} ")
        return formatted

    def build_query(self) -> str:
        """Build the query string from parts."""
        parts = []

        # SELECT
        if self.query_parts["select"]:
            cols = ", ".join(self.query_parts["select"])
            parts.append(f"SELECT {cols}")
        else:
            parts.append("SELECT *")

        # FROM
        parts.append(f"FROM {self.query_parts['from']}")

        # WHERE
        if self.query_parts["where"]:
            conditions = " AND ".join(self.query_parts["where"])
            parts.append(f"WHERE {conditions}")

        # GROUP BY
        if self.query_parts["group_by"]:
            cols = ", ".join(self.query_parts["group_by"])
            parts.append(f"GROUP BY {cols}")

        # HAVING
        if self.query_parts["having"]:
            conditions = " AND ".join(self.query_parts["having"])
            parts.append(f"HAVING {conditions}")

        # ORDER BY
        if self.query_parts["order_by"]:
            cols = ", ".join(self.query_parts["order_by"])
            parts.append(f"ORDER BY {cols} {self.query_parts['order_dir']}")

        # LIMIT
        if self.query_parts["limit"]:
            parts.append(f"LIMIT {self.query_parts['limit']}")

        # TIME
        if self.query_parts["time"]:
            parts.append(self.query_parts["time"])

        return " ".join(parts)

    def interactive_build(self):
        """Interactive step-by-step query builder."""
        self.reset()

        while True:
            self.clear_screen()
            print("=" * 60)
            print("          INTERACTIVE QUERY BUILDER")
            print("=" * 60)
            self.print_current_query()

            print("BUILD OPTIONS:")
            print("-" * 40)
            print("  1. Set SELECT columns")
            print("  2. Set FROM table (events/flows)")
            print("  3. Add WHERE condition")
            print("  4. Add GROUP BY columns")
            print("  5. Add HAVING condition")
            print("  6. Set ORDER BY")
            print("  7. Set LIMIT")
            print("  8. Set TIME clause")
            print("  9. Clear and restart")
            print("  -" * 20)
            print("  c. Copy query to clipboard")
            print("  f. Finish and display query")
            print("  q. Back to main menu")
            print("-" * 40)

            choice = input("Enter choice: ").strip().lower()

            if choice == "q":
                break
            elif choice == "1":
                self._build_select()
            elif choice == "2":
                self._build_from()
            elif choice == "3":
                self._build_where()
            elif choice == "4":
                self._build_group_by()
            elif choice == "5":
                self._build_having()
            elif choice == "6":
                self._build_order_by()
            elif choice == "7":
                self._build_limit()
            elif choice == "8":
                self._build_time()
            elif choice == "9":
                self.reset()
                print("\n  Query cleared!")
                input("  Press Enter to continue...")
            elif choice == "c":
                self._copy_to_clipboard()
            elif choice == "f":
                self._finish_query()

    def _build_select(self):
        """Build SELECT clause."""
        self.clear_screen()
        print("=" * 60)
        print("SELECT COLUMNS")
        print("=" * 60)

        table = self.query_parts["from"]
        if table == "events":
            fields = self.reference.get_all_event_fields()
        else:
            fields = self.reference.get_all_flow_fields()

        print(f"\nAvailable fields for {table}:")
        print("-" * 40)

        # Show fields in columns
        for i, field in enumerate(fields):
            print(f"  {field:<30}", end="")
            if (i + 1) % 2 == 0:
                print()
        print()

        print("\nCOMMON FUNCTIONS:")
        print("  LOGSOURCENAME(logsourceid), QIDNAME(qid), CATEGORYNAME(category)")
        print("  DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm:ss'), COUNT(*), SUM(field)")

        print("\n" + "-" * 60)
        print("Enter columns separated by commas, or:")
        print("  * for all columns")
        print("  Press Enter to keep current selection")
        print("-" * 60)

        current = ", ".join(self.query_parts["select"]) if self.query_parts["select"] else "*"
        print(f"Current: {current}\n")

        inp = input("Columns: ").strip()

        if inp:
            if inp == "*":
                self.query_parts["select"] = []
            else:
                # Parse columns
                columns = [c.strip() for c in inp.split(",")]
                self.query_parts["select"] = columns

    def _build_from(self):
        """Build FROM clause."""
        self.clear_screen()
        print("=" * 60)
        print("SELECT TABLE")
        print("=" * 60)
        print("\nAvailable tables:")
        print("  1. events - Security events from log sources")
        print("  2. flows  - Network flow data")
        print(f"\nCurrent: {self.query_parts['from']}")
        print()

        choice = input("Enter 1 or 2 (or press Enter to keep current): ").strip()

        if choice == "1":
            self.query_parts["from"] = "events"
        elif choice == "2":
            self.query_parts["from"] = "flows"

    def _build_where(self):
        """Build WHERE clause."""
        self.clear_screen()
        print("=" * 60)
        print("WHERE CONDITIONS")
        print("=" * 60)

        print("\nCurrent conditions:")
        if self.query_parts["where"]:
            for i, cond in enumerate(self.query_parts["where"], 1):
                print(f"  {i}. {cond}")
        else:
            print("  (none)")

        print("\n" + "-" * 60)
        print("OPTIONS:")
        print("  1. Add new condition")
        print("  2. Remove a condition")
        print("  3. Clear all conditions")
        print("  4. Back")
        print("-" * 60)

        choice = input("Choice: ").strip()

        if choice == "1":
            self._add_where_condition()
        elif choice == "2":
            self._remove_condition(self.query_parts["where"])
        elif choice == "3":
            self.query_parts["where"] = []
            print("\n  All conditions cleared!")
            input("  Press Enter to continue...")

    def _add_where_condition(self):
        """Add a WHERE condition."""
        self.clear_screen()
        print("=" * 60)
        print("ADD WHERE CONDITION")
        print("=" * 60)

        print("\nCOMMON PATTERNS:")
        print("-" * 60)
        print("  IP matching:       sourceip = '192.168.1.1'")
        print("  CIDR range:        INCIDR('192.168.0.0/16', sourceip)")
        print("  String equals:     username = 'admin'")
        print("  Pattern match:     payload ILIKE '%error%'")
        print("  Regex match:       username IMATCHES '.*admin.*'")
        print("  Numeric compare:   magnitude >= 7")
        print("  Range:             eventcount BETWEEN 10 AND 100")
        print("  List:              sourceport IN (22, 23, 3389)")
        print("  Null check:        username IS NOT NULL")
        print("  Log source:        LOGSOURCENAME(logsourceid) ILIKE '%Windows%'")
        print("  Event name:        QIDNAME(qid) ILIKE '%login%'")
        print("-" * 60)

        print("\nQuick add (enter number):")
        print("  1. Filter by source IP")
        print("  2. Filter by destination IP")
        print("  3. Filter by username")
        print("  4. Filter by magnitude")
        print("  5. Filter by log source")
        print("  6. Filter by event name (QID)")
        print("  7. Custom condition")

        choice = input("\nChoice: ").strip()

        condition = None

        if choice == "1":
            ip = input("Enter source IP (or CIDR): ").strip()
            if "/" in ip:
                condition = f"INCIDR('{ip}', sourceip)"
            else:
                condition = f"sourceip = '{ip}'"
        elif choice == "2":
            ip = input("Enter destination IP (or CIDR): ").strip()
            if "/" in ip:
                condition = f"INCIDR('{ip}', destinationip)"
            else:
                condition = f"destinationip = '{ip}'"
        elif choice == "3":
            user = input("Enter username (use % for wildcard): ").strip()
            if "%" in user:
                condition = f"username ILIKE '{user}'"
            else:
                condition = f"username = '{user}'"
        elif choice == "4":
            print("  Operators: = != < > <= >=")
            op = input("  Operator: ").strip() or ">="
            val = input("  Value (1-10): ").strip() or "5"
            condition = f"magnitude {op} {val}"
        elif choice == "5":
            name = input("Enter log source name pattern (use % for wildcard): ").strip()
            condition = f"LOGSOURCENAME(logsourceid) ILIKE '%{name}%'"
        elif choice == "6":
            name = input("Enter event name pattern (use % for wildcard): ").strip()
            condition = f"QIDNAME(qid) ILIKE '%{name}%'"
        elif choice == "7":
            condition = input("Enter custom condition: ").strip()

        if condition:
            self.query_parts["where"].append(condition)
            print(f"\n  Added: {condition}")
            input("  Press Enter to continue...")

    def _remove_condition(self, conditions: list):
        """Remove a condition from a list."""
        if not conditions:
            print("\n  No conditions to remove!")
            input("  Press Enter to continue...")
            return

        print("\nEnter number to remove (or press Enter to cancel): ")
        try:
            idx = input("Number: ").strip()
            if idx:
                idx = int(idx) - 1
                if 0 <= idx < len(conditions):
                    removed = conditions.pop(idx)
                    print(f"\n  Removed: {removed}")
                else:
                    print("\n  Invalid number!")
        except ValueError:
            print("\n  Invalid input!")

        input("  Press Enter to continue...")

    def _build_group_by(self):
        """Build GROUP BY clause."""
        self.clear_screen()
        print("=" * 60)
        print("GROUP BY")
        print("=" * 60)

        print("\nCurrent GROUP BY columns:")
        if self.query_parts["group_by"]:
            print("  " + ", ".join(self.query_parts["group_by"]))
        else:
            print("  (none)")

        print("\n" + "-" * 60)
        print("When using GROUP BY, use aggregation functions in SELECT:")
        print("  COUNT(*), SUM(field), AVG(field), MIN(field), MAX(field)")
        print()
        print("Example SELECT with GROUP BY:")
        print("  SELECT sourceip, COUNT(*) as count, SUM(eventcount)")
        print("-" * 60)

        print("\nEnter columns to group by (comma-separated)")
        print("Or press Enter to keep current:")

        inp = input("\nColumns: ").strip()

        if inp:
            columns = [c.strip() for c in inp.split(",")]
            self.query_parts["group_by"] = columns

    def _build_having(self):
        """Build HAVING clause."""
        self.clear_screen()
        print("=" * 60)
        print("HAVING (filter on aggregated results)")
        print("=" * 60)

        print("\nCurrent HAVING conditions:")
        if self.query_parts["having"]:
            for i, cond in enumerate(self.query_parts["having"], 1):
                print(f"  {i}. {cond}")
        else:
            print("  (none)")

        print("\n" + "-" * 60)
        print("HAVING is used to filter results after GROUP BY")
        print("Example: HAVING COUNT(*) > 10")
        print("-" * 60)

        print("\nOPTIONS:")
        print("  1. Add new HAVING condition")
        print("  2. Remove a condition")
        print("  3. Clear all")
        print("  4. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            cond = input("\nEnter HAVING condition: ").strip()
            if cond:
                self.query_parts["having"].append(cond)
        elif choice == "2":
            self._remove_condition(self.query_parts["having"])
        elif choice == "3":
            self.query_parts["having"] = []

    def _build_order_by(self):
        """Build ORDER BY clause."""
        self.clear_screen()
        print("=" * 60)
        print("ORDER BY")
        print("=" * 60)

        print("\nCurrent ORDER BY:")
        if self.query_parts["order_by"]:
            cols = ", ".join(self.query_parts["order_by"])
            print(f"  {cols} {self.query_parts['order_dir']}")
        else:
            print("  (none)")

        print("\n" + "-" * 60)
        print("Common ORDER BY columns:")
        print("  starttime, magnitude, eventcount, sourceip")
        print("  Or use aggregates: COUNT(*), SUM(eventcount)")
        print("-" * 60)

        inp = input("\nEnter column(s) to order by (comma-separated): ").strip()

        if inp:
            columns = [c.strip() for c in inp.split(",")]
            self.query_parts["order_by"] = columns

            print("\nDirection:")
            print("  1. DESC (descending - highest first)")
            print("  2. ASC (ascending - lowest first)")
            direction = input("Choice (default DESC): ").strip()
            self.query_parts["order_dir"] = "ASC" if direction == "2" else "DESC"

    def _build_limit(self):
        """Build LIMIT clause."""
        self.clear_screen()
        print("=" * 60)
        print("LIMIT")
        print("=" * 60)

        current = self.query_parts["limit"] or "(none)"
        print(f"\nCurrent LIMIT: {current}")

        print("\nEnter maximum number of results (or press Enter to clear):")
        inp = input("Limit: ").strip()

        if inp:
            try:
                self.query_parts["limit"] = int(inp)
            except ValueError:
                print("  Invalid number!")
                input("  Press Enter to continue...")
        else:
            self.query_parts["limit"] = None

    def _build_time(self):
        """Build time clause."""
        self.clear_screen()
        print("=" * 60)
        print("TIME CLAUSE")
        print("=" * 60)

        current = self.query_parts["time"] or "(none)"
        print(f"\nCurrent time clause: {current}")

        print("\n" + "-" * 60)
        print("OPTIONS:")
        print("  1. LAST (relative time)")
        print("  2. START/STOP (specific date range)")
        print("  3. Clear time clause")
        print("  4. Back")
        print("-" * 60)

        choice = input("\nChoice: ").strip()

        if choice == "1":
            print("\nExamples: 5 MINUTES, 1 HOURS, 24 HOURS, 7 DAYS")
            amount = input("Enter time amount: ").strip() or "1"
            print("Units: 1=MINUTES, 2=HOURS, 3=DAYS")
            unit_choice = input("Unit: ").strip()
            units = {"1": "MINUTES", "2": "HOURS", "3": "DAYS"}
            unit = units.get(unit_choice, "HOURS")
            self.query_parts["time"] = f"LAST {amount} {unit}"

        elif choice == "2":
            print("\nFormat: yyyy-MM-dd HH:mm or yyyy-MM-dd HH:mm:ss")
            start = input("Start datetime: ").strip()
            stop = input("Stop datetime (leave empty for now): ").strip()
            if start:
                if stop:
                    self.query_parts["time"] = f"START '{start}' STOP '{stop}'"
                else:
                    self.query_parts["time"] = f"START '{start}'"

        elif choice == "3":
            self.query_parts["time"] = None

    def _copy_to_clipboard(self):
        """Copy query to clipboard."""
        query = self.build_query()
        try:
            import subprocess
            # Try xclip first (Linux)
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                                          stdin=subprocess.PIPE)
                process.communicate(query.encode())
                print("\n  Query copied to clipboard!")
            except FileNotFoundError:
                # Try xsel
                try:
                    process = subprocess.Popen(['xsel', '--clipboard', '--input'],
                                              stdin=subprocess.PIPE)
                    process.communicate(query.encode())
                    print("\n  Query copied to clipboard!")
                except FileNotFoundError:
                    print("\n  Clipboard tools not available (install xclip or xsel)")
                    print(f"  Query: {query}")
        except Exception as e:
            print(f"\n  Could not copy to clipboard: {e}")
            print(f"  Query: {query}")

        input("  Press Enter to continue...")

    def _finish_query(self):
        """Display final query."""
        self.clear_screen()
        print("=" * 60)
        print("FINAL QUERY")
        print("=" * 60)

        query = self.build_query()
        formatted = self._format_query(query)

        print("\nFormatted:")
        print("-" * 60)
        print(formatted)
        print("-" * 60)

        print("\nSingle line:")
        print("-" * 60)
        print(query)
        print("-" * 60)

        print("\n[c] Copy to clipboard")
        print("[Enter] Continue building")
        print("[q] Back to main menu")

        choice = input("\nChoice: ").strip().lower()
        if choice == "c":
            self._copy_to_clipboard()
        elif choice == "q":
            return True
        return False

    def quick_query(self):
        """Quick query mode with hints."""
        self.clear_screen()
        print("=" * 60)
        print("QUICK QUERY MODE")
        print("=" * 60)

        print("""
Enter your AQL query directly. Press Enter twice to finish.

QUICK REFERENCE:
  SELECT * FROM events WHERE <condition> LAST <time>
  SELECT * FROM flows WHERE <condition> LAST <time>

COMMON FIELDS:
  events: sourceip, destinationip, username, magnitude, payload, qid
  flows:  sourceip, destinationip, sourcebytes, destinationbytes

COMMON FUNCTIONS:
  LOGSOURCENAME(logsourceid), QIDNAME(qid), CATEGORYNAME(category)
  COUNT(*), SUM(), AVG(), DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm')

OPERATORS:
  = != < > <= >=  |  LIKE ILIKE MATCHES IMATCHES  |  AND OR NOT
  IN (val1, val2)  |  BETWEEN x AND y  |  IS NULL  |  IS NOT NULL

TIME:
  LAST 1 HOURS  |  LAST 24 HOURS  |  LAST 7 DAYS
  START '2024-01-01 00:00' STOP '2024-01-02 00:00'
""")

        print("Enter query (press Enter twice when done):")
        print("-" * 60)

        lines = []
        empty_count = 0
        while empty_count < 1:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)

        query = " ".join(lines)

        if query.strip():
            print("\n" + "-" * 60)
            print("Your query:")
            print(query)
            print("-" * 60)

            errors = self._validate_query(query)
            if errors:
                print("\nPotential issues found:")
                for err in errors:
                    print(f"  - {err}")
            else:
                print("\nQuery looks valid!")

            print("\n[c] Copy to clipboard")
            choice = input("[Enter] Continue: ").strip().lower()
            if choice == "c":
                self._copy_to_clipboard_direct(query)

    def _copy_to_clipboard_direct(self, query: str):
        """Copy specific query to clipboard."""
        try:
            import subprocess
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                                          stdin=subprocess.PIPE)
                process.communicate(query.encode())
                print("  Query copied to clipboard!")
            except FileNotFoundError:
                try:
                    process = subprocess.Popen(['xsel', '--clipboard', '--input'],
                                              stdin=subprocess.PIPE)
                    process.communicate(query.encode())
                    print("  Query copied to clipboard!")
                except FileNotFoundError:
                    print("  Clipboard tools not available")
        except Exception:
            pass

    def validate_query(self):
        """Validate a query entered by user."""
        self.clear_screen()
        print("=" * 60)
        print("QUERY VALIDATOR")
        print("=" * 60)

        print("\nEnter your AQL query to validate (Enter twice when done):")
        print("-" * 60)

        lines = []
        empty_count = 0
        while empty_count < 1:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)

        query = " ".join(lines)

        if query.strip():
            errors = self._validate_query(query)

            print("\n" + "=" * 60)
            print("VALIDATION RESULTS")
            print("=" * 60)

            if errors:
                print("\nIssues found:")
                for err in errors:
                    print(f"  ! {err}")
            else:
                print("\n  Query appears to be valid!")

            print("\n" + "-" * 60)
            print("Note: This validates syntax only. Runtime errors may still occur.")
            print("-" * 60)

        input("\nPress Enter to continue...")

    def _validate_query(self, query: str) -> List[str]:
        """Validate AQL query and return list of errors."""
        errors = []
        query_upper = query.upper()

        # Check for SELECT
        if not query_upper.strip().startswith("SELECT"):
            errors.append("Query should start with SELECT")

        # Check for FROM
        if "FROM" not in query_upper:
            errors.append("Query is missing FROM clause")
        else:
            # Check table name
            from_match = re.search(r"FROM\s+(\w+)", query_upper)
            if from_match:
                table = from_match.group(1)
                if table not in ["EVENTS", "FLOWS"]:
                    errors.append(f"Unknown table '{table}'. Use 'events' or 'flows'")

        # Check for common syntax errors
        if "WHERE" in query_upper:
            # Check for = vs == (common mistake)
            if "==" in query:
                errors.append("Use single '=' for equality, not '=='")

            # Check for unmatched quotes
            single_quotes = query.count("'")
            if single_quotes % 2 != 0:
                errors.append("Unmatched single quotes detected")

        # Check LIKE/ILIKE usage
        if "LIKE" in query_upper and "%" not in query:
            errors.append("LIKE clause usually requires % wildcard")

        # Check time clause
        has_time = any(kw in query_upper for kw in ["LAST", "START", "STOP"])
        if not has_time:
            errors.append("Consider adding a time clause (LAST, START/STOP)")

        # Check ORDER BY before LIMIT
        if "LIMIT" in query_upper and "ORDER BY" in query_upper:
            limit_pos = query_upper.find("LIMIT")
            order_pos = query_upper.find("ORDER BY")
            if limit_pos < order_pos:
                errors.append("ORDER BY should come before LIMIT")

        # Check time clause position
        if "LIMIT" in query_upper and "LAST" in query_upper:
            limit_pos = query_upper.find("LIMIT")
            last_pos = query_upper.find("LAST")
            if last_pos < limit_pos:
                errors.append("LIMIT should come before time clause (LAST)")

        # Check for GROUP BY with aggregation
        if "GROUP BY" in query_upper:
            agg_funcs = ["COUNT(", "SUM(", "AVG(", "MIN(", "MAX(", "UNIQUECOUNT("]
            has_agg = any(func in query_upper for func in agg_funcs)
            if not has_agg:
                errors.append("GROUP BY is typically used with aggregate functions (COUNT, SUM, etc.)")

        return errors
