class Vehiculo:
    def __init__(self, id, capacidad_max=40, horas_trabajo=8):
        self.id = id
        self.capacidad_max = capacidad_max
        self.carga_actual = 0
        self.horas_trabajo = horas_trabajo
        self.ruta = []
        self.entregas = {}
        self.hora_inicio = 9.0
    
    def asignar_paquetes(self, paquetes):
        self.carga_actual = min(len(paquetes), self.capacidad_max)
        return self.carga_actual
    
    def asignar_ruta(self, ruta):
        self.ruta = ruta
    
    def calcular_detalles_ruta(self, grafo):
        hora_actual = self.hora_inicio
        detalles_ruta = []
        
        for i in range(len(self.ruta)):
            ciudad = self.ruta[i]
            if i == 0:
                detalles_ruta.append({
                    "ciudad": ciudad,
                    "llegada": hora_actual,
                    "tipo": "salida"
                })
            else:
                ciudad_anterior = self.ruta[i-1]
                tiempo_viaje = grafo.get_tiempo(ciudad_anterior, ciudad)
                
                if tiempo_viaje:
                    hora_actual += tiempo_viaje
                    detalles_ruta.append({
                        "ciudad": ciudad,
                        "llegada": hora_actual,
                        "tipo": "entrega",
                        "tiempo_viaje": tiempo_viaje
                    })
        
        return detalles_ruta, hora_actual - self.hora_inicio
    
    def get_paquetes_restantes(self):
        return self.capacidad_max - sum(self.entregas.values())
    
    def mostrar_estado(self, grafo):
        detalles_ruta, tiempo_total = self.calcular_detalles_ruta(grafo)
        
        print(f"Furgoneta {self.id}: {self.carga_actual}/{self.capacidad_max} paquetes | Horario: 9:00 - 17:00")
        print(f"Ruta: {' → '.join(self.ruta)}")
        print("Tiempos: ")
        
        for detalle in detalles_ruta:
            if detalle["tipo"] == "salida":
                print(f"  • {detalle['ciudad']} (Salida: 9:00)")
            else:
                hora = detalle["llegada"]
                hora_str = f"{int(hora)}:{int((hora - int(hora)) * 60):02d}"
                paquetes = self.entregas.get(detalle['ciudad'], 0)
                
                # Verificar si está fuera de horario
                fuera_horario = ""
                if detalle["llegada"] > 17.0:  # Después de las 5:00 PM
                    fuera_horario = "  FUERA DE HORARIO"
                
                print(f"  • {detalle['ciudad']} (Llegada: {hora_str}, Entrega: {paquetes} paquetes){fuera_horario}")
        
        tiempo_usado = f"{tiempo_total:.1f}h"
        tiempo_max = f"{self.horas_trabajo}h"
        restantes = self.get_paquetes_restantes()
        
        print(f"Tiempo usado: {tiempo_usado} / {tiempo_max} | Paquetes restantes: {restantes}")
        print()
