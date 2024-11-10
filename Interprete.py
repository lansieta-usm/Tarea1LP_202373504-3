import re

file_name = 'codigo.txt'

definidas = [] #Lista que almacena a todas las variables que se definan en 'codigo.txt'

ints = {}
strings = {}
bools = {}
#Estos diccionarios siguen el siguiente esquema: (Llave: Valor) = (Variable: Valor_Variable). Para cada tipo de dato hay un diccionario dedicado
se_ejecutan = {} #Este diccionario solo actúa si el archivo posee condicionales. Sigue el esquema (Clave: Valor) = (Numero_de_Linea: Condicional), donde Condicional corresponde a True o False, dependiendo si cierto 'if' (y su código asociado) tiene una condicion verdadera o falsa

def linea_correcta(linea): #Verifica si cierta linea de 'codigo.txt' tiene correcta su sintaxis. Si es correcta retorna la operación correspondiente a la linea. Sino, retorna False
    struct_declaracion_variables = r'(\ )*DEFINE(\ )+\$_[A-Z][A-Za-z]*$'
    struct_asig = r'(\ )*DP(\ )+\$_[A-Z][A-Za-z]*(\ )+ASIG(\ )+([-]?(0|[1-9]\d*)|True|False|\#.*\#)$'
    struct_suma = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+\+(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))'
    struct_multiplicacion = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+\*(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))'
    struct_mayor_que = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+\>(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))'
    struct_igual_que = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+\=\=(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))'
    struct_mostrar = r'(\ )*MOSTRAR(\ )*\((\ )*\$_[A-Z][A-Za-z]*(\ )*\)'
    struct_if = r'(\ )*if(\ )*\(\$_[A-Z][A-Za-z]*\)(\ )*\{'
    struct_else = r'(\ )*\}(\ )*else(\ )*\{'
    struct_corchete = r'(\ )*\}'

    if re.match(struct_declaracion_variables, linea):
        return 'Declaración de variables'
    elif re.match(struct_asig, linea):
        return 'Asignación'
    elif re.match(struct_suma, linea):
        return 'Suma'
    elif re.match(struct_multiplicacion, linea):
        return 'Multiplicación'
    elif re.match(struct_mayor_que, linea):
        return 'Mayor que'
    elif re.match(struct_igual_que, linea):
        return 'Igual que'
    elif re.match(struct_mostrar, linea):
        return 'Mostrar'
    elif re.match(struct_if, linea):
        return 'If'
    elif re.match(struct_else, linea):
        return 'Else'
    elif re.match(struct_corchete, linea):
        return 'Corchete'
    else:
        return False

def variables_definidas(linea): #Guarda en la lista 'definidas' todas las variables que se definan en cada linea correspondiente de 'codigo.txt', si encuentra que una variable se está definiendo dos veces, retorna 'Variable ya definida'
    if 'DEFINE' in linea:
        pos = linea.find('$')
        definida = linea[pos:-1]
        if definida in definidas:
            return 'Variable ya definida'
        else:
            definidas.append(definida)
    return 'Pasó'

def datatype(linea): #Determina si el tipo de dato asignado a una variable PREVIAMENTE DEFINIDA es bool/int/string y guarda su valor en el diccionario correspondiente. Retorna el tipo de dato que es la variable y en caso de que a una variable no definida se le asigne un valor, retorna ´Variable no definida´
    i=0
    asig_int = r'(\ )*DP(\ )+\$_[A-Z][A-Za-z]*(\ )+ASIG(\ )+([-]?(0|[1-9]\d*))$'
    asig_bool_mayor_que = r'(\ )*DP(\ )+\$_[A-Z][A-Za-z]*(\ )+(\>(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))))'
    #asig_bool_mayor_que = r'(\ )*DP(\ )+\$_[A-Z][A-Za-z]*(\ )+((ASIG (True|False))|\>(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))))'
    asig_bool_strings = r'(\ )*DP(\ )+\$_[A-Z][A-Za-z]*(\ )+(\=\=(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#)))'
    #asig_bool_strings = r'(\ )*DP(\ )+\$_[A-Z][A-Za-z]*(\ )+((ASIG (True|False))|\=\=(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#)))'
    asig_string = r'(\ )*DP(\ )+\$_[A-Z][A-Za-z]*(\ )+ASIG(\ )+(\#.*\#)$'
    asig_suma = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+\+(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))'
    asig_multiplicacion = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+\*(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))'

    if re.match(asig_int, linea): #Asignación de enteros
        largo = len(linea)
        i= linea.find('$')
        i2 = i
        while i<largo:
            if linea[i] == ' ':
                nombre = linea[i2:i]
                #print(nombre)
                i = linea.find('ASIG')
                i+=5
                while i == ' ':
                    i+=1
                numero = int(linea[i:-1])
                #print(numero)
                break
            i+=1
        if nombre in definidas:
            ints[nombre] = numero
            return 'Int'
        else:
            return 'Variable no definida'#.format(nombre)
    elif re.match(asig_string, linea): #Asignación de strings
        largo = len(linea)
        i= linea.find('$')
        i2 = i
        while i<largo:
            if linea[i] == ' ':
                nombre = linea[i2:i]
                i = linea.find('ASIG')
                i+=5
                while linea[i] == ' ':
                    i+=1
                string = linea[i:-1]
                break
            i+=1
        if nombre in definidas:
            strings[nombre] = string
            return 'String'
        else:
            return 'Variable no definida'#.format(nombre)
    elif re.match(asig_suma, linea): #Asignación de resultados con la operación 'Suma'
        largo= len(linea)
        i= linea.find("$")
        i2 = i
        while i<largo:
            if linea[i] == ' ':
                nombre = linea[i2:i]
                if nombre not in definidas:
                    return 'Variable no definida'
                break
            i+=1
    elif re.match(asig_multiplicacion, linea): #Asignación de resultados con la operación 'Multiplicación'
        largo= len(linea)
        i= linea.find("$")
        i2 = i
        while i<largo:
            if linea[i] == ' ':
                nombre = linea[i2:i]
                if nombre not in definidas:
                    return 'Variable no definida'
                break
            i+=1
    elif re.match(asig_bool_mayor_que, linea): #Asignación de booleanos con la operación 'Mayor que'
        largo = len(linea)
        i= linea.find("$")
        i2 = i
        while i<largo:
            if linea[i] == ' ':
                nombre = linea[i2:i]
                if nombre not in definidas:
                    return 'Variable no definida'
                #print(nombre)
                i = linea.find('>')
                i+=2
                while linea[i] == ' ':
                    i+=1
                i2 = i
                #print(i, i2)
                while i2<len(linea):
                    if linea[i2] == ' ':
                        aux1 = linea[i:i2]
                        while linea[i2] == ' ':
                            i2+=1
                        aux2 = linea[i2:-1]
                        #print(aux1, aux2)
                        i2+=1
                        #print(aux1, ints)
                        if aux1 in ints:
                            re_aux1 = ints[aux1]
                        else:
                            re_aux1 = int(aux1)
                        if aux2 in ints:
                            re_aux2 = ints[aux2]
                        else:
                            re_aux2 = int(aux2)
                            #print(re_aux1, re_aux2)
                    i2+=1
                booleano = re_aux1 > re_aux2
                if nombre in definidas:
                    bools[nombre] = booleano
                    return 'Bool'
            i+=1
    elif re.match(asig_bool_strings, linea): #Asignación de booleanos con la operación 'Igual que'
        largo = len(linea)
        i= linea.find('$')
        i2=i
        while i<largo:
            if linea[i] == ' ':
                nombre = linea[i2:i]
                if nombre not in definidas:
                    return 'Variable no definida'
                #print(nombre)
                i= linea.find('==')
                i+=3
                while linea[i] == ' ':
                    i+=1
                i2 = i
                while i2<len(linea):
                    if linea[i2] == ' ':
                        aux3 = linea[i:i2]
                        while linea[i2] == ' ':
                            i2+=1
                        aux4 = linea[i2:-1]
                        #print('aux3=',aux3,'aux4=',aux4)
                        i2+=1
                        if aux3 in ints:
                            re_aux3 = ints[aux3]
                        elif aux3 in strings:
                            re_aux3 = strings[aux3]
                        else:
                            re_aux3 = aux3
                        if aux4 in ints:
                            re_aux4 = ints[aux4]
                        elif aux4 in strings:
                            re_aux4 = strings[aux4]
                        else:
                            re_aux4 = aux4
                    i2+=1
                #print(re_aux3, re_aux4)
                booleano = str(re_aux3) == str(re_aux4)
                if nombre in definidas:
                    bools[nombre] = booleano
                    return 'Bool'
            i+=1
    else:
        pass

def resolver_suma(linea): #Determina el valor de la suma que haya en alguna linea correspondiente de 'codigo.txt'
    struct_suma = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+\+(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*))|(\#.*\#))'
    i = linea.find('+')
    i2 = i+2
    flag_string = False
    if re.match(struct_suma, linea):
        nombre = linea[3:i-1]
        print('Nombre:',nombre)
        while i2 < len(linea):
            if linea[i2] == ' ':
                sumando1 = linea[i+2:i2]
                sumando2 = linea[i2+1:-1]
                print(sumando1,"|",sumando2)
                break #######
            i2+=1
        if sumando1 in ints:
            re_sumando1 = ints[sumando1]
        elif sumando1 in strings:
            re_sumando1 = strings[sumando1]
            flag_string = True
        else:
            re_sumando1 = sumando1

        if sumando2 in ints:
            re_sumando2 = ints[sumando2]
        elif sumando2 in strings:
            re_sumando2 = strings[sumando2]
            flag_string = True
        else:
            re_sumando2 = sumando2
        re_sumando1 = str(re_sumando1)
        re_sumando2 = str(re_sumando2)
        print("Sumando 1:",re_sumando1, "Sumando 2:",re_sumando2)
        if ('#' in re_sumando1) or ('#' in re_sumando2):
            flag_string = True
        if flag_string:
            if '#' in re_sumando1:
                resultado = re_sumando1[:-1] + re_sumando2 + re_sumando1[-1:]
            elif '#' in re_sumando2:
                resultado = re_sumando2[0] + re_sumando1 + re_sumando2[1:]
            elif ('#' in re_sumando1) and ('#' in re_sumando2):
                resultado = '#' + re_sumando1[1:-1] + re_sumando2[1:-1] + '#'
            print("Resultado:",resultado)
            if nombre in definidas:
                if nombre in strings:
                    strings[nombre] = resultado
                elif nombre in ints:
                    del(ints[nombre])
                    strings[nombre] = resultado
            return resultado
        else:
            re_sumando1 = int(re_sumando1)
            re_sumando2 = int(re_sumando2)
            resultado = re_sumando1 + re_sumando2
            if nombre in definidas:
                ints[nombre] = resultado
            return resultado
    else:
        return

def resolver_multiplicacion(linea): #Determina el valor de la multiplicación que haya en alguna linea correspondiente de 'codigo.txt'
    struct_multiplicacion = r'(\ )*DP(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+\*(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))(\ )+((\$_[A-Z][A-Za-z]*)|([-]?(0|[1-9]\d*)))'
    i = linea.find('*')
    i2 = i+2
    if re.match(struct_multiplicacion, linea):
        nombre = linea[3:i-1]
        while i2 < len(linea):
            if linea[i2] == ' ':
                factor1 = linea[i+2:i2]
                factor2 = linea[i2+1:-1]
                #print(factor1, factor2)
            i2+=1
        if factor1 in ints:
            re_factor1 = ints[factor1]
        else:
            re_factor1 = factor1
        if factor2 in ints:
            re_factor2 = ints[factor2]
        else:
            re_factor2 = factor2
        resultado = int(re_factor1)*int(re_factor2) ########
        if nombre in definidas:
            ints[nombre] = resultado
            return resultado
    else:
        return

def resolver_if(linea): #Retorna True si la condición dentro de cierto if es verdadera... De lo contrario, retorna False. Puede retornar 'Variable no definida' si la variable dentro del if no se encuentra definida.
    struct_if = r'(\ )*if(\ )*\(\$_[A-Z][A-Za-z]*\)(\ )*\{'
    if re.match(struct_if, linea):
        i = linea.find('$')
        i2 = i
        while (linea[i2] != ')') and (linea[i2] != ' '):
            i2+=1
        var_condicion = linea[i:i2]
        if var_condicion in definidas:
            condicion = bools[var_condicion]
        else:
            return 'Variable no definida'
        if condicion == True:
            return True
        else:
            return False

def operaciones_de_linea(linea): #Junta en una única función muchas de las funciones definidas anteriormente
    variables_definidas(linea)
    resolver_suma(linea)
    resolver_multiplicacion(linea)
    resolver_if(linea)
    #print(resolver_if(linea))
    datatype(linea)
    #print(linea)

def llenar_se_ejecutan(nombre_archivo): #Determina qué lineas de código que estén dentro de un 'if' o un 'else' son las que realmente deben ejecutarse (lógicamente, se basa en la condición que se haya establecido en el 'if')
    i_linea = 1
    archivo = open(nombre_archivo)
    for linea in archivo:
        operaciones_de_linea(linea)
        #print(i_linea, linea)
        if (resolver_if(linea) == True) and (i_linea not in se_ejecutan):
            contador = 1
            next_line = next(archivo, None)
            se_ejecutan[i_linea] = True
            while next_line is not None:
                i_linea+=1
                #print(i_linea, next_line)
                if linea_correcta(next_line) == 'If':
                    contador+=1
                elif linea_correcta(next_line) == 'Else':
                    contador-=1
                if contador == 0:
                    se_ejecutan[i_linea] = False
                    se_ejecutan[str(i_linea)] = False
                    contador2 = 1
                    next_next_line = next(archivo, None)
                    while next_next_line is not None:
                        #print(next_next_line)
                        i_linea +=1
                        if linea_correcta(next_next_line) == 'If':
                            contador2 +=1
                        elif linea_correcta(next_next_line) == 'Corchete':
                            contador2 -=1
                        if contador2 == 0:
                            se_ejecutan[i_linea] = False
                            break
                        next_next_line = next(archivo, None)
                    break
                next_line = next(archivo, None)
        elif (resolver_if(linea) == False) and (i_linea not in se_ejecutan):
            contador = 1
            next_line = next(archivo, None)
            se_ejecutan[i_linea] = False
            while next_line is not None:
                i_linea+=1
                #print(i_linea, next_line)
                if linea_correcta(next_line) == 'If':
                    contador+=1
                elif linea_correcta(next_line) == 'Else':
                    contador-=1
                if contador == 0:
                    se_ejecutan[i_linea] = True
                    se_ejecutan[str(i_linea)] = True
                    contador2 = 1
                    next_next_line = next(archivo, None)
                    while next_next_line is not None:
                        i_linea +=1
                        if linea_correcta(next_next_line) == 'If':
                            contador2 +=1
                        elif linea_correcta(next_next_line) == 'Corchete':
                            contador2 -=1
                        if contador2 == 0:
                            se_ejecutan[i_linea] = True
                            break
                        next_next_line = next(archivo, None)
                    break
                next_line = next(archivo, None)
        i_linea+=1

def output(linea): #Escribe en 'output.txt' el valor de la variable que aparezca dentro de la funcion MOSTRAR() en 'codigo.txt'
    file2 = open('output.txt', 'w')
    if linea_correcta(linea) == 'Mostrar':
        pos = linea.find('$')
        pos2 = pos
        while (linea[pos2] != ' ') and (linea[pos2] != ')'):
            pos2 +=1
        nombre = linea[pos:pos2]
        #print(nombre)
        if nombre in definidas:
            if nombre in bools:
                file2.write(str(bools[nombre])) #####
            elif nombre in ints:
                file2.write(str(ints[nombre])) #####
            elif nombre in strings:
                file2.write(strings[nombre])

'''
# ----- APARTADO DE ERRORES ----- #
#Error de Sintaxis:
#Para cada línea, llama a la función linea_correcta(), y si ésta llega a retornar False, significa que hay un error de sintáxis
i = 1
file = open(file_name)
for line in file:
    #print(line, linea_correcta(line), datatype(line), '\n')
    if linea_correcta(line) == False:
        print('Error durante la ejecución (linea {}): Hay un error de sintaxis en la linea {}.'.format(i, i))
        file.close()
        exit()
    i+=1

#Error por definición reiterada:
#Para cada línea, llama a la función variables_definidas(), y si llega a retornar 'Variable ya definida', significa que hay una definición reiterada
struct_if = r'(\ )*if(\ )*\(\$_[A-Z][A-Za-z]*\)(\ )*\{'
struct_corchete = r'(\ )*\}'
file = open(file_name)
i = 1
for line in file:
    if re.match(struct_if, line):
        contador = 1
        next_line = next(file, None)
        while next_line is not None:
            if re.match(struct_if, next_line):
                contador+=1
            elif re.match(struct_corchete, next_line):
                contador -=1
            if contador == 0:
                line = next_line
                break
            next_line = next(file, None) 
    cond_err_var_definida = variables_definidas(line) == 'Variable ya definida'
    if cond_err_var_definida:
        print('Error durante la ejecución (linea {}): Se intentó declarar una variable que ya estaba declarada.'.format(i))
        file.close()
        exit()
    i+=1

#Error por variable no declarada:
#Para cada línea, llama a la función datatype(), y si llega a retornar 'Variable no definida', significa que se está intentando asignar un valor a una variable que no está definida
i_datatype = 1
file = open(file_name)
for line in file:
    if datatype(line) != 'Variable no definida':
        i_datatype +=1
    else:
        print('Error durante la ejecución (linea {}): Se le intentó asignar un valor a una variable que no estaba declarada previamente.'.format(i_datatype))
        file.close()
        exit()

#Error por tipo de datos incompatibles:
#Usando la función linea_correcta() se evalúa qué tipo de operación se está realizando, las variables participantes y la compatibilidad entre dichas variables
file = open(file_name)
i_line = 1
for line in file:
    if linea_correcta(line) == 'Suma':
        posicion_signo_mas = line.find('+')
        pos1 = posicion_signo_mas + 2
        while pos1 < len(line):
            if line[pos1] == ' ':
                var1 = line[posicion_signo_mas+2:pos1]
                var2 = line[pos1+1:-1]
                #print(var1, var2)
                if (var1 in bools) or (var2 in bools):
                    print('Error durante la ejecución (linea {}): Alguna(s) de las variables a sumar es(son) incompatible(s) con la operación.'.format(i_line))
                    exit()
            pos1 +=1
    elif linea_correcta(line) == 'Multiplicación':
        posicion_asterisco = line.find('*')
        pos2 = posicion_asterisco + 2
        while pos2 < len(line):
            if line[pos2] == ' ':
                var3 = line[posicion_asterisco+2:pos2]
                var4 = line[pos2+1:-1]
                #print(var3, var4)
                if (var3 in strings) or (var3 in bools) or (var4 in strings) or (var4 in bools):
                    print('Error durante la ejecución (linea {}): Alguna(s) de las variables a multiplicar es(son) incompatible(s) con la operación.'.format(i_line))
                    exit()
            pos2 +=1
    elif linea_correcta(line) == 'Mayor que':
        posicion_boquita = line.find('>')
        pos3 = posicion_boquita + 2
        while pos3 < len(line):
            if line[pos3] == ' ':
                var5 = line[posicion_boquita+2:pos3]
                var6 = line[pos3+1:-1]
                #print(var5, var6)
                if (var5 in strings) or (var5 in bools) or (var6 in strings) or (var6 in bools):
                    print('Error durante la ejecución (linea {}): Alguna(s) de las variables a evaluar con un "Mayor que" (>) es(son) incompatible(s) con la operación.'.format(i_line))
                    exit()
            pos3 +=1
    elif linea_correcta(line) == 'Igual que':
        posicion_iguales = line.find('==')+1
        pos4 = posicion_iguales + 2
        while pos4 < len(line):
            if line[pos4] == ' ':
                var7 = line[posicion_iguales+2:pos4]
                var8 = line[pos4+1:-1]
                #print(var7, var8)
                if (var7 in bools) or (var8 in bools):
                    print('Error durante la ejecución (linea {}): Alguna(s) de las variables a evaluar con un "Igual que" (==) es(son) incompatible(s) con la operación.'.format(i_line))
                    exit()
            pos4 +=1
    i_line +=1
file.close()
definidas.clear()
'''

# ----- MAIN ----- #
#Si el código llegó hasta este punto, se puede inferir que no hay errores en 'codigo.txt'
llenar_se_ejecutan(file_name)
llenar_se_ejecutan(file_name)
llenar_se_ejecutan(file_name)
llenar_se_ejecutan(file_name)
#Se llama a la función 4 veces para asegurar que todas las anidaciones posibles de los "if" [Máximo 3] funcionen correctamente

definidas.clear()

keys_list = []
for element in se_ejecutan:
    element = int(element)
    keys_list.append(element)
#print(keys_list)

final_list = []
elements = 0
while elements < len(keys_list):
    final_list.append(sorted([keys_list[elements], keys_list[elements+1]]))
    elements +=2
iterator = iter(final_list)

for element in iterator: #Ciclo que termina de determinar qué líneas de código dentro de 'ifs' o 'elses' deben realmente ser ejecutadas
    if se_ejecutan[element[0]] == True:
        counter = element[0]+1
        while counter < int(element[1]):
            if counter in se_ejecutan:
                if se_ejecutan[counter] == False:
                    break
            se_ejecutan[counter] = True
            counter +=1
        element = next(iterator)
        counter = int(element[0])+1
        while counter < int(element[1]):
            se_ejecutan[counter] = False
            counter +=1
    elif se_ejecutan[element[0]] == False:
        counter = element[0]+1
        while counter < int(element[1]):
            if counter in se_ejecutan:
                if se_ejecutan[counter] == False:
                    break
            se_ejecutan[counter] = False
            counter +=1
        element = next(iterator)
        counter = int(element[0])+1
        while counter < int(element[1]):
            se_ejecutan[counter] = True
            counter +=1

file = open(file_name)
file2 = open('output.txt', 'w')

line_counter = 1
for line in file: #Ciclo principal, aplica las operaciones de linea a las lineas correspondientes de 'codigo.txt'
    if resolver_if(line) == True:
        pass
    elif resolver_if(line) == False:
        pass
    elif resolver_if(line) == None:
        pass
    else: #Decidí incluír este error adicional.
        print('Error durante la ejecución (linea {}): Se intentó usar una variable no definida como condición del "if" de la linea {}'.format(line_counter, line_counter))
        exit()

    if line_counter not in se_ejecutan:
        operaciones_de_linea(line)
    else:
        if se_ejecutan[line_counter] == True:
            operaciones_de_linea(line)
        else:
            pass

    if linea_correcta(line) == 'Mostrar':
        output(line)

    line_counter+=1

file.close()
file2.close()

#Estos prints sirvieron como mi guía durante la programación de este código... Invito a verlos, me costaron mucho (jajaja)
"""
print('----- VER DESDE AQUI-----')
j = 0
while j < 50:
    if j in se_ejecutan:
        if se_ejecutan[j] == True:
            print("Línea {}: Si".format(j))
        else:
            print("Línea {}: No".format(j))
    j+=1
print(final_list)
print()
print(definidas)
print(bools)
print(strings)
print(ints)
print(se_ejecutan)
"""