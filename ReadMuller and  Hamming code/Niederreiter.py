# -- КРИПТОСИСТЕМА НИДЕРРАЙТЕРА --
from common import *
from generationKeys import *
from HammingCode import *
from ReedMullerCode import *

# шифрование Нидеррайтера (c = m * H(pub)^T)
def encryptionVectorNiederreiter(inputVector, publicMatrix):
    return multiMatrices([inputVector], transposeMatrix(publicMatrix))[0]

# параметры кода Хэмминга в Нидеррайтере
def optionsNiederreiterHamming(r):
    # генерация проверочной матрицы
    checkMatrix = createCheckMatrixHamming(r)
    return checkMatrix, 1

# параметры кода Рида-Маллера в Нидеррайтере
def optionsNiederreiterReedMuller(m, r):
    # генерация проверочной матрицы
    checkMatrix = createMatrixReedMuller(m, m-r-1)
    t = 2 ** (m - r - 1) - 1
    return checkMatrix, t

# криптосистема Нидеррайтера
def cryptosystemNiederreiter(inputText, selectCode, settings):
    # вычисляем параметры для кода Хемминга
    if selectCode == 1:
        r = settings['Hamming']
        checkMatrix, t = optionsNiederreiterHamming(r)
    # вычисляем параметры для кода Рида-Маллера
    elif selectCode == 2:
        m, r = settings['ReedMuller']
        checkMatrix, t = optionsNiederreiterReedMuller(m, r)
        # построим таблицу синдромов и ошибок
        errorVectors = createTableSyndromeError(checkMatrix)
    # вычисляем ключи
    randomMatrix, permutationMatrix = generationPrivateKey(checkMatrix)
    publicCheckMatrix = generationPublicMatrix(randomMatrix, checkMatrix, permutationMatrix)

    n = len(checkMatrix[0])
    nk = len(checkMatrix)
    # увеличение размера текста до длины кратной t
    inputText = addSize(inputText, t)
    # шифрование вектора
    lengthInputText = len(inputText)
    encryptedText = []
    for i in range(0, lengthInputText, t):
        # формируем вектор весом t
        inputVector = [0] * n
        for j in range(t):
            inputVector[j] = inputText[i+j]
        encryptedText.extend(encryptionVectorNiederreiter(inputVector, publicCheckMatrix))
    # дешифрование вектора
    lengthEncryptedText = len(encryptedText)
    outputText = []
    decryptedText = []
    for i in range(0, lengthEncryptedText, nk):
        # вычисление синдрома s = c * (S^T)^-1
        syndrome = multiMatrices([encryptedText[i:i+nk]], reverseMatrix(transposeMatrix(randomMatrix)))[0]
        # для кодов Рида-Маллера    
        if selectCode == 2:
            errorVector = errorVectors[convertBinaryToDecimal(syndrome)]
        # для кодов Хэмминга
        else:
            errorVector = [0] * len(permutationMatrix)
            index = convertBinaryToDecimal(syndrome)
            if index != 0:
                errorVector[index - 1] = 1
        # получение информационного вектора e * P^-1
        decryptedText.extend(multiMatrices([errorVector], reverseMatrix(transposeMatrix(permutationMatrix)))[0])
    # извлечение t информационных бит
    lengthDecryptedText = len(decryptedText)
    for i in range(0, lengthDecryptedText, n):
        outputText += decryptedText[i:i+t]
    # вырезаем последний информационный блок и добавленные биты
    return outputText[:-convertBinaryToDecimal(outputText[-t:])-t]
