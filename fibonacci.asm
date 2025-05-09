.option nopic
.attribute arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0"
.attribute unaligned_access, 0
.attribute stack_align, 16

.section .text
.globl main


fibonacci:
    addi sp, sp, -32
    sd ra, 24(sp)
    sd s0, 16(sp)
    sd s1, 8(sp)
    mv s0, a0
    li t0, 1
    ble s0, t0, fibonacci_base
    addi a0, s0, -1
    call fibonacci
    mv s1, a0
    addi a0, s0, -2
    call fibonacci
    add a0, a0, s1
    j fibonacci_end
    fibonacci_base:
    mv a0, s0
    fibonacci_end:
    ld ra, 24(sp)
    ld s0, 16(sp)
    ld s1, 8(sp)
    addi sp, sp, 32
    ret

main:
    addi sp, sp, -32
    sd ra, 24(sp)
    sd s0, 16(sp)
    sd s1, 8(sp)
    addi sp, sp, -64
    sd t0, 0(sp)
    sd t1, 8(sp)
    sd t2, 16(sp)
    sd t3, 24(sp)
    sd t4, 32(sp)
    sd t5, 40(sp)
    sd t6, 48(sp)
    li t1, 6
    mv a0, t1
    call fibonacci
    mv t0, a0
    ld t0, 0(sp)
    ld t1, 8(sp)
    ld t2, 16(sp)
    ld t3, 24(sp)
    ld t4, 32(sp)
    ld t5, 40(sp)
    ld t6, 48(sp)
    addi sp, sp, 64
    mv a0, t0
    ld ra, 24(sp)
    ld s0, 16(sp)
    ld s1, 8(sp)
    addi sp, sp, 32
    ret