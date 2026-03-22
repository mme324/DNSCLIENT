import dns.resolver

# Set the IP address of the local DNS server and a public DNS server
# (Local resolver uses system defaults — do NOT override)
real_name_server = '1.1.1.1'  # Cloudflare DNS


# Create a list of domain names to query
domainList = ['example.com.', 'safebank.com.', 'google.com.', 'nyu.edu.', 'legitsite.com.']


# Query local DNS server (system default resolver)
def query_local_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    answers = resolver.resolve(domain, question_type)
    return [r.to_text() for r in answers]


# Query public DNS server
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]
    answers = resolver.resolve(domain, question_type)
    return [r.to_text() for r in answers]


# Compare results between local and public DNS
def compare_dns_servers(domainList, question_type):
    for domain_name in domainList:
        local_ip_address = query_local_dns_server(domain_name, question_type)
        public_ip_address = query_dns_server(domain_name, question_type)
        if local_ip_address != public_ip_address:
            return False
    return True    


# Print results from both DNS servers
def local_external_DNS_output(question_type):    
    print("Local DNS Server")
    for domain_name in domainList:
        ip_address = query_local_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")

    print("\nPublic DNS Server")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")
        

# Testing function (Part 2 hook)
def exfiltrate_info(domain, question_type):
    return query_local_dns_server(domain, question_type)


if __name__ == '__main__':
    
    # Set the type of DNS query to be performed
    question_type = 'A'

    # Optional: print both outputs
    # local_external_DNS_output(question_type)
    
    # Compare DNS servers
    result = compare_dns_servers(domainList, question_type)
    print("Do both DNS servers match for all domains?", result)

    # Test single query
    result = query_local_dns_server('nyu.edu.', question_type)
    print("Local DNS result for nyu.edu.:", result)

    # Optional test
    # print(exfiltrate_info('google.com.', question_type))
