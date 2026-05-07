def soma (num1, num2) :
    resultado = num1 + num2
    print(resultado)

def subtracao (num1, num2) :
    resultado = num1 - num2
    print(resultado)

def multiplicacao(num1, num2):
    resultado = num1 * num2
    print(resultado)

def divisao(num1, num2):
    resultado = num1 / num2
    print(resultado)

def potencia(num1, num2):
    resultado = num1 ** num2
    print(resultado)


opcao = input("qual operação você quer fazer :")
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))

if opcao == "soma" :
    soma(num1, num2)

elif opcao == "subtração" :
    subtracao(num1, num2)

elif opcao == "multiplicação" :
    multiplicacao(num1, num2)

elif opcao == "divisão" :
    divisao(num1, num2)

elif opcao == "potência" :
    potencia(num1, num2)

else :
    print("Não sei fazer ")