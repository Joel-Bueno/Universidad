from city import City
from mapa import get_distance_km
import time

class Grafo:
    def __init__(self):
        self.distancias = {}
        self._inicializar_con_api()
    
    def _inicializar_con_api(self):
        print("CONSTRUYENDO GRAFO CON API DE MAPAS...")
        print("Calculando distancias reales entre ciudades de Colombia...")
        print("=" * 60)
        
        # Principales ciudades de Colombia
        ciudades = [
            "Ibague", "Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena",
            "Bucaramanga", "Pereira", "Santa Marta", "Cucuta", "Manizales",
            "Armenia", "Villavicencio", "Neiva", "Popayan", "Valledupar",
            "Monteria", "Sincelejo", "Buenaventura", "Tunja", "Riohacha"
        ]
        
        self._construir_grafo(ciudades)
    
    def _construir_grafo(self, ciudades):
        self.distancias = {}
        
        for origen in ciudades:
            self.distancias[origen] = []
            print(f"Calculando rutas desde {origen}...")
            
            for destino in ciudades:
                if origen != destino:
                    try:
                        distancia_km = get_distance_km(City(origen), City(destino))
                        # Calcular tiempo realista basado en distancia
                        if distancia_km < 100:
                            tiempo = round(distancia_km / 40, 1)  # 40 km/h en ciudad
                        elif distancia_km < 300:
                            tiempo = round(distancia_km / 60, 1)  # 60 km/h carretera
                        else:
                            tiempo = round(distancia_km / 70, 1)  # 70 km/h autopista
                        
                        # Solo incluir rutas razonables
                        if distancia_km < 800:
                            self.distancias[origen].append({
                                "ciudad": destino,
                                "distancia": distancia_km,
                                "tiempo": tiempo
                            })
                        
                        time.sleep(0.1)
                        
                    except Exception as e:
                        # Si falla la API, usar distancia estimada
                        tiempo_estimado = 2.5  # Tiempo promedio por defecto
                        self.distancias[origen].append({
                            "ciudad": destino,
                            "distancia": 150,
                            "tiempo": tiempo_estimado
                        })
            
            # Ordenar por distancia y mostrar las 3 más cercanas
            self.distancias[origen].sort(key=lambda x: x["distancia"])
            rutas_cercanas = self.distancias[origen][:3]
            rutas_str = ", ".join([f"{r['ciudad']}({r['distancia']}km)" for r in rutas_cercanas])
            print(f"  Rutas cercanas: {rutas_str}")
        
        print("=" * 60)
        print()
    
    def get_tiempo(self, origen, destino):
        for ruta in self.distancias.get(origen, []):
            if ruta["ciudad"] == destino:
                return ruta["tiempo"]
        return 3.0  # Tiempo por defecto
    
    def get_distancia(self, origen, destino):
        for ruta in self.distancias.get(origen, []):
            if ruta["ciudad"] == destino:
                return ruta["distancia"]
        return None
    
    def mostrar_grafo(self):
        print("RED DE CIUDADES PRINCIPALES DE COLOMBIA:")
        print("=" * 60)
        
        # Mostrar solo conexiones principales desde cada ciudad
        for ciudad in ["Ibague", "Bogota", "Medellin", "Cali", "Barranquilla"]:
            if ciudad in self.distancias:
                rutas = self.distancias[ciudad][:4]  # Mostrar 4 conexiones principales
                rutas_str = ", ".join([f"{r['ciudad']} ({r['distancia']}km)" for r in rutas])
                print(f"{ciudad} → [{rutas_str}]")
        
        print("... y más ciudades")
        print("=" * 60)