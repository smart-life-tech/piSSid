'''
After modifying the wpa_supplicant.conf file, it stops the access point service (hostapd) 
using sudo systemctl stop hostapd.
Then, it restarts the networking service using sudo systemctl restart networking.
By stopping the access point service and restarting the networking service, the Raspberry 
Pi transitions from access point mode to client mode, 
attempting to connect to the specified Wi-Fi network using the updated credentials.
'''
from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

def modify_wpa_supplicant(ssid, password):
    # Read the existing wpa_supplicant.conf
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as file:
        data = file.readlines()

    # Modify the relevant lines with the new credentials
    for i in range(len(data)):
        if data[i].strip().startswith('ssid='):
            data[i] = '    ssid="{}"\n'.format(ssid)
        elif data[i].strip().startswith('psk='):
            data[i] = '    psk="{}"\n'.format(password)

    # Write the modified data back to the file
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as file:
        file.writelines(data)

    print('Modified wpa_supplicant.conf with new credentials.')

def reboot():
    subprocess.run(['sudo', 'reboot'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure_and_reboot', methods=['POST'])
def configure_and_reboot():
    ssid = request.form['ssid']
    password = request.form['password']

    # Modify wpa_supplicant.conf
    modify_wpa_supplicant(ssid, password)

    # Stop the access point service (hostapd)
    subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'])

    # Restart networking to apply changes
    subprocess.run(['sudo', 'systemctl', 'restart', 'networking'])

    return "Configured Wi-Fi and restarting network. Please reconnect to the new Wi-Fi network."

@app.route('/run_scripts')
def run_scripts():
    # Run three different Python scripts sequentially
    scripts = [
        '/path/to/script1.py',
        '/path/to/script2.py',
        '/path/to/script3.py'
    ]
    
    for script in scripts:
        subprocess.run(['python', script])

    return "Scripts executed!"

if __name__ == '__main__':
    app.run(host='raspberrypi.local', port=5000)
