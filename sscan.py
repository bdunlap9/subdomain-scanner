import aiohttp, asyncio, argparse, itertools, socket, string

class AdvancedSubdomainScanner:
    def __init__(self, domain, wordlist=None, concurrency=50, length_range=None):
        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency
        self.length_range = length_range
        self.resolver = aiohttp.resolver.AsyncResolver()

    async def resolve_subdomain(self, subdomain):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(resolver=self.resolver)) as session:
                async with session.get(f'http://{subdomain}.{self.domain}') as response:
                    ip = socket.gethostbyname(subdomain)
                    print(f'{subdomain}.{self.domain} ({ip})')
        except (aiohttp.ClientConnectorError, socket.gaierror):
            pass

    async def scan_subdomains(self, subdomains):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(resolver=self.resolver)):
            tasks = []
            for subdomain in subdomains:
                task = asyncio.ensure_future(self.resolve_subdomain(subdomain))
                tasks.append(task)
                if len(tasks) >= self.concurrency:
                    await asyncio.gather(*tasks)
                    tasks.clear()
            if tasks:
                await asyncio.gather(*tasks)

    async def scan_wordlist(self):
        with open(self.wordlist, 'r') as file:
            subdomains = [line.strip() for line in file]
        await self.scan_subdomains(subdomains)

    async def brute_force(self):
        if self.length_range:
            min_length, max_length = self.length_range
            for length in range(min_length, max_length + 1):
                for subdomain in itertools.product(string.ascii_lowercase + string.digits, repeat=length):
                    subdomain = ''.join(subdomain)
                    await self.scan_subdomains([subdomain])

def main():
    parser = argparse.ArgumentParser(description="Advanced Subdomain Scanner")
    parser.add_argument("-d", "--domain", required=True, help="Domain to scan")
    parser.add_argument("-w", "--wordlist", help="Wordlist file")
    parser.add_argument("-c", "--concurrency", type=int, default=50, help="Concurrency level (default: 50)")
    parser.add_argument("-b", "--bruteforce", action="store_true", help="Enable brute force scanning")
    parser.add_argument("-r", "--range", type=int, nargs=2, help="Length range for brute force (e.g. '3 5')")
    args = parser.parse_args()

    scanner = AdvancedSubdomainScanner(args.domain, args.wordlist, args.concurrency, args.range)

    if args.wordlist:
        asyncio.run(scanner.scan_wordlist())
    
    if args.bruteforce:
        asyncio.run(scanner.brute_force())

if __name__ == "__main__":
    main()
