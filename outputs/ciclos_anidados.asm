.section .data    # Sección de datos globales
    # Variables globales si las hubiera

.section .text    # Sección de código
.globl main    # Declaración de la función main como global

putnum:    # Inicio de la función putnum
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro n en el stack
        lw      a5,0(s0)    # Cargar variable n
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función
main:    # Inicio de la función main
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        li      a5,0    # Cargar constante 0
        sw      a5,8(s0)    # Guardar valor en variable suma
        li      a5,1    # Cargar constante 1
        sw      a5,0(s0)    # Guardar valor en variable i
.L1:    # Inicio de la sección while
        lw      a5,0(s0)    # Cargar variable i
        mv      a4,a5    # Guardar primer operando
        li      a5,5    # Cargar constante 5
        slt     t0,a5,a4    # Comparación menor o igual que
        xori    a5,t0,1    # Invertir resultado
        sext.w  a4,a5    # Extender a 64 bits
        li      a5,0    # Cargar 0 en a5
        ble     a4,a5,.L2    # Comparar y saltar a .L2 si a4 <= a5
        j       .L1    # Salto a .L1
.L2:    # Fin de la sección while
        li      a5,0    # Cargar constante 0
        sw      a5,0(s0)    # Guardar valor en variable i
.L3:    # Inicio de la sección while
        lw      a5,0(s0)    # Cargar variable i
        mv      a4,a5    # Guardar primer operando
        li      a5,3    # Cargar constante 3
        slt     a5,a4,a5    # Comparación menor que
        sext.w  a4,a5    # Extender a 64 bits
        li      a5,0    # Cargar 0 en a5
        ble     a4,a5,.L4    # Comparar y saltar a .L4 si a4 <= a5
        j       .L3    # Salto a .L3
.L4:    # Fin de la sección while
        lw      a5,8(s0)    # Cargar variable suma
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función