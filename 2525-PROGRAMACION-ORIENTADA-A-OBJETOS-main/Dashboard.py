import os
import subprocess

# ==========================================================
# CONFIGURACIÓN DE COLORES ANSI
# Finalidad: mejorar la legibilidad de la interfaz en consola
# sin depender de librerías externas.
# ==========================================================
class Colores:
    TITULO = '\033[96m'
    OPCION = '\033[92m'
    ADVERTENCIA = '\033[93m'
    ERROR = '\033[91m'
    RESET = '\033[0m'
    NEGRITA = '\033[1m'


# ==========================================================
# DEFINICIÓN DE ICONOS
# Finalidad: reforzar visualmente las opciones del menú,
# manteniendo un estilo formal y funcional.
# ==========================================================
class Iconos:
    MENU = "📘"
    CARPETA = "📁"
    SCRIPT = "🐍"
    EJECUTAR = "▶"
    VOLVER = "↩"
    SALIR = "❌"
    INFO = "ℹ"
    ERROR = "⚠"


# ==========================================================
# FUNCIÓN PARA LIMPIAR LA CONSOLA
# Finalidad: evitar saturación visual y facilitar la lectura.
# ==========================================================
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# ==========================================================
# FUNCIÓN PARA MOSTRAR TÍTULOS
# Finalidad: estandarizar la presentación de encabezados.
# ==========================================================
def mostrar_titulo(texto):
    print(Colores.TITULO + Colores.NEGRITA)
    print("═" * 60)
    print(f"{Iconos.MENU} {texto}".center(60))
    print("═" * 60)
    print(Colores.RESET)


# ==========================================================
# VISUALIZACIÓN DEL CÓDIGO FUENTE
# Finalidad: permitir la revisión del script antes de ejecutar.
# ==========================================================
def mostrar_codigo(ruta_script):
    ruta_absoluta = os.path.abspath(ruta_script)

    try:
        with open(ruta_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print("\n" + Colores.ADVERTENCIA +
                  f"{Iconos.INFO} Contenido del script\n" +
                  Colores.RESET)
            print(codigo)
            return codigo

    except FileNotFoundError:
        print(Colores.ERROR + f"{Iconos.ERROR} Archivo no encontrado." + Colores.RESET)
    except Exception as e:
        print(Colores.ERROR + f"{Iconos.ERROR} Error inesperado: {e}" + Colores.RESET)

    return None


# ==========================================================
# EJECUCIÓN DE SCRIPTS
# Finalidad: ejecutar el archivo seleccionado en una terminal
# independiente, sin interrumpir el dashboard.
# ==========================================================
def ejecutar_codigo(ruta_script):
    try:
        print(Colores.OPCION + f"\n{Iconos.EJECUTAR} Ejecutando script...\n" + Colores.RESET)
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Linux / macOS
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(Colores.ERROR + f"{Iconos.ERROR} Error al ejecutar: {e}" + Colores.RESET)


# ==========================================================
# MENÚ PRINCIPAL
# Finalidad: permitir la selección de unidades académicas.
# ==========================================================
def mostrar_menu():
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2'
    }

    while True:
        limpiar_pantalla()
        mostrar_titulo("Dashboard de Scripts Python")

        for clave, unidad in unidades.items():
            print(f"{Iconos.CARPETA} {Colores.OPCION}{clave}{Colores.RESET} - {unidad}")

        print(f"\n{Iconos.SALIR} 0 - Salir del sistema")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '0':
            break
        elif opcion in unidades:
            mostrar_sub_menu(os.path.join(ruta_base, unidades[opcion]))
        else:
            print(Colores.ERROR + f"{Iconos.ERROR} Opción no válida." + Colores.RESET)
            input("Presione Enter para continuar...")


# ==========================================================
# SUBMENÚ DE CARPETAS
# Finalidad: mostrar las subcarpetas de cada unidad.
# ==========================================================
def mostrar_sub_menu(ruta_unidad):
    carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        limpiar_pantalla()
        mostrar_titulo("Selección de Carpeta")

        for i, carpeta in enumerate(carpetas, start=1):
            print(f"{Iconos.CARPETA} {Colores.OPCION}{i}{Colores.RESET} - {carpeta}")

        print(f"\n{Iconos.VOLVER} 0 - Regresar")

        opcion = input("\nSeleccione una carpeta: ")

        if opcion == '0':
            break

        try:
            indice = int(opcion) - 1
            if 0 <= indice < len(carpetas):
                mostrar_scripts(os.path.join(ruta_unidad, carpetas[indice]))
            else:
                raise ValueError
        except ValueError:
            print(Colores.ERROR + f"{Iconos.ERROR} Selección inválida." + Colores.RESET)
            input("Presione Enter para continuar...")


# ==========================================================
# MENÚ DE SCRIPTS
# Finalidad: listar, revisar y ejecutar scripts Python.
# ==========================================================
def mostrar_scripts(ruta_sub_carpeta):
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta)
               if f.is_file() and f.name.endswith('.py')]

    while True:
        limpiar_pantalla()
        mostrar_titulo("Scripts Disponibles")

        for i, script in enumerate(scripts, start=1):
            print(f"{Iconos.SCRIPT} {Colores.OPCION}{i}{Colores.RESET} - {script}")

        print(f"\n{Iconos.VOLVER} 0 - Regresar")
        print(f"{Iconos.MENU} 9 - Menú principal")

        opcion = input("\nSeleccione un script: ")

        if opcion == '0':
            break
        if opcion == '9':
            return

        try:
            indice = int(opcion) - 1
            if 0 <= indice < len(scripts):
                ruta_script = os.path.join(ruta_sub_carpeta, scripts[indice])
                codigo = mostrar_codigo(ruta_script)

                if codigo:
                    ejecutar = input("\n¿Ejecutar el script? (1 = Sí | 0 = No): ")
                    if ejecutar == '1':
                        ejecutar_codigo(ruta_script)

                input("\nPresione Enter para continuar...")
            else:
                raise ValueError
        except ValueError:
            print(Colores.ERROR + f"{Iconos.ERROR} Selección inválida." + Colores.RESET)
            input("Presione Enter para continuar...")


# ==========================================================
# PUNTO DE INICIO DEL PROGRAMA
# ==========================================================
if __name__ == "__main__":
    mostrar_menu()

     
