suma:
addi	x2,	x2,	-32	# Allocate stack frame
sd	x1,	24(x2)	# Save return address
sd	x8,	16(x2)	# Save frame pointer
sd	x9,	8(x2)	# Save saved register
addi	x8,	x2,	32	# Set up frame pointer
sd	x10,	0(x2)	# Store parameter a
sd	x11,	8(x2)	# Store parameter b
ld	x10,	0(x2)	# Load a
sd	x10,	0(x2)	# Save left operand
ld	x10,	8(x2)	# Load b
addi	x5,	x10,	0	# Move right operand
ld	x10,	0(x2)	# Restore left operand
add	x10,	x10,	x5	# Add
jal	x0,	suma_END
suma_END:
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
addi	x10,	x0,	10	# Load immediate
sd	x10,	0(x2)	# Store to x
addi	x10,	x0,	20	# Load immediate
sd	x10,	8(x2)	# Store to y
ld	x10,	0(x2)	# Load x
sd	x10,	0(x2)	# Save first argument
ld	x10,	8(x2)	# Load y
addi	x11,	x10,	0	# Move second argument to x11
ld	x10,	0(x2)	# Restore first argument to x10
jal	x1,	suma
sd	x10,	16(x2)	# Store to result
ld	x10,	16(x2)	# Load result
sd	x10,	0(x2)	# Save left operand
addi	x10,	x0,	0	# Load immediate
addi	x5,	x10,	0	# Move right operand
ld	x10,	0(x2)	# Restore left operand
sub	x10,	x10,	x5	# Compare
beq	x10,	x0,	L3	# Branch if equal to zero
addi	x5,	x0,	0	# Load 0
blt	x5,	x10,	L4	# Branch if greater than zero
L3:
addi	x10,	x0,	0	# False
jal	x0,	L5
L4:
addi	x10,	x0,	1	# True
L5:
beq	x10,	x0,	L1
jal	x0,	L2
L1:
L2:
jal	x0,	main_END
main_END:
ld	x1,	24(x2)	# Restore return address
ld	x8,	16(x2)	# Restore frame pointer
ld	x9,	8(x2)	# Restore saved register
addi	x2,	x2,	32	# Deallocate stack frame
jalr	x0,	0(x1)	# Return