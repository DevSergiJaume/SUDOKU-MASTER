# Sudoku Master

## Descripción del Programa
Sudoku Master es una aplicación interactiva que permite a los usuarios resolver cualquier rompecabezas de Sudoku de manera automática mediante un algoritmo de **backtracking**. Este método de resolución explora posibles soluciones celda por celda, descartando aquellas combinaciones incorrectas hasta encontrar la solución completa.

El programa cuenta con una interfaz gráfica creada con **Pygame**, que facilita la interacción con el tablero. Los usuarios pueden introducir sus propios números antes de resolver el Sudoku, asegurándose de que el programa respete sus entradas originales.

## Funcionamiento del Código

### 1. Interfaz Inicial
- Al iniciar el programa, se muestra una pantalla con un título elegante, un botón para comenzar y un crédito del creador.
- Al hacer clic en **"Solve your Sudoku"**, el usuario accede al tablero.

### 2. Interacción con el Tablero
- El usuario puede hacer clic en una celda vacía e introducir un número del 1 al 9.
- Los números introducidos manualmente no podrán modificarse una vez iniciado el proceso de resolución.
- Si el ratón pasa sobre una celda, esta se resalta con un fondo azul claro. Si se selecciona una celda esta se mantiene colorida hasta introducir un numero

### 3. Resolución Automática
- Al presionar el botón **"Solve Sudoku"**, el algoritmo de **backtracking** comienza a resolver el tablero.
- Una vez completado el Sudoku, se muestra el mensaje **"SOLVE"** en una caja amarilla con letras rojas.

🌟 **¡Disfruta resolviendo Sudokus con Sudoku Master!** 🎯

