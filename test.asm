.section .text
.globl _start

_start:
    # Call main
    call main
    
    # Exit program
    li a7, 93  # syscall number for exit
    li a0, 0   # exit code 0
    ecall

main:
    addi sp, sp, -4
    sw ra, 0(sp)
    
    # Variable declaration: int x
    # Variable declaration: int y
    # Variable declaration: int sum
    
    li t3, 5
    mv t0, t3
    li t3, 10
    mv t1, t3
    mv t4, t0
    mv t5, t1
    add t3, t4, t5
    mv t2, t3
    mv t4, t2
    li t5, 10
    sgt t3, t4, t5
    beqz t3, L1
    mv a0, t2
    j L2
L1:
    li a0, 0
L2:
    lw ra, 0(sp)
    addi sp, sp, 4
    ret