#include <stdio.h>
#include <stdlib.h>

// 矩陣轉置
void transpose(double *matrix, double *result, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[j * rows + i] = matrix[i * cols + j];
        }
    }
}

// 矩陣相加
void add(double *matrix1, double *matrix2, double *result, int rows, int cols) {
    for (int i = 0; i < rows * cols; i++) {
        result[i] = matrix1[i] + matrix2[i];
    }
}

// 矩陣相乘
void multiply(double *matrix1, double *matrix2, double *result, int rows1, int cols1, int cols2) {
    for (int i = 0; i < rows1; i++) {
        for (int j = 0; j < cols2; j++) {
            result[i * cols2 + j] = 0;
            for (int k = 0; k < cols1; k++) {
                result[i * cols2 + j] += matrix1[i * cols1 + k] * matrix2[k * cols2 + j];
            }
        }
    }
}

// 印出矩陣
void dump(double *matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%f ", matrix[i * cols + j]);
        }
        printf("\n");
    }
}

int main() {
    int rows1 = 2, cols1 = 3;
    int rows2 = 3, cols2 = 2;

    double matrix1[] = {1, 2, 3, 4, 5, 6};
    double matrix2[] = {7, 8, 9, 10, 11, 12};

    double transposed[cols1 * rows1];
    double sum[rows1 * cols1];
    double product[rows1 * cols2];

    printf("Matrix 1:\n");
    dump(matrix1, rows1, cols1);

    printf("Matrix 2:\n");
    dump(matrix2, rows2, cols2);

    transpose(matrix1, transposed, rows1, cols1);
    printf("Transposed Matrix 1:\n");
    dump(transposed, cols1, rows1);

    add(matrix1, matrix1, sum, rows1, cols1);
    printf("Sum of Matrix 1 and Matrix 1:\n");
    dump(sum, rows1, cols1);

    multiply(matrix1, matrix2, product, rows1, cols1, cols2);
    printf("Product of Matrix 1 and Matrix 2:\n");
    dump(product, rows1, cols2);

    return 0;
}
