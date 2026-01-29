#!/usr/bin/env python3
"""
Query Templates - Pre-built AQL queries for common use cases
"""

from typing import Dict, List, Tuple


class QueryTemplates:
    """Pre-built AQL query templates."""

    CATEGORIES = {
        "Authentication & Access": [
            {
                "name": "Failed Login Attempts",
                "description": "Find failed authentication attempts",
                "query": """SELECT sourceip, username, COUNT(*) as attempts,
LOGSOURCENAME(logsourceid) as logsource
FROM events
WHERE QIDNAME(qid) ILIKE '%fail%login%'
   OR QIDNAME(qid) ILIKE '%authentication%fail%'
GROUP BY sourceip, username
ORDER BY attempts DESC
LIMIT 100
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Successful Logins from Multiple IPs",
                "description": "Users logging in from multiple source IPs",
                "query": """SELECT username, UNIQUECOUNT(sourceip) as unique_ips,
COUNT(*) as login_count
FROM events
WHERE QIDNAME(qid) ILIKE '%success%login%'
  AND username IS NOT NULL
GROUP BY username
HAVING unique_ips > 3
ORDER BY unique_ips DESC
LAST 7 DAYS""",
                "params": ["threshold", "time_range"],
            },
            {
                "name": "After Hours Authentication",
                "description": "Login events outside business hours (customize hours)",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
sourceip, username, QIDNAME(qid) as event
FROM events
WHERE (QIDNAME(qid) ILIKE '%login%' OR QIDNAME(qid) ILIKE '%authentication%')
  AND username IS NOT NULL
ORDER BY starttime DESC
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Privileged Account Activity",
                "description": "Activity by admin/root accounts",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
sourceip, username, QIDNAME(qid) as event,
LOGSOURCENAME(logsourceid) as source
FROM events
WHERE username ILIKE '%admin%'
   OR username ILIKE '%root%'
   OR username ILIKE '%administrator%'
ORDER BY starttime DESC
LIMIT 500
LAST 24 HOURS""",
                "params": ["username_pattern", "time_range"],
            },
        ],

        "Network & Traffic": [
            {
                "name": "Top Talkers by Bytes",
                "description": "Find hosts generating most network traffic",
                "query": """SELECT sourceip,
SUM(sourcebytes + destinationbytes) as total_bytes,
SUM(sourcepackets + destinationpackets) as total_packets,
UNIQUECOUNT(destinationip) as unique_destinations
FROM flows
GROUP BY sourceip
ORDER BY total_bytes DESC
LIMIT 50
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "External RDP Connections",
                "description": "RDP (port 3389) connections from external IPs",
                "query": """SELECT sourceip, destinationip,
DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
SUM(sourcebytes) as bytes
FROM flows
WHERE destinationport = 3389
  AND NOT INCIDR('10.0.0.0/8', sourceip)
  AND NOT INCIDR('172.16.0.0/12', sourceip)
  AND NOT INCIDR('192.168.0.0/16', sourceip)
GROUP BY sourceip, destinationip
ORDER BY bytes DESC
LAST 24 HOURS""",
                "params": ["port", "time_range"],
            },
            {
                "name": "SSH Connections",
                "description": "All SSH (port 22) connections",
                "query": """SELECT sourceip, destinationip,
COUNT(*) as connections,
SUM(sourcebytes) as total_bytes
FROM flows
WHERE destinationport = 22
GROUP BY sourceip, destinationip
ORDER BY connections DESC
LIMIT 100
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Suspicious Port Activity",
                "description": "Traffic on commonly exploited ports",
                "query": """SELECT destinationport, sourceip, destinationip,
COUNT(*) as connections
FROM flows
WHERE destinationport IN (4444, 5555, 6666, 1337, 31337, 8080, 8443)
GROUP BY destinationport, sourceip, destinationip
ORDER BY connections DESC
LAST 7 DAYS""",
                "params": ["ports", "time_range"],
            },
            {
                "name": "Large Data Transfers",
                "description": "Connections with high data volume (potential exfiltration)",
                "query": """SELECT sourceip, destinationip, destinationport,
SUM(sourcebytes) as bytes_out,
SUM(destinationbytes) as bytes_in
FROM flows
WHERE sourcebytes > 100000000
GROUP BY sourceip, destinationip, destinationport
ORDER BY bytes_out DESC
LAST 24 HOURS""",
                "params": ["byte_threshold", "time_range"],
            },
        ],

        "Threat Detection": [
            {
                "name": "High Magnitude Events",
                "description": "Events with high magnitude score",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
sourceip, destinationip, username,
QIDNAME(qid) as event_name,
magnitude, severity, credibility,
LOGSOURCENAME(logsourceid) as source
FROM events
WHERE magnitude >= 7
ORDER BY magnitude DESC, starttime DESC
LIMIT 500
LAST 24 HOURS""",
                "params": ["magnitude_threshold", "time_range"],
            },
            {
                "name": "Potential Brute Force",
                "description": "Many failed attempts followed by success from same IP",
                "query": """SELECT sourceip, destinationip, username,
COUNT(*) as total_events,
LOGSOURCENAME(logsourceid) as source
FROM events
WHERE QIDNAME(qid) ILIKE '%fail%'
   OR QIDNAME(qid) ILIKE '%denied%'
GROUP BY sourceip, destinationip, username
HAVING total_events > 50
ORDER BY total_events DESC
LAST 1 HOURS""",
                "params": ["threshold", "time_range"],
            },
            {
                "name": "Living off the Land Binaries (LOLBins)",
                "description": "Detection of suspicious Windows binary execution",
                "query": """SELECT sourceip, destinationip,
UTF8(payload) as command
FROM events
WHERE UTF8(payload) IMATCHES '.*(certutil|bitsadmin|mshta|regsvr32|rundll32|wmic|powershell|cmd)\\.exe.*'
  AND LOGSOURCETYPENAME(devicetype) ILIKE '%Windows%'
GROUP BY sourceip
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Potential DNS Tunneling",
                "description": "Unusually long DNS queries (potential data exfiltration)",
                "query": """SELECT sourceip, destinationip,
COUNT(*) as query_count,
AVG(STRLEN(UTF8(payload))) as avg_query_length
FROM events
WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%DNS%'
  AND STRLEN(UTF8(payload)) > 100
GROUP BY sourceip, destinationip
HAVING query_count > 100
ORDER BY avg_query_length DESC
LAST 24 HOURS""",
                "params": ["length_threshold", "time_range"],
            },
            {
                "name": "Port Scan Detection",
                "description": "Single source connecting to many ports",
                "query": """SELECT sourceip, destinationip,
UNIQUECOUNT(destinationport) as unique_ports,
COUNT(*) as connection_attempts
FROM flows
GROUP BY sourceip, destinationip
HAVING unique_ports > 20
ORDER BY unique_ports DESC
LAST 1 HOURS""",
                "params": ["port_threshold", "time_range"],
            },
        ],

        "System Monitoring": [
            {
                "name": "Events by Log Source",
                "description": "Count events per log source",
                "query": """SELECT LOGSOURCENAME(logsourceid) as log_source,
LOGSOURCETYPENAME(devicetype) as log_type,
COUNT(*) as event_count
FROM events
GROUP BY logsourceid, devicetype
ORDER BY event_count DESC
LIMIT 50
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Events by Category",
                "description": "Event distribution by category",
                "query": """SELECT CATEGORYNAME(category) as category,
COUNT(*) as event_count,
UNIQUECOUNT(sourceip) as unique_sources
FROM events
GROUP BY category
ORDER BY event_count DESC
LIMIT 50
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Payload Size Analysis",
                "description": "Analyze payload sizes by log source",
                "query": """SELECT LOGSOURCETYPENAME(devicetype) AS log_source,
MIN(STRLEN(UTF8(payload))) AS min_size,
MAX(STRLEN(UTF8(payload))) AS max_size,
AVG(STRLEN(UTF8(payload))) AS avg_size,
COUNT(*) AS event_count
FROM events
GROUP BY devicetype
ORDER BY avg_size DESC
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Error Events",
                "description": "Find error and failure events",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
QIDNAME(qid) as event_name,
sourceip, destinationip,
LOGSOURCENAME(logsourceid) as source,
UTF8(payload) as details
FROM events
WHERE QIDNAME(qid) ILIKE '%error%'
   OR QIDNAME(qid) ILIKE '%fail%'
   OR QIDNAME(qid) ILIKE '%denied%'
ORDER BY starttime DESC
LIMIT 200
LAST 24 HOURS""",
                "params": ["time_range"],
            },
        ],

        "Windows Events": [
            {
                "name": "Windows Security Events Overview",
                "description": "Summary of Windows security events",
                "query": """SELECT QIDNAME(qid) as event_name, qid,
COUNT(*) as count
FROM events
WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Windows Security%'
GROUP BY qid
ORDER BY count DESC
LIMIT 100
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Process Creation (Event ID 4688)",
                "description": "New process creation events",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
sourceip, username,
UTF8(payload) as details
FROM events
WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Windows%'
  AND UTF8(payload) ILIKE '%4688%'
ORDER BY starttime DESC
LIMIT 500
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Account Logon Events (4624)",
                "description": "Successful Windows logon events",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
sourceip, username,
LOGSOURCENAME(logsourceid) as source
FROM events
WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Windows%'
  AND UTF8(payload) ILIKE '%4624%'
ORDER BY starttime DESC
LIMIT 500
LAST 24 HOURS""",
                "params": ["time_range"],
            },
            {
                "name": "Account Lockouts (4740)",
                "description": "Windows account lockout events",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
sourceip, username,
LOGSOURCENAME(logsourceid) as source,
COUNT(*) as lockout_count
FROM events
WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Windows%'
  AND UTF8(payload) ILIKE '%4740%'
GROUP BY sourceip, username
ORDER BY lockout_count DESC
LAST 24 HOURS""",
                "params": ["time_range"],
            },
        ],

        "Investigation Queries": [
            {
                "name": "Activity by IP Address",
                "description": "All events for a specific IP",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm:ss') as time,
QIDNAME(qid) as event_name,
sourceip, destinationip, sourceport, destinationport,
username, magnitude,
LOGSOURCENAME(logsourceid) as source
FROM events
WHERE sourceip = '{{IP_ADDRESS}}'
   OR destinationip = '{{IP_ADDRESS}}'
ORDER BY starttime DESC
LIMIT 1000
LAST 7 DAYS""",
                "params": ["ip_address", "time_range"],
            },
            {
                "name": "Activity by Username",
                "description": "All events for a specific user",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm:ss') as time,
QIDNAME(qid) as event_name,
sourceip, destinationip,
LOGSOURCENAME(logsourceid) as source,
magnitude
FROM events
WHERE username ILIKE '{{USERNAME}}'
ORDER BY starttime DESC
LIMIT 1000
LAST 7 DAYS""",
                "params": ["username", "time_range"],
            },
            {
                "name": "Connections Between Two IPs",
                "description": "Traffic between two specific hosts",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm') as time,
sourceip, destinationip,
sourceport, destinationport,
SUM(sourcebytes) as bytes_out,
SUM(destinationbytes) as bytes_in
FROM flows
WHERE (sourceip = '{{SOURCE_IP}}' AND destinationip = '{{DEST_IP}}')
   OR (sourceip = '{{DEST_IP}}' AND destinationip = '{{SOURCE_IP}}')
GROUP BY sourceip, destinationip, sourceport, destinationport
ORDER BY time DESC
LAST 7 DAYS""",
                "params": ["source_ip", "dest_ip", "time_range"],
            },
            {
                "name": "Events in Offense",
                "description": "All events contributing to an offense",
                "query": """SELECT DATEFORMAT(starttime, 'yyyy-MM-dd HH:mm:ss') as time,
QIDNAME(qid) as event_name,
sourceip, destinationip, username,
magnitude, credibility,
LOGSOURCENAME(logsourceid) as source
FROM events
WHERE INOFFENSE({{OFFENSE_ID}})
ORDER BY starttime ASC""",
                "params": ["offense_id"],
            },
        ],
    }

    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")

    def show_templates(self):
        """Display template categories and allow selection."""
        while True:
            self.clear_screen()
            print("=" * 60)
            print("              AQL QUERY TEMPLATES")
            print("=" * 60)
            print()

            categories = list(self.CATEGORIES.keys())
            for i, cat in enumerate(categories, 1):
                count = len(self.CATEGORIES[cat])
                print(f"  {i}. {cat} ({count} queries)")

            print()
            print("  0. Back to main menu")
            print("-" * 60)

            choice = input("\nSelect category: ").strip()

            if choice == "0":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(categories):
                    self._show_category(categories[idx])
            except ValueError:
                pass

    def _show_category(self, category: str):
        """Display templates in a category."""
        while True:
            self.clear_screen()
            print("=" * 60)
            print(f"  {category.upper()}")
            print("=" * 60)
            print()

            templates = self.CATEGORIES[category]
            for i, t in enumerate(templates, 1):
                print(f"  {i}. {t['name']}")
                print(f"     {t['description']}")
                print()

            print("  0. Back")
            print("-" * 60)

            choice = input("\nSelect template: ").strip()

            if choice == "0":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(templates):
                    self._show_template(templates[idx])
            except ValueError:
                pass

    def _show_template(self, template: dict):
        """Display a single template."""
        self.clear_screen()
        print("=" * 70)
        print(f"  {template['name'].upper()}")
        print("=" * 70)
        print()
        print(f"Description: {template['description']}")
        print()
        print("QUERY:")
        print("-" * 70)
        print(template['query'])
        print("-" * 70)

        if template.get('params'):
            print("\nCustomizable parameters:")
            for param in template['params']:
                print(f"  - {param}")

        print("\n" + "-" * 70)
        print("OPTIONS:")
        print("  [c] Copy to clipboard")
        print("  [m] Modify parameters")
        print("  [Enter] Back")
        print("-" * 70)

        choice = input("\nChoice: ").strip().lower()

        if choice == "c":
            self._copy_to_clipboard(template['query'])
        elif choice == "m":
            self._modify_template(template)

    def _modify_template(self, template: dict):
        """Allow user to modify template parameters."""
        query = template['query']

        self.clear_screen()
        print("=" * 60)
        print("MODIFY TEMPLATE")
        print("=" * 60)
        print()
        print("Enter values for placeholders (press Enter to keep default):")
        print()

        # Find placeholders like {{PARAM}}
        import re
        placeholders = re.findall(r'\{\{(\w+)\}\}', query)

        for ph in placeholders:
            value = input(f"  {ph}: ").strip()
            if value:
                query = query.replace(f"{{{{{ph}}}}}", value)

        # Ask about time range
        print("\nModify time range?")
        print("  1. LAST 1 HOURS")
        print("  2. LAST 24 HOURS")
        print("  3. LAST 7 DAYS")
        print("  4. LAST 30 DAYS")
        print("  5. Custom")
        print("  Enter. Keep current")

        time_choice = input("\nChoice: ").strip()

        time_map = {
            "1": "LAST 1 HOURS",
            "2": "LAST 24 HOURS",
            "3": "LAST 7 DAYS",
            "4": "LAST 30 DAYS",
        }

        if time_choice in time_map:
            # Replace existing time clause
            query = re.sub(r'LAST \d+ (MINUTES|HOURS|DAYS)', time_map[time_choice], query)
        elif time_choice == "5":
            custom_time = input("Enter custom time clause: ").strip()
            if custom_time:
                query = re.sub(r'LAST \d+ (MINUTES|HOURS|DAYS)', custom_time, query)

        print("\n" + "-" * 60)
        print("MODIFIED QUERY:")
        print("-" * 60)
        print(query)
        print("-" * 60)

        print("\n[c] Copy to clipboard")
        choice = input("[Enter] Back: ").strip().lower()
        if choice == "c":
            self._copy_to_clipboard(query)

    def _copy_to_clipboard(self, query: str):
        """Copy query to clipboard."""
        try:
            import subprocess
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                                          stdin=subprocess.PIPE)
                process.communicate(query.encode())
                print("\n  Query copied to clipboard!")
            except FileNotFoundError:
                try:
                    process = subprocess.Popen(['xsel', '--clipboard', '--input'],
                                              stdin=subprocess.PIPE)
                    process.communicate(query.encode())
                    print("\n  Query copied to clipboard!")
                except FileNotFoundError:
                    print("\n  Clipboard tools not available (install xclip or xsel)")
        except Exception as e:
            print(f"\n  Could not copy to clipboard: {e}")

        input("  Press Enter to continue...")

    def get_template_by_name(self, name: str) -> dict:
        """Find a template by name."""
        for cat, templates in self.CATEGORIES.items():
            for t in templates:
                if t['name'].lower() == name.lower():
                    return t
        return None

    def search_templates(self, keyword: str) -> List[Tuple[str, dict]]:
        """Search templates by keyword."""
        results = []
        keyword = keyword.lower()
        for cat, templates in self.CATEGORIES.items():
            for t in templates:
                if keyword in t['name'].lower() or keyword in t['description'].lower():
                    results.append((cat, t))
        return results
