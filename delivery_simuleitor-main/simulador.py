from grafo import Grafo
from vehiculo import Vehiculo
from paquete import Paquete
from optimizar import Optimizador
import random

class Simulador:
    def __init__(self):
        self.grafo = Grafo()
        self.vehiculos = []
        self.paquetes = []
        self.optimizador = Optimizador(self.grafo)
        self._inicializar_sistema()
    
    def _inicializar_sistema(self):
        # Crear 5 furgonetas
        for i in range(5):
            self.vehiculos.append(Vehiculo(i + 1))
        
        self._generar_paquetes()
    
    def _generar_paquetes(self):
        ciudades = list(self.grafo.distancias.keys())
        ciudades.remove("Ibague")  # No entregar en el origen
        
        # Generar 200 paquetes con destinos aleatorios en toda Colombia
        self.paquetes = []
        for i in range(200):
            destino = random.choice(ciudades)
            self.paquetes.append(Paquete(i + 1, destino))
        
        print("DISTRIBUCION ALEATORIA DE PAQUETES EN COLOMBIA:")
        print("=" * 50)
        conteo_ciudades = {}
        for pkg in self.paquetes:
            conteo_ciudades[pkg.ciudad_destino] = conteo_ciudades.get(pkg.ciudad_destino, 0) + 1
        
        # Mostrar top 10 ciudades con más paquetes
        top_ciudades = sorted(conteo_ciudades.items(), key=lambda x: x[1], reverse=True)[:10]
        for ciudad, cantidad in top_ciudades:
            print(f"{ciudad}: {cantidad} paquetes")
        
        print(f"... y {len(conteo_ciudades) - 10} ciudades más")
        print("=" * 50)
        print()
    
    def asignar_paquetes_optimizado(self):
        """Asigna paquetes agrupando por regiones de Colombia"""
        # Definir regiones de Colombia
        regiones = {
            "andina": ["Bogota", "Medellin", "Cali", "Bucaramanga", "Manizales", "Pereira", "Armenia", "Tunja", "Neiva"],
            "caribe": ["Barranquilla", "Cartagena", "Santa Marta", "Monteria", "Sincelejo", "Valledupar", "Riohacha"],
            "pacifica": ["Buenaventura", "Popayan"],
            "orinoquia": ["Villavicencio", "Cucuta"]
        }
        
        # Agrupar paquetes por región
        paquetes_por_region = {region: [] for region in regiones}
        paquetes_sin_region = []
        
        for pkg in self.paquetes:
            asignado = False
            for region, ciudades in regiones.items():
                if pkg.ciudad_destino in ciudades:
                    paquetes_por_region[region].append(pkg)
                    asignado = True
                    break
            if not asignado:
                paquetes_sin_region.append(pkg)
        
        # Asignar regiones a furgonetas
        regiones_lista = list(regiones.keys())
        random.shuffle(regiones_lista)
        
        # Distribuir regiones entre furgonetas
        for i, vehiculo in enumerate(self.vehiculos):
            if i < len(regiones_lista):
                region_asignada = regiones_lista[i]
                paquetes_vehiculo = paquetes_por_region[region_asignada]
                
                # Si hay pocos paquetes en la región, agregar de otras
                if len(paquetes_vehiculo) < 20 and paquetes_sin_region:
                    espacio = min(40 - len(paquetes_vehiculo), len(paquetes_sin_region))
                    paquetes_vehiculo.extend(paquetes_sin_region[:espacio])
                    paquetes_sin_region = paquetes_sin_region[espacio:]
            else:
                # Para furgonetas adicionales, mezclar paquetes sobrantes
                paquetes_vehiculo = paquetes_sin_region[:40]
                paquetes_sin_region = paquetes_sin_region[40:]
            
            vehiculo.asignar_paquetes(paquetes_vehiculo)
            
            # Contar entregas por ciudad
            entregas = {}
            for pkg in paquetes_vehiculo:
                entregas[pkg.ciudad_destino] = entregas.get(pkg.ciudad_destino, 0) + 1
            vehiculo.entregas = entregas
    
    def optimizar_rutas(self):
        print("OPTIMIZANDO RUTAS POR TODA COLOMBIA...")
        print("=" * 50)
        
        for vehiculo in self.vehiculos:
            if vehiculo.entregas:
                ciudades = list(vehiculo.entregas.keys())
                if ciudades:
                    todas_ciudades = ["Ibague"] + ciudades
                    
                    print(f"Furgoneta {vehiculo.id}: {len(ciudades)} destinos en {ciudades}")
                    
                    # Usar optimizador para encontrar mejor ruta
                    ruta_optimizada, distancia = self.optimizador.encontrar_mejor_ruta(todas_ciudades)
                    vehiculo.asignar_ruta(ruta_optimizada)
                    
                    print(f"  Ruta optimizada: {' → '.join(ruta_optimizada)}")
                    print(f"  Distancia total: {distancia:.1f}km")
                    print()
        
        print("=" * 50)
        print()
    
    def mostrar_simulacion(self):
        print("ESTADO DE LAS 5 FURGONETAS:")
        print("=" * 50)
        print()
        
        total_paquetes_asignados = 0
        total_paquetes_entregados = 0
        tiempos_totales = []
        vehiculos_en_horario = 0
        
        for vehiculo in self.vehiculos:
            vehiculo.mostrar_estado(self.grafo)
            detalles, tiempo_total = vehiculo.calcular_detalles_ruta(self.grafo)
            
            total_paquetes_asignados += vehiculo.carga_actual
            total_paquetes_entregados += sum(vehiculo.entregas.values())
            tiempos_totales.append(tiempo_total)
            
            if tiempo_total <= 8.0:
                vehiculos_en_horario += 1
        
        self._mostrar_resumen(total_paquetes_asignados, total_paquetes_entregados, 
                            vehiculos_en_horario, tiempos_totales)
    
    def _mostrar_resumen(self, total_asignados, total_entregados, en_horario, tiempos):
        tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
        
        print("=" * 50)
        print("RESUMEN:")
        print(f"• {en_horario}/5 furgonetas completaron dentro del horario")
        print(f"• {5 - en_horario} furgoneta(s) excedio el tiempo maximo")
        print(f"• Total paquetes entregados: {total_entregados}/200")
        print(f"• Tiempo promedio por furgoneta: {tiempo_promedio:.1f} horas")
        print("=" * 50)

    def ejecutar(self):
        print("SISTEMA NACIONAL DE OPTIMIZACION DE RUTAS")
        print("Centro de Distribucion: Ibague, Colombia")
        print("Cobertura: Toda Colombia")
        print("Tecnologia: API Maps + Optimizacion Recursiva")
        print()
        
        self.asignar_paquetes_optimizado()
        self.optimizar_rutas()
        self.grafo.mostrar_grafo()
        print()
        self.mostrar_simulacion()