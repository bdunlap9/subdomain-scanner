import aiohttp, asyncio, argparse, socket

class AdvancedSubdomainScanner:
    def __init__(self, domain, wordlist, concurrency=50):
        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency
        self.resolver = aiohttp.resolver.AsyncResolver()

    async def resolve_subdomain(self, subdomain):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(resolver=self.resolver)) as session:
                async with session.get(f'http://{subdomain}.{self.domain}') as response:
                    ip = socket.gethostbyname(subdomain)
                    print(f'{subdomain}.{self.domain} ({ip})')
        except (aiohttp.ClientConnectorError, socket.gaierror):
            pass

    async def scan_subdomains(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(resolver=self.resolver)):
            tasks = []
            with open(self.wordlist, 'r') as file:
                for line in file:
                    subdomain = line.strip()
                    task = asyncio.ensure_future(self.resolve_subdomain(subdomain))
                    tasks.append(task)
                    if len(tasks) >= self.concurrency:
                        await asyncio.gather(*tasks)
                        tasks.clear()
            if tasks:
                await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Advanced Subdomain Scanner")
    parser.add_argument("-d", "--domain", required=True, help="Domain to scan")
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist file")
    parser.add_argument("-c", "--concurrency", type=int, default=50, help="Concurrency level (default: 50)")
    args = parser.parse_args()

    scanner = AdvancedSubdomainScanner(args.domain, args.wordlist, args.concurrency)
    asyncio.run(scanner.scan_subdomains())

if __name__ == "__main__":
    main()
