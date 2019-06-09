# -- КРИПТОСИСТЕМА МАК-ЭЛИСА --
from random import randint
from common import *
from generationKeys import *
from HammingCode import *
from ReedMullerCode import *

# генерация случайного вектора длины n и веса t
def generatingRandomVector(n, t):
    result = [0]*n
    for i in range(t):
        index = randint(0, n - 1)
        while result[index] != 0:
            index = randint(0, n - 1)
        result[index] = 1
    return result

# шифрование вектора Мак-Элиса (c = m * G(pub) + z)
def encryptionVectorMcEliece(inputVector, publicMatrix, randomVector):
    encryptedVector = multiMatrices([inputVector], publicMatrix)[0]
    return summatorVectors(encryptedVector, randomVector)

# вычисление параметров кода Хемминга в Мак-Элисе
def optionsMcElieceHamming(r):
    # создаем проверочную систематическую матрицы
    checkMatrix = transformationCheckSysMatrixHamming(createCheckMatrixHamming(r))
    # создаем порождающую систематическую матрицу
    generatMatrix = createGenerSysMatrixHamming(checkMatrix)
    return generatMatrix, checkMatrix, 1

# вычисление параметров кода Рида-Маллера в Мак-Элисе
def optionsMcElieceReedMuller(m, r):
    # создание порождающей матрицы
    generatMatrix = createMatrixReedMuller(m, r)
    # создание проверочной матрицы
    checkMatrix = createMatrixReedMuller(m, m-r-1)
    t = 2 ** (m - r - 1) - 1
    return generatMatrix, checkMatrix, t

# криптосистема Мак-Элиса
def cryptosystemMcEliece(inputText, selectCode, settings):
    # вычисяем параметры для кода Хемминга
    if selectCode == 1:
        r = settings['Hamming']
        generatMatrix, checkMatrix, t = optionsMcElieceHamming(r)
    # вычисляем параметры для кода Рида-Маллера
    elif selectCode == 2:
        m, r = settings['ReedMuller']
        generatMatrix, checkMatrix, t = optionsMcElieceReedMuller(m, r)
    print('G = ')#!
    [print(e) for e in generatMatrix]#!
    # вычисляем ключи
    randomMatrix, permutationMatrix = generationPrivateKey(generatMatrix)
    publicGeneratMatrix = generationPublicMatrix(randomMatrix, generatMatrix, permutationMatrix)
    # вычисляем информационные и кодовые слова
    infoVectors, codeVectors = createTableInfoCode(generatMatrix)
    # находим вектора ошибок
    errorVectors = createTableSyndromeError(checkMatrix)
    k = len(generatMatrix)
    n = len(generatMatrix[0])
    # увеличиваем размер текста до длины кратной k
    inputText = addSize(inputText, k)
    # шифрование вектора
    lengthInputText = len(inputText)
    encryptedText = []
    for i in range(0, lengthInputText, k):
        randomVector = generatingRandomVector(n, t)
        encryptedText.extend(encryptionVectorMcEliece(inputText[i:i+k], publicGeneratMatrix, randomVector))
    # дешифрование вектора
    lengthEncryptedText = len(encryptedText)
    decryptedText = []
    for i in range(0, lengthEncryptedText, n):
        # вычисление вектор v = c * P^-1
        vector = multiMatrices([encryptedText[i:i+n]], reverseMatrix(permutationMatrix))[0]
        # вычисляем синдром s = v * H^T
        syndrome = multiMatrices([vector], transposeMatrix(checkMatrix))[0]
        # вычисляем кодовое слово c = v + e
        codeVector = summatorVectors(vector, errorVectors[convertBinaryToDecimal(syndrome)])
        # находим информационный вектор
        infoVector = infoVectors[codeVectors.index(codeVector)]
        # вычисляем m * S^-1
        decryptedText.extend(multiMatrices([infoVector], reverseMatrix(randomMatrix))[0])
    # вырезаем последний информационный блок и добавленные биты
    return decryptedText[:-convertBinaryToDecimal(decryptedText[-k:])-k]
