int main() {
    int i = 0;
    int suma = 0;
    
    // While loop
    while (i < 5) {
        suma = suma + i;
        i = i + 1;
    }
    putnum(suma);  // Debería imprimir 10
    
    // If-else
    if (suma > 5) {
        putnum(1);  // Debería imprimir 1
    } else {
        putnum(0);
    }
    
    // For loop
    suma = 0;
    for (i = 0; i < 5; i = i + 1) {
        if (i % 2 == 0) {
            suma = suma + i;
        }
    }
    putnum(suma);  // Debería imprimir 6 (0 + 2 + 4)
    
    return 0;
} 