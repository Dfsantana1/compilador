// Funciones de entrada/salida
int putnum(int n) {
    return n;  // En una implementación real, esto imprimiría el número
}

int main() {
    int i;
    int j;
    int suma = 0;
    
    // Ciclos anidados para crear una matriz de multiplicación
    i = 1;
    while (i <= 5) {
        j = 1;
        while (j <= 5) {
            suma = suma + (i * j);
            j = j + 1;
        }
        i = i + 1;
    }
    
    // Otro ejemplo con while anidado
    i = 0;
    while (i < 3) {
        j = 0;
        while (j < 3) {
            suma = suma + (i + j);
            j = j + 1;
        }
        i = i + 1;
    }
    
    return suma;  // Retorna la suma total
} 