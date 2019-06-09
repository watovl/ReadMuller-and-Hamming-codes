# -- ОБЩИЕ ФУНКЦИИ РАБОТЫ С МАТРИЦА И ВЕКТОРАМИ --
from copy import deepcopy

# перевод из 2-ичной СС в 10-ную СС
def convertBinaryToDecimal(vector):
    length = len(vector)
    value = 0
    for i in range(length):
        value += vector[length-i-1] * 2 ** i
    return value

# перевод 10-ичного числа в 2-ичное
def convertDecimalToBinary(value, length):
    vector = []
    for i in range(length):
        vector = [value // 2 ** i % 2] + vector
    return vector

# увеличение текста до нужной длины и добавляем информационный блок
def addSize(vector, length):
    count = 0
    # пока длина текста не кратна length добавляем 0
    while len(vector) % length:
        vector += [0]
        count += 1
    # добавляем блок с информацией о количестве добавлений
    vector += convertDecimalToBinary(count, length)
    return vector

# определитель матрицы
def matrixDeterminant(inputMatrix):
    matrix = deepcopy(inputMatrix)
    length = len(matrix)
    for i in range(length):
        # если коэффициент нулевой, находим единичный
        if matrix[i][i] == 0:
            j = i + 1
            while j < length and matrix[j][i] == 0:
                j += 1
            if j != length:
                matrix[i], matrix[j] = matrix[j], matrix[i]
        # зануление элементов столбца ниже данного [i][i]
        for j in range(i+1, length):
            multiplier = matrix[j][i]
            for k in range(length):
                matrix[j][k] = matrix[j][k] ^ multiplier * matrix[i][k]
    # вычисление определителя
    determinant = 1
    for i in range(length):
        determinant *= matrix[i][i]
    return determinant

# умножение матриц
def multiMatrices(firstMatrix, secondMatrix):
    length = len(secondMatrix[0])
    height = len(firstMatrix)
    tempLength = len(secondMatrix)
    result = [[0] * length for i in range(height)]
    for i in range(height):
        for j in range(length):
            for k in range(tempLength):
                result[i][j] ^= firstMatrix[i][k] * secondMatrix[k][j]
    return result

# суммирование векторов
def summatorVectors(firstVector, secondVector):
    length = len(firstVector)
    result = [0] * length
    for i in range(length):
        result[i] = firstVector[i] ^ secondVector[i]
    return result

# умножение векторов
def multiVectors(firstVector, secondVector):
    length = len(firstVector)
    result = [0] * length
    for i in range(length):
        result[i] = firstVector[i] * secondVector[i]
    return result

# транспонирование матрицы
def transposeMatrix(matrix):
    length = len(matrix)
    height = len(matrix[0])
    result = [[0] * length for i in range(height)]
    for i in range(height):
        for j in range(length):
            result[i][j] = matrix[j][i]
    return result

# обратная матрица (методом Гаусса)
def reverseMatrix(inputMatrix):
    matrix = deepcopy(inputMatrix)
    length = len(matrix)
    result = [[0]*length for i in range(length)]
    for i in range(length):
        result[i][i] = 1
    for i in range(length):
        # если коэффициент нулевой, находим единичный
        if matrix[i][i] == 0:
            j = i + 1
            while matrix[j][i] == 0:
                j += 1
            matrix[i], matrix[j] = matrix[j], matrix[i]
            result[i], result[j] = result[j], result[i]
        # зануление элементов столбца ниже данного [i][i]
        for j in range(i+1, length):
            multiplier = matrix[j][i]
            for k in range(length):
                matrix[j][k] = matrix[j][k] ^ multiplier * matrix[i][k]
                result[j][k] = result[j][k] ^ multiplier * result[i][k]
        # зануление элементов столбца выше данного [i][i]
        for j in range(i):
            multiplier = matrix[j][i]
            for k in range(length):
                matrix[j][k] = matrix[j][k] ^ multiplier * matrix[i][k]
                result[j][k] = result[j][k] ^ multiplier * result[i][k]
    return result

# создание таблицы информационных и кодовых слов
def createTableInfoCode(genMatrix):
    n = len(genMatrix[0])
    k = len(genMatrix)
    count = 2 ** k
    infoVector = [[] for i in range(count)]
    codeVector = [[0]*n for i in range(count)]
    for i in range(count):
        # создание информационного вектора
        infoVector[i] = convertDecimalToBinary(i, k)
        # создание кодового вектора
        for j in range(n):
            for l in range(k):
                codeVector[i][j] ^= infoVector[i][l] * genMatrix[l][j]
    return infoVector, codeVector

# создание таблицы синдромов и векторов ошибок
def createTableSyndromeError(checkMatrix):
    transCheckMatrix = transposeMatrix(checkMatrix)
    n = len(transCheckMatrix)
    m = len(transCheckMatrix[0])
    length = 2 ** m
    count = 2 ** n
    errorVector = [[] for i in range(length)]
    for i in range(count):
        # формирование вектора ошибок
        tempErrorVector = convertDecimalToBinary(i, n)
        # вычисляем синдром s = e * H^T
        tempSyndrome = multiMatrices([tempErrorVector], transCheckMatrix)[0]
        index = convertBinaryToDecimal(tempSyndrome)
        # если данный синдром образовался впервые
        if errorVector[index] == []:
            errorVector[index] = tempErrorVector
        # если вес данного вектора ошибок меньше имеющегося
        if tempErrorVector.count(0) > errorVector[index].count(0):
            errorVector[index] = tempErrorVector
    return errorVector
