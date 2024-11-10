# utils.py
import os
import platform










'''
>>> Funciones utilitarias
'''
def verificar_rutas_almacenamiento():
    storage_path = os.path.join('Storage', 'Frames')
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    return storage_path

def limpiar_consola():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return ''