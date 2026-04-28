def escalones(n):
    if n < 0:
        return [], 0
    if n == 0:
        return [[]], 1
        
    combinaciones_previas = [[]]  
    if n >= 1:
        combinaciones_actual = [[1]]
    if n >= 2:
        combinaciones_siguiente = [[1,1], [2]]
    
    if n == 0:
        return combinaciones_previas, 1
    elif n == 1:
        return combinaciones_actual, 1
    elif n == 2:
        return combinaciones_siguiente, 2
    
    count_prev, count_act, count_sig = 1, 1, 2
    
    for i in range(3, n + 1):
        nuevas_combinaciones = []
        for comb in combinaciones_siguiente:
            nuevas_combinaciones.append(comb + [1])
        for comb in combinaciones_actual:
            nuevas_combinaciones.append(comb + [2])
        for comb in combinaciones_previas:
            nuevas_combinaciones.append(comb + [3])
        
        nuevo_count = count_prev + count_act + count_sig
        
        
        combinaciones_previas = combinaciones_actual
        combinaciones_actual = combinaciones_siguiente
        combinaciones_siguiente = nuevas_combinaciones
        
        count_prev, count_act, count_sig = count_act, count_sig, nuevo_count
    
    return combinaciones_siguiente, count_sig

n = int(input("Ingrese cantidad de escalones: "))
result_comb, result_count = escalones(n)
print("Cantidad de combinaciones para", n, "posibles escalones:", result_count)
print("Combinaciones para", n, "escalones:", result_comb)
