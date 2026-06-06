
import re
from typing import List, Tuple

DATE_PATTERN = re.compile(
    r'^(january|february|march|april|may|june|july|august|september|october|november|december|'
    r'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
    r'\s+\d{1,2}\s*,?\s*\d{4}',
    re.IGNORECASE | re.MULTILINE
)

NUMERIC_DATE_PATTERN = re.compile(
    r'^\d{1,2}/\d{1,2}/\d{2,4}',
    re.MULTILINE
)

def is_bullet(line: str) -> bool:
    return bool(re.match(r'^\s*[\*\-•]', line))

def is_date(line: str) -> bool:
    clean = line.strip().replace('**', '')
    return bool(DATE_PATTERN.match(clean)) or bool(NUMERIC_DATE_PATTERN.match(clean))

def is_client_header(clean: str, next_lines: List[str]) -> bool:
    if not clean or is_bullet(clean) or is_date(clean) or len(clean.split()) > 5:
        return False
    for nl in next_lines:
        if not nl.strip():
            continue
        return is_bullet(nl.strip())
    return False

def split_message_logic(content: str, author: str, timestamp: str, server: str, channel: str, report_type: str) -> List[str]:
    header_base = f"Server: {server} | Channel: #{channel} | Report-Type: {report_type}"
    lines = content.split('\n')
    
    segments = []
    current_date = timestamp
    current_client = None
    current_bullets = []

    i = 0
    while i < len(lines):
        line = lines[i]
        clean = line.strip().replace('**', '')
        next_lines = lines[i+1:i+4]

        if not clean:
            i += 1
            continue

        if is_date(clean):
            if current_bullets:
                segments.append((current_date, current_client, current_bullets))
                current_bullets = []
                current_client = None
            current_date = clean
            i += 1
        elif is_client_header(clean, next_lines):
            if current_bullets:
                segments.append((current_date, current_client, current_bullets))
                current_bullets = []
            current_client = clean
            i += 1
        elif is_bullet(line):
            current_bullets.append(line.strip())
            i += 1
        else:
            current_bullets.append(line.strip())
            i += 1

    if current_bullets:
        segments.append((current_date, current_client, current_bullets))

    chunks = []
    for date, client, bullets in segments:
        client_label = f"\n{client}" if client else ""
        chunk_body = '\n'.join(bullets)
        chunks.append(
            f"{header_base} | Period: {date}\n"
            f"[{timestamp}] {author}:{client_label}\n{chunk_body}"
        )

    return chunks if chunks else [
        f"{header_base} | Period: {timestamp}\n"
        f"[{timestamp}] {author}:\n{content.strip()}"
    ]

def parse_and_chunk_discord_messages(
    content: str, author: str, timestamp: str, server: str, channel: str
) -> List[str]:
    # Determine report type from channel name
    report_type = "DAILY" if "daily" in channel.lower() else ("WEEKLY" if "weekly" in channel.lower() else "GENERAL")
    return split_message_logic(content, author, timestamp, server, channel, report_type)
