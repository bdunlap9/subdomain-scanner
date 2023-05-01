# Advanced Subdomain Scanner

An asynchronous subdomain scanner written in Python, designed to quickly scan for subdomains using a wordlist or brute force approach. The scanner uses aiohttp to handle multiple connections concurrently, significantly speeding up the scanning process.

## Features

- Asynchronous subdomain scanning
- Wordlist-based subdomain scanning
- Brute force subdomain scanning with specified length range
- Adjustable concurrency level for scanning

## Requirements

- Python 3.7+
- aiohttp

To install aiohttp, run:

```
pip install aiohttp
```

## Usage

```
usage: Advanced Subdomain Scanner [-h] -d DOMAIN [-w WORDLIST] [-c CONCURRENCY] [-b] [-r RANGE]

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to scan
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist file
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Concurrency level (default: 50)
  -b, --bruteforce      Enable brute force scanning
  -r RANGE, --range RANGE
                        Length range for brute force (e.g. '3 5')
```

### Examples

Scan a domain using a wordlist:

```
python advanced_subdomain_scanner.py -d example.com -w wordlist.txt
```

Scan a domain using brute force with a length range of 3 to 5 characters:

```
python advanced_subdomain_scanner.py -d example.com -b -r 3 5
```

Scan a domain using both a wordlist and brute force:

```
python advanced_subdomain_scanner.py -d example.com -w wordlist.txt -b -r 3 5
```

Adjust the concurrency level (default is 50):

```
python advanced_subdomain_scanner.py -d example.com -w wordlist.txt -c 100
```

## Note

Please use this tool responsibly and only on domains you have permission to scan. Misuse of this tool may lead to legal consequences.
