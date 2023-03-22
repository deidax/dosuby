#!/usr/bin/env python3

import dnslib

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow


def dnsrec(domain, output):
	result = {}
	print(f'\n{Y}[!] Starting DNS Enumeration...{W}\n')
	types = ['A', 'AAAA', 'ANY', 'CAA', 'CNAME', 'MX', 'NS', 'TXT']
	full_ans = []
	for Type in types:
		q = dnslib.DNSRecord.question(domain, Type)
		pkt = q.send('8.8.8.8', 53, tcp='UDP')
		ans = dnslib.DNSRecord.parse(pkt)
		ans = str(ans)
		ans = ans.split('\n')
		full_ans.extend(ans)
	full_ans = set(full_ans)
	dns_found = []

	for entry in full_ans:
		if entry.startswith(';') is False:
			dns_found.append(entry)
		else:
			pass

	if len(dns_found) != 0:
		for entry in dns_found:
			print(f'{C}{entry}{W}')
	else:
		print(f'{R}[-] {C}DNS Records Not Found!{W}')

	dmarc_target = f'_dmarc.{domain}'
	q = dnslib.DNSRecord.question(dmarc_target, 'TXT')
	pkt = q.send('8.8.8.8', 53, tcp='UDP')
	dmarc_ans = dnslib.DNSRecord.parse(pkt)
	dmarc_ans = str(dmarc_ans)
	dmarc_ans = dmarc_ans.split('\n')
	dmarc_found = []

	for entry in dmarc_ans:
		if entry.startswith('_dmarc') is True:
			dmarc_found.append(entry)
		else:
			pass
	if len(dmarc_found) != 0:
		for entry in dmarc_found:
			print(f'{C}{entry}{W}')
			if output != 'None':
				result.setdefault('dmarc', []).append(entry)
	else:
		print(f'\n{R}[-] {C}DMARC Record Not Found!{W}')
		if output != 'None':
			result.setdefault('dmarc', ['DMARC Record Not Found!'])
	result.update({'exported': False})



if __name__ == "__main__":
    dnsrec(domain='uca.ma', output=None)


########
from dnslib import DNSRecord, DNSHeader, QTYPE, RR, A
import socket

def resolve_dns(domain_name, qtype):
    # create a DNS query message for the given domain name and query type
    query = DNSRecord.question(domain_name, qtype)
    # send the DNS query to the local resolver
    response = query.send("127.0.0.1", 53, timeout=5)
    # parse the DNS response message
    response_msg = DNSRecord.parse(response)
    # extract the list of answers from the response
    answers = response_msg.rr

    # iterate over the answers and extract the subdomains
    subdomains = set()
    for answer in answers:
        if answer.rtype == QTYPE.CNAME:
            # if the answer is a CNAME record, extract the domain name from it
            subdomain = str(answer.rdata.label)
            subdomains.add(subdomain)
        elif answer.rtype == QTYPE.A:
            # if the answer is an A record, extract the IP address and hostname from it
            ip_address = socket.inet_ntoa(answer.rdata)
            hostname = str(answer.get_rname(response_msg))
            subdomain = hostname[:-1]  # remove trailing period from hostname
            subdomains.add(subdomain)

    return subdomains

# example usage
domain_name = "example.com"
qtype = QTYPE.ANY  # query for all record types
subdomains = resolve_dns(domain_name, qtype)
print(subdomains)
