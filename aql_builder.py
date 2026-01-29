#!/usr/bin/env python3
"""
AQL Builder - An intuitive tool for creating IBM QRadar AQL queries
"""

import sys
from typing import Optional
from aql_reference import AQLReference
from query_builder import QueryBuilder
from templates import QueryTemplates

class AQLBuilder:
    """Main AQL Builder application."""

    def __init__(self):
        self.reference = AQLReference()
        self.builder = QueryBuilder()
        self.templates = QueryTemplates()

    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")

    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("           AQL BUILDER - QRadar Query Helper")
        print("=" * 60)
        print()

    def print_menu(self):
        """Print the main menu."""
        print("MAIN MENU")
        print("-" * 40)
        print("  1. Build a new query (step-by-step)")
        print("  2. Query templates (pre-built queries)")
        print("  3. Reference - Fields")
        print("  4. Reference - Functions")
        print("  5. Reference - Operators")
        print("  6. Reference - Time clauses")
        print("  7. Quick query (free-form with hints)")
        print("  8. Validate a query")
        print("  9. Help / AQL Syntax Guide")
        print("  0. Exit")
        print("-" * 40)

    def get_choice(self, prompt: str = "Enter choice: ", valid: Optional[list] = None) -> str:
        """Get user input with optional validation."""
        while True:
            try:
                choice = input(prompt).strip()
                if valid is None or choice in valid:
                    return choice
                print(f"  Invalid choice. Please enter one of: {', '.join(valid)}")
            except (KeyboardInterrupt, EOFError):
                print("\n")
                return "0"

    def show_help(self):
        """Display AQL syntax help."""
        self.clear_screen()
        self.print_header()
        print("AQL SYNTAX GUIDE")
        print("=" * 60)
        print("""
BASIC QUERY STRUCTURE:
  SELECT <columns>
  FROM <table>
  [WHERE <conditions>]
  [GROUP BY <columns>]
  [HAVING <conditions>]
  [ORDER BY <columns> [ASC|DESC]]
  [LIMIT <number>]
  [LAST <time> | START '<datetime>' STOP '<datetime>']

TABLES:
  - events    : Security events
  - flows     : Network flow data

EXAMPLES:
  1. Simple query:
     SELECT * FROM events LAST 1 HOURS

  2. Filter by IP:
     SELECT sourceip, destinationip, username
     FROM events
     WHERE sourceip = '192.168.1.1'
     LAST 24 HOURS

  3. Aggregation:
     SELECT sourceip, COUNT(*) as count
     FROM events
     GROUP BY sourceip
     ORDER BY count DESC
     LIMIT 10
     LAST 7 DAYS

  4. Using functions:
     SELECT LOGSOURCENAME(logsourceid), QIDNAME(qid), sourceip
     FROM events
     WHERE magnitude > 5
     LAST 1 HOURS

TIPS:
  - Use single quotes for strings: WHERE username = 'admin'
  - Use double quotes for column aliases: AS "My Column"
  - Field names are case-sensitive
  - Keywords (SELECT, FROM, etc.) are NOT case-sensitive
  - Use ILIKE for case-insensitive matching
  - Use IMATCHES for case-insensitive regex
""")
        input("\nPress Enter to continue...")

    def run(self):
        """Run the main application loop."""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()

            choice = self.get_choice(valid=[str(i) for i in range(10)])

            if choice == "0":
                print("\nGoodbye!")
                break
            elif choice == "1":
                self.builder.interactive_build()
            elif choice == "2":
                self.templates.show_templates()
            elif choice == "3":
                self.reference.show_fields()
            elif choice == "4":
                self.reference.show_functions()
            elif choice == "5":
                self.reference.show_operators()
            elif choice == "6":
                self.reference.show_time_clauses()
            elif choice == "7":
                self.builder.quick_query()
            elif choice == "8":
                self.builder.validate_query()
            elif choice == "9":
                self.show_help()


def main():
    """Main entry point."""
    app = AQLBuilder()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
