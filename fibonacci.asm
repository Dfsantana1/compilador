FIBONACCI:
addi	x2,	x2,	-40	# Reservar espacio en la pila
sd	x1,	32(x2)	# Guardar RA
sd	x8,	24(x2)	# Guardar s0
sd	x9,	16(x2)	# Guardar s1
sd	x10,	8(x2)	# Guardar a0
sd	x11,	0(x2)	# Guardar a1


FIBONACCI_END:
ld	x1,	32(x2)	# Restaurar RA
ld	x8,	24(x2)	# Restaurar s0
ld	x9,	16(x2)	# Restaurar s1
ld	x10,	8(x2)	# Restaurar a0
ld	x11,	0(x2)	# Restaurar a1
addi	x2,	x2,	40
jalr	x0,	0(x1)	# Retornar
MAIN:
addi	x2,	x2,	-40	# Reservar espacio en la pila
sd	x1,	32(x2)	# Guardar RA
sd	x8,	24(x2)	# Guardar s0
sd	x9,	16(x2)	# Guardar s1
sd	x10,	8(x2)	# Guardar a0
sd	x11,	0(x2)	# Guardar a1


MAIN_END:
ld	x1,	32(x2)	# Restaurar RA
ld	x8,	24(x2)	# Restaurar s0
ld	x9,	16(x2)	# Restaurar s1
ld	x10,	8(x2)	# Restaurar a0
ld	x11,	0(x2)	# Restaurar a1
addi	x2,	x2,	40
jalr	x0,	0(x1)	# Retornar