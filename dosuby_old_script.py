try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

try:
    from urllib.parse import urlparse
except ImportError:
    print("No module named 'urllib' found")

try:
    import dns
except ImportError:
    print("No module named 'dns' found")

try:
    import dns.resolver
except ImportError:
    print("No module named 'dnspython' found")

import sys
import argparse
from termcolor import colored, cprint
from art import *
from cmsdetector import *



def _get_a_record(site, dnsserver=None, banner='',querytype='A', file_out=None):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5

    if dnsserver:
        resolver.nameservers = [dnsserver]

    result = []
    while len(resolver.nameservers):
        try:
            msg = ''
            try:
                resolved = dns.resolver.resolve(site, querytype)
                for val in resolved:
                    if querytype == 'CNAME':
                        msg = f'    [{banner}]: {val.target}'
                        if file_out:
                            file_out.write(msg+"\n")
                        print(colored(msg, 'yellow'))
                    else:
                        msg = f'    [{banner}]: {val.to_text()}'
                        if file_out:
                            file_out.write(msg+"\n")
                        print(colored(msg, 'yellow'))
            except dns.resolver.NoAnswer:
                msg = f'    [!] No DNS response IN : {querytype}'
                if file_out:
                    file_out.write(msg+"\n")
                print(colored(msg, 'red'))
                
            return result

        except dns.exception.Timeout:
            msg = "    [!] DNS Timeout for using " + resolver.nameservers[0] + ": " + querytype
            if file_out:
                file_out.write(msg+"\n")
            print(msg)
            resolver.nameservers.remove(resolver.nameservers[0])
    # If all the requests failed
    return msg

if __name__ == '__main__':
    # to search
    domains = []
    tprint("dosuby")
    print('v1.0.0\n')
    # Initialize parser
    msg = "Simple Subdomains Scanner"
    parser = argparse.ArgumentParser(description=msg)
    # Adding optional argument
    parser.add_argument("-d", "--domain", required=True, help = "Ex: domain.com")
    parser.add_argument("-s", "--stop", type=int, default=10, choices=range(10, 201),metavar="[0-200]", help = "Page to stop at. default is 10")
    parser.add_argument("-t", "--time-pause", type=int, default=10, choices=range(2, 11),metavar="[2-10]", help = "Time to pause between requests. default is 2 seconds")
    parser.add_argument("-e", "--extra", default=False, action=argparse.BooleanOptionalAction, help = "Show dns information on subdomains")
    parser.add_argument("-cms", "--cms-detector", default=False, action=argparse.BooleanOptionalAction, help = "Try to detecte cms used")
    parser.add_argument("-o", "--output-file", help = "Save output as text file")
    
    # Read arguments from command line
    args = parser.parse_args()
    target = args.domain
    extra = args.extra
    stop_arg = args.stop
    cms = args.cms_detector
    output_file = args.output_file
    if target:
        f = None
        if output_file:
            f = open(output_file, "a")
        try:
            if output_file:
                f.write("Finding subdomains for: " + target + "\n")
                f.write("+="*20)
                f.write("\n")
            print("Finding subdomains for: % s" % target)
            print("+="*20)
            query = f'site:*.{target} -site:www.{target}'
            i=1
            for j in search(query, tld="com", num=10, stop=stop_arg, pause=2):
                # extract domain
                url = urlparse(j)
                d = url.netloc
                clean_url = '{uri.scheme}://{uri.netloc}/'.format(uri=url)
                if d not in domains:
                    domains.append(d)
                    if output_file:
                        f.write(f'[{i}] Subdomain found : {d}\n')
                    print(colored(f'[{i}] Subdomain found : {d}', 'green'))
                    i+=1
                    _get_a_record(d, banner='IP', file_out=f)
                    if extra is True:
                        _get_a_record(d, banner='AAAA', querytype='AAAA', file_out=f)
                        _get_a_record(d, banner='PTR', querytype='PTR', file_out=f)
                        _get_a_record(d, banner='NS', querytype='NS', file_out=f)
                        _get_a_record(d, banner='CNAME', querytype='CNAME', file_out=f)
                        _get_a_record(d, banner='MX', querytype='MX', file_out=f)
                        _get_a_record(d, banner='SOA', querytype='SOA', file_out=f)
                        _get_a_record(d, banner='TXT', querytype='TXT', file_out=f)
                    if cms is True:
                        runCmsDetector(url=clean_url, file_out=f)
                    print('-------'*6)
                    if output_file:
                        f.write('------------------\n')
        except Exception as e:
            if output_file:
                f.write('-------[ERROR]-------\n')
                f.write(str(e))
            print("[x]", e)
        if output_file:
            f.close()
    else:
        print("Use -h option to display the help menu.")



