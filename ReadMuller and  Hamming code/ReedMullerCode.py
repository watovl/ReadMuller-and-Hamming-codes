# -- КОД РИДА-МАЛЛЕРА --
from common import *

# создание информационной матрицы
def createInfoMatrix(m):
    n = 2**m
    result = [[] for i in range(n)]
    for i in range(n):
        result[i] = convertDecimalToBinary(i, m)
    return transposeMatrix(result)

# создание порождающей матрицы
def createMatrixReedMuller(m, r):
    n = 2 ** m
    result = [[1] * n]
    if r > 0:
        result.extend(createInfoMatrix(m))
        # создание подматрицы умножением векторов
        for count in range(1, r):
            tempMatrix = []
            end = 2
            for i in range(m - count):
                for j in range(1, end):
                    tempMatrix = [multiVectors(result[m-i-count], result[-j])] + tempMatrix
                end += count
            result.extend(tempMatrix)
    return result
