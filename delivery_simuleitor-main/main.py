from simulador import Simulador
#Se abre primero el terminal para definir la variable de entorno con la API Key de OpenRouteService
#se debe ingersa este env, para que la api funcciones correctamente
#$env:ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjY4YmRmZmNiMGQxNjQ0ZGI4MWQwYjMxMDFhNmVkMTIzIiwiaCI6Im11cm11cjY0In0="

def main():
    print("SISTEMA DE OPTIMIZACION DE RUTAS DE PAQUETERIA")
    print("Centro de Distribución: Ibagué")
    print("=" * 50)
    print()
    
    # Ejecutar el simulador completo
    simulador = Simulador()
    simulador.ejecutar()

if __name__ == "__main__":
    main()