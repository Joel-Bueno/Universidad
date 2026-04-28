def busqueda_binaria_recursiva(lista, elemento, inicio=0, fin=None):
    """
    Búsqueda binaria recursiva para encontrar una ciudad en lista ordenada
    """
    if fin is None:
        fin = len(lista) - 1
    
    if inicio > fin:
        return False
    
    medio = (inicio + fin) // 2
    
    if lista[medio] == elemento:
        return True
    elif lista[medio] < elemento:
        return busqueda_binaria_recursiva(lista, elemento, medio + 1, fin)
    else:
        return busqueda_binaria_recursiva(lista, elemento, inicio, medio - 1)

def busqueda_lineal(lista, elemento):
    """
    Búsqueda lineal simple
    """
    for item in lista:
        if item == elemento:
            return True
    return False