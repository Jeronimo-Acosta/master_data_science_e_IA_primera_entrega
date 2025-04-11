import sys
import os

# RUTA BASE RELATIVA DESDE EL ARCHIVO ACTUAL (NOTEBOOKS/MAIN.PY) HACIA SRC.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from etl import load_data as run_etl
from eda import run_eda
from stats import run_stats

def main():
    '''
    Llama a los archivos etl.py, eda.py y stats.py para ejecutar el flujo de trabajo.
    '''
    
    print("Iniciando ETL...")
    datasets = run_etl()
    print("\n Datasets cargados:")
    for nombre, df in datasets.items():
        print(f"→ {nombre}: {df.shape[0]} filas, {df.shape[1]} columnas")
    print ("ETL completado.")

    print("\n Iniciando EDA...")
    run_eda()
    print ("EDA completado.")

    print("\n Iniciando análisis estadístico...")
    run_stats()
    print ("Análisis estadístico completado.")

'''
RESULTADOS:

1. Matriz de correlación:
La matriz de correlación muestra cómo las diferentes variables se relacionan entre sí a lo largo del
tiempo. Se observó que: 
- La vacunación promedio tiene una correlación positiva con la esperanza de vida (0.63), lo que sugiere
que, a medida que aumentan las tasas de vacunación, la esperanza de vida tiende a mejorar.
- La vacunación promedio tiene una correlación negativa con la mortalidad infantil (-0.67), indicando
que un aumento en las tasas de vacunación está asociado con una reducción en la mortalidad infantil.

2. Regresión lineal:
- Esperanza de vida vs Tasa de vacunación: la regresión muestra que existe una relación positiva entre
ambas variables, con un R² de 0.40, lo que significa que aproximadamente el 40% de la variabilidad
en la esperanza de vida puede ser explicada por la tasa de vacunación. Esto respalda la hipótesis de
que la vacunación tiene un impacto positivo en la esperanza de vida.
- Mortalidad infantil vs Tasa de vacunación: la relación es negativa, con un R² de 0.45, lo que implica
que un 45% de la variabilidad en la mortalidad infantil puede ser explicada por las tasas de vacunación.
Esto indica que un aumento en la tasa de vacunación está asociado con una disminución en la mortalidad 
infantil.

3. Distribución de los residuos:
El análisis de residuos muestra que, para ambas regresiones, los residuos siguen un patrón relativamente
aleatorio, lo que sugiere que los modelos son adecuados para las relaciones entre las variables.

4. Pruebas de hipótesis:
Los tests de hipótesis realizados sobre los efectos de las vacunas sobre la esperanza de vida y la 
mortalidad infantil fueron significativos, lo que implica que las vacunas tienen un impacto positivo 
en ambas variables.

En resumen, los resultados obtenidos indican que las vacunas juegan un papel crucial en la mejora 
de la esperanza de vida y en la reducción de la mortalidad infantil, lo que justifica su implementación
masiva a nivel mundial.
'''

if __name__ == "__main__":
    main()