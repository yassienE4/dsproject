import re

import re
import math
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login", "verify", "secure", "account",
    "update", "bank", "paypal", "free", "bonus"
]

SUSPICIOUS_TLDS = (".xyz", ".ru", ".tk", ".ml", ".ga", ".cf")

def entropy(s):
    probs = [s.count(c)/len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    return {
        # Basic
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),

        # Structure
        "num_dots": domain.count('.'),
        "num_subdomains": max(domain.count('.') - 1, 0),

        # Content signals
        "num_digits": sum(c.isdigit() for c in url),
        "has_dash": int('-' in domain),

        # Security tricks
        "has_ip": int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', domain))),
        "has_at": int('@' in url),

        # Phishing signals
        "has_suspicious_words": int(
            any(word in url for word in SUSPICIOUS_WORDS)
        ),
        "is_suspicious_tld": int(domain.endswith(SUSPICIOUS_TLDS)),

        # Complexity
        "url_entropy": entropy(url),
    }