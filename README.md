# Compilador Small C a RISC-V

Este proyecto implementa un compilador que traduce código fuente escrito en Small C a código ensamblador RISC-V.

## Características

- Soporta tipos de datos `int` y `char`
- Maneja estructuras de control: `if`, `else`, `while`, `for`
- Variables globales a nivel de funciones
- Arreglos de tamaño constante
- Genera código ensamblador RISC-V compatible con [godbolt.org](https://godbolt.org)

## Requisitos

- Python 3.6 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd <nombre-del-directorio>
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

El compilador se ejecuta desde la línea de comandos:

```bash
python main.py <archivo_entrada.sc> <archivo_salida.asm>
```

### Ejemplo

1. Crear un archivo de entrada `program.sc`:
```c
int main() {
    char c = 'a';
    int x = 5;
    for(int i = 0; i < 10; i++) {
        if (x > 0) {
            return x;
        }
    }
    return 0;
}
```

2. Compilar el programa:
```bash
python main.py program.sc program.asm
```

3. El archivo `program.asm` contendrá el código ensamblador RISC-V generado.

## Estructura del Proyecto

- `lexer.py`: Implementa el analizador léxico
- `parser.py`: Implementa el analizador sintáctico
- `semantic.py`: Implementa el analizador semántico
- `codegen.py`: Implementa el generador de código RISC-V
- `main.py`: Punto de entrada del compilador

## Gramática Small C

La gramática implementada soporta:

- Declaraciones de variables y funciones
- Tipos de datos: `int` y `char`
- Operadores aritméticos: `+`, `-`, `*`, `/`
- Operadores relacionales: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Estructuras de control: `if`, `else`, `while`, `for`
- Arreglos de tamaño constante
- Llamadas a funciones

## Ejemplos

### Ejemplo 1: Factorial
```c
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int result = factorial(5);
    return result;
}
```

### Ejemplo 2: Array y Bucle
```c
int main() {
    int arr[5];
    int i;
    for(i = 0; i < 5; i++) {
        arr[i] = i * 2;
    }
    return arr[4];
}
```

## Verificación

El código ensamblador generado puede ser verificado en [godbolt.org](https://godbolt.org) seleccionando el compilador RISC-V.

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 