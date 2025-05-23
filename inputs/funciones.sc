int cuadrado(int x) {
    return x * x;
}

int suma_cuadrados(int a, int b) {
    return cuadrado(a) + cuadrado(b);
}

int main() {
    int a = 3;
    int b = 4;
    int resultado = suma_cuadrados(a, b);
  return resultado;
} 