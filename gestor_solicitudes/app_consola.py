cola_pendientes = []
pila_historial = []
siguiente_id = 1


def mostrar_estado():
    print("\nPendientes:", cola_pendientes)
    print("Historial:", pila_historial)

def registrar_solicitud(cliente, asunto):
    global siguiente_id
    cliente = cliente.strip()
    asunto = asunto.strip()
    if not cliente or not asunto:
        return None

    cliente_normalizado = cliente.casefold()
    asunto_normalizado = asunto.casefold()
    if any(
        solicitud["cliente"].casefold() == cliente_normalizado
        and solicitud["asunto"].casefold() == asunto_normalizado
        for solicitud in cola_pendientes
    ):
        return None

    solicitud = {
        "id": siguiente_id,
        "cliente": cliente,
        "asunto": asunto,
        "estado": "pendiente"
    }
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return solicitud


def obtener_estadisticas():
    ids_solicitudes = {
        solicitud["id"]
        for solicitud in cola_pendientes + pila_historial
    }
    return {
        "pendientes": len(cola_pendientes),
        "atendidas": len(pila_historial),
        "total_solicitudes": len(ids_solicitudes)
    }


registrar_solicitud("Ana", "No conecta a Wi-Fi")
registrar_solicitud("Luis", "Impresora sin papel")
registrar_solicitud("Sofía", "Equipo lento")
mostrar_estado()

def atender_siguiente():
    if not cola_pendientes:
        return None

    solicitud = cola_pendientes.pop(0)
    solicitud["estado"] = "atendida"
    pila_historial.append(solicitud)
    return solicitud


print("Atendida:", atender_siguiente())
mostrar_estado()

def deshacer_ultima_atencion():
    if not pila_historial:
        return None

    solicitud = pila_historial.pop()
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)
    return solicitud


print("Restaurada:", deshacer_ultima_atencion())
mostrar_estado()

def consultar_siguiente():
    if not cola_pendientes:
        return None
    return cola_pendientes[0]

print("Siguiente:", consultar_siguiente())

def buscar_solicitud(id_solicitud):
    for solicitud in cola_pendientes:
        if solicitud["id"] == id_solicitud:
            return solicitud
    for solicitud in pila_historial:
        if solicitud["id"] == id_solicitud:
            return solicitud
    return None

def cancelar_pendiente(id_solicitud):
    solicitud = buscar_solicitud(id_solicitud)
    if solicitud and solicitud["estado"] == "pendiente":
        cola_pendientes.remove(solicitud)
        return solicitud
    return None

def deshacer_varias(cantidad):
    
        try:
            cantidad = int(cantidad)
            if cantidad >= 0:
                for _ in range(cantidad):
                    deshacer_ultima_atencion()
            else:
                    print("Cantidad inválida")
        except ValueError:
            print("Cantidad inválida")

    

def ejecutar_menu():
    while True:
        print("\n1. Registrar solicitud")
        print("2. Atender siguiente")
        print("3. Deshacer última atención")
        print("4. Mostrar estado")
        print("5. Consultar siguiente")
        print("6. Buscar solicitud")
        print("7. Cancelar pendiente")
        print("8. Deshacer varias")
        print("9. Mostrar estadísticas")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            cliente = input("Cliente: ")
            asunto = input("Asunto: ")
            resultado = registrar_solicitud(cliente, asunto)
            if resultado:
                print("Registrada:", resultado)
            else:
                print("No registrada: datos inválidos o solicitud pendiente equivalente")
            
        elif opcion == "2":
            print("Atendida:", atender_siguiente())

        elif opcion == "3":
            print("Restaurada:", deshacer_ultima_atencion())

        elif opcion == "4":
            mostrar_estado()

        elif opcion == "5":
            print("Siguiente:", consultar_siguiente())

        elif opcion == "6":
            id_solicitud = int(input("ID de la solicitud: "))
            solicitud = buscar_solicitud(id_solicitud)
            print("Solicitud encontrada:", solicitud if solicitud else "No encontrada")

        elif opcion == "7":
            id_solicitud = int(input("ID de la solicitud: "))
            solicitud = cancelar_pendiente(id_solicitud)
            print("Solicitud cancelada:", solicitud if solicitud else "No encontrada")

        elif opcion == "8":
            cantidad = input("Cantidad a deshacer: ")
            deshacer_varias(cantidad)

        elif opcion == "9":
            print("Estadísticas:", obtener_estadisticas())

        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    ejecutar_menu()