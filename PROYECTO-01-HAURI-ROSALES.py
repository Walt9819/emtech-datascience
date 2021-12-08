import sys

from lifestore_file import lifestore_products, lifestore_searches, lifestore_sales

# lifestore_searches = [id_search, id product]
# lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
# lifestore_products = [id_product, name, price, category, stock]


#### Funciones de utilidad
def contabilizarApariciones(datos, elemento_con_id_producto=0):
    """
    Cuenta el número de incidencias de un producto en un arreglo de datos.
    Regresa un diccionario con las llaves siendo el id de los productos, 
    y su valor el número de apariciones que tuvo en `datos`.
    """
    repeticiones = {} # si suponemos que los id son continuos y ordenados, podría ser un arreglo
    for dat in datos:
        id_producto = dat[elemento_con_id_producto]
        # consideramos esta como su primera aparición si no había antes, de lo contrario le sumamos una más
        if id_producto not in repeticiones.keys():
            repeticiones[id_producto] = 1
        else:
            repeticiones[id_producto] += 1
    return repeticiones


def ordenarDiccionario(d, descendente=True):
    """
    Toma un diccionario y lo ordena según sus valores.
    Regresa un arreglo ordenado de tuplas, con formato `(key, value)`.
    Adaptado de: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    """
    return [(k, v) for k, v in sorted(d.items(), key=lambda item: item[1], reverse=descendente)]


def buscarProducto(productos, id_producto, elemento_con_id = 0):
    """
    Regresa el índice del producto buscado en la lista de productos
    """
    for p in productos:
        if p[elemento_con_id] == id_producto:
            return p


def imprimirTop(productos, n, mayores=True, value=""):
    """
    Imprime en pantalla la información de los `n` productos con mayor valor (si `mejores`),
    en caso contrario los de menor valor.
    """
    num_productos = len(productos)
    rango = productos[:n] if mayores else productos[num_productos:num_productos-n-1:-1] # definimos los productos a desplegar dependiendo de si queremos los de mayor o menor valor
    i = 1 if mayores else num_productos # empezamos en 1 si queremos los mejores, en caso contrario empezamos con número de productos disponibles
    # recorremos e imprimimos los productos en el rango
    for prod, venta in rango:
        producto = buscarProducto(lifestore_products, prod) # buscamos el producto
        imprimirProducto(producto, i, (value, venta))
        i += 1 if mayores else -1 # aumntamos la posición en uno por cada producto si ascendemos, en caso contrario le restamos


def imprimirProducto(producto, i, value=None):
    """
    Imprime información importante de un producto de forma legible
    """
    vS = '\n' + str(value[0]) + ': ' + str(value[1]) if value else '' # con cierto valor si fue dado
    print(f"{i}. ID: {producto[0]}\tNombre: {producto[1]}{vS}\nPrecio: {producto[2]}\nCategoría: {producto[3]}\nInventario: {producto[4]}", end="\n\n")


def ventasPorFecha(ventas, productos, elemento_fecha = 3, elemento_producto=1, elemento_precio_en_producto=2, caracter_fecha='/'):
    """
    Cuenta y acumula las ventas en ´ventas´ según la fecha en el elemento ´elemento_fecha´,
    separada en el formato ´d/m/a´ con separador ´caracter_fecha´.
    Regresa un diccionario con llaves de cada año disponible, cada uno con los meses de venta
    como llave, teniendo dos valores ´numeroVentas´ y ´montoVentas´, el primero con el número total
    de ventas ese mes, y el segundo el monto total de dichas ventas. 
    """
    ventas_total = {}
    # guardar para cada año y cada mes las ventas realizadas
    for venta in ventas:
        producto = venta[elemento_producto] # obtener el producto
        fecha = venta[elemento_fecha] # obtener la fecha
        fecha = fecha.split(caracter_fecha) # separar día, mes y año
        day = fecha[0]
        month = int(fecha[1])
        year = int(fecha[2])
        # guardar en el diccionario con la llave del año
        if not year in ventas_total.keys():
            ventas_total[year] = {} # diccionario para los meses de este año
        if not month in ventas_total[year].keys():
            ventas_total[year][month] = {"numeroVentas": 0, "montoVentas": 0} # agregamos el mes si es que todavía no existe, con dos llaves: `numeroVentas` (cantidad de ventas realizadas) y `montoVentas` (monto acumulado de las ventas)
        ventas_total[year][month]["numeroVentas"] += 1 # aumentamos en 1 las ventas de este mes
        ventas_total[year][month]["montoVentas"] += buscarProducto(productos, producto)[elemento_precio_en_producto] # obtenemos el precio del producto comprado
    return ventas_total


def agregarSiMayor(actuales, nuevo, max_valores=3):
    """
    Revisa si el monto en la tupla ´nuevo´ es mayor al menor que ya
    había en las tuplas ´actuales´, si sí reemplaza al menor. Agrega valores
    hasta tener al menos los ´max_valores´ mayores
    """
    # si no tenemos el número máximo de meses todavía, agregamos el nuevo
    if len(actuales) < max_valores:
        actuales.append(nuevo)
    # si el menor valor de los actuales es menor que el nuevo, entonces lo va a reemplazar
    # en las tuplas el primer valor es el mes (´nuevo[0]´) y el segundo el monto (´nuevo[1]´)
    elif actuales[-1][1] < nuevo[1]:
        actuales[-1] = nuevo
    actuales.sort(key=lambda a: a[1], reverse=True) # regresamos el arreglo ordenado _inplace_ según el segundo valor de las tuplas para las siguientes comparaciones


def seleccionDeOpcion(acciones):
    opciones = "\n".join([f"{i}. {ac[0]}" for i, ac in enumerate(acciones)]) # hacemos una lista con las opciones
    ans = None # empezamos sin selección
    # hacemos un ciclo infinito
    while True:
        # preguntamos por la acción a analizar
        ans = input(f"\n{'/'*80}\nHola, ¿qué análisis deseas explorar? Elige una de las opciones siguientes:\n{opciones}\nOpción: ")
        # si no es un número, es inválida
        try:
            ans = int(ans)
        except:
            print("Operación inválida, por favor vuelve a intentarlo")
            continue
        # si da un número fuera de las opciones, es inválido
        if ans >= len(acciones):
            print("Operación inválida, por favor vuelve a intentarlo")
            continue
        # si es una de las opciones, ejecutar su respectiva función asociada
        acciones[ans][1]() # ejecutarla


def conteoPorCategoria(todos_productos, conteo_productos, id_categoria_producto=3):
    """
    Revisa y clasifica los productos por categoría y revisa cuántos aparecen con conteo y cuántos no.
    Regresa el total de productos por categoría, y el total sin conteo
    """
    productosConteo = [k[0] for k in conteo_productos] # elegir todos los productos con conteo
    sinConteo = {} # productos en cada categoría sin conteo
    total = {} # todos los productos por categiría
    # para cada producto, agregarlo a su categoría, y si no tuvo conteo, agregarlo también a sin conteo
    for producto in todos_productos:
        cat = producto[id_categoria_producto] # obtenemos la categoría del producto
        if cat in total.keys():
            total[cat] += 1
        else:
            total[cat] = 1
        if not producto[0] in productosConteo:
            # si no estuvo en el conteo, agregarlo a sin conteo
            if cat in sinConteo.keys():
                sinConteo[cat] += 1
            else:
                sinConteo[cat] = 1
    return total, sinConteo # regresamos ambos resultados



#### Interacción del usuario
def main():
    login() # el usuario tiene que ingresar las credenciales primero
    # todas las posibles acciones a realizar
    acciones = [
        ("Salir", sys.exit), 
        ("Productos más vendidos o rezagados", productosMasVendidos), 
        ("Productos por reseña en el servicio", productosPorResenas), 
        ("Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año", ingresosVentasMensualesAnuales)
    ]
    seleccionDeOpcion(acciones) # permitir al usuario seleccionar la opción deseada
    

#### Login
def login():
    # Usuario aceptado: admin
    # Contra aceptada: 12345

    # Pedir al usuario las credenciales de ingreso
    usr = input("Usuario: ")
    passw = input("Contraseña: ")

    intentos = 0
    LIM_INTENTOS = 3
    # Si las ingresa de forma incorrecta volver a preguntar, 3 intentos y se cierra el programa
    while not (usr == "admin" and passw == "12345"):
        intentos += 1
        print(f"El usuario y/o contraseña no son correctos. Vuelve a intentarlo.\nIntentos restantes: {LIM_INTENTOS - intentos}")
        if intentos >= LIM_INTENTOS:
            sys.exit()
        usr = input("Usuario: ")
        passw = input("Contraseña: ")
    return True


#### 1. Productos más vendidos y rezagados
def productosMasVendidos():
    print(f"{'*' * 60}\n1. Productos más vendidos y productos rezagados\n{'*' * 60}") # título
    ## ventas de productos
    ventas = contabilizarApariciones(lifestore_sales, 1) # diccionario con todas las ventas por producto; el id_product es el elemento _1_
    # ordenamos los valores
    ventas = ordenarDiccionario(ventas)

    ## búsquedas de productos
    busquedas = contabilizarApariciones(lifestore_searches, 1) # diccionario con las búsquedas por producto; el id_product es el elemento _1_
    #ordenamos los valores
    busquedas = ordenarDiccionario(busquedas)
    
    ## Top mejores ventas y búsquedas
    print(f"{'-' * 40}\nLos mejores productos\n{'-' * 40}")
    # Ventas
    print(f"{'*' * 5} Mejores productos por ventas:")
    imprimirTop(ventas, 5, mayores=True, value="Ventas")

    # Búsquedas
    print(f"{'*' * 5} Mejores productos por búsqueda:")
    imprimirTop(busquedas, 10, mayores=True, value="Búsquedas")

    ## Top peores ventas y búsqueda
    print(f"{'-' * 40}\nLos peores productos\n{'-' * 40}")
    # Ventas
    print(f"{'*' * 5} Peores productos por ventas:")
    imprimirTop(ventas, 5, mayores=False, value="Ventas")

    # Búsquedas
    print(f"{'*' * 5} Peores productos por búsqueda:")
    imprimirTop(busquedas, 10, mayores=False, value="Búsquedas")

    ## Sin búsquedas ni ventas
    print(f"{'-' * 40}\nSin movimiento\n{'-' * 40}")
    # Ventas
    print(f"{'*' * 5} Productos sin ventas por categoría:")
    total, sinVentas = conteoPorCategoria(lifestore_products, ventas)
    for k in total.keys():
        print(f"Categoría: {k}\nTotal de productos: {total[k]}\nProductos sin ventas: {sinVentas[k] if k in sinVentas.keys() else '0'}", end='\n\n')

    # Búsquedas
    print(f"{'*' * 5} Productos sin búsquedas por categoría:")
    total, sinBusquedas = conteoPorCategoria(lifestore_products, busquedas)
    for k in total.keys():
        print(f"Categoría: {k}\nTotal de productos: {total[k]}\nProductos sin búsquedas: {sinBusquedas[k] if k in sinBusquedas.keys() else '0'}", end='\n\n')



#### 2. Productos por reseña del servicio
def productosPorResenas():
    print(f"{'*' * 60}\n2. Productos por reseña en el servicio\n{'*' * 60}") # título

    ## Ordenar por calificación (compra[1] es id_product, compra[2] es la calificación de la reseña)
    calificaciones = {compra[1]: compra[2] for compra in lifestore_sales}
    calificaciones = ordenarDiccionario(calificaciones)

    ## Top mejores calificaciones
    print(f"{'-' * 40}\nLos mejores productos\n{'-' * 40}")
    imprimirTop(calificaciones, 5, mayores=True, value="Calificación")

    ## Top peores calificaciones
    print(f"{'-' * 40}\nLos peores productos\n{'-' * 40}")
    imprimirTop(calificaciones, 5, mayores=False, value="Calificación")


#### 3. Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año
def ingresosVentasMensualesAnuales():
    print(f"{'*' * 60}\n3. Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año\n{'*' * 60}") # título

    ## Agrupamos las ventas por mes y año
    ventas = ventasPorFecha(lifestore_sales, lifestore_products) # agrupamos por años y meses

    ## Desplegamos el resumen de ventas por mes para cada año
    for y in sorted(ventas):
        months = ventas[y] # obtenemos los diccionarios de este año
        print(f"{'-' * 40}\nVentas para el año {y}\n{'-' * 40}")
        total = 0 # ventas totales anuales
        mejores = [] # lista con los mejores meses en ventas
        # desplegamos la lista de ventas por mes
        for m in sorted(months):
            valores = months[m] # obtenemos este mes del diccionario
            nVentas = valores["numeroVentas"]
            mVentas = valores["montoVentas"]
            total += mVentas # incrementamos las ganancias anuales
            agregarSiMayor(mejores, (m, nVentas)) # si tiene más ventas que los anteriores, lo agregamos
            print(f"Mes: {m}\nVentas: {nVentas}\nMonto de venta promedio: {mVentas / nVentas:.2f}", end="\n\n")
        print(f"Ganancias totales anuales: {total:.2f}", end="\n\n")
        print(f"Meses con mayor número de ventas: ")
        for mes, nV in mejores:
            print(f"Mes: {mes}\tNúmero de ventas: {nV}")


# Ejecutar la función main primero
if __name__ == "__main__":
    main()