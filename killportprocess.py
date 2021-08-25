import sys
from psutil import process_iter
from signal import SIGTERM # or SIGKILL
_killdCount = 0
_errorCount = 0
_arglen = len(sys.argv)
kports = []
# firebase emulator ports 
#kports = [9099,5000,5001,8088,8085,9000,4000]
test_port = list(sys.argv)
for portstr in test_port:
    #print("["+portstr +"]")
    if str(portstr).find('killportprocess.py') == -1 : 
        portnum = int(portstr)
        kports.append(portnum)
if len(kports) == 0:
    print("Please specify port number you need stop.")
    sys.exit()

print(f'Searching Port {kports} ....')

for proc in process_iter():
    #print(proc)
    #or conns in proc.connections(kind='inet'):
    for lconn in proc.connections():
        for ekport in kports:
            if lconn.laddr.port == ekport:
                 print(f'Port Open:  {str(lconn.laddr.port)} PID: {str(proc.pid)}')
                 try:
                     proc.send_signal(SIGTERM)
                     _killdCount = _killdCount +1
                 except Exception as e:
                     print(f'SIGTERM ERROR : {e} ')
                     _errorCount = _errorCount + 1
if(_killdCount == 0 and _errorCount == 0):
    print('No Port is detected!')

if(_killdCount == kports.count):
    print(f'Success Count {_killdCount} == {str(len(kports))}')
else:
    print(f'Killed Count {_killdCount} DOES NOT MATCH {str(len(kports))}')


             

           