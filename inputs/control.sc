int main() {
    int i = 0;
    int suma = 0;
    
    // While loop
    while (i < 5) {
        suma = suma + i;
        i = i + 1;
    }
    
    // If-else
    if (suma > 5) {
        suma = suma + 1;
    } else {
        suma = suma - 1;
    }
    
    // For loop
    for (i = 0; i < 5; i = i + 1) {
        if (i % 2 == 0) {
            suma = suma + i;
        }
    }
    
    return suma;  // Retorna la suma final
} 