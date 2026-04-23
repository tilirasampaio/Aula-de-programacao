i = 0

while i<=100:
    j = i
    controle = 0
    while j > 0:
        if i%j == 0:
            controle += 1
        if controle == 2:
            print (i)
        j -= 1
      
        
i += 1