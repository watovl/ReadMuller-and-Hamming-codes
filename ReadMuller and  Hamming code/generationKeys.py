# -- ГЕНЕРАЦИЯ КЛЮЧА В КРИПТОСИСТЕМАХ --
from random import randint
from common import multiMatrices, matrixDeterminant

# генерация рандомной матрицы S
def generationRandomMatrix(size):
    return [[randint(0, 1) for i in range(size)] for j in range(size)]

# генерация матрицы перестановок P
def generationPermutationMatrix(size):
    result = [[0] * size for i in range(size)]
    for i in range(size):
        # подбирать пустую строчку
        index = randint(0, size - 1)
        while result[index].count(1):
            index = randint(0, size - 1)
        result[index][i] = 1
    return result

# генерация закрытого ключа
def generationPrivateKey(sourceMatrix):
    height = len(sourceMatrix) # количество строк
    length = len(sourceMatrix[0]) # количество столбцов
    # генерация случайной невырожденной матрицы S
    randomMatrix = generationRandomMatrix(height)
    while matrixDeterminant(randomMatrix) == 0:
        randomMatrix = generationRandomMatrix(height)
    # генерация матрицы перестановок P
    permutationMatrix = generationPermutationMatrix(length)
    return (randomMatrix, permutationMatrix)

# M(pub)=S*M*P
def generationPublicMatrix(randomMatrix, sourceMatrix, permutMatrix):
    return multiMatrices(multiMatrices(randomMatrix, sourceMatrix), permutMatrix)
