# Compilador SmallC y Calculadora

Este proyecto implementa un compilador para un subconjunto del lenguaje C llamado SmallC, junto con una calculadora simple que demuestra su funcionamiento.

## Descripción General

El compilador SmallC está implementado en Python y utiliza PLY (Python Lex-Yacc) para el análisis léxico y sintáctico. El proyecto incluye:

1. Un compilador completo para SmallC
2. Una calculadora que demuestra el uso del compilador
3. Herramientas de análisis léxico, sintáctico y semántico
4. Generador de código C

## Componentes del Compilador

### 1. Analizador Léxico (lexer.py)
- Convierte el código fuente en tokens
- Reconoce:
  - Identificadores (variables y funciones)
  - Números enteros
  - Operadores (+, -, *, /, ==, !=, <, <=, >, >=)
  - Palabras reservadas (if, else, while, int, void, return)
  - Símbolos especiales ({, }, ;, etc.)

### 2. Analizador Sintáctico (parser.py)
- Convierte los tokens en un Árbol de Sintaxis Abstracta (AST)
- Implementa la gramática del lenguaje
- Maneja:
  - Declaraciones de variables y funciones
  - Expresiones aritméticas
  - Estructuras de control
  - Llamadas a funciones

### 3. Analizador Semántico (semantic.py)
- Verifica el significado del código
- Mantiene una tabla de símbolos
- Realiza comprobaciones de:
  - Variables no declaradas
  - Funciones no definidas
  - Ámbitos de variables
  - Tipos de datos

### 4. Generador de Código (codegen.py)
- Convierte el AST en código C válido
- Genera código manteniendo la estructura original
- Maneja la indentación y formato

## La Calculadora

La calculadora implementada demuestra el uso del compilador con un programa que realiza operaciones básicas:

```c
int main(void) {
    int a;
    int b;
    int suma;
    int resta;
    int multiplicacion;
    int division;
    
    a = 20;
    b = 5;
    
    suma = a + b;
    resta = a - b;
    multiplicacion = a * b;
    division = a / b;
    
    return suma;
}
```

### Características de la Calculadora
- Realiza las cuatro operaciones básicas:
  1. Suma (+)
  2. Resta (-)
  3. Multiplicación (*)
  4. División (/)
- Maneja números enteros
- Incluye manejo básico de errores (división por cero)

## Requisitos

- Python 3.6 o superior
- PLY (Python Lex-Yacc)
- GCC (para compilar el código C generado)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python3 -m venv venv
   ```
3. Activar el entorno virtual:
   ```bash
   source venv/bin/activate
   ```
4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Compilando un Programa SmallC

1. Crear un archivo con extensión `.sc` (por ejemplo, `calculadora.sc`)
2. Ejecutar el compilador:
   ```bash
   python main.py calculadora.sc
   ```
3. El compilador generará un archivo `.c` con el mismo nombre

### Ejecutando la Calculadora

1. Compilar el código C generado:
   ```bash
   gcc calculadora.c -o calculadora
   ```
2. Ejecutar el programa:
   ```bash
   ./calculadora
   ```

## Estructura del Proyecto

```
.
├── README.md
├── requirements.txt
├── main.py
├── lexer.py
├── parser.py
├── semantic.py
├── codegen.py
├── calculadora.sc
└── calculadora.c (generado)
```

## Limitaciones

- Solo soporta números enteros
- No soporta números de punto flotante
- No soporta arrays
- No soporta estructuras o uniones
- No soporta punteros
- No soporta directivas del preprocesador
- No soporta variables globales

## Ejemplos de Uso

### Ejemplo Simple
```c
int main(void) {
    int a;
    int b;
    int c;
    
    a = 10;
    b = 5;
    c = a + b;
    
    return c;
}
```

### Ejemplo con Múltiples Operaciones
```c
int main(void) {
    int a;
    int b;
    int suma;
    int resta;
    int multiplicacion;
    int division;
    
    a = 20;
    b = 5;
    
    suma = a + b;
    resta = a - b;
    multiplicacion = a * b;
    division = a / b;
    
    return suma;
}
```

## Solución de Problemas

### Errores Comunes

1. **Error de sintaxis**
   - Verificar que el código siga la gramática de SmallC
   - Asegurarse de que todas las declaraciones estén al inicio de cada bloque

2. **Error de compilación**
   - Verificar que todas las variables estén declaradas
   - Asegurarse de que los tipos de datos sean correctos

3. **Error de ejecución**
   - Verificar que no haya división por cero
   - Asegurarse de que los valores estén dentro del rango de enteros

## Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Hacer fork del repositorio
2. Crear una rama para tu característica
3. Hacer commit de tus cambios
4. Hacer push a la rama
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 