import re

def extract_features(url):
    return {
        "url_length": len(url),
        "num_dots": url.count('.'),
        "num_slashes": url.count('/'),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": len(re.findall(r'[^a-zA-Z0-9]', url)),
        "has_ip": int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        "has_https": int("https" in url.lower()),
        "has_dash": int('-' in url),
        "num_subdomains": url.count('.') - 1 if url.count('.') > 0 else 0
    }