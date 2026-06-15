import json
import subprocess
import sys

# ------------------------------------------------------------
# Caso de prueba para nivel de acoplamiento segun dependencias
#
# Requerimiento no funcional 03 - Mantenibilidad
# Utilizando pydeps
# ------------------------------------------------------------

def obtener_deps():
    result = subprocess.run(
        ['pydeps', '../stock', '--no-output', '--show-deps'],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


def calcular_metricas(deps):
    # Excluir módulos externos
    EXCLUIR = ['django', 'os', 'sys', 'csv', 'json', 'pathlib', 'datetime']
    
    def es_propio(nombre):
        if nombre == '__main__':
            return False
        for excl in EXCLUIR:
            if nombre == excl or nombre.startswith(excl + '.'):
                return False
        return nombre.startswith('stock')

    print("=" * 60)
    print("                       Nivel de acoplamiento (dependencias)")
    print("=" * 60)
    
    print("Modulo\t\tImportado por\tImporta a\t\tTotal\tEvaluacion")
    print("-" * 60)
    
    for nombre, datos in deps.items():
        if not es_propio(nombre):
            continue
        
        fan_in = len(datos.get('imported_by', []))
        fan_out = len(datos.get('imports', []))
        total = fan_in + fan_out
        
        if total <= 6:
            eval_text = "Bajo"
        elif total <= 10:
            eval_text = "Medio"
        else:
            eval_text = "Alto"
        
        nombre_limpio = nombre.replace('stock.', '')
        
        print(f"{nombre_limpio}\t\t{fan_in}\t\t{fan_out}\t\t{total}\t\t{eval_text}")


deps = obtener_deps()
calcular_metricas(deps)
