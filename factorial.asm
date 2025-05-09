factorial:
addi	x2,	x2,	-32	# Allocate stack frame
sd	x1,	24(x2)	# Save return address
sd	x8,	16(x2)	# Save frame pointer
sd	x9,	8(x2)	# Save saved register
addi	x8,	x2,	32	# Set up frame pointer
sd	x10,	0(x2)	# Store parameter n
ld	x10,	0(x2)	# Load n
sd	x10,	0(x2)	# Save left operand
addi	x10,	x0,	1	# Load immediate
addi	x5,	x10,	0	# Move right operand
ld	x10,	0(x2)	# Restore left operand
sub	x10,	x10,	x5	# Compare
slti	x10,	x10,	1	# Set if less
xori	x10,	x10,	1	# Invert for <=
beq	x10,	x0,	L1
jal	x0,	L2
L1:
L2:
ld	x10,	0(x2)	# Load n
sd	x10,	0(x2)	# Save left operand
addi	x2,	x2,	-8	# Reserve space for argument
ld	x10,	0(x2)	# Load n
sd	x10,	0(x2)	# Save left operand
addi	x10,	x0,	1	# Load immediate
addi	x5,	x10,	0	# Move right operand
ld	x10,	0(x2)	# Restore left operand
sub	x10,	x10,	x5	# Subtract
sd	x10,	0(x2)	# Save argument
addi	x2,	x2,	-8	# Adjust stack for next arg
jal	x1,	factorial
addi	x2,	x2,	8	# Restore stack after arg
addi	x2,	x2,	8	# Restore argument space
addi	x5,	x10,	0	# Move right operand
ld	x10,	0(x2)	# Restore left operand
mul	x10,	x10,	x5	# Multiply
jal	x0,	factorial_END
factorial_END:
ld	x1,	24(x2)	# Restore return address
ld	x8,	16(x2)	# Restore frame pointer
ld	x9,	8(x2)	# Restore saved register
addi	x2,	x2,	32	# Deallocate stack frame
jalr	x0,	0(x1)	# Return
main:
addi	x2,	x2,	-32	# Allocate stack frame
sd	x1,	24(x2)	# Save return address
sd	x8,	16(x2)	# Save frame pointer
sd	x9,	8(x2)	# Save saved register
addi	x8,	x2,	32	# Set up frame pointer
addi	x10,	x0,	5	# Load immediate
sd	x10,	0(x2)	# Store to x
addi	x2,	x2,	-8	# Reserve space for argument
ld	x10,	0(x2)	# Load x
sd	x10,	0(x2)	# Save argument
addi	x2,	x2,	-8	# Adjust stack for next arg
jal	x1,	factorial
addi	x2,	x2,	8	# Restore stack after arg
addi	x2,	x2,	8	# Restore argument space
sd	x10,	8(x2)	# Store to result
ld	x10,	8(x2)	# Load result
sd	x10,	0(x2)	# Save left operand
addi	x10,	x0,	0	# Load immediate
addi	x5,	x10,	0	# Move right operand
ld	x10,	0(x2)	# Restore left operand
sub	x10,	x10,	x5	# Compare
slt	x10,	x5,	x10	# Set if greater
beq	x10,	x0,	L3
jal	x0,	L4
L3:
L4:
jal	x0,	main_END
main_END:
ld	x1,	24(x2)	# Restore return address
ld	x8,	16(x2)	# Restore frame pointer
ld	x9,	8(x2)	# Restore saved register
addi	x2,	x2,	32	# Deallocate stack frame
jalr	x0,	0(x1)	# Return