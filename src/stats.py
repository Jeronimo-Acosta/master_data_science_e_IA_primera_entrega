
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.api as sm
from scipy import stats
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression

# DEFINICIÓN DE DIRECTORIOS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")
FIGURES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "figures")


def run_stats() :
    '''
    Realiza un análisis estadístico descriptivo e inferencial de los datasets. Calcula parámetros de
    tendencia central (media, mediana, moda) y de dispersión (rango, varianza, desviación estándar, 
    percentiles). Además, genera gráficos de histogramas, boxplots y KDE para cada variable numérica.
    También realiza un análisis de correlación entre las variables, un análisis de regresión lineal
    entre las variables de interés y dos tests de hipótesis.
    Aclaración: se realizan estas tareas para los seis datasets de entrada tal como están, por más de 
    que no tenga mucho sentido, dada la estructura de lo mismos, a fin de cumplir con el enunciado. Por
    ejemplo, hay vacunas que no se aplican en algunos países, simplemente porque las enfermedades que 
    previenen no son endémicas en esos países, como la fiebre amarilla, que es endémica en África y 
    Sudamérica, y por lo tanto arroja valores de cero en muchos países. Lo mismo sucede con muertes que
    podrían haberse evitado con la aplicación de la vacuna correspondiente. Lo que sí tiene más sentido,
    que se desarrolla luego en este mismo archivo, es un análisis similar pero agrupando por país y/o
    año.
    Al igual que en eda.py, son seis funciones de análisis estadístico, uno para cada 
    dataset, pues la estructura de cada uno es similar pero no exactamente igual. Las seis funciones
    de análisis estadístico son muy similares entre sí. 
    '''

    # CARGA DE LOS DATASETS YA LIMPIOS
    vaccination_coverage = pd.read_csv(os.path.join(PROCESSED_PATH, 'vaccination_coverage_processed.csv'))
    life_expectancy = pd.read_csv(os.path.join(PROCESSED_PATH, 'life_expectancy_processed.csv'))
    child_mortality = pd.read_csv(os.path.join(PROCESSED_PATH, 'child_mortality_processed.csv'))
    preventable_deaths = pd.read_csv(os.path.join(PROCESSED_PATH, 'preventable_deaths_processed.csv'))
    literacy = pd.read_csv(os.path.join(PROCESSED_PATH, 'literacy_processed.csv'))
    gdp = pd.read_csv(os.path.join(PROCESSED_PATH, 'gdp_processed.csv'))
    
    # LLAMADA A LAS FUNCIONES DE ESTADÍSTICA
    stats_vaccination_coverage(vaccination_coverage)
    stats_life_expectancy(life_expectancy)
    stats_child_mortality(child_mortality)
    stats_preventable_deaths(preventable_deaths)
    stats_literacy(literacy)
    stats_gdp(gdp)
    stats_inferential(vaccination_coverage, life_expectancy, preventable_deaths, literacy, child_mortality, gdp)


# ---------------------- ESTADÍSTICA DE VACCINES_COVERAGE ----------------------

def stats_vaccination_coverage(vaccination_coverage) :
    """
    Realiza un análisis estadístico descriptivo e inferencial, tanto al dataset como tal, así como 
    al dataset agrupado según corresponda. Calcula parámetros de tendencia central (media, mediana, moda) y de dispersión (rango, varianza, desviación estándar, 
    percentiles). Exporta como .png los gráficos a data/figures. 
    """

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO 
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    vaccines_columns = vaccination_coverage.columns.difference(['País', 'Año'])
    vaccination_coverage_mean = vaccination_coverage[vaccines_columns].mean()
    vaccination_coverage_median = vaccination_coverage[vaccines_columns].median()
    vaccination_coverage_mode = vaccination_coverage[vaccines_columns].mode().iloc[0]
    vaccination_coverage_std = vaccination_coverage[vaccines_columns].std()
    vaccination_coverage_var = vaccination_coverage[vaccines_columns].var()
    vaccination_coverage_percentile_25 = vaccination_coverage[vaccines_columns].quantile(0.25)
    vaccination_coverage_percentile_50 = vaccination_coverage[vaccines_columns].quantile(0.50)
    vaccination_coverage_percentile_75 = vaccination_coverage[vaccines_columns].quantile(0.75)
    vaccination_coverage_min = vaccination_coverage[vaccines_columns].min()
    vaccination_coverage_max = vaccination_coverage[vaccines_columns].max()
    vaccination_coverage_range = vaccination_coverage_max - vaccination_coverage_min

    print(f"La media para cada vacuna es:\n{vaccination_coverage_mean}\n")
    print(f"La mediana para cada vacuna es:\n{vaccination_coverage_median}\n")
    print(f"La moda para cada vacuna es:\n{vaccination_coverage_mode}\n")
    print(f"La desviación estándar para cada vacuna es:\n{vaccination_coverage_std}\n")
    print(f"La varianza para cada vacuna es:\n{vaccination_coverage_var}\n")
    print(f"El percentil 25 para cada vacuna es:\n{vaccination_coverage_percentile_25}\n")
    print(f"El percentil 50 para cada vacuna es:\n{vaccination_coverage_percentile_50}\n")
    print(f"El percentil 75 para cada vacuna es:\n{vaccination_coverage_percentile_75}\n")
    print(f"El valor mínimo para cada vacuna es:\n{vaccination_coverage_min}\n")
    print(f"El valor máximo para cada vacuna es:\n{vaccination_coverage_max}\n")
    print(f"El rango para cada vacuna es:\n{vaccination_coverage_range}\n")

    # GRÁFICO DE HISTOGRAMA, BOXPLOT Y KDE DE CADA VACUNA
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA EN EL ARCHIVO MAIN.PY. SÓLO LO HAGO PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    sns.set(style="whitegrid")

    # RENOMBRO PARA QUE LOS TÍTULOS EN LAS GRÁFICAS NO SE SUPERPONGAN
    short_names = {
        'Porcentaje de niños de un año que han recibido tres dosis de vacuna contra la Hepatitis B (HEPB3)': 'Hepatitis B (HEPB3)',
        'Porcentaje de niños de un año que han recibido tres dosis de vacuna contra Haemophilus influenzae tipo b (HIB3)': 'Hib (HIB3)',
        'Porcentaje de niños de un año que han recibido su primera dosis de vacuna contra la poliomielitis inactivada (IPV1)': 'Polio 1ª dosis (IPV1)',
        'Porcentaje de niños de un año que han recibido su primera dosis de vacuna contra el sarampión (MCV1)': 'Sarampión (MCV1)',
        'Porcentaje de niños de un año que han recibido la tercera dosis de vacuna conjugada contra el neumococo (PCV3)': 'Neumococo (PCV3)',
        'Porcentaje de niños de un año que han recibido su tercera dosis de vacuna oral o inactivada contra la poliomielitis (POL3)': 'Polio 3ª dosis (POL3)',
        'Porcentaje de niños de un año que han recibido una dosis de vacuna contra la rubéola (RCV1)': 'Rubéola (RCV1)',
        'Porcentaje de niños de un año que han recibido su dosis final recomendada (2ª o 3ª) de vacuna contra el rotavirus (ROTAC)': 'Rotavirus (ROTAC)',
        'Porcentaje de niños de un año que han recibido una dosis de vacuna contra la fiebre amarilla (YFV)': 'Fiebre amarilla (YFV)',
        'Porcentaje de niños de un año que han recibido tres dosis de vacuna combinada contra la difteria, el tétanos y la tosferina (DTP3)': 'DTP (DTP3)',
    }

    for column in vaccines_columns:
        plt.figure(figsize=(24, 6))

        # HISTOGRAMA
        plt.subplot(1, 3, 1)
        sns.histplot(vaccination_coverage[column], kde=False, color="skyblue", bins=30)
        plt.title(f"Histograma de {short_names[column]}")
        plt.xlabel('Porcentaje')
        plt.ylabel('Frecuencia')

        # BOXPLOT
        plt.subplot(1, 3, 2)
        sns.boxplot(x=vaccination_coverage[column], color="lightgreen")
        plt.title(f"Boxplot de {short_names[column]}")
        plt.xlabel('Porcentaje')

        # KDE
        plt.subplot(1, 3, 3)
        sns.kdeplot(vaccination_coverage[column].dropna(), shade=True, color="coral")
        plt.title(f"KDE de {short_names[column]}")
        plt.xlabel('Porcentaje')
        plt.ylabel('Densidad')

        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, f"vacunas_{short_names[column].replace(' ', '_')}.png"))
        plt.close()

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO PARA LA VACUNA IPV1 PARA EL AÑO 2019 EN TODO EL MUNDO
    ipv1 = "Porcentaje de niños de un año que han recibido su primera dosis de vacuna contra la poliomielitis inactivada (IPV1)"
    global_vaccination_2019 = vaccination_coverage[vaccination_coverage['Año'] == 2019]
    values_2019 = global_vaccination_2019[ipv1]

    print(f"Estadísticas descriptivas globales para '{ipv1}' en 2019:")
    print(f"Media: {values_2019.mean():.2f}")
    print(f"Mediana: {values_2019.median():.2f}")
    print(f"Moda: {values_2019.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {values_2019.std():.2f}")
    print(f"Varianza: {values_2019.var():.2f}")
    print(f"Mínimo: {values_2019.min():.2f}")
    print(f"Máximo: {values_2019.max():.2f}")
    print(f"Rango: {values_2019.max() - values_2019.min():.2f}")
    print(f"Percentil 25: {values_2019.quantile(0.25):.2f}")
    print(f"Percentil 50: {values_2019.quantile(0.50):.2f}")
    print(f"Percentil 75: {values_2019.quantile(0.75):.2f}")

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO PARA LA VACUNA IPV1 PARA ESPAÑA A LO LARGO DE LOS AÑOS
    polio_spain = vaccination_coverage[vaccination_coverage['País'] == 'España']
    spain_values = polio_spain[ipv1]

    print(f"\nEstadísticas descriptivas de '{ipv1}' en España a lo largo de los años:")
    print(f"Media: {spain_values.mean():.2f}")
    print(f"Mediana: {spain_values.median():.2f}")
    print(f"Moda: {spain_values.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {spain_values.std():.2f}")
    print(f"Varianza: {spain_values.var():.2f}")
    print(f"Mínimo: {spain_values.min():.2f}")
    print(f"Máximo: {spain_values.max():.2f}")
    print(f"Rango: {spain_values.max() - spain_values.min():.2f}")
    print(f"Percentil 25: {spain_values.quantile(0.25):.2f}")
    print(f"Percentil 50: {spain_values.quantile(0.50):.2f}")
    print(f"Percentil 75: {spain_values.quantile(0.75):.2f}")

    # GRAFICO HISTOGRAMA, BOXPLOT Y KDE DE LA VACUNA IPV1 PARA EL AÑO 2019 A NIVEL GLOBAL Y EN ESPAÑA A LO LARGO DE LOS AÑOS
    sns.set(style="whitegrid")

    # GLOBAL 2019
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA 2019
    plt.subplot(1, 3, 1)
    sns.histplot(values_2019, kde=False, color="skyblue", bins=15)
    plt.title("Histograma IPV1 - Global 2019")
    plt.xlabel("Porcentaje de vacunación")
    plt.ylabel("Frecuencia")

    # BOXPLOT 2019
    plt.subplot(1, 3, 2)
    sns.boxplot(x=values_2019, color="lightgreen")
    plt.title("Boxplot IPV1 - Global 2019")
    plt.xlabel("Porcentaje de vacunación")

    # KDE 2019
    plt.subplot(1, 3, 3)
    sns.kdeplot(values_2019.dropna(), shade=True, color="coral")
    plt.title("KDE IPV1 - Global 2019")
    plt.xlabel("Porcentaje de vacunación")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "IPV1_2019.png"))
    plt.close()

    # ESPAÑA A LO LARGO DE LOS AÑOS
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 1)
    sns.histplot(spain_values, kde=False, color="orange", bins=len(spain_values))
    plt.title("Histograma IPV1 - España (todos los años)")
    plt.xlabel("Porcentaje de vacunación")
    plt.ylabel("Frecuencia")

    # BOXPLOT ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 2)
    sns.boxplot(x=spain_values, color="salmon")
    plt.title("Boxplot IPV1 - España (todos los años)")
    plt.xlabel("Porcentaje de vacunación")

    # KDE ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 3)
    sns.kdeplot(spain_values.dropna(), shade=True, color="sienna")
    plt.title("KDE IPV1 - España (todos los años)")
    plt.xlabel("Porcentaje de vacunación")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "IPV1_espana_historico.png"))
    plt.close()
    
    # IMPUTACIÓN DE LOS VALORES NAN CON LA MEDIANA DE CADA COLUMNA, AGRUPADO POR PAÍS
    '''SE IMPUTA DE ESTA MANERA PORQUE LA DISTRIBUCIÓN DE LOS VALORES FALTANTES ES TOTALMENTE ALEATORIA.
    YA HECHO EL ANÁLISIS ESTADÍSTICO, SE EXPORTA PARA VISUALIZAR EN POWER BI SIN NULOS''' 
    vaccines = [col for col in vaccination_coverage.columns if col not in ['País', 'Año']]
    vaccination_coverage[vaccines] = vaccination_coverage[vaccines].transform(lambda x: x.fillna(x.median()))

    # NUEVA EXPLORACIÓN DEL DATAFRAME VACCINATION_COVERAGE PARA CHEQUEAR QUE LOS VALORES NAN HAYAN SIDO CORRECTAMENTE REEMPLAZADOS
    print(vaccination_coverage.head(10000))
    print(vaccination_coverage.info())

    for column in vaccination_coverage.columns:
        print(f"Columna: {column}")
        print(vaccination_coverage[column].unique())
        print("-" * 40) # Separa entre columna y columna.

    vaccination_coverage.isna().sum()

    vaccination_coverage.to_csv(os.path.join(PROCESSED_PATH, 'vaccination_coverage_processed_sin_nulos.csv'), index=False)

    return vaccination_coverage


# ---------------------- ESTADÍSTICA DE LIFE_EXPECTANCY ----------------------

def stats_life_expectancy(life_expectancy):
    '''
    Realiza un análisis estadístico descriptivo e inferencial, tanto al dataset como tal, así como 
    al dataset agrupado según corresponda. Calcula parámetros de tendencia central (media, mediana, moda) y de dispersión (rango, varianza, desviación estándar, 
    percentiles). Exporta como .png los gráficos a data/figures. 
    '''
    
    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO 
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    life_expectancy_mean = life_expectancy['Esperanza de vida al nacer'].mean() 
    life_expectancy_median = life_expectancy['Esperanza de vida al nacer'].median() 
    life_expectancy_mode = life_expectancy['Esperanza de vida al nacer'].mode().iloc[0] 
    life_expectancy_std = life_expectancy['Esperanza de vida al nacer'].std() 
    life_expectancy_var = life_expectancy['Esperanza de vida al nacer'].var() 
    life_expectancy_percentile_25 = life_expectancy['Esperanza de vida al nacer'].quantile(0.25) 
    life_expectancy_percentile_50 = life_expectancy['Esperanza de vida al nacer'].quantile(0.50) 
    life_expectancy_percentile_75 = life_expectancy['Esperanza de vida al nacer'].quantile(0.75) 
    life_expectancy_min = life_expectancy['Esperanza de vida al nacer'].min() 
    life_expectancy_max = life_expectancy['Esperanza de vida al nacer'].max()
    life_expectancy_range = life_expectancy_max - life_expectancy_min
    print(f"La media de la esperanza de vida es:\n{life_expectancy_mean}\n") 
    print(f"La mediana de la esperanza de vida es:\n{life_expectancy_median}\n") 
    print(f"La moda de la esperanza de vida es:\n{life_expectancy_mode}\n") 
    print(f"La desviación estándar de la esperanza de vida es:\n{life_expectancy_std}\n") 
    print(f"La varianza de la esperanza de vida es:\n{life_expectancy_var}\n")
    print(f"El percentil 25 para la esperanza de vida es:\n{life_expectancy_percentile_25}\n") 
    print(f"El percentil 50 para la esperanza de vida es:\n{life_expectancy_percentile_50}\n") 
    print(f"El percentil 75 para la esperanza de vida es:\n{life_expectancy_percentile_75}\n") 
    print(f"El valor mínimo para la esperanza de vida es:\n{life_expectancy_min}\n") 
    print(f"El valor máximo para la esperanza de vida es:\n{life_expectancy_max}\n") 
    print(f"El rango para la esperanza de vida es:\n{life_expectancy_range}\n") 

    # GRAFICO HISTOGRAMA, BOXPLOT Y KDE DE LA ESPERANZA DE VIDA
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    sns.set(style="whitegrid")
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA
    plt.subplot(1, 3, 1)
    sns.histplot(life_expectancy['Esperanza de vida al nacer'], kde=False, color="skyblue", bins=30)
    plt.title("Histograma de Esperanza de vida al nacer")
    plt.xlabel('Años')
    plt.ylabel('Frecuencia')

    # BOXPLOT
    plt.subplot(1, 3, 2)
    sns.boxplot(x=life_expectancy['Esperanza de vida al nacer'], color="lightgreen")
    plt.title("Boxplot de Esperanza de vida al nacer")
    plt.xlabel('Años')

    # KDE
    plt.subplot(1, 3, 3)
    sns.kdeplot(life_expectancy['Esperanza de vida al nacer'].dropna(), shade=True, color="coral")
    plt.title("KDE de Esperanza de vida al nacer")
    plt.xlabel('Años')
    plt.ylabel('Densidad')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "esperanza_vida_global.png"))
    plt.close()

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO PARA ESPERANZA DE VIDA AL NACER EN 2019 A NIVEL GLOBAL
    vida_col = "Esperanza de vida al nacer"
    global_life_2019 = life_expectancy[life_expectancy['Año'] == 2019]
    values_vida_2019 = global_life_2019[vida_col]

    print(f"Estadísticas descriptivas globales para '{vida_col}' en 2019:")
    print(f"Media: {values_vida_2019.mean():.2f}")
    print(f"Mediana: {values_vida_2019.median():.2f}")
    print(f"Moda: {values_vida_2019.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {values_vida_2019.std():.2f}")
    print(f"Varianza: {values_vida_2019.var():.2f}")
    print(f"Mínimo: {values_vida_2019.min():.2f}")
    print(f"Máximo: {values_vida_2019.max():.2f}")
    print(f"Rango: {values_vida_2019.max() - values_vida_2019.min():.2f}")
    print(f"Percentil 25: {values_vida_2019.quantile(0.25):.2f}")
    print(f"Percentil 50: {values_vida_2019.quantile(0.50):.2f}")
    print(f"Percentil 75: {values_vida_2019.quantile(0.75):.2f}")

    # ANÁLISIS ESTADÍSTICO PARA ESPERANZA DE VIDA AL NACER EN ESPAÑA A LO LARGO DEL TIEMPO
    vida_spain = life_expectancy[life_expectancy['País'] == 'España']
    spain_vida_values = vida_spain[vida_col]

    print(f"\nEstadísticas descriptivas de '{vida_col}' en España a lo largo de los años:")
    print(f"Media: {spain_vida_values.mean():.2f}")
    print(f"Mediana: {spain_vida_values.median():.2f}")
    print(f"Moda: {spain_vida_values.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {spain_vida_values.std():.2f}")
    print(f"Varianza: {spain_vida_values.var():.2f}")
    print(f"Mínimo: {spain_vida_values.min():.2f}")
    print(f"Máximo: {spain_vida_values.max():.2f}")
    print(f"Rango: {spain_vida_values.max() - spain_vida_values.min():.2f}")
    print(f"Percentil 25: {spain_vida_values.quantile(0.25):.2f}")
    print(f"Percentil 50: {spain_vida_values.quantile(0.50):.2f}")
    print(f"Percentil 75: {spain_vida_values.quantile(0.75):.2f}")

    # GRÁFICO DE HISTOGRAMA, BOXPLOT Y KDE DE LA DE ESPERANZA DE VIDA AL NACER PARA EL AÑO 2019 A NIVEL GLOBAL Y EN ESPAÑA A LO LARGO DE LOS AÑOS
    sns.set(style="whitegrid")

    # GLOBAL 2019
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA 2019
    plt.subplot(1, 3, 1)
    sns.histplot(values_vida_2019, kde=False, color="cornflowerblue", bins=15)
    plt.title("Histograma Esperanza de vida - Global 2019")
    plt.xlabel("Años")
    plt.ylabel("Frecuencia")

    # BOXPLOT 2019
    plt.subplot(1, 3, 2)
    sns.boxplot(x=values_vida_2019, color="mediumseagreen")
    plt.title("Boxplot Esperanza de vida - Global 2019")
    plt.xlabel("Años")

    # KDE 2019
    plt.subplot(1, 3, 3)
    sns.kdeplot(values_vida_2019.dropna(), shade=True, color="coral")
    plt.title("KDE Esperanza de vida - Global 2019")
    plt.xlabel("Años")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "esperanza_vida_2019.png"))
    plt.close()

    # ESPAÑA A LO LARGO DE LOS AÑOS 
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA ESPAÑA A LO LARGO DE LOS AÑOS 
    plt.subplot(1, 3, 1)
    sns.histplot(spain_vida_values, kde=False, color="goldenrod", bins=len(spain_vida_values))
    plt.title("Histograma Esperanza de vida - España (todos los años)")
    plt.xlabel("Años")
    plt.ylabel("Frecuencia")

    # BOXPLOT ESPAÑA A LO LARGO DE LOS AÑOS 
    plt.subplot(1, 3, 2)
    sns.boxplot(x=spain_vida_values, color="tomato")
    plt.title("Boxplot Esperanza de vida - España (todos los años)")
    plt.xlabel("Años")

    # KDE ESPAÑA A LO LARGO DE LOS AÑOS 
    plt.subplot(1, 3, 3)
    sns.kdeplot(spain_vida_values.dropna(), shade=True, color="orangered")
    plt.title("KDE Esperanza de vida - España (todos los años)")
    plt.xlabel("Años")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "esperanza_vida_espana_historico.png"))
    plt.close()


# ---------------------- ESTADÍSTICA DE PREVENTABLE_DEATHS ----------------------

def stats_preventable_deaths(preventable_deaths):
    '''
    Realiza un análisis estadístico descriptivo e inferencial, tanto al dataset como tal, así como 
    al dataset agrupado según corresponda. Calcula parámetros de tendencia central (media, mediana, moda) y de dispersión (rango, varianza, desviación estándar, 
    percentiles). Exporta como .png los gráficos a data/figures. 
    '''

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO 
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    preventable_deaths_mean = preventable_deaths['Muertes'].mean() 
    preventable_deaths_median = preventable_deaths['Muertes'].median() 
    preventable_deaths_mode = preventable_deaths['Muertes'].mode()
    preventable_deaths_std = preventable_deaths['Muertes'].std() 
    preventable_deaths_var = preventable_deaths['Muertes'].var() 
    preventable_deaths_percentile_25 = preventable_deaths['Muertes'].quantile(0.25) 
    preventable_deaths_percentile_50 = preventable_deaths['Muertes'].quantile(0.50) 
    preventable_deaths_percentile_75 = preventable_deaths['Muertes'].quantile(0.75) 
    preventable_deaths_min = preventable_deaths['Muertes'].min() 
    preventable_deaths_max = preventable_deaths['Muertes'].max()
    preventable_deaths_range = preventable_deaths_max - preventable_deaths_min
    print(f"La media por año y país es:\n{preventable_deaths_mean}\n") 
    print(f"La mediana por año y país es:\n{preventable_deaths_median}\n") 
    print(f"La moda por año y país es:\n{preventable_deaths_mode}\n") 
    print(f"La desviación estándar por año y país es:\n{preventable_deaths_std}\n") 
    print(f"La varianza por año y país es:\n{preventable_deaths_var}\n")
    print(f"El percentil 25 por año y país es:\n{preventable_deaths_percentile_25}\n") 
    print(f"El percentil 50 por año y país es:\n{preventable_deaths_percentile_50}\n") 
    print(f"El percentil 75 por año y país es:\n{preventable_deaths_percentile_75}\n") 
    print(f"El valor mínimo por año y país es:\n{preventable_deaths_min}\n") 
    print(f"El valor máximo por año y país es:\n{preventable_deaths_max}\n") 
    print(f"El rango por año y país es:\n{preventable_deaths_range}\n") 
    
    # GRAFICO HISTOGRAMA, BOXPLOT y KDE
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    for cause in preventable_deaths['Causa de muerte'].unique():
        plt.figure(figsize=(24, 6))
        filtered_data = preventable_deaths[preventable_deaths['Causa de muerte'] == cause]

        # HISTOGRAMA
        plt.subplot(1, 3, 1)
        sns.histplot(filtered_data['Muertes'], kde=False, color="skyblue", bins=30)
        plt.title(f"Histograma de muertes por {cause}")
        plt.xlabel('Muertes')
        plt.ylabel('Frecuencia')

        # BOXPLOT
        plt.subplot(1, 3, 2)
        sns.boxplot(x=filtered_data['Muertes'], color="lightgreen")
        plt.title(f"Boxplot de muertes por {cause}")
        plt.xlabel('Muertes')

        # KDE
        plt.subplot(1, 3, 3)
        sns.kdeplot(filtered_data['Muertes'], fill=True, color="steelblue")
        plt.title(f"KDE de muertes por {cause}")
        plt.xlabel('Muertes')
        plt.ylabel('Densidad')

        plt.tight_layout()
        filename = f"muertes_prevenibles_{cause.lower().replace(' ', '_').replace('/', '_')}.png"
        plt.savefig(os.path.join(FIGURES_PATH, filename))
        plt.close()
    
    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO PARA MUERTES EN 2019 A NIVEL GLOBAL
    deaths_col = "Muertes"
    global_deaths_2019 = preventable_deaths[preventable_deaths['Año'] == 2019]
    sum_deaths_2019 = global_deaths_2019.groupby("País")[deaths_col].sum()

    print(f"Estadísticas descriptivas globales para '{deaths_col}' en 2019:")
    print(f"Media: {sum_deaths_2019.mean():.2f}")
    print(f"Mediana: {sum_deaths_2019.median():.2f}")
    print(f"Moda: {sum_deaths_2019.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {sum_deaths_2019.std():.2f}")
    print(f"Varianza: {sum_deaths_2019.var():.2f}")
    print(f"Mínimo: {sum_deaths_2019.min():.2f}")
    print(f"Máximo: {sum_deaths_2019.max():.2f}")
    print(f"Rango: {sum_deaths_2019.max() - sum_deaths_2019.min():.2f}")
    print(f"Percentil 25: {sum_deaths_2019.quantile(0.25):.2f}")
    print(f"Percentil 50: {sum_deaths_2019.quantile(0.50):.2f}")
    print(f"Percentil 75: {sum_deaths_2019.quantile(0.75):.2f}")

    # ANÁLISIS ESTADÍSTICO PARA MUERTES EN ESPAÑA A LO LARGO DEL TIEMPO
    spain_deaths = preventable_deaths[preventable_deaths['País'] == 'España']
    spain_deaths_sum = spain_deaths.groupby("Año")[deaths_col].sum()

    print(f"\nEstadísticas descriptivas de '{deaths_col}' en España a lo largo de los años:")
    print(f"Media: {spain_deaths_sum.mean():.2f}")
    print(f"Mediana: {spain_deaths_sum.median():.2f}")
    print(f"Moda: {spain_deaths_sum.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {spain_deaths_sum.std():.2f}")
    print(f"Varianza: {spain_deaths_sum.var():.2f}")
    print(f"Mínimo: {spain_deaths_sum.min():.2f}")
    print(f"Máximo: {spain_deaths_sum.max():.2f}")
    print(f"Rango: {spain_deaths_sum.max() - spain_deaths_sum.min():.2f}")
    print(f"Percentil 25: {spain_deaths_sum.quantile(0.25):.2f}")
    print(f"Percentil 50: {spain_deaths_sum.quantile(0.50):.2f}")
    print(f"Percentil 75: {spain_deaths_sum.quantile(0.75):.2f}")

    # GRAFICO HISTOGRAMA, BOXPLOT Y KDE DE MUERTES QUE SE PODRÍAN HABER PREVENIDO POR VACUNACIÓN PARA EL AÑO 2019 A NIVEL GLOBAL Y EN ESPAÑA A LO LARGO DE LOS AÑOS
    sns.set(style="whitegrid")

    # GLOBAL 2019
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA 2019
    plt.subplot(1, 3, 1)
    sns.histplot(sum_deaths_2019, kde=False, color="slateblue", bins=15)
    plt.title("Histograma de Muertes Prevenibles - Global 2019")
    plt.xlabel("Muertes")
    plt.ylabel("Frecuencia")

    # BOXPLOT 2019
    plt.subplot(1, 3, 2)
    sns.boxplot(x=sum_deaths_2019, color="lightblue")
    plt.title("Boxplot de Muertes Prevenibles - Global 2019")
    plt.xlabel("Muertes")

    # KDE 2019
    plt.subplot(1, 3, 3)
    sns.kdeplot(sum_deaths_2019, fill=True, color="mediumslateblue")
    plt.title("KDE de Muertes Prevenibles - Global 2019")
    plt.xlabel("Muertes")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "muertes_prevenibles_2019.png"))
    plt.close()

    # ESPAÑA A LO LARGO DE LOS AÑOS 
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 1)
    sns.histplot(spain_deaths_sum, kde=False, color="orangered", bins=len(spain_deaths_sum))
    plt.title("Histograma de Muertes Prevenibles - España (todos los años)")
    plt.xlabel("Muertes")
    plt.ylabel("Frecuencia")

    # BOXPLOT ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 2)
    sns.boxplot(x=spain_deaths_sum, color="salmon")
    plt.title("Boxplot de Muertes Prevenibles - España (todos los años)")
    plt.xlabel("Muertes")

    # KDE ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 3)
    sns.kdeplot(spain_deaths_sum, fill=True, color="tomato")
    plt.title("KDE de Muertes Prevenibles - España (todos los años)")
    plt.xlabel("Muertes")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "muertes_prevenibles_espana_historico.png"))
    plt.close()


# ---------------------- ESTADÍSTICA DE GDP ----------------------

def stats_gdp(gdp):
    '''
    Realiza un análisis estadístico descriptivo e inferencial, tanto al dataset como tal, así como 
    al dataset agrupado según corresponda. Calcula parámetros de tendencia central (media, mediana, moda) y de dispersión (rango, varianza, desviación estándar, 
    percentiles). Exporta como .png los gráficos a data/figures. 

    '''

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO 
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    gdp_mean = gdp['PIB per cápita a precios constantes'].mean() 
    gdp_median = gdp['PIB per cápita a precios constantes'].median() 
    gdp_mode = gdp['PIB per cápita a precios constantes'].mode().iloc[0] 
    gdp_std = gdp['PIB per cápita a precios constantes'].std() 
    gdp_var = gdp['PIB per cápita a precios constantes'].var() 
    gdp_percentile_25 = gdp['PIB per cápita a precios constantes'].quantile(0.25) 
    gdp_percentile_50 = gdp['PIB per cápita a precios constantes'].quantile(0.50) 
    gdp_percentile_75 = gdp['PIB per cápita a precios constantes'].quantile(0.75) 
    gdp_min = gdp['PIB per cápita a precios constantes'].min() 
    gdp_max = gdp['PIB per cápita a precios constantes'].max()
    gdp_range = gdp_max - gdp_min
    print(f"La media por año y país es:\n{gdp_mean}\n") 
    print(f"La mediana por año y país es:\n{gdp_median}\n") 
    print(f"La moda por año y país es:\n{gdp_mode}\n") 
    print(f"La desviación estándar por año y país es:\n{gdp_std}\n") 
    print(f"La varianza por año y país es:\n{gdp_var}\n")
    print(f"El percentil 25 por año y país es:\n{gdp_percentile_25}\n") 
    print(f"El percentil 50 por año y país es:\n{gdp_percentile_50}\n") 
    print(f"El percentil 75 por año y país es:\n{gdp_percentile_75}\n") 
    print(f"El valor mínimo por año y país es:\n{gdp_min}\n") 
    print(f"El valor máximo por año y país es:\n{gdp_max}\n") 
    print(f"El rango por año y país es:\n{gdp_range}\n") 

    # GRÁFICO DE HISTOGRAMA, BOXPLOT Y KDE DEL PIB
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    sns.set(style="whitegrid")
    column = 'PIB per cápita a precios constantes'
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA
    plt.subplot(1, 3, 1)
    sns.histplot(gdp[column], kde=False, color="skyblue", bins=30)
    plt.title(f"Histograma de {column}")
    plt.xlabel('PIB per cápita')
    plt.ylabel('Frecuencia')

    # BOXPLOT
    plt.subplot(1, 3, 2)
    sns.boxplot(x=gdp[column], color="lightgreen")
    plt.title(f"Boxplot de {column}")
    plt.xlabel('PIB per cápita')

    # KDE
    plt.subplot(1, 3, 3)
    sns.kdeplot(gdp[column], fill=True, color="steelblue")
    plt.title(f"KDE de {column}")
    plt.xlabel('PIB per cápita')
    plt.ylabel('Densidad')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "PIB_global.png"))
    plt.close()

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO PARA 2019 A NIVEL GLOBAL
    gdp_col = "PIB per cápita a precios constantes"
    global_gdp_2019 = gdp[gdp['Año'] == 2019]
    values_gdp_2019 = global_gdp_2019[gdp_col]

    print(f"Estadísticas descriptivas globales para '{gdp_col}' en 2019:")
    print(f"Media: {values_gdp_2019.mean():.2f}")
    print(f"Mediana: {values_gdp_2019.median():.2f}")
    print(f"Moda: {values_gdp_2019.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {values_gdp_2019.std():.2f}")
    print(f"Varianza: {values_gdp_2019.var():.2f}")
    print(f"Mínimo: {values_gdp_2019.min():.2f}")
    print(f"Máximo: {values_gdp_2019.max():.2f}")
    print(f"Rango: {values_gdp_2019.max() - values_gdp_2019.min():.2f}")
    print(f"Percentil 25: {values_gdp_2019.quantile(0.25):.2f}")
    print(f"Percentil 50: {values_gdp_2019.quantile(0.50):.2f}")
    print(f"Percentil 75: {values_gdp_2019.quantile(0.75):.2f}")

    # ANÁLISIS ESTADÍSTICO PARA ESPAÑA A LO LARGO DEL TIEMPO
    spain_gdp = gdp[gdp['País'] == 'España']
    spain_gdp_values = spain_gdp[gdp_col]

    print(f"\nEstadísticas descriptivas de '{gdp_col}' en España a lo largo de los años:")
    print(f"Media: {spain_gdp_values.mean():.2f}")
    print(f"Mediana: {spain_gdp_values.median():.2f}")
    print(f"Moda: {spain_gdp_values.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {spain_gdp_values.std():.2f}")
    print(f"Varianza: {spain_gdp_values.var():.2f}")
    print(f"Mínimo: {spain_gdp_values.min():.2f}")
    print(f"Máximo: {spain_gdp_values.max():.2f}")
    print(f"Rango: {spain_gdp_values.max() - spain_gdp_values.min():.2f}")
    print(f"Percentil 25: {spain_gdp_values.quantile(0.25):.2f}")
    print(f"Percentil 50: {spain_gdp_values.quantile(0.50):.2f}")
    print(f"Percentil 75: {spain_gdp_values.quantile(0.75):.2f}")

    # GRÁFICO DE HISTOGRAMA Y BOXPLOT DEL PIB EN 2019 A NIVEL GLOBAL Y EN ESPAÑA A LO LARGO DE LOS AÑOS
    sns.set(style="whitegrid")

    # GLOBAL 2019
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA 2019
    plt.subplot(1, 3, 1)
    sns.histplot(values_gdp_2019, kde=False, color="darkcyan", bins=15)
    plt.title("Histograma del PIB per cápita - Global 2019")
    plt.xlabel("PIB per cápita (precios constantes)")
    plt.ylabel("Frecuencia")

    # BOXPLOT 2019
    plt.subplot(1, 3, 2)
    sns.boxplot(x=values_gdp_2019, color="aquamarine")
    plt.title("Boxplot del PIB per cápita - Global 2019")
    plt.xlabel("PIB per cápita (precios constantes)")

    # KDE 2019
    plt.subplot(1, 3, 3)
    sns.kdeplot(values_gdp_2019, fill=True, color="teal")
    plt.title("KDE del PIB per cápita - Global 2019")
    plt.xlabel("PIB per cápita (precios constantes)")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "PIB_2019.png"))
    plt.close()

    # ESPAÑA A LO LARGO DE LOS AÑOS
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 1)
    sns.histplot(spain_gdp_values, kde=False, color="darkorange", bins=len(spain_gdp_values))
    plt.title("Histograma del PIB per cápita - España (todos los años)")
    plt.xlabel("PIB per cápita (precios constantes)")
    plt.ylabel("Frecuencia")

    # BOXPLOT ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 2)
    sns.boxplot(x=spain_gdp_values, color="sandybrown")
    plt.title("Boxplot del PIB per cápita - España (todos los años)")
    plt.xlabel("PIB per cápita (precios constantes)")

    # KDE ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 3)
    sns.kdeplot(spain_gdp_values, fill=True, color="chocolate")
    plt.title("KDE del PIB per cápita - España (todos los años)")
    plt.xlabel("PIB per cápita (precios constantes)")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "PIB_espana_historico.png"))
    plt.close()


# ---------------------- ESTADÍSTICA DE LITERACY ----------------------

def stats_literacy(literacy):
    '''
    Realiza un análisis estadístico descriptivo e inferencial, tanto al dataset como tal, así como 
    al dataset agrupado según corresponda. Calcula parámetros de tendencia central (media, mediana, moda) y de dispersión (rango, varianza, desviación estándar, 
    percentiles). Exporta como .png los gráficos a data/figures. 
    '''

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    tasa_alfabetizacion = literacy.columns.difference(['País', 'Año']) 
    literacy_mean = literacy['Tasa de alfabetización'].mean() 
    literacy_median = literacy['Tasa de alfabetización'].median() 
    literacy_mode = literacy['Tasa de alfabetización'].mode().iloc[0] 
    literacy_std = literacy['Tasa de alfabetización'].std() 
    literacy_var = literacy['Tasa de alfabetización'].var() 
    literacy_percentile_25 = literacy['Tasa de alfabetización'].quantile(0.25) 
    literacy_percentile_50 = literacy['Tasa de alfabetización'].quantile(0.50) 
    literacy_percentile_75 = literacy['Tasa de alfabetización'].quantile(0.75) 
    literacy_min = literacy['Tasa de alfabetización'].min() 
    literacy_max = literacy['Tasa de alfabetización'].max()
    literacy_range = literacy_max - literacy_min

    print(f"La media por año y país es:\n{literacy_mean}\n") 
    print(f"La mediana por año y país es:\n{literacy_median}\n") 
    print(f"La moda por año y país es:\n{literacy_mode}\n") 
    print(f"La desviación estándar por año y país es:\n{literacy_std}\n") 
    print(f"La varianza por año y país es:\n{literacy_var}\n")
    print(f"El percentil 25 por año y país es:\n{literacy_percentile_25}\n") 
    print(f"El percentil 50 por año y país es:\n{literacy_percentile_50}\n") 
    print(f"El percentil 75 por año y país es:\n{literacy_percentile_75}\n") 
    print(f"El valor mínimo por año y país es:\n{literacy_min}\n") 
    print(f"El valor máximo por año y país es:\n{literacy_max}\n") 
    print(f"El rango por año y país es:\n{literacy_range}\n")

    # GRÁFICO DE HISTOGRAMA, BOXPLOT Y KDE 
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    sns.set(style="whitegrid")
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA
    plt.subplot(1, 3, 1)
    sns.histplot(literacy['Tasa de alfabetización'], kde=False, color="skyblue", bins=30)
    plt.title("Histograma de Tasa de alfabetización")
    plt.xlabel('Porcentaje')
    plt.ylabel('Frecuencia')

    # BOXPLOT
    plt.subplot(1, 3, 2)
    sns.boxplot(x=literacy['Tasa de alfabetización'], color="lightgreen")
    plt.title("Boxplot de Tasa de alfabetización")
    plt.xlabel('Porcentaje')

    # KDE
    plt.subplot(1, 3, 3)
    sns.kdeplot(literacy['Tasa de alfabetización'], fill=True, color="steelblue")
    plt.title("KDE de Tasa de alfabetización")
    plt.xlabel("Porcentaje")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "literacy_global.png"))
    plt.close()

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO PARA TASA DE ALFABETIZACIÓN EN 2019 A NIVEL GLOBAL
    literacy_col = "Tasa de alfabetización"
    global_literacy_2019 = literacy[literacy['Año'] == 2019]
    values_literacy_2019 = global_literacy_2019[literacy_col]

    print(f"Estadísticas descriptivas globales para '{literacy_col}' en 2019:")
    print(f"Media: {values_literacy_2019.mean():.2f}")
    print(f"Mediana: {values_literacy_2019.median():.2f}")
    print(f"Moda: {values_literacy_2019.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {values_literacy_2019.std():.2f}")
    print(f"Varianza: {values_literacy_2019.var():.2f}")
    print(f"Mínimo: {values_literacy_2019.min():.2f}")
    print(f"Máximo: {values_literacy_2019.max():.2f}")
    print(f"Rango: {values_literacy_2019.max() - values_literacy_2019.min():.2f}")
    print(f"Percentil 25: {values_literacy_2019.quantile(0.25):.2f}")
    print(f"Percentil 50: {values_literacy_2019.quantile(0.50):.2f}")
    print(f"Percentil 75: {values_literacy_2019.quantile(0.75):.2f}")

    # ANÁLISIS ESTADÍSTICO PARA ESPAÑA A LO LARGO DEL TIEMPO
    literacy_spain = literacy[literacy['País'] == 'España']
    spain_literacy_values = literacy_spain[literacy_col]

    print(f"\nEstadísticas descriptivas de '{literacy_col}' en España a lo largo de los años:")
    print(f"Media: {spain_literacy_values.mean():.2f}")
    print(f"Mediana: {spain_literacy_values.median():.2f}")
    print(f"Moda: {spain_literacy_values.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {spain_literacy_values.std():.2f}")
    print(f"Varianza: {spain_literacy_values.var():.2f}")
    print(f"Mínimo: {spain_literacy_values.min():.2f}")
    print(f"Máximo: {spain_literacy_values.max():.2f}")
    print(f"Rango: {spain_literacy_values.max() - spain_literacy_values.min():.2f}")
    print(f"Percentil 25: {spain_literacy_values.quantile(0.25):.2f}")
    print(f"Percentil 50: {spain_literacy_values.quantile(0.50):.2f}")
    print(f"Percentil 75: {spain_literacy_values.quantile(0.75):.2f}")

    # GRÁFICO DE HISTOGRAMA, BOXPLOT Y KDE DE TASA DE ALFABETIZACIÓN PARA EL AÑO 2019 A NIVEL GLOBAL Y PARA ESPAÑA A LO LARGO DEL TIEMPO
    sns.set(style="whitegrid")

    # GLOBAL 2019
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA 2019
    plt.subplot(1, 3, 1)
    sns.histplot(values_literacy_2019, kde=False, color="teal", bins=15)
    plt.title("Histograma Tasa de alfabetización - Global 2019")
    plt.xlabel("Porcentaje")
    plt.ylabel("Frecuencia")

    # BOXPLOT 2019
    plt.subplot(1, 3, 2)
    sns.boxplot(x=values_literacy_2019, color="lightgreen")
    plt.title("Boxplot Tasa de alfabetización - Global 2019")
    plt.xlabel("Porcentaje")

    # KDE 2019
    plt.subplot(1, 3, 3)
    sns.kdeplot(values_literacy_2019, fill=True, color="mediumseagreen")
    plt.title("KDE Tasa de alfabetización - Global 2019")
    plt.xlabel("Porcentaje")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "literacy_2019.png"))
    plt.close()

    # ESPAÑA A LO LARGO DE LOS AÑOS
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 1)
    sns.histplot(spain_literacy_values, kde=False, color="darkorange", bins=len(spain_literacy_values))
    plt.title("Histograma Tasa de alfabetización - España (todos los años)")
    plt.xlabel("Porcentaje")
    plt.ylabel("Frecuencia")

    # BOXPLOT ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 2)
    sns.boxplot(x=spain_literacy_values, color="tomato")
    plt.title("Boxplot Tasa de alfabetización - España (todos los años)")
    plt.xlabel("Porcentaje")

    # KDE ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 3)
    sns.kdeplot(spain_literacy_values, fill=True, color="orangered")
    plt.title("KDE Tasa de alfabetización - España (todos los años)")
    plt.xlabel("Porcentaje")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "literacy_espana_historico.png"))
    plt.close()


# ---------------------- ESTADÍSTICA DE CHILD_MORTALITY ----------------------

def stats_child_mortality(child_mortality):
    '''
    Realiza un análisis estadístico descriptivo e inferencial, tanto al dataset como tal, así como 
    al dataset agrupado según corresponda. Calcula parámetros de tendencia central (media, mediana, moda) y de dispersión (rango, varianza, desviación estándar, 
    percentiles). Exporta como .png los gráficos a data/figures. 
    '''

    # HAGO ANÁLISIS ESTADÍSTICO DESCRIPTIVO 
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    child_mortality_mean = child_mortality['Mortalidad infantil'].mean() 
    child_mortality_median = child_mortality['Mortalidad infantil'].median() 
    child_mortality_mode = child_mortality['Mortalidad infantil'].mode().iloc[0] 
    child_mortality_std = child_mortality['Mortalidad infantil'].std() 
    child_mortality_var = child_mortality['Mortalidad infantil'].var() 
    child_mortality_percentile_25 = child_mortality['Mortalidad infantil'].quantile(0.25) 
    child_mortality_percentile_50 = child_mortality['Mortalidad infantil'].quantile(0.50) 
    child_mortality_percentile_75 = child_mortality['Mortalidad infantil'].quantile(0.75) 
    child_mortality_min = child_mortality['Mortalidad infantil'].min() 
    child_mortality_max = child_mortality['Mortalidad infantil'].max()
    child_mortality_range = child_mortality_max - child_mortality_min

    print(f"La media por año y país es:\n{child_mortality_mean}\n") 
    print(f"La mediana por año y país es:\n{child_mortality_median}\n") 
    print(f"La moda por año y país es:\n{child_mortality_mode}\n") 
    print(f"La desviación estándar por año y país es:\n{child_mortality_std}\n") 
    print(f"La varianza por año y país es:\n{child_mortality_var}\n")
    print(f"El percentil 25 por año y país es:\n{child_mortality_percentile_25}\n") 
    print(f"El percentil 50 por año y país es:\n{child_mortality_percentile_50}\n") 
    print(f"El percentil 75 por año y país es:\n{child_mortality_percentile_75}\n") 
    print(f"El valor mínimo por año y país es:\n{child_mortality_min}\n") 
    print(f"El valor máximo por año y país es:\n{child_mortality_max}\n") 
    print(f"El rango por año y país es:\n{child_mortality_range}\n")

    # GRÁFICO DE HISTOGRAMA, BOXPLOT Y KDE 
    ''' 
    NO TIENE MUCHO SENTIDO HACERLO SIN AGRUPAR, COMO SE EXPLICA ARRIBA. SÓLO SE HACE PARA
    CUMPLIR CON EL ENUNCIADO. LO QUE SÍ TIENE SENTIDO ES UN ANÁLISIS SIMILAR AGRUPANDO, QUE SE HACE LUEGO 
    DEL ANÁLISIS SIN AGRUPAR.
    '''

    sns.set(style="whitegrid")
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA
    plt.subplot(1, 3, 1)
    sns.histplot(child_mortality['Mortalidad infantil'], kde=False, color="skyblue", bins=30)
    plt.title("Histograma de Mortalidad infantil")
    plt.xlabel('Porcentaje')
    plt.ylabel('Frecuencia')

    # BOXPLOT
    plt.subplot(1, 3, 2)
    sns.boxplot(x=child_mortality['Mortalidad infantil'], color="lightgreen")
    plt.title("Boxplot de Mortalidad infantil")
    plt.xlabel('Porcentaje')

    # KDE
    plt.subplot(1, 3, 3)
    sns.kdeplot(child_mortality['Mortalidad infantil'], fill=True, color="steelblue")
    plt.title("KDE de Mortalidad infantil")
    plt.xlabel("Porcentaje")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "child_mortality_global.png"))
    plt.close()

    # ANÁLISIS ESTADÍSTICO DESCRIPTIVO PARA MORTALIDAD INFANTIL EN 2019 A NIVEL GLOBAL
    mortality_col = "Mortalidad infantil"
    global_mortality_2019 = child_mortality[child_mortality['Año'] == 2019]
    values_mortality_2019 = global_mortality_2019[mortality_col]

    print(f"Estadísticas descriptivas globales para '{mortality_col}' en 2019:")
    print(f"Media: {values_mortality_2019.mean():.2f}")
    print(f"Mediana: {values_mortality_2019.median():.2f}")
    print(f"Moda: {values_mortality_2019.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {values_mortality_2019.std():.2f}")
    print(f"Varianza: {values_mortality_2019.var():.2f}")
    print(f"Mínimo: {values_mortality_2019.min():.2f}")
    print(f"Máximo: {values_mortality_2019.max():.2f}")
    print(f"Rango: {values_mortality_2019.max() - values_mortality_2019.min():.2f}")
    print(f"Percentil 25: {values_mortality_2019.quantile(0.25):.2f}")
    print(f"Percentil 50: {values_mortality_2019.quantile(0.50):.2f}")
    print(f"Percentil 75: {values_mortality_2019.quantile(0.75):.2f}")

    # ANÁLISIS ESTADÍSTICO PARA MORTALIDAD INFANTIL EN ESPAÑA A LO LARGO DEL TIEMPO
    mortality_spain = child_mortality[child_mortality['País'] == 'España']
    spain_mortality_values = mortality_spain[mortality_col]

    print(f"\nEstadísticas descriptivas de '{mortality_col}' en España a lo largo de los años:")
    print(f"Media: {spain_mortality_values.mean():.2f}")
    print(f"Mediana: {spain_mortality_values.median():.2f}")
    print(f"Moda: {spain_mortality_values.mode().iloc[0]:.2f}")
    print(f"Desviación estándar: {spain_mortality_values.std():.2f}")
    print(f"Varianza: {spain_mortality_values.var():.2f}")
    print(f"Mínimo: {spain_mortality_values.min():.2f}")
    print(f"Máximo: {spain_mortality_values.max():.2f}")
    print(f"Rango: {spain_mortality_values.max() - spain_mortality_values.min():.2f}")
    print(f"Percentil 25: {spain_mortality_values.quantile(0.25):.2f}")
    print(f"Percentil 50: {spain_mortality_values.quantile(0.50):.2f}")
    print(f"Percentil 75: {spain_mortality_values.quantile(0.75):.2f}")

    # GRÁFICO DE HISTOGRAMA, BOXPLOT Y KDE PARA MORTALIDAD INFANTIL A NIVEL GLOBAL EN 2019 Y PARA ESPAÑA A LO LARGO DEL TIEMPO
    sns.set(style="whitegrid")

    # GLOBAL 2019
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA 2019
    plt.subplot(1, 3, 1)
    sns.histplot(values_mortality_2019, kde=False, color="mediumpurple", bins=15)
    plt.title("Histograma Mortalidad Infantil - Global 2019")
    plt.xlabel("Mortalidad por cada 1.000 nacidos vivos")
    plt.ylabel("Frecuencia")

    # BOXPLOT 2019
    plt.subplot(1, 3, 2)
    sns.boxplot(x=values_mortality_2019, color="plum")
    plt.title("Boxplot Mortalidad Infantil - Global 2019")
    plt.xlabel("Mortalidad por cada 1.000 nacidos vivos")

    # KDE 2019
    plt.subplot(1, 3, 3)
    sns.kdeplot(values_mortality_2019, fill=True, color="purple")
    plt.title("KDE Mortalidad Infantil - Global 2019")
    plt.xlabel("Mortalidad por cada 1.000 nacidos vivos")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "child_mortality_2019.png"))
    plt.close()

    # ESPAÑA A LO LARGO DE LOS AÑOS
    plt.figure(figsize=(24, 6))

    # HISTOGRAMA ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 1)
    sns.histplot(spain_mortality_values, kde=False, color="firebrick", bins=len(spain_mortality_values))
    plt.title("Histograma Mortalidad Infantil - España (todos los años)")
    plt.xlabel("Mortalidad por cada 1.000 nacidos vivos")
    plt.ylabel("Frecuencia")

    # BOXPLOT ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 2)
    sns.boxplot(x=spain_mortality_values, color="lightcoral")
    plt.title("Boxplot Mortalidad Infantil - España (todos los años)")
    plt.xlabel("Mortalidad por cada 1.000 nacidos vivos")

    # KDE ESPAÑA A LO LARGO DE LOS AÑOS
    plt.subplot(1, 3, 3)
    sns.kdeplot(spain_mortality_values, fill=True, color="indianred")
    plt.title("KDE Mortalidad Infantil - España (todos los años)")
    plt.xlabel("Mortalidad por cada 1.000 nacidos vivos")
    plt.ylabel("Densidad")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "child_mortality_espana_historico.png"))
    plt.close()


# ---------------------- ANÁLISIS ESTADÍSTICO INFERENCIAL ----------------------

def stats_inferential(vaccination_coverage, life_expectancy, preventable_deaths, literacy, child_mortality, gdp) :
    '''
    Grafica la matriz de correlación entre las variables más representativas de los datasets. Realiza 
    un análisis de regresión lineal entre distintas variables representativas de los datasets. 
    Estudia los residuos. Exporta todas las gráficas como .png a data/figures.
    '''
    # MATRIZ DE CORRELACIÓN ENTRE INDICADORES GLOBALES CON HEATMAP (PERÍODO 1980-2019)
    years = list(range(1980, 2020))

    vacunas_cols = [
        "Porcentaje de niños de un año que han recibido tres dosis de vacuna contra la Hepatitis B (HEPB3)",
        "Porcentaje de niños de un año que han recibido tres dosis de vacuna contra Haemophilus influenzae tipo b (HIB3)",
        "Porcentaje de niños de un año que han recibido su primera dosis de vacuna contra la poliomielitis inactivada (IPV1)",
        "Porcentaje de niños de un año que han recibido su primera dosis de vacuna contra el sarampión (MCV1)",
        "Porcentaje de niños de un año que han recibido la tercera dosis de vacuna conjugada contra el neumococo (PCV3)",
        "Porcentaje de niños de un año que han recibido su tercera dosis de vacuna oral o inactivada contra la poliomielitis (POL3)",
        "Porcentaje de niños de un año que han recibido una dosis de vacuna contra la rubéola (RCV1)",
        "Porcentaje de niños de un año que han recibido su dosis final recomendada (2ª o 3ª) de vacuna contra el rotavirus (ROTAC)",
        "Porcentaje de niños de un año que han recibido una dosis de vacuna contra la fiebre amarilla (YFV)",
        "Porcentaje de niños de un año que han recibido tres dosis de vacuna combinada contra la difteria, el tétanos y la tosferina (DTP3)"
    ]

    vacunas_avg = vaccination_coverage[vaccination_coverage['Año'].isin(years)].groupby("Año")[vacunas_cols].mean().mean(axis=1)
    vida_avg = life_expectancy[life_expectancy["Año"].isin(years)].groupby("Año")["Esperanza de vida al nacer"].mean()
    muertes_avg = preventable_deaths[preventable_deaths["Año"].isin(years)].groupby("Año")["Muertes"].mean()
    alfabet_avg = literacy[literacy["Año"].isin(years)].groupby("Año")["Tasa de alfabetización"].mean()
    mortalidad_avg = child_mortality[child_mortality["Año"].isin(years)].groupby("Año")["Mortalidad infantil"].mean()
    gdp_avg = gdp[gdp["Año"].isin(years)].groupby("Año")["PIB per cápita a precios constantes"].mean()

    df_corr = pd.DataFrame({
        "Vacunación promedio (%)": vacunas_avg,
        "Esperanza de vida": vida_avg,
        "Muertes prevenibles": muertes_avg,
        "Alfabetización (%)": alfabet_avg,
        "Mortalidad infantil": mortalidad_avg,
        "PIB per cápita": gdp_avg
    }).dropna()

    correlation_matrix = df_corr.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de correlación entre indicadores globales (1980-2019)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "correlation_matrix.png"))

    # REGRESIÓN LINEAL
    def plot_regression(df, x_col, y_col, title, filename):
        '''
        Realiza un análisis de regresión lineal entre dos variables y exporta el gráfico como .png a
        data/figures.
        '''

        # REMOVER OUTLIERS USANDO Z-SCORE
        df_clean = df[[x_col, y_col]].copy()
        z_scores = np.abs(zscore(df_clean))
        df_no_outliers = df_clean[(z_scores < 2.5).all(axis=1)]
        print(f"[INFO] '{title}': Se eliminaron {len(df_clean) - len(df_no_outliers)} outliers")

        X = df_no_outliers[[x_col]]
        y = df_no_outliers[y_col]
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = model.score(X, y)

        plt.figure(figsize=(8, 5))
        plt.scatter(X, y, label="Datos sin outliers", alpha=0.7)
        plt.plot(X, y_pred, color="red", label=f"Regresión (R² = {r2:.2f})")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, filename))
        plt.close()


    # ANÁLISIS DE REGRESIÓN LINEAL ENTRE VARIABLES
    plot_regression(df_corr, "Vacunación promedio (%)", "Esperanza de vida", "Esperanza de vida vs Tasa de vacunación", "regresion_vida_vacunacion.png")
    plot_regression(df_corr, "Vacunación promedio (%)", "Mortalidad infantil", "Mortalidad infantil vs Tasa de vacunación", "regresion_mortalidad_vacunacion.png")
    plot_regression(df_corr, "Vacunación promedio (%)", "Muertes prevenibles", "Muertes prevenibles vs Tasa de vacunación", "regresion_muertes_vacunacion.png")
    plot_regression(df_corr, "Vacunación promedio (%)", "Alfabetización (%)", "Tasa de alfabetización vs Tasa de vacunación", "regresion_alfabetizacion_vacunacion.png")
    plot_regression(df_corr, "Vacunación promedio (%)", "PIB per cápita", "PIB per cápita vs Tasa de vacunación", "regresion_pib_vacunacion.png")

    # ESTUDIO DE RESIDUOS
    def plot_residue(df, x_col, y_col, title, filename_base):
        '''
        Estudia los resiudos de un modelo de regresión lineal entre dos variables y exporta los gráficos
        como .png a data/figures.
        '''

        # CREACIÓN DEL MODELO
        X = df[[x_col]]
        y = df[y_col]

        modelo = LinearRegression()
        modelo.fit(X, y)
        y_pred = modelo.predict(X)
        r2 = modelo.score(X, y)

        plt.figure(figsize=(8, 5))
        plt.scatter(X, y, label='Datos reales', alpha=0.7)
        plt.plot(X, y_pred, color='red', label=f'Regresión (R² = {r2:.2f})')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, f"{filename_base}.png"))
        plt.close()

        residuos = y - y_pred

        plt.figure(figsize=(10, 5))
        plt.scatter(y_pred, residuos, color="darkorange")
        plt.axhline(0, color='gray', linestyle='--')
        plt.xlabel("Valores Predichos")
        plt.ylabel("Residuos")
        plt.title("Gráfico de Residuos")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, f"residuos_{filename_base}.png"))
        plt.close()

        plt.figure(figsize=(8, 5))
        sns.histplot(residuos, kde=True, color="mediumpurple")
        plt.title("Distribución de los Residuos")
        plt.xlabel("Residuos")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, f"hist_residuos_{filename_base}.png"))
        plt.close()

        plt.figure(figsize=(6, 6))
        stats.probplot(residuos, dist="norm", plot=plt)
        plt.title("Q-Q Plot de los Residuos")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, f"qqplot_{filename_base}.png"))
        plt.close()


    # ESTUDIO DE RESIDUOS PARA DISTINTAS VARIABLES
    plot_residue(df_corr, "Vacunación promedio (%)", "Esperanza de vida", "Esperanza de vida vs Tasa de vacunación", "vida_vacunacion")
    plot_residue(df_corr, "Vacunación promedio (%)", "Mortalidad infantil", "Mortalidad infantil vs Tasa de vacunación", "mortalidad_vacunacion")
    plot_residue(df_corr, "Vacunación promedio (%)", "Muertes prevenibles", "Muertes prevenibles vs Tasa de vacunación", "muertes_vacunacion")
    plot_residue(df_corr, "Vacunación promedio (%)", "Alfabetización (%)", "Tasa de alfabetización vs Tasa de vacunación", "alfabetizacion_vacunacion")
    plot_residue(df_corr, "Vacunación promedio (%)", "PIB per cápita", "PIB per cápita vs Tasa de vacunación", "pib_vacunacion")

  
    # TEST DE HIPÓTESIS
    '''
    Se estudia la relación entre la tasa de vacunación y la esperanza de vida, así como entre la tasa
    de vacunación y la mortalidad infantil. Por lo tanto, las hipótesis nula (H0) y alternativa (H1)
    son: 

    - Vacunación promedio y esperanza de vida
    H0: La vacunación promedio no tiene efecto sobre la esperanza de vida, ergo el coeficiente de la
    regresión es igual a cero. 
    H1: La vacunación promedio tiene un efecto sobre la esperanza de vida, ergo el coeficiente es 
    distinto de cero.

    - Vacunación promedio y mortalidad infantil
    H0: La vacunación promedio no tiene efecto sobre la mortalidad infantil, ergo el coeficiente de la
    regresión es igual a cero.
    H1: La vacunación promedio tiene un efecto sobre la mortalidad infantil, ergo el coeficiente es
    distinto de cero.
    '''

    def test_hipotesis(df, x_col, y_col, descripcion):
        '''
        Realiza un test de hipótesis para evaluar la relación entre dos variables.
        '''

        print(f"\nTEST DE HIPÓTESIS: {descripcion}")

        X = df[[x_col]]
        y = df[y_col]
        
        X = sm.add_constant(X)
        
        modelo = sm.OLS(y, X).fit()

        print(modelo.summary())

        coef = modelo.params[x_col]
        p_valor = modelo.pvalues[x_col]
        ic_95 = modelo.conf_int().loc[x_col]

        print(f"\nResultados del análisis:")
        print(f"  Coeficiente: {coef:.4f}")
        print(f"  p-valor: {p_valor:.4f}")
        print(f"  Intervalo de confianza al 95%: [{ic_95[0]:.4f}, {ic_95[1]:.4f}]")

        if p_valor < 0.05:
            print("  Conclusión: El efecto es estadísticamente significativo (se rechaza H0).")
        else:
            print("  Conclusión: El efecto no es estadísticamente significativo (no se rechaza H0).")

    # SE TESTEAN POR SEPARADO LAS DOS HIPÓTESIS NULAS
    test_hipotesis(df_corr, "Vacunación promedio (%)", "Esperanza de vida", "Vacunación sobre Esperanza de vida")
    test_hipotesis(df_corr, "Vacunación promedio (%)", "Mortalidad infantil", "Vacunación sobre Mortalidad infantil")