from common import convertDecimalToBinary, convertBinaryToDecimal
from McEliece import cryptosystemMcEliece
from Niederreiter import cryptosystemNiederreiter

# основные настройки скрипта
SETTINGS_FILE = 'settings\\settings.txt'

# загрузка настроек для функций
with open(SETTINGS_FILE) as file:
    settings = eval(file.read())


inputText = input("Введите текс: ")
# перевод текста в бинарный вектор
binText = []
for symbol in inputText:
    binText.extend(convertDecimalToBinary(ord(symbol), 8))

selectCryptosystem = int(input('Выберите способ кодирования:\n1)Мак-Элиса\n2)Нидеррайтера\n'))
selectCode = int(input('Выберите код:\n1)Код Хемминга\n2)Код Рида-Маллера\n'))

# криптосистема Мак-Элиса
if selectCryptosystem == 1:
    binDecryptedText = cryptosystemMcEliece(binText, selectCode, settings["McEliece"])
# криптосистема Нидеррайтера
elif selectCryptosystem == 2:
    binDecryptedText = cryptosystemNiederreiter(binText, selectCode, settings["Niederreiter"])

# перевод бинарного вектора в символьный текст
lengthDecryptedText = len(binDecryptedText)
outputText = ''
for i in range(0, lengthDecryptedText, 8):
    outputText += chr(convertBinaryToDecimal(binDecryptedText[i:i+8]))

print('Раскодированный текст:', outputText)
