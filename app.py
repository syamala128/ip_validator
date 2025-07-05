from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

def validate_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False

def get_ip_class_and_subnet(ip):
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return 'A', '255.0.0.0'
    elif 128 <= first_octet <= 191:
        return 'B', '255.255.0.0'
    elif 192 <= first_octet <= 223:
        return 'C', '255.255.255.0'
    elif 224 <= first_octet <= 239:
        return 'D (Multicast)', 'N/A'
    elif 240 <= first_octet <= 254:
        return 'E (Experimental)', 'N/A'
    else:
        return 'Invalid', 'N/A'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        ip = request.form['ip']
        if validate_ip(ip):
            ip_class, subnet = get_ip_class_and_subnet(ip)
            result = {
                'ip': ip,
                'valid': True,
                'class': ip_class,
                'subnet': subnet
            }
        else:
            result = {
                'ip': ip,
                'valid': False
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
