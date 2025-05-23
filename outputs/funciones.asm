.section .data    # Sección de datos globales
    # Variables globales si las hubiera

.section .text    # Sección de código
.globl main    # Declaración de la función main como global

cuadrado:    # Inicio de la función cuadrado
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro x en el stack
        lw      a5,0(s0)    # Cargar variable x
        mv      a4,a5    # Guardar primer operando
        lw      a5,0(s0)    # Cargar variable x
        mulw    a5,a4,a5    # Multiplicación de operandos
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función
suma_cuadrados:    # Inicio de la función suma_cuadrados
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        sw      a0,0(s0)    # Guardar parámetro a en el stack
        sw      a1,4(s0)    # Guardar parámetro b en el stack
        lw      a5,0(s0)    # Cargar variable a
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    cuadrado    # Llamar a función cuadrado
        mv      a5,a0    # Guardar resultado de la función
        mv      a4,a5    # Guardar primer operando
        lw      a5,4(s0)    # Cargar variable b
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    cuadrado    # Llamar a función cuadrado
        mv      a5,a0    # Guardar resultado de la función
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
        li      a5,3    # Cargar constante 3
        sw      a5,0(s0)    # Guardar valor en variable a
        li      a5,4    # Cargar constante 4
        sw      a5,4(s0)    # Guardar valor en variable b
        lw      a5,0(s0)    # Cargar variable a
        sw      a5,0(sp)    # Guardar primer argumento temporalmente
        lw      a5,4(s0)    # Cargar variable b
        mv      a1,a5    # Mover segundo argumento a a1
        lw      a0,0(sp)    # Cargar primer argumento en a0
        call    suma_cuadrados    # Llamar a función suma_cuadrados
        mv      a5,a0    # Guardar resultado de la función
        sw      a5,8(s0)    # Guardar valor en variable resultado
        lw      a5,8(s0)    # Cargar variable resultado
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función