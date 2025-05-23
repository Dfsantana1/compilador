.section .data    # Sección de datos globales
    # Variables globales si las hubiera

.section .text    # Sección de código
.globl main    # Declaración de la función main como global

main:    # Inicio de la función main
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        li      a5,0    # Cargar constante 0
        sw      a5,0(s0)    # Guardar valor en variable suma
.L1:    # Inicio de la sección for
        mv      a4,a5    # Guardar primer operando
        li      a5,5    # Cargar constante 5
        slt     a5,a4,a5    # Comparación menor que
        sext.w  a4,a5    # Extender a 64 bits
        li      a5,0    # Cargar 0 en a5
        ble     a4,a5,.L2    # Comparar y saltar a .L2 si a4 <= a5
        mv      a4,a5    # Guardar primer operando
        li      a5,1    # Cargar constante 1
        addw    a5,a4,a5    # Suma de operandos
        j       .L1    # Salto a .L1
.L2:    # Fin de la sección for
        lw      a5,0(s0)    # Cargar variable suma
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función