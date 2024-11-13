import tkinter as tk
import random

import razas 
import animales
import terrenos_y_materiales as tm


ALTO = 50
ANCHO = 50

def nuevo_personaje(raza):
    personajes = {'Enano': razas.Enano(),
                  'Humano': razas.Humano(),
                  'Elfo': razas.Elfo(),
                  'Mago': razas.Mago(),
                  'Orco': razas.Orco(),
                  'Goblin': razas.Goblin(),
                  'Trol': razas.Trol()}
    
    return personajes[raza]

def nuevo_animal(tipo):    
    creaturas = {
        'Gallina': animales.Gallina(),  
        'Pescado': animales.Pescado(),
        'Perro': animales.Perro(),    
        'Gato': animales.Gato(),     
        'Cerdo': animales.Cerdo(),    
        'Vaca': animales.Vaca(),  
        'Caballo': animales.Caballo(),  
        'Poni': animales.Poni(),    
        'Conejo': animales.Conejo(),   
        'Rana': animales.Rana(),     
        'Borrego': animales.Borrego(),  
        'Chivo': animales.Chivo(),     
        'Jabali': animales.Jabali(),
        'Oso': animales.Oso()
    }
    
    return creaturas[tipo]
    
def nuevo_fruto(tipo):
    recursos = {'Manzana': tm.Manzana(),
                'Naranja': tm.Naranja(),
                'Mango': tm.Mango(),
                'Uva': tm.Uva(),
                'Sandía': tm.Sandia(),
                'Fresa': tm.Fresa(),
                'Trigo': tm.Trigo()}
    
    return recursos[tipo]

def generar_terreno():    
    terrenos = tm.lista_terrenos()
    probabilidades = [30, 20, 20, 30, 10, 10]
    
    mapa = []
    for i in range(ALTO):
        fila = []
        for j in range(ANCHO):
            terreno = random.choices(terrenos, weights=probabilidades, k=1)[0]
            fila.append(terreno)
        mapa.append(fila)
    return mapa

def colocar_personajes(mapa, raza, area):
    x_inicio, x_fin, y_inicio, y_fin = area
    cantidad = random.randint(5, 8)  # Cantidad de personajes de esa raza
    for _ in range(cantidad):
        x = random.randint(x_inicio, x_fin)
        y = random.randint(y_inicio, y_fin)
        mapa[x][y] = nuevo_personaje(raza)

def colocar_animales(mapa, tipo, area):
    x_o, y_o = area
    cantidad = random.randint(1, 3)  
    for _ in range(cantidad):
        x = random.randint(x_o, 49)
        y = random.randint(y_o, 49)
        mapa[x][y] = nuevo_animal(tipo)  

def colocar_recursos(mapa, tipo, area):
    x_o, y_o = area
    cantidad = random.randint(1, 3)  
    for _ in range(cantidad):
        x = random.randint(x_o, 49)
        y = random.randint(y_o, 49)
        mapa[x][y] = nuevo_fruto(tipo)

def generar_mapa():
    mapa = generar_terreno()

    areas = {
        'Enano': (0, 9, 0, 9),      
        'Elfo': (0, 9, 10, 19),   
        'Humano': (0, 9, 20, 29),  
        'Mago': (10, 29, 35, 49),   
        'Orco': (40, 49, 10, 19), 
        'Trol': (40, 49, 20, 29), 
        'Goblin': (40, 49, 30, 39)    
    }

    # Colocar personajes de cada raza en sus áreas
    for raza, area in areas.items():
        colocar_personajes(mapa, raza, area)
    
    creaturas = animales.lista_animales()
    for animal in creaturas:
        x = random.randint(0, 49)
        y = random.randint(0, 49)
        colocar_animales(mapa, animal.tipo, (x, y))    
    
    frutos = tm.lista_frutos()
    for fruto in frutos:
        x = random.randint(0, 49)
        y = random.randint(0, 49)
        colocar_recursos(mapa, fruto.tipo, (x, y))  
    
    return mapa

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, _):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def mostrar_mapa(root, mapa):
    for i, fila in enumerate(mapa):
        for j, item in enumerate(fila):
            if isinstance(item, razas.Personaje):
                color = "blue"    # Color para personajes
            elif isinstance(item, animales.Animal):
                color = "green"   # Color para animales
            elif isinstance(item, tm.Frutos):  # Asumiendo que el tipo es Fruto
                color = "red"     # Color para frutos
            else:
                color = "purple"   # Color para terreno o cualquier otro tipo
                
            label = tk.Label(root, text=item.simbolo, font=("Consolas", 6), fg=color)
            label.grid(row=i, column=j)
            Tooltip(label, item.info)  # Tooltip con la info del objeto


# Función para imprimir el mapa en la terminal
def imprimir_mapa_consola(mapa):
    output = ''
    for fila in mapa:
        for tipo in fila:
            output += ''.join(tipo.simbolo)
            
        output += '\n'
        
    print(output)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mapa")
    
    mapa = generar_mapa()
    mostrar_mapa(root, mapa)
    imprimir_mapa_consola(mapa)
    
    root.mainloop()
