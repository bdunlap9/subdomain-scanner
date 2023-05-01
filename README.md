# Subdomain Scanner

The Subdomain Scanner is a simple Python script that helps you discover subdomains for a given domain using a list of potential subdomain names. This tool is useful for penetration testing, information gathering, and reconnaissance.

## Features

- Scans subdomains using a list of potential names.
- Concurrent scanning for faster results.
- Displays found subdomains with corresponding IP addresses.

## Requirements

- Python 3.7 or higher
- aiohttp
- asyncio

## Installation

1. Clone the repository:

```
git clone https://github.com/bdunlap9/subdomain-scanner.git
```

2. Change to the project directory:

```
cd subdomain-scanner
```

3. Install the required Python packages:

```
pip install -r requirements.txt
```

## Usage

To use the Subdomain Scanner, run the following command:

```
python sscan.py -d <domain> -w <wordlist>
```

Replace `<domain>` with the domain you want to scan and `<wordlist>` with the path to a wordlist file containing potential subdomain names. The scanner will attempt to resolve each subdomain in the wordlist and display the results.

Example:

```
python sscan.py -d example.com -w wordlist.txt
```

## Customization

You can customize the Subdomain Scanner by modifying the `sscan.py` file. You can change the concurrency settings, add new features, or update the output format based on your requirements.

## Contributing

Contributions to this project are welcome. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with your changes.
3. Commit your changes and push them to your fork.
4. Create a pull request to merge your changes with the main repository.

## License

This project is released under the MIT License.
