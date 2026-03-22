import dns.resolver

real_name_server = '1.1.1.1'

domainList = ['example.com.', 'safebank.com.', 'google.com.', 'nyu.edu.', 'legitsite.com.']


# LOCAL → return SINGLE value
def query_local_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    answers = resolver.resolve(domain, question_type)
    return answers[0].to_text()


# EXTERNAL → return FULL list
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]
    answers = resolver.resolve(domain, question_type)
    return [r.to_text() for r in answers]


def compare_dns_servers(domainList, question_type):
    for domain_name in domainList:
        local_ip_address = query_local_dns_server(domain_name, question_type)
        public_ip_address = query_dns_server(domain_name, question_type)

        # normalize comparison
        if isinstance(public_ip_address, list):
            if local_ip_address not in public_ip_address:
                return False
        else:
            if local_ip_address != public_ip_address:
                return False

    return True    


def local_external_DNS_output(question_type):    
    print("Local DNS Server")
    for domain_name in domainList:
        ip_address = query_local_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")

    print("\nPublic DNS Server")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")
        

def exfiltrate_info(domain, question_type):
    return query_local_dns_server(domain, question_type)


if __name__ == '__main__':
    question_type = 'A'

    result = compare_dns_servers(domainList, question_type)
    print("Do both DNS servers match for all domains?", result)

    result = query_local_dns_server('nyu.edu.', question_type)
    print("Local DNS result for nyu.edu.:", result)
