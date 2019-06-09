# -- КОД ХЕММИНГА --
from common import transposeMatrix, convertDecimalToBinary

# создание проверочной матрицы
def createCheckMatrixHamming(r):
    n = 2**r - 1
    result = [[] for i in range(n)]
    for i in range(n):
        result[i] = convertDecimalToBinary(i + 1, r)
    return transposeMatrix(result)

# приведение порождающей матрицы к систематическому виду перестановкой столбцов
def transformationCheckSysMatrixHamming(checkMatrix):
    checkSysMatrix = transposeMatrix(checkMatrix)
    r = len(checkSysMatrix[0])
    n = len(checkSysMatrix)
    # строки с индесом = 2**i(единичные) перемещаем в конец
    for i in range(r):
        checkSysMatrix[2**i - 1], checkSysMatrix[n - i - 1] = checkSysMatrix[n - i - 1], checkSysMatrix[2**i - 1]
    return transposeMatrix(checkSysMatrix)

# создание порождающей систематической матрицы
def createGenerSysMatrixHamming(checkSysMatrix):
    r = len(checkSysMatrix)
    n = len(checkSysMatrix[0])
    result = [[0]*n for i in range(n - r)]
    # создание единичной подматрицы
    for i in range(n - r):
        result[i][i] = 1
    # создание информационной подматрицы P
    for i in range(r):
        for j in range(n - r):
            result[j][i + n - r] = checkSysMatrix[i][j]
    return result
