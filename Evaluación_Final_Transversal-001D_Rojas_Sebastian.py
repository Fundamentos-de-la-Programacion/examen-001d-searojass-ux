
def leer_opcion():
    """Solicita la opción del menú, valida que sea entero y maneja excepciones."""
    try:
        opcion = int(input("Ingrese opción: "))
        if 1 <= opcion <= 6:
            return opcion
        else:
            print("Debe seleccionar una opción válida")
            return None
    except ValueError:
        print("Debe seleccionar una opción válida (ingrese un número entero)")
        return None


def buscar_codigo(codigo, dicc_peliculas):
    """Busca si el código existe sin importar mayúsculas o minúsculas."""
    codigo_upper = codigo.strip().upper()
  
    for c in dicc_peliculas.keys():
        if c.upper() == codigo_upper:
            return True
    return False


def obtener_clave_real(codigo, dicc_peliculas):
    """Retorna la clave exacta tal como está guardada (ej: 'P101' si entra 'p101')."""
    codigo_upper = codigo.strip().upper()
    for c in dicc_peliculas.keys():
        if c.upper() == codigo_upper:
            return c
    return codigo



def cupos_genero(genero, dicc_peliculas, dicc_cartelera):
    """Calcula y muestra el total de cupos acumulados de un género."""
    genero_buscado = genero.strip().lower()
    total_cupos = 0
    
    for cod, datos in dicc_peliculas.items():
        genero_pelicula = datos[1].strip().lower()
        if genero_pelicula == genero_buscado:

            if cod in dicc_cartelera:
                total_cupos += dicc_cartelera[cod][1]
                
    print(f"El total de cupos disponibles es: {total_cupos}")


def busqueda_precio(p_min, p_max, dicc_peliculas, dicc_cartelera):
    """Busca películas en un rango de precio con cupos > 0 y ordena alfabéticamente."""
    if p_min < 0 or p_max < 0 or p_min > p_max:
        print("Error: Rango de precios inválido.")
        return

    resultados = []
    for cod, datos_cartelera in dicc_cartelera.items():
        precio = datos_cartelera[0]
        cupos = datos_cartelera[1]
        
        if p_min <= precio <= p_max and cupos > 0:
            if cod in dicc_peliculas:
                titulo = dicc_peliculas[cod][0]
                resultados.append(f"{titulo}--{cod}")
                
    if len(resultados) > 0:
        resultados.sort()
        print(f"Las películas encontradas son: {resultados}")
    else:
        print("No hay películas en ese rango de precios.")


def actualizar_precio(codigo, nuevo_precio, dicc_peliculas, dicc_cartelera):
    """Actualiza el precio de la película si el código existe."""
    if buscar_codigo(codigo, dicc_peliculas):
        clave_real = obtener_clave_real(codigo, dicc_peliculas)
        dicc_cartelera[clave_real][0] = nuevo_precio
        return True
    return False


def validar_codigo(codigo, dicc_peliculas):
    if not codigo.strip():
        return False

    if buscar_codigo(codigo, dicc_peliculas):
        return False
    return True

def validar_titulo(titulo):
    return bool(titulo.strip())

def validar_genero(genero):
    return bool(genero.strip())

def validar_duracion(duracion):
    return duracion > 0

def validar_clasificacion(clasificacion):
    return clasificacion.strip().upper() in ['A', 'B', 'C']

def validar_idioma(idioma):
    return bool(idioma.strip())

def validar_precio(precio):
    return precio > 0

def validar_cupos(cupos):
    return cupos >= 0

def agregar_pelicula(codigo, titulo, genero, duracion, clasificacion, idioma, es_3d, precio, cupos, dicc_peliculas, dicc_cartelera):
    """Inserta la película en ambas estructuras si el código es único."""
    if buscar_codigo(codigo, dicc_peliculas):
        return False
    
    codigo_formateado = codigo.strip().upper()

    dicc_peliculas[codigo_formateado] = [
        titulo.strip(), 
        genero.strip().lower(), 
        duracion, 
        clasificacion.strip().upper(), 
        idioma.strip(), 
        es_3d
    ]

    dicc_cartelera[codigo_formateado] = [precio, cupos]
    return True


def eliminar_pelicula(codigo, dicc_peliculas, dicc_cartelera):
    """Elimina el registro de ambos diccionarios si existe."""
    if buscar_codigo(codigo, dicc_peliculas):
        clave_real = obtener_clave_real(codigo, dicc_peliculas)
        del dicc_peliculas[clave_real]
        del dicc_cartelera[clave_real]
        return True
    return False

def main():

    peliculas = {
        'P101': ['Luz de Otoño', 'drama', 110, 'B', 'Español', False],
        'P102': ['Noche Neón', 'acción', 125, 'C', 'Ingles', True],
        'P103': ['Planeta Agua', 'documental', 90, 'A', 'Español', False],
        'P104': ['Risa Total', 'comedia', 105, 'A', 'Español', True],
        'P105': ['Código Zero', 'thriller', 118, 'C', 'Ingles', True],
        'P106': ['Viaje Lunar', 'ciencia ficción', 132, 'B', 'Ingles', False]
    }

    cartelera = {
        'P101': [5990, 40],
        'P102': [7990, 0],
        'P103': [4990, 25],
        'P104': [6990, 12],
        'P105': [8990, 8],
        'P106': [7490, 3]
    }

    continuar = True
    while continuar:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Cupos por género")
        print("2. Búsqueda de películas por rango de precio")
        print("3. Actualizar precio de película")
        print("4. Agregar película")
        print("5. Eliminar película")
        print("6. Salir")
        print("=====================================")
        
        opc = leer_opcion()
        if opc is None:
            continue
        
        if opc == 1:
            gen = input("Ingrese género a consultar: ")
            cupos_genero(gen, peliculas, cartelera)
        elif opc == 2:
            while True:
                try:
                    p_min = int(input("Ingrese precio mínimo: "))
                    p_max = int(input("Ingrese precio máximo: "))
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        busqueda_precio(p_min, p_max, peliculas, cartelera)
                        break
                    else:
                        print("El precio mínimo debe ser menor o igual al máximo y ambos mayores a cero.")
                except ValueError:
                    print("Debe ingresar valores enteros")

        elif opc == 3:
            procesando = True
            while procesando:
                cod = input("Ingrese código de película: ")
                try:
                    nuevo_p = int(input("Ingrese nuevo precio: "))
                    if nuevo_p > 0:
                        if actualizar_precio(cod, nuevo_p, peliculas, cartelera):
                            print("Precio actualizado")
                        else:
                            print("El código no existe")
                    else:
                        print("El precio debe ser un entero positivo.")
                except ValueError:
                    print("Debe ingresar un valor entero para el precio")
                
                resp = input("¿Desea actualizar otro precio (s/n)?: ").strip().lower()
                if resp != 's':
                    procesando = False
        elif opc == 4:
            cod = input("Ingrese código de película: ")
            if not validar_codigo(cod, peliculas):
                print("Error: Código vacío o ya existente en el sistema.")
                continue

            tit = input("Ingrese título: ")
            if not validar_titulo(tit):
                print("Error: El título no puede estar vacío.")
                continue

            gen = input("Ingrese género: ")
            if not validar_genero(gen):
                print("Error: El género no puede estar vacío.")
                continue

            try:
                dur = int(input("Ingrese duración (minutos): "))
                if not validar_duracion(dur):
                    print("Error: La duración debe ser un entero mayor que cero.")
                    continue
            except ValueError:
                print("Error: Debe ingresar un entero para la duración.")
                continue

            clas = input("Ingrese clasificación (A/B/C): ")
            if not validar_clasificacion(clas):
                print("Error: La clasificación debe ser exactamente 'A', 'B' o 'C'.")
                continue

            idi = input("Ingrese idioma: ")
            if not validar_idioma(idi):
                print("Error: El idioma no puede estar vacío.")
                continue

            resp_3d = input("¿Es 3D? (s/n): ").strip().lower()
            if resp_3d in ['s', 'n']:
                es_3d = True if resp_3d == 's' else False
            else:
                print("Error: Debe responder 's' o 'n'.")
                continue

            try:
                prec = int(input("Ingrese precio: "))
                if not validar_precio(prec):
                    print("Error: El precio debe ser un número entero mayor que cero.")
                    continue
            except ValueError:
                print("Error: Debe ingresar un valor entero para el precio.")
                continue
            try:
                cup = int(input("Ingrese cupos: "))
                if not validar_cupos(cup):
                    print("Error: Los cupos deben ser un entero mayor o igual a cero.")
                    continue
            except ValueError:
                print("Error: Debe ingresar un valor entero para los cupos.")
                continue

            if agregar_pelicula(cod, tit, gen, dur, clas, idi, es_3d, prec, cup, peliculas, cartelera):
                print("Película agregada")
            else:
                print("El código ya existe")
        elif opc == 5:
            cod = input("Ingrese código de película a eliminar: ")
            if eliminar_pelicula(cod, peliculas, cartelera):
                print("Película eliminada")
            else:
                print("El código no existe")
        elif opc == 6:
            print("Programa finalizado.")
            continuar = False

if __name__ == "__main__":
    main()