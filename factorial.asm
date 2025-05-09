.section .text
.globl _start

_start:
    # Call main
    call main
    
    # Save result
    mv s0, a0
    
    # Exit program with factorial result
    li a7, 93  # syscall number for exit
    mv a0, s0  # use factorial result as exit code
    ecall

factorial:
    addi sp, sp, -4
    sw ra, 0(sp)
    
    # Check if n <= 1
    li t2, 1
    bgt a0, t2, L1
    
    # Return 1 if n <= 1
    li a0, 1
    j L2
    
L1:
    # Save n
    mv t1, a0
    
    # Calculate n-1
    addi a0, t1, -1
    
    # Call factorial(n-1)
    call factorial
    
    # Multiply n * factorial(n-1)
    mul a0, t1, a0
    
L2:
    lw ra, 0(sp)
    addi sp, sp, 4
    ret

main:
    addi sp, sp, -4
    sw ra, 0(sp)
    
    # Call factorial(4)
    li a0, 4
    call factorial
    
    # Return result
    lw ra, 0(sp)
    addi sp, sp, 4
    ret