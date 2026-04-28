import time
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123") # Pon tu contraseña de Docker aquí

class MotorRecomendacion:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def limpiar_y_configurar(self):
        with self.driver.session() as s:
            s.run("MATCH (n) DETACH DELETE n")
            s.run("CREATE INDEX IF NOT EXISTS FOR (u:Usuario) ON (u.nombre)")
            s.run("CREATE INDEX IF NOT EXISTS FOR (p:Producto) ON (p.nombre)")

    def carga_masiva(self):
        with self.driver.session() as s:
            # 1. Usuarios con sus Nombres y Ciudades
            usuarios = [
                ("Ana", "Bogotá"), 
                ("Luis", "Medellín"), 
                ("Carla", "Cali"), 
                ("Carlos", "Cartagena"), 
                ("Sofia", "Pereira")
            ]
            for nombre, ciudad in usuarios:
                s.run("MERGE (u:Usuario {nombre: $n}) SET u.ciudad = $c", n=nombre, c=ciudad)
                
            # 2. Productos que se pueden comprar
            productos = ["Laptop Gamer", "Monitor 4K", "Teclado Mecánico", "Audífonos"]
            for p in productos:
                s.run("MERGE (pr:Producto {nombre: $n})", n=p)

            # 3. Relaciones entre ellos (Quién conoce a quién)
            amistades = [
                ("Ana", "Luis"), ("Ana", "Carla"), 
                ("Luis", "Carlos"), ("Carla", "Sofia")
            ]
            for u1, u2 in amistades:
                s.run("""
                    MATCH (a:Usuario {nombre: $n1}), (b:Usuario {nombre: $n2})
                    MERGE (a)-[:CONOCE]->(b)
                """, n1=u1, n2=u2)
            
            # 4. Productos que compraron
            compras = [
                ("Luis", "Laptop Gamer"), 
                ("Carla", "Monitor 4K"),
                ("Carlos", "Teclado Mecánico"), 
                ("Ana", "Audífonos")
            ]
            for u, p in compras:
                s.run("""
                    MATCH (usuario:Usuario {nombre: $n}), (prod:Producto {nombre: $p})
                    MERGE (usuario)-[:COMPRO]->(prod)
                """, n=u, p=p)

    @staticmethod
    def medir_rendimiento(func):
        def wrapper(*args, **kwargs):
            inicio = time.time()
            res = func(*args, **kwargs)
            return res, time.time() - inicio
        return wrapper

    @medir_rendimiento
    def recomendacion_compleja(self, nombre_usuario):
        # Análisis de redes: Recomienda productos basados en las compras de la red de amigos
        with self.driver.session() as s:
            query = """
                MATCH (yo:Usuario {nombre: $n})-[:CONOCE*1..2]-(amigo)-[:COMPRO]->(prod:Producto)
                WHERE NOT (yo)-[:COMPRO]->(prod) AND yo <> amigo
                RETURN DISTINCT prod.nombre AS producto, count(amigo) AS frecuencia
                ORDER BY frecuencia DESC
            """
            return [row.data() for row in s.run(query, n=nombre_usuario)]

# ── EJECUCIÓN ──
if __name__ == "__main__":
    app = MotorRecomendacion(URI, AUTH)
    
    print(" Preparando base de datos...")
    app.limpiar_y_configurar()
    
    print(" Insertando usuarios, ciudades, productos y relaciones...")
    app.carga_masiva()
    print(" Todo cargado correctamente.\n")

    print("--- EVALUACIÓN DE RENDIMIENTO (Motor de Recomendaciones) ---")
    resultados, tiempo = app.recomendacion_compleja("Ana")
    
    print(f" Tiempo de la consulta: {tiempo:.5f} segundos")
    print(" Sugerencias para Ana:")
    for r in resultados:
        print(f"   - {r['producto']} (Comprado por {r['frecuencia']} persona/s en su red)")

    app.close()