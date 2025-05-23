int main() {
    int suma = 0;
    
    // For loop that adds numbers from 0 to 4
    for (int i = 0; i < 5; i = i + 1) {
        suma = suma + i;
    }
    
    return suma;  // Should return 10 (0+1+2+3+4)
} 