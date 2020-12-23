#!/usr/bin/python

import socket, argparse, time, itertools
from threading import *

def main(default, brute, brute_wordlist, wordlist):
    global start_time
    start_time = time.time()
    if args.default: # the domain list on this is from a friend of mines script The Reaper (Cri)
        default_list_of_subdomains = [
                "dc", "test", "api", "old", "ns2", "play", "server", "server1", "server2", "gateway", "app", 
                "media", "help", "embed", "status", "ns1", "host", "dashboard", "blog", "autodiscovery", "beta", 
                "dev", "wiki", "autoconfig", "secure", "irc", "irix", "fileserver", "backup", "agent", "c2c", 
                "ts3", "login", "mssql", "mysql", "localhost", "nameserver", "netstats", "mobile", "mobil",  "ftp",
                "webadmin", "uploads", "transfer", "tmp", "support", "smtp0#", "smtp#", "smtp", "sms", "shopping", 
                "sandbox", "proxy", "manager", "cpanel", "webmail", "forum", "driect- connect", "vb", "forums", 
                "pop#", "pop", "home", "direct", "mail", "access", "admin", "oracle", "monitor", "administrator", 
                "email", "downloads", "ssh", "webmin", "paralel", "parallels", "www0", "www", "www1", "www2", 
                "www3", "www4", "www5", "autoconfig.admin", "autoconfig", "autodiscover.admin", "autodiscover", 
                "sip", "msoid", "lyncdiscover"
        ]

        for sub in default_list_of_subdomains:
            try:
                host = str(sub) + '.' + str(args.default)
                ip = socket.gethostbyname(str(host))
                print('[NAMESERVER] -> ' + host + ' -> [IP] -> ' + ip)
            except:
                pass
    elif args.brute:
        gen = itertools.combinations_with_replacement('abcdefghijklmnopqrstuvwxyz0123456789', int(50))
        for sub in gen:
            try:
                host = str(sub) + '.' + str(args.dbrute)
                ip = socket.gethostbyname(str(host))
                print('[NAMESERVER] -> ' + host + ' -> [IP] -> ' + ip)
            except:
                print(f'Scan progress: {sub}')
    elif args.brute_wordlist and args.wordlist:
        try:
            print('Loading word list...')
            f = open(args.wordlist, 'r')
            line = f.readline()
            wl = string.split(line)
            print(f'     ', len(wl), 'words loaded!')
            try:
                for sub in wl:
                    host = str(sub) + '.' + str(args.brute_wordlist)
                    ip = socket.gethostbyname(str(host))
                    print('[NAMESERVER] -> ' + host + ' -> [IP] -> ' + ip)
            except:
               pass
        except:
            print('Error has occurred while loading the word list file! Please try again.')
    else:
        print('Invalid argument used! Please try again')

if __name__ == '__main__':
    t1 = Thread(target=main)
    t1.start()
    t1.join()
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-default', type=str, help='default subdomain scanner (Uses a default wordlist)')
    parser.add_argument('-brute', type=str, help='Pure brute force method')
    parser.add_argument('-brute_wordlist', type=str, help='Brute force method using a wordlist (Must use -wordlist in command)')
    parser.add_argument('-wordlist', type=str, help='Location of Wordlist file to use')    
    args = parser.parse_args()
    default = args.default
    brute = args.brute
    brute_wordlist = args.brute_wordlist
    wordlist = args.wordlist
    main(default, brute, brute_wordlist,  wordlist)
    print('%s seconds' % (time.time() - start_time))
