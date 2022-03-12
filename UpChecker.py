# python

# imports
import subprocess

# ping host url
host = "www.google.com"
ping = subprocess.Popen(
    ["ping", "-c", "4", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)
ping, error = ping.communicate()

# echo ping results
print ping

