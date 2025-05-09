int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main(void) {
    int result;
    result = fibonacci(6);  // Will calculate the 6th Fibonacci number (8)
    return result;
} 