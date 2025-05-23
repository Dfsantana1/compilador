.section .data    # Sección de datos globales
    # Variables globales si las hubiera

.section .text    # Sección de código
.globl main    # Declaración de la función main como global

main:    # Inicio de la función main
        addi    sp,sp,-32    # Reservar espacio en el stack
        sd      ra,24(sp)    # Guardar return address
        sd      s0,16(sp)    # Guardar frame pointer
        addi    s0,sp,32    # Configurar nuevo frame pointer
        li      a5,10    # Cargar constante 10
        sw      a5,0(s0)    # Guardar valor en variable a
        li      a5,3    # Cargar constante 3
        sw      a5,4(s0)    # Guardar valor en variable b
        lw      a5,0(s0)    # Cargar variable a
        mv      a4,a5    # Guardar primer operando
        lw      a5,4(s0)    # Cargar variable b
        addw    a5,a4,a5    # Suma de operandos
        sw      a5,8(s0)    # Guardar valor en variable suma
        lw      a5,0(s0)    # Cargar variable a
        mv      a4,a5    # Guardar primer operando
        lw      a5,4(s0)    # Cargar variable b
        subw    a5,a4,a5    # Resta de operandos
        sw      a5,12(s0)    # Guardar valor en variable resta
        lw      a5,0(s0)    # Cargar variable a
        mv      a4,a5    # Guardar primer operando
        lw      a5,4(s0)    # Cargar variable b
        mulw    a5,a4,a5    # Multiplicación de operandos
        sw      a5,16(s0)    # Guardar valor en variable multiplicacion
        lw      a5,0(s0)    # Cargar variable a
        mv      a4,a5    # Guardar primer operando
        lw      a5,4(s0)    # Cargar variable b
        divw    a5,a4,a5    # División de operandos
        sw      a5,20(s0)    # Guardar valor en variable division
        lw      a5,8(s0)    # Cargar variable suma
        mv      a4,a5    # Guardar primer operando
        lw      a5,12(s0)    # Cargar variable resta
        addw    a5,a4,a5    # Suma de operandos
        mv      a4,a5    # Guardar primer operando
        lw      a5,16(s0)    # Cargar variable multiplicacion
        addw    a5,a4,a5    # Suma de operandos
        mv      a4,a5    # Guardar primer operando
        lw      a5,20(s0)    # Cargar variable division
        addw    a5,a4,a5    # Suma de operandos
        mv      a0,a5    # Mover resultado a a0
        j       .L3    # Salto a etiqueta .L3
        ld      ra,24(sp)    # Restaurar return address
        ld      s0,16(sp)    # Restaurar frame pointer
        addi    sp,sp,32    # Liberar espacio en el stack
        jr      ra    # Retornar de la función