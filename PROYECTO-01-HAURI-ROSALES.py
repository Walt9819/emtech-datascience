import sys

from lifestore_file import lifestore_products, lifestore_searches, lifestore_sales

# lifestore_searches = [id_search, id product]
# lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
# lifestore_products = [id_product, name, price, category, stock]


#### Login
# Usuario aceptado: admin
# Contra aceptada: 12345

# Pedir al usuario las credenciales de ingreso
usr = input("Usuario: ")
passw = input("Contraseña: ")

intentos = 0
# Si las ingresa de forma incorrecta volver a preguntar, 3 intentos y se cierra el programa
while not (usr == "admin" and passw == "12345"):
    print("El usuario y/o contraseña no son correctos. Vuelve a intentarlo")
    if intentos >= 3:
        sys.exit()
    intentos += 1



#### 1. Productos más vendidos y rezagados
print(f"{'*' * 10} Productos más vendidos y rezagados {'*' * 10}", end="\n\n") # título


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


def imprimirTop(productos, n, mayores=True):
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
        print(f"{i}. ID: {producto[0]}\tNombre: {producto[1]}\nVentas: {venta}\nPrecio: {producto[2]}\nCategoría: {producto[3]}\nInventario: {producto[4]}", end="\n\n")
        i += 1 if mayores else -1 # aumntamos la posición en uno por cada producto si ascendemos, en caso contrario le restamos


## ventas de productos
ventas = contabilizarApariciones(lifestore_sales, 1) # diccionario con todas las ventas por producto; el id_product es el elemento _1_
# ordenamos los valores
ventas = ordenarDiccionario(ventas)

## búsquedas de productos
busquedas = contabilizarApariciones(lifestore_searches, 1) # diccionario con las búsquedas por producto; el id_product es el elemento _1_
#ordenamos los valores
busquedas = ordenarDiccionario(busquedas)

## Top mejores ventas y búsquedas
# Ventas
print(f"{'-' * 40}\nLos mejores productos\n{'-' * 40}")
print(f"{'*' * 5} Mejores productos por ventas:")
imprimirTop(ventas, 5, mayores=True)

# Búsquedas
print(f"{'*' * 5} Mejores productos por búsqueda:")
imprimirTop(busquedas, 10, mayores=True)

## Top peores ventas y búsqueda
print(f"{'-' * 40}\nLos peores productos\n{'-' * 40}")
print(f"{'*' * 5} Peores productos por ventas:")
imprimirTop(ventas, 5, mayores=False)

# Búsquedas
print(f"{'*' * 5} Peores productos por búsqueda:")
imprimirTop(busquedas, 10, mayores=False)

#### 2. Productos por reseña del servicio


#### 3. Total de ingresos y ventas prmoedio mensuales, total anual y meses con más ventas al año

