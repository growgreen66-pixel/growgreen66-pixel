"""Sample log parser for demonstration purposes

Usage:
  python3 samples/log_parser.py [logfile]

This simple parser reads a text log file (or stdin) and demonstrates:
- basic Python scripting for log parsing
- extracting common fields (timestamp, level, IP)
- counting events per log level and per IP
- printing a short summary that can be linked from your README as evidence of scripting and log-analysis skills

Notes:
- This is a compact example intended as a learning artifact, not production code.
"""

import re
import sys
from collections import Counter

LOG_LINE_RE = re.compile(r"(?P<timestamp>\S+)\s+(?P<host>\S+)\s+(?P<proc>[^:]+):\s*(?P<message>.*)")
IP_RE = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")
LEVEL_RE = re.compile(r"\b(INFO|DEBUG|WARN|WARNING|ERROR|CRITICAL)\b", re.IGNORECASE)


def parse_lines(lines):
    level_counts = Counter()
    ip_counts = Counter()
    total = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        total += 1
        m = LOG_LINE_RE.match(line)
        message = line
        if m:
            message = m.group("message")
        # find level
        lvl = LEVEL_RE.search(message)
        if lvl:
            level_counts[lvl.group(1).upper()] += 1
        # find IPs
        for ip in IP_RE.findall(line):
            ip_counts[ip] += 1

    return total, level_counts, ip_counts


def main():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        with open(fname, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    total, level_counts, ip_counts = parse_lines(lines)

    print(f"Parsed {total} log lines")
    if level_counts:
        print("Log levels:")
        for lvl, cnt in level_counts.most_common():
            print(f"  {lvl}: {cnt}")
    else:
        print("No log levels detected (INFO/ERROR/etc.)")

    if ip_counts:
        print("Top IPs:")
        for ip, cnt in ip_counts.most_common(10):
            print(f"  {ip}: {cnt}")
    else:
        print("No IP addresses detected")


if __name__ == '__main__':
    main()
