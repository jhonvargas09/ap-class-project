#include<stdio.h>

int main()
{
  int firsNumber;
  int secondNumber;
  printf("ingrse primer valor: ");
  scanf("%d", &firsNumber);
    printf("ingrse segundo valor: ");
  scanf("%d", &secondNumber);
//operaciones..
int result1 = firsNumber + secondNumber;
int result2 = firsNumber * secondNumber;
int result3 = firsNumber / secondNumber;
int result4 = firsNumber - secondNumber;
//espacio...
printf("\n");
//resultados
  printf("resultado de sumar: %d\n", result1);
  printf("resultado de multiplicar: %d\n", result2);
  printf("resultado de dividir: %d\n", result3);
  printf("resultado de restar: %d\n", result4);

    return 0;
}