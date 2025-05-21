from flask import Flask, jsonify, request, render_template
import math
import random

app = Flask(__name__)

# Coordenadas de ciudades
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754, -103.346253),
    'Monterrey': (25.691611, -100.321838),
    'Quintana Roo': (21.163111, -86.802315),
    'Michoacán': (19.701400, -101.208296),
    'Aguascalientes': (21.876410, -102.264386),
    'CDMX': (19.432713, -99.133183),
    'QRO': (20.597194, -100.386670)
}

# Calcular distancia euclidiana
def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Evaluar la distancia total de una ruta
def evalua_ruta(ruta):
    return sum(distancia(coord[ruta[i]], coord[ruta[i+1]]) for i in range(len(ruta) - 1)) + distancia(coord[ruta[-1]], coord[ruta[0]])

# Simulated Annealing para optimizar ruta
def simulated_annealing(ruta, T, T_MIN, V_enfriamiento):
    while T > T_MIN:
        for _ in range(V_enfriamiento):
            i, j = random.sample(range(1, len(ruta) - 1), 2)
            ruta[i], ruta[j] = ruta[j], ruta[i]
        T -= 0.005
    return ruta

@app.route('/ruta', methods=['POST'])
def obtener_ruta():
    datos = request.json
    origen, destino = datos["origen"], datos["destino"]

    ciudades_intermedias = [ciudad for ciudad in coord.keys() if ciudad not in [origen, destino]]
    random.shuffle(ciudades_intermedias)
    ruta_optima = [origen] + ciudades_intermedias + [destino]

    ruta_optima = simulated_annealing(ruta_optima, datos["temperatura_inicial"], datos["temperatura_min"], 100)
    distancia_total = evalua_ruta(ruta_optima)

    return jsonify({
        "ruta": ruta_optima,
        "distancia_total": round(distancia_total, 2),
        "coordenadas": [coord[ciudad] for ciudad in ruta_optima]
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
