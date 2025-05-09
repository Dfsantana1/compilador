int suma(int a, int b) {
    return a + b;
}

int resta(int a, int b) {
    return a - b;
}

int multiplicacion(int a, int b) {
    return a * b;
}

int division(int a, int b) {
    if (b == 0) {
        return 0;  // Division por cero
    }
    return a / b;
}

int main(void) {
    int a;
    int b;
    int suma;
    int resta;
    int multiplicacion;
    int division;
    
    a = 20;
    b = 5;
    
    suma = a + b;
    resta = a - b;
    multiplicacion = a * b;
    division = a / b;
    
    return suma;
} 