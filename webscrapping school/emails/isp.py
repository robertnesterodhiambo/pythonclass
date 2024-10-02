import socket
from ipwhois import IPWhois

def get_isp(domain):
    try:
        # Get the IP address of the domain
        ip = socket.gethostbyname(domain)
        # Use IPWhois to get ISP information
        ip_info = IPWhois(ip)
        result = ip_info.lookup_whois()
        return result['asn_description']  # ISP information
    except Exception as e:
        return f"Error: {str(e)}"

domain = "vivantes.de"
isp = get_isp(domain)
print(f"The ISP of {domain} is: {isp}")
