def load_data():
    """
    Carga los siete datasets, unifica los dos dataset de "Deaths vaccines could have
    prevented" y devuelve todos los datasets dentro de un diccionario de DataFrames
    """

    import pandas as pd
    import os

    # RUTA BASE RELATIVA DESDE EL ARCHIVO ACTUAL (SRC/ETL.PY) HACIA DATA/RAW
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "data", "raw")

    # CARGA DE DATASETS
    vaccination_coverage = pd.read_csv(os.path.join(DATA_PATH, "Global vaccination coverage.csv"))
    life_expectancy = pd.read_csv(os.path.join(DATA_PATH, "Life expectancy.csv"))
    child_mortality = pd.read_csv(os.path.join(DATA_PATH, "Under five mortality rate.csv"))
    preventable_deaths_1 = pd.read_csv(os.path.join(DATA_PATH, "Deaths vaccines could have prevented 1.csv"))
    preventable_deaths_2 = pd.read_csv(os.path.join(DATA_PATH, "Deaths vaccines could have prevented 2.csv"))
    literacy = pd.read_csv(os.path.join(DATA_PATH, "Literacy.csv"))
    gdp = pd.read_csv(os.path.join(DATA_PATH, "Gross Domestic Product.csv"))

    # UNIFICACIÓN VERTICAL DE LOS DATASETS DE "DEATHS VACCINES COULD HAVE PREVENTED"
    preventable_deaths = pd.concat([preventable_deaths_1, preventable_deaths_2], ignore_index=True)

    return {
        "vaccination_coverage": vaccination_coverage,
        "life_expectancy": life_expectancy,
        "child_mortality": child_mortality,
        "preventable_deaths": preventable_deaths,
        "literacy": literacy,
        "gdp": gdp
    }

