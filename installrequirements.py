from sys import executable
import subprocess
subprocess.run([executable, "-m", "pip", "install", "-r", "requirements.txt"])  
