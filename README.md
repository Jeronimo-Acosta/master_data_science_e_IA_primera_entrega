# Análisis de Tasa de Vacunación y Otros Indicadores Globales

Este repositorio contiene siete datasets. En el caso de los datasets de "Deaths vaccines could have prevented", se trata del mismo dataset partido en dos, por lo que se lo unifica y terminan siendo seis datasets con los que se trabaja a lo largo del código. 
Se hace un análisis de la tasa de vacunación y su relación con indicadores globales como la esperanza de vida, mortalidad infantil, PIB y alfabetización. 

## Estructura del repositorio

El repositorio consta de la siguiente estructura:

├── data/
│   ├── raw/ (datasets crudos)
│   └── processed/ (datasets limpios)
│   └── figures/ (imágenes generadas por el código o utilizadas en el dashboard)
├── dashboards/   
├── notebooks/
│   ├── main.py
├── src/
│   ├── etl.py
│   ├── eda.py
│   └── stats.py
├── requirements.txt
├── .gitignore
└── README.md

El main.py dentro de notebooks llama a etl.py, eda.py y stats.py dentro de src, y exporta datos a data/processed e imágenes a data/figures. 

## Pipeline

Debido a que los seis datasets con los que se trabaja a lo largo de todo el proyecto son similares pero no exactamente iguales, el código es muy repetitivo, porque exige funciones específicas para cada dataset que realizan extensas tareas de limpieza y procesamiento. Por ejemplo, casi todos trabajan con la columna de "Entidades", que son localizaciones geográficas. Al margen de incluir países, cada columna de "Entidades" de cada dataset puede contener también nombres de ciudades o sus propias categorías inventadas, como "África-subsahariana", "Australasia", "Países de bajos ingresos (OMS)". Para que todos los datasets trabajen exclusivamente con países, se debe crear un diccionario customizado de geografías que no sean países, para luego eliminar esos elementos y los datos asociados de la columna "Entidades" (que, a su vez, luego pasará a llamarse "Países").
Respecto al análisis y gráficos estadísticos, en primera instancia, para todos los casos, se procede a calcular y graficar distintos atributos estadísticos como media o varianza, por más de que conceptualmente no tengan mucho sentido, con el simple fin de cumplir con el enunciado. Para realizar estos análisis y poder extraer conclusiones más útiles, se los repite, para cada dataset, pero agrupando según país o año. 

## Instalación

Para replicar este proyecto:

- Clona este repositorio a tu máquina local con el siguiente comando: git clone https://github.com/Jeronimo-Acosta/master_data_science_e_IA_primera_entrega/tree/main
- python -m venv venv (en Windows)
- .\venv\Scripts\actívate (en Windows)
- pip install -r requirements.txt
- python notebooks/main.py