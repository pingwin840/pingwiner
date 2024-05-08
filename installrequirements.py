from sys import executable, platform
import subprocess
subprocess.run([executable, "-m", "pip", "install", "-r", "requirements.txt"])  