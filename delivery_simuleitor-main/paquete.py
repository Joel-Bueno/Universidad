class Paquete:
    def __init__(self, id, ciudad_destino):
        self.id = id
        self.ciudad_destino = ciudad_destino
        self.entregado = False
    
    def marcar_entregado(self):
        self.entregado = True