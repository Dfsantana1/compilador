int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main(void) {
    int n;
    int result;
    
    n = 6;
    result = fibonacci(n);
    return result;
} 