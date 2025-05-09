main:
addi	x2,	x2,	-32	# Allocate stack frame
sd	x1,	24(x2)	# Save return address
sd	x8,	16(x2)	# Save frame pointer
sd	x9,	8(x2)	# Save saved register
addi	x8,	x2,	32	# Set up frame pointer
addi	x10,	x0,	10	# Load immediate
sd	x10,	0(x2)	# Store to a
addi	x10,	x0,	5	# Load immediate
sd	x10,	8(x2)	# Store to b
ld	x10,	0(x2)	# Load a
addi	x1,	x10,	0	# Save left operand
ld	x10,	8(x2)	# Load b
add	x10,	x1,	x10	# Add
sd	x10,	16(x2)	# Store to c
ld	x10,	16(x2)	# Load c
jal	x0,	main_END
main_END:
ld	x1,	24(x2)	# Restore return address
ld	x8,	16(x2)	# Restore frame pointer
ld	x9,	8(x2)	# Restore saved register
addi	x2,	x2,	32	# Deallocate stack frame
jalr	x0,	0(x1)	# Return