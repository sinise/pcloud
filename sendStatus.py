import urllib
import urllib2
from subprocess import PIPE, Popen

#execute commandd
def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

# Get the ip of the rpi
eth0 = cmdline("ip addr list eth0 |grep 'inet ' |cut -d' ' -f6|cut -d/ -f1")
wlan0 = cmdline("ip addr list wlan0 |grep 'inet ' |cut -d' ' -f6|cut -d/ -f1")
ip = None
if (eth0):
    ip = eth0
if (wlan0):
    ip = wlan0

#get cpu avarge load
cpu = float(cmdline("cat /proc/loadavg | cut -d' ' -f1"))

#get the mac of the rpi (always use eth0 mac as identification
# regardless if the connection is ower wify)
eth0mac = cmdline("ip link show eth0 | awk '/ether/ {print $2}'")

#get % of mem used
memTotal = cmdline("cat /proc/meminfo | grep MemTotal")
memTotal = memTotal[10:-3]
memTotal = memTotal.strip()
memFree = cmdline("cat /proc/meminfo | grep MemFree")
memFree = memFree[8:-3]
memFree = memFree.strip()
memUsed = float(memFree) / (float(memTotal) / 100)
memUsed = int(memUsed)

url = 'http://10.0.0.30/rpi/recvStatusRpi_action/11:11:11:11:11:11'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'ip' : ip,
          'mac' : eth0mac,
          'wan' : '10.0.0.2',   #should be removed from here and determined by server
          'cpu' : cpu,		#cpu load (avarge number of ready processes in queue over 1 min)
          'ram' : memUsed,      #memory used in percent
          'url' : 'dr.dk',
          'urlViaServer' : '0',
          'orientation' : '0',
          'lastMTransTime' : '' }
headers = { 'User-Agent' : user_agent }

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
