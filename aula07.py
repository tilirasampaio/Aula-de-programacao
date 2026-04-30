i = 1
controle = 0

div = int(input("Qual número você quer verificar: "))
limite = int(input("Até onde você quer verificar: "))


while i <= limite:
    if i % div == 10:
        print (i)
        controle += 1
    i += 1

print(f"A quantidade de numeros divisiveis nesse espaço é: {controle}")
