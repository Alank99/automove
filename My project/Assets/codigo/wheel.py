"""
Genera un archivo .obj de una llanta de auto, a partir de los parametros de entrada desde la linea de comandos.
Para ejecutar el programa se debe ingresar en la linea de comandos:
python wheel.py [lado] [radio] [anchura]
donde:
lado: numero de lados de la llanta
radio: radio de la llanta
anchura: anchura de la llanta

Si no se ingresan parametros, se toman los siguientes valores por defecto.

Por Alan Anthony Hernadez Perez A01783347
"""


import math
import sys

def Normalizar(vector):
    magnitud = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    return [vector[0]/magnitud, vector[1]/magnitud, vector[2]/magnitud]

def ProductoCruz(u,v):

    normal = [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    ]
    return normal    

def Rueda(archivo, lado, radio, anchura):
    puntos = []
    normales = []

    # puntos
    for i in range(lado):
        angulo = 2 * math.pi * i / lado
        x = anchura / 2
        y = radio * math.cos(angulo)
        z = radio * math.sin(angulo)
        puntos.append([x, y, z])
        puntos.append([-x, y, z])

    # normales
    for i in range(lado-1):
        if (i == lado-2):
            #normal de la ultima cara interior de la llanta, se conecta al inicio

            v1 = [puntos [i * 2 + 1][0] - puntos[i * 2 ][0], puntos [i * 2 + 1][1] - puntos[i * 2 ][1], puntos [i * 2 + 1][2] - puntos[i * 2 ][2]] #punto ultima - punto antepeultimo
            v2 =[puntos [0][0] - puntos[ i*2+1][0], puntos [0][1] - puntos [i *2 +1][1], puntos[0][2] - puntos[i * 2 +1][2]] #punto 0 - punto ultima
            normal = Normalizar(ProductoCruz(v1, v2))
            normales.append(normal)
        else:
            #normales de la cara interior de la llanta
            v1 = [puntos [i * 2 + 1][0] - puntos[i * 2 ][0], puntos [i*2 +1][1] - puntos[i * 2 ][1], puntos [i*2 +1][2] - puntos[i * 2 ][2]] #punto 1 - punto 0
            v2 =[puntos [i * 2 + 2][0] - puntos[ i*2+1][0], puntos [i * 2 + 2][1] - puntos [i *2 +1][1], puntos[i * 2 +2][2] - puntos[i * 2 +1][2]]#punto 2 - punto 1
        normal = Normalizar(ProductoCruz(v1, v2))
        normales.append(normal)
    
    
    with open(archivo, "w") as archivo_salida:
    # Escribirpuntos
        archivo_salida.write("# puntos\n")
        for punto in puntos:
            archivo_salida.write("v {:.4f} {:.4f} {:.4f}\n".format(punto[0], punto[1], punto[2]))
        # puntos centrales para la caras de los lados
        archivo_salida.write("v {:.4f} {:.4f} {:.4f}\n".format(anchura/2, 0, 0))
        archivo_salida.write("v {:.4f} {:.4f} {:.4f}\n".format(-anchura/2, 0, 0))
        puntos.append([anchura/2, 0, 0]) 
        puntos.append([-anchura/2, 0, 0])

    # EscribirNormales
        archivo_salida.write("\n# normales\n")
        for n in normales:
            archivo_salida.write("vn {:.4f} {:.4f} {:.4f}\n".format(n[0], n[1], n[2]))
        # normales de las caras de los lados
        archivo_salida.write("vn {:.4f} {:.4f} {:.4f}\n".format(1,0,0))
        archivo_salida.write("vn {:.4f} {:.4f} {:.4f}\n".format(-1,0,0))
        normales.append([1,0,0])
        normales.append([-1,0,0])

    # EscribirCaras
        archivo_salida.write("\n# caras\n")
        for i in range(lado):     
            if(i == lado-1):
                #conexion de los ultimos puntos con los primeros de la cara interior
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(len(puntos)-3 ,i+1 , len(puntos)-2 , i+1, 1, i+1))
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(len(puntos)-2 ,i+1 , 2 , i+1, 1, i+1))
                #conexion de los ultimos puntos con los primeros de la cara de lateral
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(len(puntos)-1 ,len(normales)-1 , i * 2 + 1, len(normales)-1, 1, len(normales)-1))
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(len(puntos), len(normales), 2, len(normales), i * 2 + 2, len(normales)))
            else:
                #conexion de los puntos de la cara interior
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(i*2+1, i+1, i*2+2, i+1,i*2+3, i+1))
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(i*2+4, i+1, i*2+3, i+1,i*2+2, i+1))
                #conexion de los puntos de la cara de lateral
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(len(puntos)-1 ,len(normales)-1 , i * 2 + 1, len(normales)-1, i * 2 + 3, len(normales)-1))
                archivo_salida.write("f {}//{} {}//{} {}//{}\n".format(len(puntos), len(normales), i * 2 + 4, len(normales), i * 2 + 2, len(normales)))

            
        


if __name__ == "__main__":
    if len(sys.argv) != 4:
        lado = 8
        radio = 1
        anchura = 0.5
    else:
        lado = int(sys.argv[1])
        radio = float(sys.argv[2])
        anchura = float(sys.argv[3])
    if lado < 3 or lado > 360:
        lado = 8
    if radio < 1:
        radio = 1
    if anchura < 0.5:
        anchura = 0.5

    archivo = "llantita.obj"
    Rueda(archivo, lado, radio, anchura)