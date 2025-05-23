// Funciones de entrada/salida
int putnum(int n) {
    return n;  // En una implementación real, esto imprimiría el número
}

int main() {
    int i;
    int j;
    int suma = 0;
    
    // Ciclos anidados para crear una matriz de multiplicación
    for (i = 1; i <= 5; i = i + 1) {
        for (j = 1; j <= 5; j = j + 1) {
            suma = suma + (i * j);
   }
    }
    

    // Otro ejemplo con while anidado
    i = 0;
    while (i < 3) {
        j = 0;
        while (j < 3) {
            j = j + 1;
        }
        i = i + 1;
    }
    
    return 0;
} 