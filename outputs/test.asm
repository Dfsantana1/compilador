.section .data    # Sección de datos globales
    # Variables globales si las hubiera

.section .text    # Sección de código
.globl main    # Declaración de la función main como global

suma:    # Inicio de la función suma
        addi    sp,sp,-16    # Reservar espacio en el stack
        sw      ra,12(sp)    # Guardar return address
        sw      s0,8(sp)    # Guardar frame pointer
        addi    s0,sp,16    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro a en el stack
        sw      a1,4(s0)    # Guardar parámetro b en el stack
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        lw      ra,12(sp)    # Restaurar return address
        lw      s0,8(sp)    # Restaurar frame pointer
        addi    sp,sp,16    # Liberar espacio en el stack
        jr      ra    # Retornar de la función
main:    # Inicio de la función main
        addi    sp,sp,-8    # Reservar espacio en el stack
        sw      ra,4(sp)    # Guardar return address
        sw      s0,0(sp)    # Guardar frame pointer
        addi    s0,sp,8    # Configurar nuevo frame pointer
        sw      a5,0(s0)    # Guardar valor en variable a
        sw      a5,4(s0)    # Guardar valor en variable b
        sw      a5,8(s0)    # Guardar valor en variable r
        j       .L3    # Salto a etiqueta .L3
        lw      ra,4(sp)    # Restaurar return address
        lw      s0,0(sp)    # Restaurar frame pointer
        addi    sp,sp,8    # Liberar espacio en el stack
        jr      ra    # Retornar de la función