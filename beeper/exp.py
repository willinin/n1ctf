#coding:utf-8
from pwn import *
import os

context.arch='amd64'
#context.log_level='debug'

io=process('./beeper')

password = '\x86\x13\x81\x09\x62\xff\x44\xd3\x3f\xcd\x19\xb0\xfb\x88\xfd\xae\x20\xdf'

def pass_pwd(content):
    io.recvuntil('password:\n')
    io.sendline(content.ljust(111,'\x00'))
    
if __name__ == '__main__':
    pause()
    pass_pwd(password)
    #pause()
    #io.interactive()
    #this a so boring probem!
