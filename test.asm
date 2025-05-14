.section .data
    # Variables globales si las hubiera

.section .text
.globl main

main:
        addi    sp,sp,-32
        sd      ra,24(sp)
        sd      s0,16(sp)
        addi    s0,sp,32
        li      a5,8
        sw      a5,0(s0)
        li      a5,8
        sw      a5,4(s0)
        lw      a5,0(s0)
        mv      a4,a5
        lw      a5,4(s0)
        subw    a5,a4,a5
        sw      a5,8(s0)
        lw      a5,8(s0)
        mv      a4,a5
        li      a5,0
        slt     a5,a5,a4
        sext.w  a4,a5
        li      a5,0
        ble     a4,a5,.L1
        li      a5,1
        mv      a0,a5
        j       .L3
        j       .L2
.L1:
        j       .L3
.L2:
        ld      ra,24(sp)
        ld      s0,16(sp)
        addi    sp,sp,32
        jr      ra