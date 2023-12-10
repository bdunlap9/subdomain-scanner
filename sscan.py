import aiohttp, asyncio, argparse, logging, signal, socket, string, sys

class SubdomainScanError(Exception):
    pass

class AdvancedSubdomainScanner:
    def __init__(self, domain, wordlist=None, concurrency=50, length_range=None, output_file=None):
        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency
        self.length_range = length_range
        self.output_file = output_file
        self.resolver = aiohttp.resolver.AsyncResolver()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def resolve_subdomain(self, subdomain):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(resolver=self.resolver)) as session:
                async with session.get(f'http://{subdomain}.{self.domain}') as response:
                    ip = socket.gethostbyname(subdomain)
                    self.logger.info(f'{subdomain}.{self.domain} ({ip})')
        except (aiohttp.ClientConnectorError, socket.gaierror) as e:
            self.logger.error(f"Error resolving {subdomain}.{self.domain}: {e}")

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
        try:
            async with open(self.wordlist, 'r') as file:
                subdomains = [line.strip() for line in file]
            await self.scan_subdomains(subdomains)
        except FileNotFoundError as e:
            raise SubdomainScanError(f"Wordlist file not found: {self.wordlist}")

    async def brute_force(self):
        if self.length_range:
            min_length, max_length = self.length_range
            for length in range(min_length, max_length + 1):
                await self._brute_force_recursive('', length)

    async def _brute_force_recursive(self, current, remaining_length):
        if remaining_length == 0:
            await self.scan_subdomains([current])
        else:
            for char in string.ascii_lowercase + string.digits:
                await self._brute_force_recursive(current + char, remaining_length - 1)

    async def run_scans(self):
        if self.wordlist:
            await self.scan_wordlist()

        if self.length_range:
            await self.brute_force()

def main():
    parser = argparse.ArgumentParser(description="Advanced Subdomain Scanner")
    parser.add_argument("-d", "--domain", required=True, help="Domain to scan")
    parser.add_argument("-w", "--wordlist", help="Wordlist file")
    parser.add_argument("-c", "--concurrency", type=int, default=50, help="Concurrency level (default: 50)")
    parser.add_argument("-b", "--bruteforce", action="store_true", help="Enable brute force scanning")
    parser.add_argument("-r", "--range", type=int, nargs=2, help="Length range for brute force (e.g. '3 5')")
    parser.add_argument("-o", "--output", help="Output file for results")
    args = parser.parse_args()

    scanner = AdvancedSubdomainScanner(args.domain, args.wordlist, args.concurrency, args.range, args.output)

    def signal_handler(signal, frame):
        print("Exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        asyncio.run(scanner.run_scans())
    except SubdomainScanError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
