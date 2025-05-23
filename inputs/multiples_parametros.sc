// Funciones de entrada/salida
int putnum(int n) {
    return n;  // En una implementación real, esto imprimiría el número
}

// Función que calcula el promedio de 5 números
int promedio(int a, int b, int c, int d, int e) {
    return (a + b + c + d + e) / 5;
}

// Función que encuentra el máximo de 4 números
int maximo(int a, int b, int c, int d) {
    int max = a;
    if (b > max) max = b;
    if (c > max) max = c;
    if (d > max) max = d;
    return max;
}

// Función que calcula una combinación lineal de 3 números
int combinacion_lineal(int x, int y, int z, int a, int b, int c) {
    return (a * x) + (b * y) + (c * z);
}

int main() {
    int resultado;
    
    // Prueba de promedio
    resultado = promedio(10, 20, 30, 40, 50);
    
    // Prueba de máximo
    resultado = maximo(5, 8, 3, 9);
    
    // Prueba de combinación lineal
    resultado = combinacion_lineal(2, 3, 4, 1, 2, 3);
    
    return resultado;  // Retorna el último resultado calculado
} 