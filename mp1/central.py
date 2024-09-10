# Parte 1: Cargar los datos
from posixpath import split


def cargar_datos(lineas_archivo):
    generos_peliculas = set()
    peliculas_por_genero = {}
    info_peliculas = []

    for linea in lineas_archivo:
        datos = linea.split(',')
        titulo = datos[0]
        popularidad = datos[1]
        voto_promedio = datos[2]
        cantidad_votos = datos[3]
        generos = datos[4].split(';')


        generos_peliculas.update(generos)

        info_peliculas.append((titulo, popularidad, voto_promedio, cantidad_votos, generos))

        for genero in generos:
            if genero not in peliculas_por_genero:
                peliculas_por_genero[genero] = []  # Crear lista si el género no existe
            peliculas_por_genero[genero].append(titulo)  # Añadir el título de la película a su género

    peliculas_por_genero_lista = [
        (genero, peliculas)
        for genero, peliculas in peliculas_por_genero.items()
    ]

    return list(generos_peliculas), peliculas_por_genero_lista, info_peliculas

# Parte 2: Completar las consultas
def obtener_puntaje_y_votos(nombre_pelicula):
    lineas_archivo = leer_archivo()  # Definir lineas_archivo dentro de la función
    for linea in lineas_archivo:
        datos = linea.split(',')
        if datos[0] == nombre_pelicula:
            return float(datos[2]), int(datos[3])

    return None, None


def filtrar_y_ordenar(genero_pelicula):
    peliculas_filtradas = [
        linea.split(',')[0]
        for linea in leer_archivo()
        if genero_pelicula in linea.split(',')[4].split(';')
    ]
    peliculas_ordenadas = sorted(peliculas_filtradas, reverse=True)
    return peliculas_ordenadas

def obtener_estadisticas(genero_pelicula, criterio):
    indices = {"popularidad": 1, "voto promedio": 2, "cantidad votos": 3}
    indice = indices.get(criterio)

    if indice is None:
        raise ValueError("Criterio inválido")

    valores = []
    for linea in leer_archivo():
        campos = linea.split(',')
        if genero_pelicula in campos[4].split(';'):
            valores.append(float(campos[indice]))

    if valores:
        return max(valores), min(valores), sum(valores) / len(valores)
    return 0, 0, 0


# NO ES NECESARIO MODIFICAR DESDE AQUI HACIA ABAJO

def solicitar_accion():
    print("\n¿Qué desea hacer?\n")
    print("[0] Revisar estructuras de datos")
    print("[1] Obtener puntaje y votos de una película")
    print("[2] Filtrar y ordenar películas")
    print("[3] Obtener estadísticas de películas")
    print("[4] Salir")

    eleccion = input("\nIndique su elección (0, 1, 2, 3, 4): ")
    while eleccion not in "01234":
        eleccion = input("\nElección no válida.\nIndique su elección (0, 1, 2, 3, 4): ")
    eleccion = int(eleccion)
    return eleccion


def leer_archivo():
    lineas_peliculas = []
    with open("movies.csv", "r", encoding="utf-8") as datos:
        for linea in datos.readlines()[1:]:
            lineas_peliculas.append(linea.strip())
    return lineas_peliculas


def revisar_estructuras(generos_peliculas, peliculas_por_genero, info_peliculas):
    print("\nGéneros de películas:")
    for genero in generos_peliculas:
        print(f"    - {genero}")

    print("\nTítulos de películas por genero:")
    for genero in peliculas_por_genero:
        print(f"    genero: {genero[0]}")
        for titulo in genero[1]:
            print(f"        - {titulo}")

    print("\nInformación de cada película:")
    for pelicula in info_peliculas:
        print(f"    Nombre: {pelicula[0]}")
        print(f"        - Popularidad: {pelicula[1]}")
        print(f"        - Puntaje Promedio: {pelicula[2]}")
        print(f"        - Votos: {pelicula[3]}")
        print(f"        - Géneros: {pelicula[4]}")


def solicitar_nombre():
    nombre = input("\nIngrese el nombre de la película: ")
    return nombre


def solicitar_genero():
    genero = input("\nIndique el género de película: ")
    return genero


def solicitar_genero_y_criterio():
    genero = input("\nIndique el género de película: ")
    criterio = input(
        "\nIndique el criterio (popularidad, voto promedio, cantidad votos): "
    )
    return genero, criterio


def main():
    lineas_archivo = leer_archivo()
    datos_cargados = True
    try:
        generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(
            lineas_archivo
        )
    except TypeError as error:
        if "cannot unpack non-iterable NoneType object" in repr(error):
            print(
                "\nTodavía no puedes ejecutar el programa ya que no has cargado los datos\n"
            )
            datos_cargados = False
    if datos_cargados:
        salir = False
        print("\n********** ¡Bienvenid@! **********")
        while not salir:
            accion = solicitar_accion()

            if accion == 0:
                revisar_estructuras(
                    generos_peliculas, peliculas_por_genero, info_peliculas
                )

            elif accion == 1:
                nombre_pelicula = solicitar_nombre()
                ptje, votos = obtener_puntaje_y_votos(nombre_pelicula)
                print(f"\nObteniendo puntaje promedio y votos de {nombre_pelicula}")
                print(f"    - Puntaje promedio: {ptje}")
                print(f"    - Votos: {votos}")

            elif accion == 2:
                genero = solicitar_genero()
                nombres_peliculas = filtrar_y_ordenar(genero)
                print(f"\nNombres de películas del género {genero} ordenados:")
                for nombre in nombres_peliculas:
                    print(f"    - {nombre}")

            elif accion == 3:
                genero, criterio = solicitar_genero_y_criterio()
                estadisticas = obtener_estadisticas(genero, criterio)
                print(f"\nEstadísticas de {criterio} de películas del género {genero}:")
                print(f"    - Máximo: {estadisticas[0]}")
                print(f"    - Mínimo: {estadisticas[1]}")
                print(f"    - Promedio: {estadisticas[2]}")

            else:
                salir = True
        print("\n********** ¡Adiós! **********\n")


if __name__ == "__main__":
    main()
