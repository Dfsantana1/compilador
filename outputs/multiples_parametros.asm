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
promedio:    # Inicio de la función promedio
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro a en el stack
        sw      a1,4(s0)    # Guardar parámetro b en el stack
        sw      a1,8(s0)    # Guardar parámetro c en el stack
        sw      a1,12(s0)    # Guardar parámetro d en el stack
        sw      a1,16(s0)    # Guardar parámetro e en el stack
        lw      a5,0(s0)    # Cargar variable a
        mv      a4,a5    # Guardar primer operando
        lw      a5,4(s0)    # Cargar variable b
        addw    a5,a4,a5    # Suma de operandos
        mv      a4,a5    # Guardar primer operando
        lw      a5,8(s0)    # Cargar variable c
        addw    a5,a4,a5    # Suma de operandos
        mv      a4,a5    # Guardar primer operando
        lw      a5,12(s0)    # Cargar variable d
        addw    a5,a4,a5    # Suma de operandos
        mv      a4,a5    # Guardar primer operando
        lw      a5,16(s0)    # Cargar variable e
        addw    a5,a4,a5    # Suma de operandos
        mv      a4,a5    # Guardar primer operando
        li      a5,5    # Cargar constante 5
        divw    a5,a4,a5    # División de operandos
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función
maximo:    # Inicio de la función maximo
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro a en el stack
        sw      a1,4(s0)    # Guardar parámetro b en el stack
        sw      a1,8(s0)    # Guardar parámetro c en el stack
        sw      a1,12(s0)    # Guardar parámetro d en el stack
        lw      a5,0(s0)    # Cargar variable a
        sw      a5,16(s0)    # Guardar valor en variable max
        lw      a5,4(s0)    # Cargar variable b
        mv      a4,a5    # Guardar primer operando
        lw      a5,16(s0)    # Cargar variable max
        slt     a5,a5,a4    # Comparación mayor que
        sext.w  a4,a5    # Extender a 64 bits
        li      a5,0    # Cargar 0 en a5
        ble     a4,a5,.L1    # Comparar y saltar a .L1 si a4 <= a5
        lw      a5,4(s0)    # Cargar variable b
        sw      a5,16(s0)    # Guardar valor en variable max
        j       .L2    # Salto a .L2
.L1:    # Inicio de la sección else
.L2:    # Fin de la sección if
        lw      a5,8(s0)    # Cargar variable c
        mv      a4,a5    # Guardar primer operando
        lw      a5,16(s0)    # Cargar variable max
        slt     a5,a5,a4    # Comparación mayor que
        sext.w  a4,a5    # Extender a 64 bits
        li      a5,0    # Cargar 0 en a5
        ble     a4,a5,.L3    # Comparar y saltar a .L3 si a4 <= a5
        lw      a5,8(s0)    # Cargar variable c
        sw      a5,16(s0)    # Guardar valor en variable max
        j       .L4    # Salto a .L4
.L3:    # Inicio de la sección else
.L4:    # Fin de la sección if
        lw      a5,12(s0)    # Cargar variable d
        mv      a4,a5    # Guardar primer operando
        lw      a5,16(s0)    # Cargar variable max
        slt     a5,a5,a4    # Comparación mayor que
        sext.w  a4,a5    # Extender a 64 bits
        li      a5,0    # Cargar 0 en a5
        ble     a4,a5,.L5    # Comparar y saltar a .L5 si a4 <= a5
        lw      a5,12(s0)    # Cargar variable d
        sw      a5,16(s0)    # Guardar valor en variable max
        j       .L6    # Salto a .L6
.L5:    # Inicio de la sección else
.L6:    # Fin de la sección if
        lw      a5,16(s0)    # Cargar variable max
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función
combinacion_lineal:    # Inicio de la función combinacion_lineal
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro x en el stack
        sw      a1,4(s0)    # Guardar parámetro y en el stack
        sw      a1,8(s0)    # Guardar parámetro z en el stack
        sw      a1,12(s0)    # Guardar parámetro a en el stack
        sw      a1,16(s0)    # Guardar parámetro b en el stack
        sw      a1,20(s0)    # Guardar parámetro c en el stack
        lw      a5,12(s0)    # Cargar variable a
        mv      a4,a5    # Guardar primer operando
        lw      a5,0(s0)    # Cargar variable x
        mulw    a5,a4,a5    # Multiplicación de operandos
        mv      a4,a5    # Guardar primer operando
        lw      a5,16(s0)    # Cargar variable b
        mv      a4,a5    # Guardar primer operando
        lw      a5,4(s0)    # Cargar variable y
        mulw    a5,a4,a5    # Multiplicación de operandos
        addw    a5,a4,a5    # Suma de operandos
        mv      a4,a5    # Guardar primer operando
        lw      a5,20(s0)    # Cargar variable c
        mv      a4,a5    # Guardar primer operando
        lw      a5,8(s0)    # Cargar variable z
        mulw    a5,a4,a5    # Multiplicación de operandos
        addw    a5,a4,a5    # Suma de operandos
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
        li      a5,10    # Cargar constante 10
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        li      a5,20    # Cargar constante 20
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,30    # Cargar constante 30
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,40    # Cargar constante 40
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,50    # Cargar constante 50
        mv      a1,a5    # Mover segundo argumento a a1
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    promedio    # Llamar a función promedio
        mv      a5,a0    # Guardar resultado de la función
        sw      a5,0(s0)    # Guardar valor en variable resultado
        li      a5,5    # Cargar constante 5
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        li      a5,8    # Cargar constante 8
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,3    # Cargar constante 3
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,9    # Cargar constante 9
        mv      a1,a5    # Mover segundo argumento a a1
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    maximo    # Llamar a función maximo
        mv      a5,a0    # Guardar resultado de la función
        sw      a5,0(s0)    # Guardar valor en variable resultado
        li      a5,2    # Cargar constante 2
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        li      a5,3    # Cargar constante 3
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,4    # Cargar constante 4
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,1    # Cargar constante 1
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,2    # Cargar constante 2
        mv      a1,a5    # Mover segundo argumento a a1
        li      a5,3    # Cargar constante 3
        mv      a1,a5    # Mover segundo argumento a a1
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    combinacion_lineal    # Llamar a función combinacion_lineal
        mv      a5,a0    # Guardar resultado de la función
        sw      a5,0(s0)    # Guardar valor en variable resultado
        lw      a5,0(s0)    # Cargar variable resultado
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función