from search import busqueda_binaria_recursiva

class Optimizador:
    def __init__(self, grafo):
        self.grafo = grafo
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')
        self.contador_recursiones = 0

    def calcular_distancia_ruta(self, ruta):
        total = 0
        for i in range(len(ruta) - 1):
            a, b = ruta[i], ruta[i + 1]
            dist = self.grafo.get_distancia(a, b)
            total += dist if dist else 1000
        return total

    def optimizar_recursivo(self, ruta_actual, ciudades_restantes, distancia_actual=0):
        self.contador_recursiones += 1
        
        # Caso base: no quedan ciudades
        if not ciudades_restantes:
            if distancia_actual < self.mejor_distancia:
                self.mejor_distancia = distancia_actual
                self.mejor_ruta = ruta_actual.copy()
            return

        # Podar si ya es peor
        if distancia_actual >= self.mejor_distancia:
            return

        # Probar cada ciudad restante
        for i, siguiente_ciudad in enumerate(ciudades_restantes):
            ultima_ciudad = ruta_actual[-1]
            distancia_segmento = self.grafo.get_distancia(ultima_ciudad, siguiente_ciudad) or 1000
            
            nueva_ruta = ruta_actual + [siguiente_ciudad]
            nuevas_restantes = ciudades_restantes[:i] + ciudades_restantes[i+1:]
            nueva_distancia = distancia_actual + distancia_segmento
            
            self.optimizar_recursivo(nueva_ruta, nuevas_restantes, nueva_distancia)

    def vecino_mas_cercano(self, ciudades):
        if len(ciudades) <= 2:
            return ciudades, self.calcular_distancia_ruta(ciudades)

        no_visitadas = set(ciudades[1:])
        ruta = [ciudades[0]]
        ciudad_actual = ciudades[0]
        distancia_total = 0

        while no_visitadas:
            ciudad_cercana = None
            distancia_minima = float('inf')
            
            for ciudad in no_visitadas:
                dist = self.grafo.get_distancia(ciudad_actual, ciudad)
                if dist and dist < distancia_minima:
                    distancia_minima = dist
                    ciudad_cercana = ciudad
            
            if ciudad_cercana:
                ruta.append(ciudad_cercana)
                distancia_total += distancia_minima
                ciudad_actual = ciudad_cercana
                no_visitadas.remove(ciudad_cercana)
            else:
                ruta.extend(no_visitadas)
                break

        return ruta, distancia_total

    def encontrar_mejor_ruta(self, ciudades):
        if len(ciudades) <= 1:
            return ciudades, 0

        print(f"Optimizando {len(ciudades)} ciudades...")

        # Verificar que todas las ciudades existen en el grafo usando búsqueda binaria
        ciudades_ordenadas = sorted(self.grafo.distancias.keys())
        for ciudad in ciudades:
            if not busqueda_binaria_recursiva(ciudades_ordenadas, ciudad):
                print(f"  Advertencia: {ciudad} no encontrada en el grafo")

        # Para pocas ciudades usar recursión
        if len(ciudades) <= 6:
            self.mejor_ruta = None
            self.mejor_distancia = float('inf')
            self.contador_recursiones = 0
            
            self.optimizar_recursivo([ciudades[0]], ciudades[1:], 0)
            
            print(f"  Recursiones: {self.contador_recursiones}")
            print(f"  Mejor distancia: {self.mejor_distancia:.1f}km")
            
            return self.mejor_ruta, self.mejor_distancia
        else:
            # Para muchas ciudades usar vecino más cercano
            return self.vecino_mas_cercano(ciudades)