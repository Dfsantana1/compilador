.section .data    # Sección de datos globales
    # Variables globales si las hubiera

.section .text    # Sección de código
.globl main    # Declaración de la función main como global

factorial:    # Inicio de la función factorial
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro n en el stack
        lw      a5,0(s0)    # Cargar variable n
        mv      a4,a5    # Guardar primer operando
        li      a5,1    # Cargar constante 1
        slt     t0,a5,a4    # Comparación menor o igual que
        xori    a5,t0,1    # Invertir resultado
        sext.w  a4,a5    # Extender a 64 bits
        li      a5,0    # Cargar 0 en a5
        ble     a4,a5,.L1    # Comparar y saltar a .L1 si a4 <= a5
        j       .L2    # Salto a .L2
.L1:    # Inicio de la sección else
.L2:    # Fin de la sección if
        lw      a5,0(s0)    # Cargar variable n
        mv      a4,a5    # Guardar primer operando
        lw      a5,0(s0)    # Cargar variable n
        mv      a4,a5    # Guardar primer operando
        li      a5,1    # Cargar constante 1
        subw    a5,a4,a5    # Resta de operandos
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    factorial    # Llamar a función factorial
        mv      a5,a0    # Guardar resultado de la función
        mulw    a5,a4,a5    # Multiplicación de operandos
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
        li      a5,5    # Cargar constante 5
        sw      a5,0(s0)    # Guardar valor en variable n
        lw      a5,0(s0)    # Cargar variable n
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    factorial    # Llamar a función factorial
        mv      a5,a0    # Guardar resultado de la función
        sw      a5,4(s0)    # Guardar valor en variable result
        lw      a5,4(s0)    # Cargar variable result
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función