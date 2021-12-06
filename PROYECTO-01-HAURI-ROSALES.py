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


#### 2. Productos por reseña del servicio


#### 3. Total de ingresos y ventas prmoedio mensuales, total anual y meses con más ventas al año

