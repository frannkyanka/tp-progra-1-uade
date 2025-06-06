"""
-----------------------------------------------------------------------------------------------
Título:
Fecha:
Autor:

Descripción:

Pendientes:
-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
...


#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------


def crearEntidad(entidades, campos):
    entidad = {}
    for campo, tipo in campos.items():
        entidad[campo] = inputCampo(campo, tipo, entidades)
    return entidad

def editarEntidad(entidades, campos):
    idEntidad = input("ID: ")
    if idEntidad not in entidades:
        print("El ID no existe.")
        return entidades
    print("Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")
    entidad = entidades[idEntidad]
    for campo, tipo in campos.items():
        if campo == "id":
            continue  # No se edita el ID
        entidad[campo] = inputCampo(campo, tipo, entidades, actual=entidad[campo])
    entidades[idEntidad] = entidad
    return entidades

def listarEntidades(entidades, campos):
    for idEntidad, datos in entidades.items():
        if "activo" in datos and not datos["activo"]:
            continue
        print(f"ID: {idEntidad}")
        for campo, tipo in campos.items():
            printCampo = printCamelCase(campo)
            if campo == "id":
                continue
            if tipo == dict:
                print(f"{printCampo}: {', '.join(datos[campo].values())}")
            elif tipo == bool:
                print(f"{printCampo}: {'Sí' if datos[campo] else 'No'}")
            else:
                print(f"{printCampo}: {datos[campo]}")
        print("---------------------------")

def eliminarEntidad(entidades, nombreEntidad="entidad"):
    print(f"Ingrese el ID de {nombreEntidad} a eliminar:")
    idEntidad = input(f"ID de {nombreEntidad}: ")
    if idEntidad in entidades:
        entidades[idEntidad]["activo"] = False
        print(f"{nombreEntidad.capitalize()} con ID {idEntidad} eliminada.")
    else:
        print(f"El ID de {nombreEntidad} no existe.")
    return entidades


def printCamelCase(texto):
    resultado = ""
    for i, c in enumerate(texto):
        if c.isupper() and i != 0:
            resultado += " "
        resultado += c
    return resultado.capitalize()


def inputCampo(campo, tipo, entidades=None, actual=None):
    printCampo = printCamelCase(campo)
    if isIdCampo(campo):
        return handleIdCampo(entidades)
    if tipo == dict:
        return handleDictCampo(campo, printCampo, actual)
    elif tipo == bool:
        return handleBoolCampo(printCampo, actual)
    elif tipo == int:
        return handleIntCampo(printCampo, actual)
    elif tipo == float:
        return handleFloatCampo(printCampo, actual)
    else:  # str u otros
        return handleStrCampo(printCampo, actual)
    
def isIdCampo(campo):
    return campo.lower() == "id"

def handleIdCampo(entidades):
    while True:
        idEntidad = input("ID:")
        if idEntidad in entidades:
            print("El ID ya existe. Intente con otro.")
        elif not idEntidad.strip():
            print("El ID no puede estar vacío. Intente con otro.")
        else:
            return idEntidad

def handleDictCampo(campo, printCampo, actual):
    resultado = {} if actual is None else actual.copy()
    contador = len(resultado) + 1
    while True:
        valor = input(f"Ingrese un valor para {printCampo} (o 'fin' para terminar): ")
        if valor.lower() == "fin":
            break
        if not valor.strip():
            print("El valor no puede estar vacío. Intente nuevamente.")
            continue
        resultado[f"{campo[:-1]}{contador}"] = valor
        contador += 1
    return resultado

def handleBoolCampo(printCampo, actual):
    if actual is not None:
        entrada = input(f"{printCampo} (si/no, actual: {'sí' if actual else 'no'}): ").strip().lower()
        if entrada == "":
            return actual
    else:
        entrada = input(f"{printCampo} (si/no): ").strip().lower()
    return entrada == "si"

def handleIntCampo(printCampo, actual):
    while True:
        prompt = f"{printCampo}" + (f" (actual: {actual})" if actual is not None else "") + ": "
        entrada = input(prompt)
        if entrada == "" and actual is not None:
            return actual
        try:
            return int(entrada)
        except ValueError:
            print("Debe ingresar un número entero.")

def handleFloatCampo(printCampo, actual):
    while True:
        prompt = f"{printCampo}" + (f" (actual: {actual})" if actual is not None else "") + ": "
        entrada = input(prompt)
        if entrada == "" and actual is not None:
            return actual
        try:
            return float(entrada)
        except ValueError:
            print("Debe ingresar un número decimal.")

def handleStrCampo(printCampo, actual):
    entrada = input(f"{printCampo}" + (f" (actual: {actual})" if actual is not None else "") + ": ")
    if entrada == "" and actual is not None:
        return actual
    return entrada


#----------------------------------------------------------------------------------------------
# SALONES
#----------------------------------------------------------------------------------------------

def camposSalon():
    return {
        "id": str,
        "nombre": str,
        "ubicacion": str,
        "capacidad": int,
        "equipamientos": dict,
        "empleados": dict,
        "accesoDiscapacitados": bool
    }

def ingresarSalon(salones):
    print("Ingrese los datos del salón:")
    campos = camposSalon()
    salon = crearEntidad(salones, campos)
    salon["activo"] = True  # Por defecto, el salón es activo al ingresarlo
    salones[salon["id"]] = salon
    return salones

def editarSalon(salones):
    print("Ingrese el ID del Salon a editar:")
    campos = camposSalon()
    salon = editarEntidad(salones, campos)
    if salon is None:
        return salones
    salones[salon["id"]] = salon
    return salones

def listarSalones(salones):
    print("Listado de salones activos:")
    campos = camposSalon()
    listarEntidades(salones, campos)
    


def eliminarSalon(salones):
    return eliminarEntidad(salones, "salón")


#----------------------------------------------------------------------------------------------
# BANDAS
#----------------------------------------------------------------------------------------------

def camposBanda():
    return {
        "id": str,
        "nombre": str,
        "generoMusical": str,
        "costoMediaHora": float,
        "contacto": str,
        "integrantes": dict
    }   

def ingresarBanda(bandas):
    print("Ingrese los datos de la banda:")
    campos = camposBanda()
    banda = crearEntidad(bandas, campos)
    banda["activo"] = True  # Por defecto, la banda es activa al ingresarla
    bandas[banda["id"]] = banda
    return bandas

def editarBanda(bandas):
    print("Ingrese el ID de la Banda a editar:")
    campos = camposBanda()
    banda = editarEntidad(bandas, campos)
    if banda is None:
        return bandas
    bandas[banda["id"]] = banda
    return bandas

def listarBandas(bandas):
    print("Listado de bandas activas:")
    campos = camposBanda()
    listarEntidades(bandas, campos)

def eliminarBanda(bandas):
        return eliminarEntidad(bandas, "banda")

#----------------------------------------------------------------------------------------------
# EVENTOS
#----------------------------------------------------------------------------------------------

def registrarEvento(eventos, salones, bandas):
    print("Registro de evento")

    id = input("Ingrese el ID del evento: ")
    if id in eventos:
        print("Ya existe un evento con ese ID.")
    else:
        fecha = input("Ingrese la fecha (formato libre): ")
        idSalon = input("Ingrese el ID del salón: ")

        if idSalon in salones:
            idBanda = input("Ingrese el ID de la banda: ")
            if idBanda in bandas:
                eventos[id] = {
                    "id": id,
                    "fecha": fecha,
                    "idSalon": idSalon,
                    "idBanda": idBanda
                }
                print("Evento registrado correctamente.")
            else:
                print("El ID de la banda no existe.")
        else:
            print("El ID del salón no existe.")

    return eventos

#----------------------------------------------------------------------------------------------
# INFORMES
#----------------------------------------------------------------------------------------------

def salonConMasEventos(eventos, salones):
    print("Salón con más eventos")

    conteo = {}

    for clave in eventos:
        idSalon = eventos[clave]["idSalon"]
        if idSalon in conteo:
            conteo[idSalon] += 1
        else:
            conteo[idSalon] = 1

    if len(conteo) == 0:
        print("No hay eventos registrados.")
    else:
        maxEventos = 0
        idSalonMax = ""

        for idSalon in conteo:
            if conteo[idSalon] > maxEventos:
                maxEventos = conteo[idSalon]
                idSalonMax = idSalon

        nombreSalon = salones[idSalonMax]["nombre"]
        print("El salón con más eventos es:", nombreSalon, "con", maxEventos, "evento(s).")

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
    salones = {
    "1": {
        "id": "1",
        "activo": True,
        "nombre": "Salón A",
        "ubicacion": "Centro",
        "capacidad": 200,
        "equipamientos": {
            "equipamiento1": "Sonido",
            "equipamiento2": "Luces",
            "equipamiento3": "Pantalla",  
        },
        "empleados": {
        "empleado1": "Juan Pérez",
        "empleado2": "Ana Gómez",
        "empleado3": "Luis Díaz",
        },
        "accesoDiscapacitados": True
        },
    }
    bandas = {
        "1": {
            "id": "1",
            "activo": True,
            "nombre": "Los Rockers",
            "generoMusical": "Rock",
            "costoMediaHora": 5000.0,
            "contacto": "rockers@email.com",
            "integrantes": {
                "integrante1": "Carlos",
                "integrante2": "Miguel",
                "integrante3": "Sofía",
                }
        }
    }
    eventos = {
        "1": {
            "id": "1",
            "fecha": "2025-06-10",
            "idSalon": "1",
            "idBanda": "1"
        },
        "2": {
            "id": "2",
            "fecha": "2025-06-15",
            "idSalon": "1",
            "idBanda": "1"
        }
    }



    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        while True:
            opciones = 5
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print("[1] Gestión de Salones")
            print("[2] Gestión de Bandas")
            print("[3] Registro de Evento")
            print("[4] Listado de Informes")
            print("---------------------------")
            print("[0] Salir del programa")
            print("---------------------------")
            print()
            
            opcionSubmenu = ""
            opcionMenuPrincipal = input("Seleccione una opción: ")
            if opcionMenuPrincipal in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcionMenuPrincipal == "0": # Opción salir del programa
            exit() # También puede ser sys.exit() para lo cual hay que importar el módulo sys

        elif opcionMenuPrincipal == "1":   # Opción 1 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > MENÚ DE SALONES")
                    print("---------------------------")
                    print("[1] Ingresar Salón")
                    print("[2] Editar Salón")
                    print("[3] Listar Salones activos")
                    print("[4] Eliminar Salón")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    salones = ingresarSalon(salones)
                    
                elif opcionSubmenu == "2":   # Opción 2 del submenú
                    salones = editarSalon(salones)
                
                elif opcionSubmenu == "3":   # Opción 3 del submenú
                    listarSalones(salones)
                
                elif opcionSubmenu == "4":   # Opción 4 del submenú
                    salones = eliminarSalon(salones)

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")


        elif opcionMenuPrincipal == "2":   # Opción 2 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > MENÚ DE BANDAS")
                    print("---------------------------")
                    print("[1] Ingresar Banda")
                    print("[2] Editar Banda")
                    print("[3] Listar Bandas activas")
                    print("[4] Eliminar Banda")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    bandas = ingresarBanda(bandas)
                    
                elif opcionSubmenu == "2":   # Opción 2 del submenú
                    bandas = editarBanda(bandas)

                elif opcionSubmenu == "3":   # Opción 3 del submenú
                    listarBandas(bandas)
                
                elif opcionSubmenu == "4":   # Opción 4 del submenú
                    bandas = eliminarBanda(bandas)

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")

        
        elif opcionMenuPrincipal == "3":   # Opción 3 del menú principal
            while True:
                while True:
                    opciones = 1
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Eventos")
                    print("---------------------------")
                    print("[1] Registro de Evento")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    eventos = registrarEvento(eventos)
                    

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")

        
        elif opcionMenuPrincipal == "4":   # Opción 4 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > INFORMES")
                    print("---------------------------")
                    print("[1] Eventos del Mes")
                    print("[2] Resumen Anual de Eventos por Banda (Cantidades)")
                    print("[3] Resumen Anual de Eventos por Banda(Pesos)")
                    print("[4] Ranking anual de costo por salón (Ordenado de mayor costo a menor)")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcionSubmenu == "0": # Opción salir del submenú
                    break # No sale del programa, sino que vuelve al menú anterior
                
                elif opcionSubmenu == "1":   # Opción 1 del submenú
                    ...
                    
                elif opcionSubmenu == "2":   # Opción 2 del submenú
                    ...
                
                elif opcionSubmenu == "3":   # Opción 3 del submenú
                    ...
                
                elif opcionSubmenu == "4":   # Opción 4 del submenú
                    ...

                input("\nPresione ENTER para volver al menú.") # Pausa entre opciones
                print("\n\n")


        if opcionSubmenu != "0": # Pausa entre opciones. No la realiza si se vuelve de un submenú
            input("\nPresione ENTER para volver al menú.")
            print("\n\n")


# Punto de entrada al programa
main()