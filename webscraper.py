#!/usr/bin/env python3
import re
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

# Base configuration
TARGET_URL = "http://10.50.13.174"  # Replace with your target URL
TARGET_DOMAIN = urlparse(TARGET_URL).netloc

VISITED_URLS = set()
URL_QUEUE = [TARGET_URL]

# Common directories and files to guess
COMMON_PATHS = [
    '/login.php', '/img/', '/scripts/', '/admin/', 
    '/config.php', '/backup/', '/secret/'
]

# Regex patterns
PASS_PATTERN = re.compile(r'\b(password|pass)\b', re.IGNORECASE)
USER_PATTERN = re.compile(r'\b(username|user)\b', re.IGNORECASE)
SECRET_20_PATTERN = re.compile(r'(?:[\s\'"]|><)([a-zA-Z0-9]{20})(?:[\s\'"]|><)')
FILE_PATTERN = re.compile(r'\b[\w\-\.]+\.(sh|py|ps|txt)\b', re.IGNORECASE)

class AdvancedPageParser(HTMLParser):
    def __init__(self, current_url):
        super().__init__()
        self.current_url = current_url
        self.links = []
        self.discovered_inputs = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        # 1. Track standard links for crawling
        if tag == 'a' and 'href' in attr_dict:
            href = attr_dict['href']
            if href and not ('?' in href and any(x in href for x in ['C=', 'O='])):
                full_url = urljoin(self.current_url, href)
                full_url = urlparse(full_url)._replace(fragment='').geturl()
                
                if not full_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.ico', '.css')):
                    if urlparse(full_url).netloc == TARGET_DOMAIN:
                        if full_url not in VISITED_URLS and full_url not in URL_QUEUE:
                            self.links.append(full_url)
                            
        # 2. Detect any form input elements
        if tag in ['input', 'textarea', 'select']:
            # Gather interesting attributes to describe the input field
            field_type = attr_dict.get('type', 'text') if tag == 'input' else tag
            field_name = attr_dict.get('name', '[no name attribute]')
            field_id = attr_dict.get('id', '')
            
            description = f"<{tag}> (type: '{field_type}', name: '{field_name}'"
            if field_id:
                description += f", id: '{field_id}'"
            description += ")"
            
            self.discovered_inputs.append(description)

def check_and_report(html_content, url, status_code, detected_inputs):
    """Scans text content and checks discovered inputs, printing if anything matches."""
    findings = []
    
    # Text-based pattern matching
    pass_matches = PASS_PATTERN.findall(html_content)
    if pass_matches:
        findings.append(f"  [!] Found password keyword(s): {set(pass_matches)}")
        
    user_matches = USER_PATTERN.findall(html_content)
    if user_matches:
        findings.append(f"  [!] Found username keyword(s): {set(user_matches)}")
        
    secret_matches = SECRET_20_PATTERN.findall(html_content)
    if secret_matches:
        findings.append(f"  [!] Found 20-character string(s): {set(secret_matches)}")

    full_file_matches = [m.group(0) for m in re.finditer(FILE_PATTERN, html_content)]
    if full_file_matches:
        findings.append(f"  [!] Found targeted file reference(s): {set(full_file_matches)}")

    # Input field reporting
    if detected_inputs:
        findings.append(f"  [*] Detected Input Field(s):")
        for inp in detected_inputs:
            findings.append(f"      {inp}")

    # Print a summary section if anything noteworthy was observed
    if findings:
        print(f"\n[+] Findings Discovered: {url} (Status: {status_code})")
        for finding in findings:
            print(finding)

def process_crawler():
    print(f"[*] Starting target scan on domain: {TARGET_DOMAIN}...")
    
    base_url = f"{urlparse(TARGET_URL).scheme}://{TARGET_DOMAIN}"
    for path in COMMON_PATHS:
        guessed_url = urljoin(base_url, path)
        if guessed_url not in URL_QUEUE:
            URL_QUEUE.append(guessed_url)
            
    while URL_QUEUE:
        current_url = URL_QUEUE.pop(0)
        
        if current_url in VISITED_URLS:
            continue
            
        try:
            VISITED_URLS.add(current_url)
            response = requests.get(current_url, timeout=5)
            
            if response.status_code in [200, 403]:
                content_type = response.headers.get("Content-Type", "")
                
                inputs_found = []
                # If HTML, parse for both links and structure tags
                if "text/html" in content_type:
                    parser = AdvancedPageParser(current_url)
                    parser.feed(response.text)
                    inputs_found = parser.discovered_inputs
                    URL_QUEUE.extend(parser.links)
                
                # Check text content patterns and evaluate findings
                if "text/html" in content_type or "text/plain" in content_type:
                    check_and_report(response.text, current_url, response.status_code, inputs_found)
                    
        except requests.exceptions.RequestException:
            pass

    print("\n[*] Crawl complete. Clean summary report finished.")

if __name__ == "__main__":
    process_crawler()
