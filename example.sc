int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main(void) {
    int x;
    int result;
    x = 5;
    result = factorial(x);
    if (result > 0) {
        return result;
    }
    return 0;
} 