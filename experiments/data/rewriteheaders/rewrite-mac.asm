ldxb r2, [r1+12]
ldxb r3, [r1+13]
lsh r3, 0x8
or r3, r2
mov r0, 0x0
ldxw r2, [r1]
jne r2, 0x03020100, +1
mov r0, 0x1
exit
