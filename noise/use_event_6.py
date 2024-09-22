import subprocess

def libreoffice_thread():
    # Run event_6.py using LibreOffice's Python interpreter.
    cmd = ["/opt/libreoffice5.4/program/python", "/home/user01/ran/T-Smade/noise/event_6.py"]

    # Capture output and errors for debugging.
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print output and error messages to assist with debugging.
    print("Output:", process.stdout)
    print("Error:", process.stderr)

if __name__ == "__main__":
    libreoffice_thread()