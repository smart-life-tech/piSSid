from flask import Flask, render_template, request,redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure_wifi', methods=['POST'])
def configure_wifi():
    ssid = request.form['ssid']
    password = request.form['password']

    # Update wpa_supplicant file with new Wi-Fi credentials
    # Note: This is a simplified example and may need further adjustments.
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as f:
        f.write(f'network={{\n  ssid="{ssid}"\n  psk="{password}"\n}}\n')

    return "Wi-Fi configured successfully!"

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

@app.route('/reboot', methods=['POST'])
def reboot_pi():
    # Perform any necessary cleanup or save operations before rebooting
    # For example, save any configurations or data
    
    # Reboot the Raspberry Pi
    subprocess.run(['sudo', 'reboot'])
    
    # Redirect to the index page after initiating the reboot
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
