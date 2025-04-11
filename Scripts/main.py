import sys
import os

# SE AÑADE EL PATH DE LA CARPETA SRC AL SYS.PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from etl import load_data as run_etl
from eda import run_eda
from stats import run_stats

def main():
    print("Iniciando ETL...")
    datasets = run_etl()
    print("\n atasets cargados:")
    for nombre, df in datasets.items():
        print(f"→ {nombre}: {df.shape[0]} filas, {df.shape[1]} columnas")
    print ("ETL completado.")

    print("\n Iniciando EDA...")
    run_eda()
    print ("EDA completado.")

    print("\n Iniciando análisis estadístico...")
    run_stats()
    print ("Análisis estadístico completado.")

if __name__ == "__main__":
    main()