import subprocess
import re

result = subprocess.run(['ifconfig'], capture_output=True, text=True)
output = result.stdout
print(output)
# wifi 인터페이스 이름(en1) 연결 - ethernet 주소(ether)와 IP 주소(inet) 출력 (참고, 유선 인터페이스 이름(en0))
interface = 'en1'
match = re.search(fr'\b{interface}\b.*?(ether)\s+(\S+)', output, re.DOTALL)
if match:
    if match.group(1) == 'ether':
        print(f'MAC address: {match.group(2)}')

ip_match = re.search(fr'\b{interface}\b.*?inet\s+(\d+\.\d+\.\d+\.\d+)', output, re.DOTALL)
print(ip_match)
if ip_match:
    print(f'IP address: {ip_match.group(1)}')
