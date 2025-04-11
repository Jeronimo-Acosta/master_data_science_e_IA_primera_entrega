def run_eda() :
    """
    Limpia y transforma los datasets. Consiste en seis funciones, una función para cada dataset, pues 
    la morfología de cada dataset no es exactamente igual. Sin embargo, las seis funciones son muy 
    similares entre sí. Se eliminan filas y columnas innecesarias y se traducen los nombres de los 
    países al español. Se exportan los datasets procesados como CSV a data/processed y devuelve los 
    datasets ya limpios. 
    """
    
    import pandas as pd
    import os
    from src.etl import load_data

    # CARGA DE DATOS
    datasets = load_data()

    # ASIGNACIÓN DE LOS DATASETS A VARIABLES INDIVIDUALES
    vaccination_coverage = datasets["vaccination_coverage"]
    life_expectancy = datasets["life_expectancy"]
    child_mortality = datasets["child_mortality"]
    preventable_deaths = datasets["preventable_deaths"]
    literacy = datasets["literacy"]
    gdp = datasets["gdp"]

    # RUTA BASE RELATIVA DESDE EL ARCHIVO ACTUAL (SRC/EDA.PY) HACIA DATA/PROCESSED
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

    # LLAMADA A LAS FUNCIONES DE LIMPIEZA, SOBREESCRIBIENDO LOS DATASETS ORIGINALES
    vaccination_coverage = eda_vaccination_coverage(vaccination_coverage)
    life_expectancy = eda_life_expectancy(life_expectancy)
    child_mortality = eda_child_mortality(child_mortality)
    preventable_deaths = eda_preventable_deaths(preventable_deaths)
    literacy = eda_literacy(literacy)
    gdp = eda_gdp(gdp)

    # EXPORTACIÓN DE LOS DATASETS PROCESADOS COMO CSV A DATA/PROCESSED
    vaccination_coverage.to_csv(os.path.join(PROCESSED_PATH, 'vaccination_coverage_processed.csv'), index=False)
    life_expectancy.to_csv(os.path.join(PROCESSED_PATH, 'life_expectancy_processed.csv'), index=False)
    preventable_deaths.to_csv(os.path.join(PROCESSED_PATH, 'preventable_deaths_processed.csv'), index=False)
    gdp.to_csv(os.path.join(PROCESSED_PATH, 'gdp_processed.csv'), index=False)
    literacy.to_csv(os.path.join(PROCESSED_PATH, 'literacy_processed.csv'), index=False)
    child_mortality.to_csv(os.path.join(PROCESSED_PATH, 'child_mortality_processed.csv'), index=False)

    return {
    "vaccination_coverage": vaccination_coverage,
    "life_expectancy": life_expectancy,
    "child_mortality": child_mortality,
    "preventable_deaths": preventable_deaths,
    "literacy": literacy,
    "gdp": gdp
    }


 # ---------------------- EXPLORACIÓN DE VACCINES_COVERAGE ----------------------

def eda_vaccination_coverage(vaccination_coverage):
    '''
    Realiza el EDA ya explicado para vaccination_coverage.
    '''    

    print(vaccination_coverage.head(10000))
    print(vaccination_coverage.info())

    for column in vaccination_coverage.columns:
        print(f"Columna: {column}")
        print(vaccination_coverage[column].unique())
        print("-" * 40) # Separa entre columna y columna.

    vaccination_coverage.isna().sum()

    # ELIMINACIÓN DE LAS FILAS DE GEOGRAFÍAS REPETIDAS
    repeated_geographies = ['African Region (WHO)', 'Central African Republic', 'East Asia and the Pacific (UNICEF)', 
        'Eastern Mediterranean (WHO)', 'Eastern and Southern Africa (UNICEF)', 'European Region (WHO)', 
        'High-income countries', 'Latin America and the Caribbean (UNICEF)', 'Low-income countries', 
        'Lower-middle-income countries', 'Middle East and North Africa (UNICEF)', 'Middle-income countries', 
        'Region of the Americas (WHO)', 'South Asia (UNICEF)', 'South-East Asia Region (WHO)', 
        'Upper-middle-income countries', 'West and Central Africa (UNICEF)', 'Western Pacific Region (WHO)', 
        'World']
    vaccination_coverage = vaccination_coverage[~vaccination_coverage['Entity'].isin(repeated_geographies)]

    # ELIMINACIÓN DE LA COLUMNA "CODE"
    vaccination_coverage.drop(columns=["Code"], inplace=True)

    # TRADUCCIÓN Y REEMPLAZO DE LOS NOMBRES DE LOS PAÍSES DE LA COLUMNA "ENTITY" AL ESPAÑOL
    country_translation_dict = {
        'Afghanistan': 'Afganistán', 'Albania': 'Albania', 'Algeria': 'Argelia', 'Andorra': 'Andorra', 'Angola': 'Angola',
        'Antigua and Barbuda': 'Antigua y Barbuda', 'Argentina': 'Argentina', 'Armenia': 'Armenia', 'Australia': 'Australia', 'Austria': 'Austria',
        'Azerbaijan': 'Azerbaiyán', 'Bahamas': 'Bahamas', 'Bahrain': 'Baréin', 'Bangladesh': 'Bangladesh', 'Barbados': 'Barbados', 'Belarus': 'Bielorrusia',
        'Belgium': 'Bélgica', 'Belize': 'Belice', 'Benin': 'Benín', 'Bhutan': 'Bután', 'Bolivia': 'Bolivia', 'Bosnia and Herzegovina': 'Bosnia y Herzegovina',
        'Botswana': 'Botsuana', 'Brazil': 'Brasil', 'Brunei': 'Brunéi', 'Bulgaria': 'Bulgaria', 'Burkina Faso': 'Burkina Faso', 'Burundi': 'Burundi',
        'Cambodia': 'Camboya', 'Cameroon': 'Camerún', 'Canada': 'Canadá', 'Cape Verde': 'Cabo Verde', 'Chad': 'Chad', 'Chile': 'Chile', 'China': 'China',
        'Colombia': 'Colombia', 'Comoros': 'Comoras', 'Congo': 'Congo', 'Cook Islands': 'Islas Cook', 'Costa Rica': 'Costa Rica', "Cote d'Ivoire": 'Costa de Marfil',
        'Croatia': 'Croacia', 'Cuba': 'Cuba', 'Cyprus': 'Chipre', 'Czechia': 'República Checa', 'Democratic Republic of Congo': 'República Democrática del Congo',
        'Denmark': 'Dinamarca', 'Djibouti': 'Yibuti', 'Dominica': 'Dominica', 'Dominican Republic': 'República Dominicana', 'East Timor': 'Timor Oriental',
        'Ecuador': 'Ecuador', 'Egypt': 'Egipto', 'El Salvador': 'El Salvador', 'Equatorial Guinea': 'Guinea Ecuatorial', 'Eritrea': 'Eritrea', 'Estonia': 'Estonia',
        'Eswatini': 'Eswatini', 'Ethiopia': 'Etiopía', 'Fiji': 'Fiyi', 'Finland': 'Finlandia', 'France': 'Francia', 'Gabon': 'Gabón', 'Gambia': 'Gambia',
        'Georgia': 'Georgia', 'Germany': 'Alemania', 'Ghana': 'Ghana', 'Greece': 'Grecia', 'Grenada': 'Granada', 'Guatemala': 'Guatemala', 'Guinea': 'Guinea',
        'Guinea-Bissau': 'Guinea-Bisáu', 'Guyana': 'Guyana', 'Haiti': 'Haití', 'Honduras': 'Honduras', 'Hungary': 'Hungría', 'Iceland': 'Islandia', 'India': 'India',
        'Indonesia': 'Indonesia', 'Iran': 'Irán', 'Iraq': 'Irak', 'Ireland': 'Irlanda', 'Israel': 'Israel', 'Italy': 'Italia', 'Jamaica': 'Jamaica', 'Japan': 'Japón',
        'Jordan': 'Jordania', 'Kazakhstan': 'Kazajistán', 'Kenya': 'Kenia', 'Kiribati': 'Kiribati', 'Kuwait': 'Kuwait', 'Kyrgyzstan': 'Kirguistán', 'Laos': 'Laos',
        'Latvia': 'Letonia', 'Lebanon': 'Líbano', 'Lesotho': 'Lesoto', 'Liberia': 'Liberia', 'Libya': 'Libia', 'Lithuania': 'Lituania', 'Luxembourg': 'Luxemburgo',
        'Madagascar': 'Madagascar', 'Malawi': 'Malaui', 'Malaysia': 'Malasia', 'Maldives': 'Maldivas', 'Mali': 'Malí', 'Malta': 'Malta',
        'Marshall Islands': 'Islas Marshall', 'Mauritania': 'Mauritania', 'Mauritius': 'Mauricio', 'Mexico': 'México',
        'Micronesia (country)': 'Micronesia', 'Moldova': 'Moldavia', 'Monaco': 'Mónaco', 'Mongolia': 'Mongolia', 'Montenegro': 'Montenegro',
        'Morocco': 'Marruecos', 'Mozambique': 'Mozambique', 'Myanmar': 'Birmania', 'Namibia': 'Namibia', 'Nauru': 'Naurú', 'Nepal': 'Nepal', 'Netherlands': 'Países Bajos',
        'New Zealand': 'Nueva Zelanda', 'Nicaragua': 'Nicaragua', 'Niger': 'Níger', 'Nigeria': 'Nigeria', 'Niue': 'Niue', 'North Korea': 'Corea del Norte',
        'North Macedonia': 'Macedonia del Norte', 'Norway': 'Noruega', 'Oman': 'Omán', 'Pakistan': 'Pakistán', 'Palau': 'Palau', 'Palestine': 'Palestina', 'Panama': 'Panamá',
        'Papua New Guinea': 'Papúa Nueva Guinea', 'Paraguay': 'Paraguay', 'Peru': 'Perú', 'Philippines': 'Filipinas', 'Poland': 'Polonia', 'Portugal': 'Portugal',
        'Qatar': 'Catar', 'Romania': 'Rumanía', 'Russia': 'Rusia', 'Rwanda': 'Ruanda', 'Saint Kitts and Nevis': 'San Cristóbal y Nieves', 'Saint Lucia': 'Santa Lucía',
        'Saint Vincent and the Grenadines': 'San Vicente y las Granadinas', 'Samoa': 'Samoa', 'San Marino': 'San Marino',
        'Sao Tome and Principe': 'Santo Tomé y Príncipe', 'Saudi Arabia': 'Arabia Saudita', 'Senegal': 'Senegal', 'Serbia': 'Serbia', 'Seychelles': 'Seychelles',
        'Sierra Leone': 'Sierra Leona', 'Singapore': 'Singapur', 'Slovakia': 'Eslovaquia', 'Slovenia': 'Eslovenia', 'Solomon Islands': 'Islas Salomón',
        'Somalia': 'Somalia', 'South Africa': 'Sudáfrica', 'South Korea': 'Corea del Sur', 'South Sudan': 'Sudán del Sur', 'Spain': 'España', 'Sri Lanka': 'Sri Lanka',
        'Sudan': 'Sudán', 'Suriname': 'Surinam', 'Sweden': 'Suecia', 'Switzerland': 'Suiza', 'Syria': 'Siria', 'Tajikistan': 'Tayikistán', 'Tanzania': 'Tanzania',
        'Thailand': 'Tailandia', 'Togo': 'Togo', 'Tonga': 'Tonga', 'Trinidad and Tobago': 'Trinidad y Tobago', 'Tunisia': 'Túnez', 'Turkey': 'Turquía',
        'Turkmenistan': 'Turkmenistán', 'Tuvalu': 'Tuvalu', 'Uganda': 'Uganda', 'Ukraine': 'Ucrania', 'United Arab Emirates': 'Emiratos Árabes Unidos',
        'United Kingdom': 'Reino Unido', 'United States': 'Estados Unidos', 'Uruguay': 'Uruguay', 'Uzbekistan': 'Uzbekistán', 'Vanuatu': 'Vanuatu',
        'Venezuela': 'Venezuela', 'Vietnam': 'Vietnam', 'Yemen': 'Yemen', 'Zambia': 'Zambia', 'Zimbabwe': 'Zimbabue'
    }
    vaccination_coverage['Entity'] = vaccination_coverage['Entity'].replace(country_translation_dict)

    # REEMPLAZO DE LOS NOMBRES DE LAS COLUMNAS POR NOMBRES EN ESPAÑOL
    vaccination_coverage.columns = [
        'País',
        'Año',
        'Porcentaje de niños de un año que han recibido tres dosis de vacuna contra la Hepatitis B (HEPB3)',
        'Porcentaje de niños de un año que han recibido tres dosis de vacuna contra Haemophilus influenzae tipo b (HIB3)',
        'Porcentaje de niños de un año que han recibido su primera dosis de vacuna contra la poliomielitis inactivada (IPV1)',
        'Porcentaje de niños de un año que han recibido su primera dosis de vacuna contra el sarampión (MCV1)',
        'Porcentaje de niños de un año que han recibido la tercera dosis de vacuna conjugada contra el neumococo (PCV3)',
        'Porcentaje de niños de un año que han recibido su tercera dosis de vacuna oral o inactivada contra la poliomielitis (POL3)',
        'Porcentaje de niños de un año que han recibido una dosis de vacuna contra la rubéola (RCV1)',
        'Porcentaje de niños de un año que han recibido su dosis final recomendada (2ª o 3ª) de vacuna contra el rotavirus (ROTAC)',
        'Porcentaje de niños de un año que han recibido una dosis de vacuna contra la fiebre amarilla (YFV)',
        'Porcentaje de niños de un año que han recibido tres dosis de vacuna combinada contra la difteria, el tétanos y la tosferina (DTP3)'
    ]

    # NUEVA EXPLORACIÓN DEL DATAFRAME VACCINATION_COVERAGE PARA CHEQUEAR QUE ESTÉ LIMPIO
    print(vaccination_coverage.head(10000))
    print(vaccination_coverage.info())

    for column in vaccination_coverage.columns:
        print(f"Columna: {column}")
        print(vaccination_coverage[column].unique())
        print("-" * 40) # Separa entre columna y columna.

    return vaccination_coverage


# ---------------------- EXPLORACIÓN DE LIFE_EXPECTANCY ----------------------

def eda_life_expectancy(life_expectancy):
    '''
    Realiza el EDA ya explicado para life_expectancy.
    '''

    print(life_expectancy.head(10000)) 
    print(life_expectancy.info()) 

    for column in life_expectancy.columns: 
        print(f"Columna: {column}") 
        print(life_expectancy[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 

    life_expectancy.isna().sum() 

    # ELIMINACIÓN DE LAS FILAS DE GEOGRAFÍAS REPETIDAS 
    repeated_geographies = ['Africa', 'Americas', 'Asia', 'England and Wales', 'Europe', 'Falkland Islands', 'High-and-upper-middle-income countries', 'High-income countries', 'Land-locked Developing Countries (LLDC)', 'Latin America and the Caribbean', 'Least developed countries', 'Less developed regions', 'Less developed regions, excluding China', 'Less developed regions, excluding least developed countries', 'Low-and-Lower-middle-income countries', 'Low-and-middle-income countries', 'Low-income countries', 'Lower-middle-income countries', 'Middle-income countries', 'More developed regions', 'No income group available', 'Northern America', 'Oceania', 'Small Island Developing States (SIDS)', 'USSR', 'Upper-middle-income countries', 'World'] 
    life_expectancy = life_expectancy[~life_expectancy['Entity'].isin(repeated_geographies)] 

    # ELIMINACIÓN DE LA COLUMNA "CODE"
    life_expectancy.drop(columns=["Code"], inplace=True) 

    # TRADUCCIÓN Y REEMPLAZO DE LOS PAÍSES DE LA COLUMNA "ENTITY" AL ESPAÑOL 
    country_translation_dict = {
        'Afghanistan': 'Afganistán', 'Albania': 'Albania', 'Algeria': 'Argelia', 'American Samoa': 'Samoa Americana', 
        'Andorra': 'Andorra', 'Angola': 'Angola', 'Anguilla': 'Anguila', 'Antigua and Barbuda': 'Antigua y Barbuda', 
        'Argentina': 'Argentina', 'Armenia': 'Armenia', 'Aruba': 'Aruba', 'Australia': 'Australia', 'Austria': 'Austria', 
        'Azerbaijan': 'Azerbaiyán', 'Bahamas': 'Bahamas', 'Bahrain': 'Baréin', 'Bangladesh': 'Bangladés', 
        'Barbados': 'Barbados', 'Belarus': 'Bielorrusia', 'Belgium': 'Bélgica', 'Belize': 'Belice', 'Benin': 'Benín', 
        'Bermuda': 'Bermudas', 'Bhutan': 'Bután', 'Bolivia': 'Bolivia', 'Bonaire Sint Eustatius and Saba': 'Bonaire, Sint Eustatius y Saba', 
        'Bosnia and Herzegovina': 'Bosnia y Herzegovina', 'Botswana': 'Botsuana', 'Brazil': 'Brasil', 
        'British Virgin Islands': 'Islas Vírgenes Británicas', 'Brunei': 'Brunéi', 'Bulgaria': 'Bulgaria', 
        'Burkina Faso': 'Burkina Faso', 'Burundi': 'Burundi', 'Cambodia': 'Camboya', 'Cameroon': 'Camerún', 
        'Canada': 'Canadá', 'Cape Verde': 'Cabo Verde', 'Cayman Islands': 'Islas Caimán', 
        'Central African Republic': 'República Centroafricana', 'Chad': 'Chad', 'Chile': 'Chile', 'China': 'China', 
        'Colombia': 'Colombia', 'Comoros': 'Comoras', 'Congo': 'Congo', 'Cook Islands': 'Islas Cook', 
        'Costa Rica': 'Costa Rica', "Cote d'Ivoire": 'Costa de Marfil', 'Croatia': 'Croacia', 'Cuba': 'Cuba', 
        'Curacao': 'Curazao', 'Cyprus': 'Chipre', 'Czechia': 'República Checa', 'Democratic Republic of Congo': 'República Democrática del Congo', 
        'Denmark': 'Dinamarca', 'Djibouti': 'Yibuti', 'Dominica': 'Dominica', 'Dominican Republic': 'República Dominicana', 
        'East Timor': 'Timor Oriental', 'Ecuador': 'Ecuador', 'Egypt': 'Egipto', 'El Salvador': 'El Salvador', 
        'Equatorial Guinea': 'Guinea Ecuatorial', 'Eritrea': 'Eritrea', 'Estonia': 'Estonia', 'Eswatini': 'Esuatini', 
        'Ethiopia': 'Etiopía', 'Faroe Islands': 'Islas Feroe', 'Fiji': 'Fiyi', 'Finland': 'Finlandia', 'France': 'Francia', 
        'French Guiana': 'Guayana Francesa', 'French Polynesia': 'Polinesia Francesa', 'Gabon': 'Gabón', 
        'Gambia': 'Gambia', 'Georgia': 'Georgia', 'Germany': 'Alemania', 'Ghana': 'Ghana', 'Gibraltar': 'Gibraltar', 
        'Greece': 'Grecia', 'Greenland': 'Groenlandia', 'Grenada': 'Granada', 'Guadeloupe': 'Guadalupe', 'Guam': 'Guam', 
        'Guatemala': 'Guatemala', 'Guernsey': 'Guernsey', 'Guinea': 'Guinea', 'Guinea-Bissau': 'Guinea-Bisáu', 
        'Guyana': 'Guyana', 'Haiti': 'Haití', 'Honduras': 'Honduras', 'Hong Kong': 'Hong Kong', 'Hungary': 'Hungría', 
        'Iceland': 'Islandia', 'India': 'India', 'Indonesia': 'Indonesia', 'Iran': 'Irán', 'Iraq': 'Irak', 
        'Ireland': 'Irlanda', 'Isle of Man': 'Isla de Man', 'Israel': 'Israel', 'Italy': 'Italia', 'Jamaica': 'Jamaica', 
        'Japan': 'Japón', 'Jersey': 'Jersey', 'Jordan': 'Jordania', 'Kazakhstan': 'Kazajistán', 'Kenya': 'Kenia', 
        'Kiribati': 'Kiribati', 'Kosovo': 'Kosovo', 'Kuwait': 'Kuwait', 'Kyrgyzstan': 'Kirguistán', 'Laos': 'Laos', 
        'Latvia': 'Letonia', 'Lebanon': 'Líbano', 'Lesotho': 'Lesoto', 'Liberia': 'Liberia', 'Libya': 'Libia', 
        'Liechtenstein': 'Liechtenstein', 'Lithuania': 'Lituania', 'Luxembourg': 'Luxemburgo', 'Macao': 'Macao', 
        'Madagascar': 'Madagascar', 'Malawi': 'Malawi', 'Malaysia': 'Malasia', 'Maldives': 'Maldivas', 'Mali': 'Malí', 
        'Malta': 'Malta', 'Marshall Islands': 'Islas Marshall', 'Martinique': 'Martinica', 'Mauritania': 'Mauritania', 
        'Mauritius': 'Mauricio', 'Mayotte': 'Mayotte', 'Mexico': 'México', 'Micronesia (country)': 'Micronesia', 
        'Moldova': 'Moldavia', 'Monaco': 'Mónaco', 'Mongolia': 'Mongolia', 'Montenegro': 'Montenegro', 
        'Montserrat': 'Montserrat', 'Morocco': 'Marruecos', 'Mozambique': 'Mozambique', 'Myanmar': 'Birmania', 
        'Namibia': 'Namibia', 'Nauru': 'Nauru', 'Nepal': 'Nepal', 'Netherlands': 'Países Bajos', 'New Caledonia': 'Nueva Caledonia', 
        'New Zealand': 'Nueva Zelanda', 'Nicaragua': 'Nicaragua', 'Niger': 'Níger', 'Nigeria': 'Nigeria', 'Niue': 'Niue', 
        'North Korea': 'Corea del Norte', 'North Macedonia': 'Macedonia del Norte', 'Northern Ireland': 'Irlanda del Norte', 
        'Northern Mariana Islands': 'Islas Marianas del Norte', 'Norway': 'Noruega', 'Oman': 'Omán', 'Pakistan': 'Pakistán', 
        'Palau': 'Palau', 'Palestine': 'Palestina', 'Panama': 'Panamá', 'Papua New Guinea': 'Papúa Nueva Guinea', 'Paraguay': 'Paraguay', 
        'Peru': 'Perú', 'Philippines': 'Filipinas', 'Poland': 'Polonia', 'Portugal': 'Portugal', 'Puerto Rico': 'Puerto Rico', 
        'Qatar': 'Catar', 'Reunion': 'Reunión', 'Romania': 'Rumanía', 'Russia': 'Rusia', 'Rwanda': 'Ruanda', 
        'Saint Barthelemy': 'San Bartolomé', 'Saint Helena': 'Santa Elena', 'Saint Kitts and Nevis': 'San Cristóbal y Nieves', 
        'Saint Lucia': 'Santa Lucía', 'Saint Martin (French part)': 'San Martín (parte francesa)', 
        'Saint Pierre and Miquelon': 'San Pedro y Miquelón', 'Saint Vincent and the Grenadines': 'San Vicente y las Granadinas', 
        'Samoa': 'Samoa', 'San Marino': 'San Marino', 'Sao Tome and Principe': 'Santo Tomé y Príncipe', 'Saudi Arabia': 'Arabia Saudita', 
        'Scotland': 'Escocia', 'Senegal': 'Senegal', 'Serbia': 'Serbia', 'Seychelles': 'Seychelles', 'Sierra Leone': 'Sierra Leona', 
        'Singapore': 'Singapur', 'Sint Maarten (Dutch part)': 'Sint Maarten (parte holandesa)', 'Slovakia': 'Eslovaquia', 
        'Slovenia': 'Eslovenia', 'Solomon Islands': 'Islas Salomón', 'Somalia': 'Somalia', 'South Africa': 'Sudáfrica', 'South Korea': 'Corea del Sur', 
        'South Sudan': 'Sudán del Sur', 'Spain': 'España', 'Sri Lanka': 'Sri Lanka', 'Sudan': 'Sudán', 'Suriname': 'Surinam', 
        'Sweden': 'Suecia', 'Switzerland': 'Suiza', 'Syria': 'Siria', 'Taiwan': 'Taiwán', 'Tajikistan': 'Tayikistán', 
        'Tanzania': 'Tanzania', 'Thailand': 'Tailandia', 'Togo': 'Togo', 'Tokelau': 'Tokelau', 'Tonga': 'Tonga', 
        'Trinidad and Tobago': 'Trinidad y Tobago', 'Tunisia': 'Túnez', 'Turkey': 'Turquía', 'Turkmenistan': 'Turkmenistán', 
        'Turks and Caicos Islands': 'Islas Turcas y Caicos', 'Tuvalu': 'Tuvalu', 'Uganda': 'Uganda', 'Ukraine': 'Ucrania', 
        'United Arab Emirates': 'Emiratos Árabes Unidos', 'United Kingdom': 'Reino Unido', 'United States': 'Estados Unidos', 
        'United States Virgin Islands': 'Islas Vírgenes de los Estados Unidos', 'Uruguay': 'Uruguay', 'Uzbekistan': 'Uzbekistán', 
        'Vanuatu': 'Vanuatu', 'Vatican': 'Vaticano', 'Venezuela': 'Venezuela', 'Vietnam': 'Vietnam', 'Wallis and Futuna': 'Wallis y Futuna', 
        'Western Sahara': 'Sáhara Occidental', 'Yemen': 'Yemen', 'Zambia': 'Zambia', 'Zimbabwe': 'Zimbabue'
    }
    life_expectancy['Entity'] = life_expectancy['Entity'].replace(country_translation_dict) 

    # REEMPLAZO DE LOS NOMBRES DE LAS COLUMNAS POR NOMBRES EN ESPAÑOL
    life_expectancy.columns=['País', 'Año', 'Esperanza de vida al nacer']

    # NUEVA EXPLORACIÓN DEL DATAFRAME LIFE_EXPECTANCY PARA CHEQUEAR QUE ESTÉ LIMPIO 
    print(life_expectancy.head(10000))
    print(life_expectancy.info()) 

    for column in life_expectancy.columns: 
        print(f"Columna: {column}")
        print(life_expectancy[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 

    life_expectancy.isna().sum() 
    
    return life_expectancy


# ---------------------- EXPLORACIÓN DE PREVENTABLE_DEATHS ----------------------

def eda_preventable_deaths(preventable_deaths):
    '''
    Realiza el EDA ya explicado para preventable_deaths.
    '''

    print(preventable_deaths.head(10000)) 
    print(preventable_deaths.info()) 

    for column in preventable_deaths.columns: 
        print(f"Columna: {column}") 
        print(preventable_deaths[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 

    preventable_deaths.isna().sum() # No tiene nulos

    # ELIMINACIÓN DE LAS FILAS DE GEOGRAFÍAS REPETIDAS 
    repeated_geographies = ['Aceh', 'Acre', 'Advanced Health System', 'Adís Abeda', 'Afar', 'Africa Subsahariana', 'Africa Subsahariana Central',  'Africa Subsahariana Occidental', 'Africa Subsahariana Sur', 'Agder', 'Aguascalientes', 'Aichi', 'Akita',
    'Alabama', 'Alagoas', 'Alaska', 'Amapa', 'Amazonas', 'Amhara', 'América', 'América Latina & Caribe - BM', 'América Latina Andina', 'América Latina Central', 'América Latina Tropical', 'América Latina y el Caribe',
    'América del Norte', 'América del Norte Ingresos Altos', 'América del Sur', 'Andhra Pradesh', 'Aomori', 'Ardebil', 'Arizona', 'Arkansas', 'Arunachal Pradesh', 'Asia', 'Asia Central', 'Asia Oriental',
    'Asia Oriental & Pacífico - BM', 'Asia del Sur', 'Asia del Sur - BM', 'Asia-Pacífico Ingresos Altos', 'Assam', 'Association of Southeast Asian Nations', 'Australasia', 'Azad Jammu y Cachemira',
    'Azerbaiyán Occidental', 'Azerbaiyán Oriental', 'Bahréin', 'Bahía', 'Bahía de Homa', 'Baja California', 'Baja California Sur', 'Bali', 'Baluchistán','Bantén', 'Baringo', 'Barnet', 'Barnsley', 'Basic Health System',
    'Bath y Noreste de Somerset', 'Bedford', 'Bedfordshire central', 'Bengala Occidental', 'Bengkulu', 'Benishangul-Gumaz', 'Bexley', 'Bihar', 'Birmingham', 'Blackburn con Darwen', 'Blackpool', 'Bolton', 'Bomet',
    'Borneo Central', 'Borneo Meridional', 'Borneo Occidental', 'Borneo Oriental', 'Borneo Septentrional', 'Bosque de Bracknell', 'Bosque de Waltham', 'Bournemouth', 'Bradford', 'Brazil Central-West', 'Brazil North', 'Brazil Northeast', 'Brazil South',
    'Brazil Southeast', 'Brent', 'Brighton y Hove', 'Bristol, ciudad de', 'Bromley', 'Buckinghamshire', 'Bungoma', 'Bushehr', 'Busia', 'Cabo Norte', 'Cabo Occidental', 'Cabo Oriental', 'Calderdale', 'California', 'Cambridgeshire',
    'Camden', 'Campeche', 'Caribe', 'Carolina del Norte', 'Carolina del Sur', 'Ceará', 'Central Africa', 'Chahar Mahal y Bajtiarí', 'Cheshire West y Chester', 'Chhattisgarh', 'Chiapas', 'Chiba', 'Chihuahua', 'Ciudad de México', 'Coahuila',
    'Colima', 'Colorado', 'Commonwealth', 'Commonwealth Ingresos Altos', 'Commonwealth Ingresos Bajos', 'Commonwealth Ingresos Medios', 'Condado de Durham', 'Connecticut', 'Cornualles', 'Coventry', 'Croydon', 'Cuatro Regiones del Mundo',
    'Cumbria', 'Célebes Central', 'Célebes Meridional', 'Célebes Occidental', 'Célebes Septentrional', 'Célebes Sureste', 'Dakota del Norte', 'Dakota del Sur', 'Darlington', 'Delaware', 'Delhi', 'Derbyshire', 'Devon', 'Dire Dawa',
    'Distrito de Columbia', 'Doncaster', 'Dorset', 'Dudley', 'Durango', 'Ealing', 'East Midlands', 'East Riding de Yorkshire', 'East Sussex', 'Eastern Africa', 'Ehime', 'Elgeyo-Marakwet', 'Embu', 'Enfield', 'Enterrar', 'Escocia', 'Espíritu Santo',
    'Essex', 'Estado Libre', 'Este de Cheshire', 'Este de Inglaterra', 'Estocolmo', 'Europa', 'Europa &  Asia Central - BM', 'Europa Central', 'Europa Central, Oriental y Asia Central ', 'Europa Occidental', 'Europa Oriental', 'Fars',
    'Florida', 'Fukui', 'Fukuoka', 'Fukushima', 'G20', 'Gales', 'Gambela', 'Garissa', 'Gateshead', 'Gauteng', 'Gifu', 'Gilgit-Baltistán', 'Gloucestershire', 'Goa', 'Golestán', 'Gorontalo', 'Goías', 'Grada', 'Gran Londres', 'Greenwich',
    'Guam', 'Guanajuato', 'Guerrero', 'Guilán ', 'Gulf Cooperation Council', 'Gunma', 'Guyarat', 'Halton', 'Hamadán', 'Hammersmith y Fulham', 'Hampshire', 'Harar', 'Haringey', 'Hartlepool', 'Haryana', 'Havering', 'Hawái', 'Health System Grouping Levels',
    'Herefordshire, Condado de', 'Hertfordshire', 'Hidalgo', 'Hillingdon', 'Himachal Pradesh', 'Hiroshima', 'Hokkaidō','Hormozgán', 'Hounslow', 'Hyōgo', 'ISD Alto', 'ISD Alto-Medio ', 'ISD Bajo', 'ISD Bajo-Medio', 'ISD Medio', 'Ibaraki',
    'Idaho', 'Ilam', 'Illinois', 'Indiana', 'Inglaterra', 'Ingresos Altos', 'Innlandet', 'Iowa', 'Iraq', 'Irlanda del Norte', 'Isfahán', 'Ishikawa', 'Isiolo', 'Isla de Wight', 'Islas Bangka-Belitung','Islas Riau','Islington', 'Iwate',
    'Jaiber Pastunjuá', 'Jalisco', 'Jambi', 'Jammu y Cachemira', 'Java Central', 'Java Occidental', 'Java Oriental', 'Jharkhand', 'Jorasán Razaví', 'Jorasán del Norte', 'Jorasán del Sur', 'Juzestán', 'Kagawa', 'Kagoshima', 'Kajiado',
    'Kakamega', 'Kanagawa', 'Kansas', 'Karnataka', 'Kensington y Chelsea', 'Kent', 'Kentucky', 'Kerala', 'Kericho', 'Kermanshah', 'Kermán', 'Kiambu', 'Kilifi', 'Kingston upon Hull, Ciudad de', 'Kingston upon Thames', 'Kioto',
    'Kirinyaga', 'Kirklees', 'Kisii', 'Kisumu', 'Kitui', 'Knowsley', 'Kohkiluyeh y Buyer Ahmad', 'Kumamoto', 'Kurdistán', 'KwaZulu-Natal', 'Kwale', 'Kōchi', 'Ladrando y Dagenham', 'Laikipia', 'Lambeth', 'Lampung',
    'Lamu', 'Lancashire', 'Las Bahamas', 'Leeds', 'Leicester', 'Leicestershire', 'Lewisham', 'Leyendo', 'Limited Health System', 'Limpopo', 'Lincolnshire', 'Liverpool', 'Lorestán', 'Los seis territorios menores', 'Luisiana', 'Luton',
    'Macedonia', 'Machakos', 'Madhya Pradesh', 'Maharashtra', 'Maine', 'Makueni', 'Mali', 'Manchester', 'Mandera', 'Manipur', 'Marañón', 'Markazí', 'Marsabit', 'Maryland', 'Massachusetts', 'Mato Grosso', 'Mato Grosso del Sur',
    'Mazandarán', 'Medway', 'Meghalaya', 'Merton', 'Meru', 'Michigan', 'Michoacán', 'Middlesbrough', 'Mie', 'Migori', 'Milton Keynes', 'Minas Gerais', 'Minimal Health System', 'Minnesota', 'Misisipi', 'Misuri', 'Miyagi', 'Miyazaki',
    'Mizorán', 'Molucas', 'Molucas Septentrionales', 'Mombasa', 'Montana', 'Montes Elburz', 'Morelos', 'Mpumalanga', 'Mudar', 'Mundo', 'Mundo Árabe', 'Muranga', 'Máquina de alquiler', 'Møre og Romsdal', 'Naciones Nacionalidades y Pueblos Sur',
    'Nagaland', 'Nagano', 'Nagasaki', 'Nairobi', 'Nakuru', 'Nandi', 'Nara', 'Narok','Nayarit', 'Nebraska', 'Nevada', 'Newcastle upon Tyne', 'Newham', 'Niigata', 'Nordland', 'Noreste de Inglaterra', 'Noreste de Lincolnshire', 'Norfolk',
    'Noroeste', 'Noroeste de Inglaterra', 'North Lincolnshire', 'North Somerset', 'North Tyneside', 'Northamptonshire', 'Northern Africa', 'Northumberland', 'Nottingham', 'Nottinghamshire', 'Nueva Jersey', 'Nueva York', 'Nuevo Hampshire',
    'Nuevo León', 'Nuevo Mexico', 'Nusatenggara Occidental', 'Nusatenggara Oriental', 'Nyamira', 'Nyandarua', 'Nyeri', 'Oaxaca', 'Oceanía', 'Ohio', 'Okayama', 'Okinawa', 'Oklahoma', 'Oldham', 'Oregón', 'Organization of Islamic Cooperation',
    'Orissa', 'Oromía', 'Osaka', 'Oslo', 'Oxfordshire', 'Palaos', 'Papúa', 'Papúa Occidental', 'Paraná', 'Paraíba', 'Pará', 'Países de la OCDE', 'Pensilvania', 'Pernambuco', 'Peterborough', 'Piauí', 'Plymouth', 'Poole', 'Portsmouth',
    'Puebla', 'Punyab', 'Qazvín', 'Qom', 'Querétaro', 'Quintana Roo', 'Rajastán', 'Redbridge', 'Redcar y Cleveland', 'Regiones Banco Mundial', 'Región Africana', 'Región Europea', 'Región Mediterránea Oriental', 'Región Nórdica',
    'Región OMS', 'Región de las Américas', 'Región del Pacífico Occidental', 'Región del Sureste Asiático', 'República Centroafricana', 'Rhode Island', 'Riau', 'Richmond upon Thames', 'Rochdale', 'Rogaland', 'Rondonia', 'Roraima', 'Rotherham',
    'Rutland', 'Río Grande del Norte', 'Río Grande del Sur', 'Río Tana', 'Río de Janeiro', 'Saga', 'Sahel Region', 'Saitama', 'Salford', 'Samburu', 'Samoa Americana', 'San Luis Potosí', 'San Paulo', 'Sandwell', 'Santa Catarina',
    'Sefton', 'Semnán', 'Sergipe', 'Sheffield', 'Shiga', 'Shimane', 'Shizuoka', 'Shropshire', 'Siaya', 'Sikkim', 'Sinaloa', 'Sind', 'Sistán y Baluchistán', 'Solihull', 'Somali', 'Sonora', 'South Gloucestershire', 'South Tyneside',
    'Southampton', 'Southend-on-Sea', 'Southern Africa', 'Southwark', 'St Helens', 'Staffordshire', 'Stockport', 'Stockton-on-Tees', 'Stoke on Trent', 'Suazilandia', 'Sudeste Asiático', 'Suecia excepto Estocolmo', 'Suffolk',
    'Sumatra Meridional', 'Sumatra Occidental', 'Sumatra Septentrional', 'Sunderland', 'Sureste Asia, Asia Oriental y Oceanía', 'Sureste de Inglaterra', 'Suroeste de Inglaterra', 'Surrey', 'Sutton', 'Swindon', 'Tabasco', 'Taita-Taveta',
    'Taiwán', 'Tamaulipas', 'Tameside', 'Tamil Nadu', 'Teherán', 'Telangana', 'Telford y Wrekin', 'Tennessee', 'Territorio de la Capital Islamabad', 'Texas', 'Tharaka-Nithi', 'Thurrock', 'Tigray', 'Tlaxcala', 'Tocantins',
    'Tochigi', 'Tokelau', 'Tokio', 'Tokushima', 'Torbay', 'Tottori', 'Tower Hamlets', 'Toyama', 'Trafford', 'Trans-Nzoia', 'Tripura', 'Troms y Finnmark', 'Trøndelag', 'Turkana', 'Uasin Gishu', 'Unión Africana ', 'Unión Europea',
    'Utah', 'Uttar Pradesh', 'Uttarakhand', 'Veracruz', 'Vermont', 'Vestfold y Telemark', 'Vestland', 'Vihiga', 'Viken', 'Virginia', 'Virginia Occidental', 'Voltereta', 'Wajir', 'Wakayama', 'Wakefield',
    'Walsall', 'Wandsworth', 'Warrington', 'Warwickshire', 'Washington', 'West Berkshire', 'West Midlands', 'West Pokot', 'West Sussex', 'Western Africa', 'Westminster', 'Wigan', 'Wiltshire', 'Windsor y Maidenhead',
    'Wirral', 'Wisconsin', 'Wokingham', 'Wolverhampton', 'Worcestershire', 'Wyoming', 'Yakarta', 'Yamagata', 'Yamaguchi', 'Yamanashi', 'Yazd', 'Yogyakarta', 'York', 'Yorkshire del norte', 'Yorkshire y Humber', 'Yucatán', 'Zacatecas',
    'Zanyán', 'derby', 'África', 'África Subsahariana - BM', 'África Subsahariana Oriental', 'África del Norte & Medio Oriente - BM',
    'África del Norte y Medio Oriente', 'Ōita', 'Bermudas', 'Granada', 'Islas Cook']
    preventable_deaths = preventable_deaths[~preventable_deaths['location_name'].isin(repeated_geographies)] 

    # ELIMINACIÓN DE LAS FILAS DE "PORCENTAJE" Y "TASA". SÓLO INTERESA EL NÚMERO ABSOLUTO DE MUERTES
    preventable_deaths = preventable_deaths[~preventable_deaths['metric_name'].isin(['Porcentaje', 'Tasa'])]

    # ELIMINACIÓN DE LAS COLUMNAS QUE NO SON NECESARIAS PARA EL ANÁLISIS
    preventable_deaths.drop(columns=['measure_id', 'measure_name', 'location_id', 'sex_id', 'sex_name', 'age_id', 'age_name', 'cause_id', 'metric_name', 'metric_id', 'upper', 'lower'], inplace=True)

    # REEMPLAZO DE LOS NOMBRES DE LAS COLUMNAS POR NOMBRES EN ESPAÑOL
    preventable_deaths.columns = [ 'País', 'Causa de muerte', 'Año', 'Muertes']

    # NUEVA EXPLORACIÓN DE PREVENTABLE_DEATHS PARA CHEQUEAR QUE ESTÉ LIMPIO
    print(preventable_deaths.head(10000)) 
    print(preventable_deaths.info()) 

    for column in preventable_deaths.columns: 
        print(f"Columna: {column}") 
        print(preventable_deaths[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 
    
    return preventable_deaths


# ---------------------- EXPLORACIÓN DE GDP ----------------------

def eda_gdp(gdp):
    '''
    Realiza el EDA ya explicado para gdp.
    '''

    print(gdp.head(10000)) 
    print(gdp.info()) 
    for column in gdp.columns: 
        print(f"Columna: {column}") 
        print(gdp[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 
    gdp.isna().sum() 

    # ELIMINACIÓN DE LA COLUMNA "CODE"
    gdp.drop(columns=["Code"], inplace=True) 

    # ELIMINACIÓN DE LAS FILAS DE GEOGRAFÍAS REPETIDAS 
    repeated_geographies = ['Bermuda', 'East Asia and Pacific (WB)', 'Europe and Central Asia (WB)', 'European Union (27)', 'High-income countries', 'Latin America and Caribbean (WB)', 'Low-income countries', 'Lower-middle-income countries', 'Middle East and North Africa (WB)', 'Middle-income countries', 'North America (WB)', 'South Asia (WB)', 'Sub-Saharan Africa (WB)', 'United States Virgin Islands', 'Upper-middle-income countries', 'World']
    gdp = gdp[~gdp['Entity'].isin(repeated_geographies)] 

    # TRADUCCIÓN Y REEMPLAZO DE LOS NOMBRES DE PAÍSES AL ESPAÑOL 
    country_translation_dict = {
        'Afghanistan': 'Afganistán', 'Albania': 'Albania', 'Algeria': 'Argelia', 'Andorra': 'Andorra',
        'Angola': 'Angola', 'Antigua and Barbuda': 'Antigua y Barbuda', 'Argentina': 'Argentina',
        'Armenia': 'Armenia', 'Aruba': 'Aruba', 'Australia': 'Australia', 'Austria': 'Austria',
        'Azerbaijan': 'Azerbaiyán', 'Bahamas': 'Bahamas', 'Bahrain': 'Baréin', 'Bangladesh': 'Bangladesh', 'Barbados': 'Barbados',
        'Belarus': 'Bielorrusia', 'Belgium': 'Bélgica', 'Belize': 'Belice', 'Benin': 'Benín',
        'Bhutan': 'Bután', 'Bolivia': 'Bolivia', 'Bosnia and Herzegovina': 'Bosnia y Herzegovina', 'Botswana': 'Botsuana',
        'Brazil': 'Brasil', 'Brunei': 'Brunéi', 'Bulgaria': 'Bulgaria', 'Burkina Faso': 'Burkina Faso',
        'Burundi': 'Burundi', 'Cambodia': 'Camboya', 'Cameroon': 'Camerún', 'Canada': 'Canadá',
        'Cape Verde': 'Cabo Verde', 'Cayman Islands': 'Islas Caimán', 'Central African Republic': 'República Centroafricana', 'Chad': 'Chad',
        'Chile': 'Chile', 'China': 'China', 'Colombia': 'Colombia', 'Comoros': 'Comoras',
        'Congo': 'Congo', 'Costa Rica': 'Costa Rica', "Cote d'Ivoire": 'Costa de Marfil', 'Croatia': 'Croacia',
        'Curacao': 'Curazao', 'Cyprus': 'Chipre', 'Czechia': 'República Checa', 'Democratic Republic of Congo': 'República Democrática del Congo',
        'Denmark': 'Dinamarca', 'Djibouti': 'Yibuti', 'Dominica': 'Dominica', 'Dominican Republic': 'República Dominicana',
        'East Timor': 'Timor Oriental', 'Ecuador': 'Ecuador', 'Egypt': 'Egipto', 'El Salvador': 'El Salvador',
        'Equatorial Guinea': 'Guinea Ecuatorial', 'Estonia': 'Estonia', 'Eswatini': 'Esuatini', 'Ethiopia': 'Etiopía',
        'Faeroe Islands': 'Islas Feroe', 'Fiji': 'Fiyi', 'Finland': 'Finlandia', 'France': 'Francia',
        'Gabon': 'Gabón', 'Gambia': 'Gambia', 'Georgia': 'Georgia', 'Germany': 'Alemania',
        'Ghana': 'Ghana', 'Greece': 'Grecia', 'Greenland': 'Groenlandia', 'Grenada': 'Granada',
        'Guatemala': 'Guatemala', 'Guinea': 'Guinea', 'Guinea-Bissau': 'Guinea-Bisáu', 'Guyana': 'Guyana',
        'Haiti': 'Haití', 'Honduras': 'Honduras', 'Hong Kong': 'Hong Kong', 'Hungary': 'Hungría',
        'Iceland': 'Islandia', 'India': 'India', 'Indonesia': 'Indonesia', 'Iran': 'Irán',
        'Iraq': 'Irak', 'Ireland': 'Irlanda', 'Israel': 'Israel', 'Italy': 'Italia',
        'Jamaica': 'Jamaica', 'Japan': 'Japón', 'Jordan': 'Jordania', 'Kazakhstan': 'Kazajistán',
        'Kenya': 'Kenia', 'Kiribati': 'Kiribati', 'Kosovo': 'Kosovo', 'Kuwait': 'Kuwait',
        'Kyrgyzstan': 'Kirguistán', 'Laos': 'Laos', 'Latvia': 'Letonia', 'Lebanon': 'Líbano',
        'Lesotho': 'Lesoto', 'Liberia': 'Liberia', 'Libya': 'Libia', 'Lithuania': 'Lituania',
        'Luxembourg': 'Luxemburgo', 'Macao': 'Macao', 'Madagascar': 'Madagascar', 'Malawi': 'Malaui',
        'Malaysia': 'Malasia', 'Maldives': 'Maldivas', 'Mali': 'Malí', 'Malta': 'Malta',
        'Marshall Islands': 'Islas Marshall', 'Mauritania': 'Mauritania', 'Mauritius': 'Mauricio', 'Mexico': 'México',
        'Micronesia (country)': 'Micronesia', 'Moldova': 'Moldavia', 'Mongolia': 'Mongolia', 'Montenegro': 'Montenegro',
        'Morocco': 'Marruecos', 'Mozambique': 'Mozambique', 'Myanmar': 'Birmania', 'Namibia': 'Namibia',
        'Nauru': 'Nauru', 'Nepal': 'Nepal', 'Netherlands': 'Países Bajos', 'New Zealand': 'Nueva Zelanda',
        'Nicaragua': 'Nicaragua', 'Niger': 'Níger', 'Nigeria': 'Nigeria', 'North Macedonia': 'Macedonia del Norte',
        'Norway': 'Noruega', 'Oman': 'Omán', 'Pakistan': 'Pakistán', 'Palau': 'Palaos',
        'Palestine': 'Palestina', 'Panama': 'Panamá', 'Papua New Guinea': 'Papúa Nueva Guinea', 'Paraguay': 'Paraguay',
        'Peru': 'Perú', 'Philippines': 'Filipinas', 'Poland': 'Polonia', 'Portugal': 'Portugal',
        'Puerto Rico': 'Puerto Rico', 'Qatar': 'Catar', 'Romania': 'Rumanía', 'Russia': 'Rusia',
        'Rwanda': 'Ruanda', 'Saint Kitts and Nevis': 'San Cristóbal y Nieves', 'Saint Lucia': 'Santa Lucía', 'Saint Vincent and the Grenadines': 'San Vicente y las Granadinas',
        'Samoa': 'Samoa', 'San Marino': 'San Marino', 'Sao Tome and Principe': 'Santo Tomé y Príncipe', 'Saudi Arabia': 'Arabia Saudita',
        'Senegal': 'Senegal', 'Serbia': 'Serbia', 'Seychelles': 'Seychelles', 'Sierra Leone': 'Sierra Leona',
        'Singapore': 'Singapur', 'Sint Maarten (Dutch part)': 'Sint Maarten (parte neerlandesa)',
        'Slovakia': 'Eslovaquia', 'Slovenia': 'Eslovenia', 'Solomon Islands': 'Islas Salomón', 'Somalia': 'Somalia',
        'South Africa': 'Sudáfrica', 'South Korea': 'Corea del Sur', 'Spain': 'España', 'Sri Lanka': 'Sri Lanka',
        'Sudan': 'Sudán', 'Suriname': 'Surinam', 'Sweden': 'Suecia', 'Switzerland': 'Suiza',
        'Syria': 'Siria', 'Tajikistan': 'Tayikistán', 'Tanzania': 'Tanzania', 'Thailand': 'Tailandia',
        'Togo': 'Togo', 'Tonga': 'Tonga', 'Trinidad and Tobago': 'Trinidad y Tobago', 'Tunisia': 'Túnez',
        'Turkey': 'Turquía', 'Turkmenistan': 'Turkmenistán', 'Turks and Caicos Islands': 'Islas Turcas y Caicos', 'Tuvalu': 'Tuvalu',
        'Uganda': 'Uganda', 'Ukraine': 'Ucrania', 'United Arab Emirates': 'Emiratos Árabes Unidos', 'United Kingdom': 'Reino Unido',
        'United States': 'Estados Unidos', 'Uruguay': 'Uruguay', 'Uzbekistan': 'Uzbekistán', 'Vanuatu': 'Vanuatu',
        'Vietnam': 'Vietnam', 'Zambia': 'Zambia', 'Zimbabwe': 'Zimbabue'
    }
    gdp['Entity'] = gdp['Entity'].replace(country_translation_dict)

    # REEMPLAZO DE LOS NOMBRES DE LAS COLUMNAS POR NOMBRES EN ESPAÑOL
    gdp.columns = ['País', 'Año', 'PIB per cápita a precios constantes']

    # NUEVA EXPLORACIÓN DE GDP PARA CHEQUEAR QUE ESTÉ LIMPIO
    print(gdp.head(10000)) 
    print(gdp.info()) 

    for column in gdp.columns: 
        print(f"Columna: {column}") 
        print(gdp[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 

    gdp.isna().sum() 

    return gdp


# ---------------------- EXPLORACIÓN DE LITERACY ----------------------

def eda_literacy(literacy):
    '''
    Realiza el EDA ya explicado para literacy.
    '''

    print(literacy.head(10000)) 
    print(literacy.info()) 

    for column in literacy.columns: 
        print(f"Columna: {column}") 
        print(literacy[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 

    literacy.isna().sum() 

    # ELIMINACIÓN DE LAS FILAS DE GEOGRAFÍAS REPETIDAS 
    repeated_geographies = ['Arab World', 'Arab World (WB)', 'British Virgin Islands', 'Caribbean small states', 'Central Europe and the Baltics', 'Central Europe and the Baltics (WB)', 'Early-demographic dividend', 'East Asia & Pacific', 'East Asia & Pacific (IDA & IBRD)', 'East Asia & Pacific (excluding high income)', 'East Asia and the Pacific (WB)', 'Europe & Central Asia', 'Europe & Central Asia (IDA & IBRD)', 'Europe & Central Asia (excluding high income)', 'Europe and Central Asia (WB)', 'Fragile and conflict affected situations', 'Heavily indebted poor countries (HIPC)', 'IBRD only', 'IDA & IBRD total', 'IDA blend', 'IDA only', 'IDA total', 'Late-demographic dividend', 'Latin America & Caribbean', 'Latin America & Caribbean (IDA & IBRD)', 'Latin America & Caribbean (excluding high income)', 'Latin America and Caribbean (WB)', 'Least developed countries: UN classification', 'Low income', 'Low-income countries', 'Lower middle income', 'Lower-middle-income countries', 'Middle East & North Africa', 'Middle East & North Africa (IDA & IBRD)', 'Middle East & North Africa (excluding high income)', 'Middle East and North Africa (WB)', 'Middle income', 'North America (WB)', 'Northern Mariana Islands', 'Other small states', 'Pacific island small states', 'Pre-demographic dividend', 'Saint Pierre and Miquelon', 'Small states', 'South Asia', 'South Asia (IDA & IBRD)', 'South Asia (WB)', 'Southern and Eastern Africa (WB)', 'Sub-Saharan Africa', 'Sub-Saharan Africa (IDA & IBRD)', 'Sub-Saharan Africa (WB)', 'Sub-Saharan Africa (excluding high income)', 'Upper middle income', 'Upper-middle-income countries', 'Virgin Islands', 'Western and Central Africa (WB)', 'World']
    literacy = literacy[~literacy['Entity'].isin(repeated_geographies)] 

    # ELIMINACIÓN DE LA COLUMNA "CODE"
    literacy.drop(columns=["Code"], inplace=True) 

    # TRADUCCIÓN Y REEMPLAZO DE LOS NOMBRES DE PAÍSES AL ESPAÑOL 
    country_translation_dict = {
        'Afghanistan': 'Afganistán', 'Albania': 'Albania', 'Algeria': 'Argelia', 'American Samoa': 'Samoa Americana', 'Andorra': 'Andorra', 'Angola': 'Angola',
        'Anguilla': 'Anguila', 'Antigua and Barbuda': 'Antigua y Barbuda', 'Argentina': 'Argentina', 'Armenia': 'Armenia', 'Aruba': 'Aruba',
        'Australia': 'Australia', 'Austria': 'Austria', 'Azerbaijan': 'Azerbaiyán', 'Bahamas': 'Bahamas', 'Bahrain': 'Baréin', 'Bangladesh': 'Bangladés',
        'Barbados': 'Barbados', 'Belarus': 'Bielorrusia', 'Belgium': 'Bélgica', 'Belize': 'Belice', 'Benin': 'Benín', 'Bermuda': 'Bermudas', 'Bhutan': 'Bután',
        'Bolivia': 'Bolivia', 'Bosnia and Herzegovina': 'Bosnia y Herzegovina', 'Botswana': 'Botsuana', 'Brazil': 'Brasil', 'Brunei': 'Brunéi',
        'Bulgaria': 'Bulgaria', 'Burkina Faso': 'Burkina Faso', 'Burundi': 'Burundi', 'Cambodia': 'Camboya', 'Cameroon': 'Camerún', 'Canada': 'Canadá',
        'Cape Verde': 'Cabo Verde', 'Cayman Islands': 'Islas Caimán', 'Central African Republic': 'República Centroafricana', 'Chad': 'Chad', 'Chile': 'Chile',
        'China': 'China', 'Colombia': 'Colombia', 'Comoros': 'Comoras', 'Congo': 'Congo', 'Cook Islands': 'Islas Cook', 'Costa Rica': 'Costa Rica',
        'Cote d\'Ivoire': 'Costa de Marfil', 'Croatia': 'Croacia', 'Cuba': 'Cuba', 'Cyprus': 'Chipre', 'Czechia': 'República Checa',
        'Democratic Republic of Congo': 'República Democrática del Congo', 'Denmark': 'Dinamarca', 'Djibouti': 'Yibuti', 'Dominica': 'Dominica',
        'Dominican Republic': 'República Dominicana', 'East Timor': 'Timor Oriental', 'Ecuador': 'Ecuador', 'Egypt': 'Egipto', 'El Salvador': 'El Salvador',
        'Equatorial Guinea': 'Guinea Ecuatorial', 'Eritrea': 'Eritrea', 'Estonia': 'Estonia', 'Eswatini': 'Esuatini', 'Ethiopia': 'Etiopía', 'Fiji': 'Fiyi',
        'Finland': 'Finlandia', 'France': 'Francia', 'French Polynesia': 'Polinesia Francesa', 'Gabon': 'Gabón', 'Gambia': 'Gambia', 'Georgia': 'Georgia',
        'Germany': 'Alemania', 'Ghana': 'Ghana', 'Gibraltar': 'Gibraltar', 'Greece': 'Grecia', 'Greenland': 'Groenlandia', 'Grenada': 'Granada', 'Guam': 'Guam',
        'Guatemala': 'Guatemala', 'Guinea': 'Guinea', 'Guinea-Bissau': 'Guinea-Bisáu', 'Guyana': 'Guyana', 'Haiti': 'Haití', 'Honduras': 'Honduras',
        'Hong Kong': 'Hong Kong', 'Hungary': 'Hungría', 'Iceland': 'Islandia', 'India': 'India', 'Indonesia': 'Indonesia', 'Iran': 'Irán', 'Iraq': 'Irak',
        'Ireland': 'Irlanda', 'Israel': 'Israel', 'Italy': 'Italia', 'Jamaica': 'Jamaica', 'Japan': 'Japón', 'Jordan': 'Jordania', 'Kazakhstan': 'Kazajistán',
        'Kenya': 'Kenia', 'Kiribati': 'Kiribati', 'Kosovo': 'Kosovo', 'Kuwait': 'Kuwait', 'Kyrgyzstan': 'Kirguistán', 'Laos': 'Laos', 'Latvia': 'Letonia',
        'Lebanon': 'Líbano', 'Lesotho': 'Lesoto', 'Liberia': 'Liberia', 'Libya': 'Libia', 'Liechtenstein': 'Liechtenstein', 'Lithuania': 'Lituania',
        'Luxembourg': 'Luxemburgo', 'Macao': 'Macao', 'Madagascar': 'Madagascar', 'Malawi': 'Malawi', 'Malaysia': 'Malasia', 'Maldives': 'Maldivas', 'Mali': 'Malí',
        'Malta': 'Malta', 'Marshall Islands': 'Islas Marshall', 'Mauritania': 'Mauritania', 'Mauritius': 'Mauricio', 'Mexico': 'México', 'Micronesia': 'Micronesia',
        'Moldova': 'Moldavia', 'Monaco': 'Mónaco', 'Mongolia': 'Mongolia', 'Montenegro': 'Montenegro', 'Montserrat': 'Montserrat', 'Morocco': 'Marruecos',
        'Mozambique': 'Mozambique', 'Myanmar': 'Birmania', 'Namibia': 'Namibia', 'Nepal': 'Nepal', 'Netherlands': 'Países Bajos', 'New Caledonia': 'Nueva Caledonia',
        'New Zealand': 'Nueva Zelanda', 'Nicaragua': 'Nicaragua', 'Niger': 'Níger', 'Nigeria': 'Nigeria', 'Niue': 'Niue', 'North Korea': 'Corea del Norte',
        'North Macedonia': 'Macedonia del Norte', 'Norway': 'Noruega', 'Oman': 'Omán', 'Pakistan': 'Pakistán', 'Palau': 'Palau', 'Palestine': 'Palestina', 'Panama': 'Panamá',
        'Papua New Guinea': 'Papúa Nueva Guinea', 'Paraguay': 'Paraguay', 'Peru': 'Perú', 'Philippines': 'Filipinas', 'Poland': 'Polonia', 'Portugal': 'Portugal',
        'Puerto Rico': 'Puerto Rico', 'Qatar': 'Catar', 'Romania': 'Rumanía', 'Russia': 'Rusia', 'Rwanda': 'Ruanda', 'Saint Helena': 'Santa Elena',
        'Saint Kitts and Nevis': 'San Cristóbal y Nieves', 'Saint Lucia': 'Santa Lucía', 'Saint Vincent and the Grenadines': 'San Vicente y las Granadinas',
        'Samoa': 'Samoa', 'San Marino': 'San Marino', 'Sao Tome and Principe': 'Santo Tomé y Príncipe', 'Saudi Arabia': 'Arabia Saudita', 'Senegal': 'Senegal',
        'Serbia': 'Serbia', 'Seychelles': 'Seychelles', 'Sierra Leone': 'Sierra Leona', 'Singapore': 'Singapur', 'Slovakia': 'Eslovaquia', 'Slovenia': 'Eslovenia',
        'Solomon Islands': 'Islas Salomón', 'Somalia': 'Somalia', 'South Africa': 'Sudáfrica', 'South Korea': 'Corea del Sur', 'South Sudan': 'Sudán del Sur',
        'Spain': 'España', 'Sri Lanka': 'Sri Lanka', 'Sudan': 'Sudán', 'Suriname': 'Surinam', 'Sweden': 'Suecia', 'Switzerland': 'Suiza', 'Syria': 'Siria',
        'Taiwan': 'Taiwán', 'Tajikistan': 'Tayikistán', 'Tanzania': 'Tanzania', 'Thailand': 'Tailandia', 'Togo': 'Togo', 'Tonga': 'Tonga',
        'Trinidad and Tobago': 'Trinidad y Tobago', 'Tunisia': 'Túnez', 'Turkey': 'Turquía', 'Turkmenistan': 'Turkmenistán',
        'Turks and Caicos Islands': 'Islas Turcas y Caicos', 'Uganda': 'Uganda', 'Ukraine': 'Ucrania', 'United Arab Emirates': 'Emiratos Árabes Unidos',
        'United Kingdom': 'Reino Unido', 'United States': 'Estados Unidos', 'Uruguay': 'Uruguay', 'Uzbekistan': 'Uzbekistán', 'Vanuatu': 'Vanuatu',
        'Vatican': 'Vaticano', 'Venezuela': 'Venezuela', 'Vietnam': 'Vietnam', 'Wallis and Futuna': 'Wallis y Futuna', 'Yemen': 'Yemen', 'Zambia': 'Zambia',
        'Zimbabwe': 'Zimbabue'
    }
    literacy['Entity'] = literacy['Entity'].replace(country_translation_dict) 

    # REEMPLAZO DE LOS NOMBRES DE LAS COLUMNAS POR NOMBRES EN ESPAÑOL
    literacy.columns = ['País', 'Año', 'Tasa de alfabetización']

    # NUEVA EXPLORACIÓN DE LITERACY PARA CHEQUEAR QUE ESTÉ LIMPIO 
    print(literacy.head(10000))
    print(literacy.info()) 

    for column in literacy.columns: 
        print(f"Columna: {column}")
        print(literacy[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 

    literacy.isna().sum()
 
    return literacy


# ---------------------- EXPLORACIÓN DE CHILD_MORTALITY ----------------------

def eda_child_mortality(child_mortality):
    '''
    Realiza el EDA ya explicado para child_mortality.
    '''
    
    print(child_mortality.head(10000)) 
    print(child_mortality.info()) 

    for column in child_mortality.columns: 
        print(f"Columna: {column}") 
        print(child_mortality[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 

    child_mortality.isna().sum() 

    # ELIMINACIÓN DE LAS FILAS DE GEOGRAFÍAS REPETIDAS 
    repeated_geographies = ['Africa', 'Australia and New Zealand', 'British Virgin Islands', 'Central Asia (SDG)', 'Central Asia and Southern Asia (SDG)', 'Eastern Asia (SDG)', 'Eastern Asia and South-Eastern Asia (SDG)', 'Europe', 'Europe (SDG)', 'European Union (27)', 'High-income countries', 'Landlocked developing countries (SDG)', 'Latin America and the Caribbean (SDG)', 'Least developed countries (SDG)', 'Low-income countries', 'Lower-middle-income countries', 'North America', 'Northern Africa (SDG)', 'Northern America (SDG)', 'Northern America and Europe (SDG)', 'Oceania', 'Oceania (SDG)', 'Oceania excluding Australia and New Zealand', 'Small island developing States (SDG)', 'South America', 'South-Eastern Asia (SDG)', 'Southern Asia (SDG)', 'Sub-Saharan Africa (SDG)', 'Upper-middle-income countries', 'Western Asia (SDG)', 'Western Asia and Northern Africa (SDG)', 'World']
    child_mortality = child_mortality[~child_mortality['Entity'].isin(repeated_geographies)] 

    # ELIMINACIÓN DE LA COLUMNA "CODE"
    child_mortality.drop(columns=['Code'], inplace=True) 

    # TRADUCCIÓN Y REEMPLAZO DE LOS NOMBRES DE PAÍSES AL ESPAÑOL
    country_translation_dict = {
        'Afghanistan': 'Afganistán', 'Albania': 'Albania', 'Algeria': 'Argelia', 'Andorra': 'Andorra', 'Angola': 'Angola',
        'Anguilla': 'Anguila', 'Antigua and Barbuda': 'Antigua y Barbuda', 'Argentina': 'Argentina', 'Armenia': 'Armenia',
        'Asia': 'Asia', 'Australia': 'Australia', 'Austria': 'Austria', 'Azerbaijan': 'Azerbaiyán', 'Bahamas': 'Bahamas',
        'Bahrain': 'Baréin', 'Bangladesh': 'Bangladesh', 'Barbados': 'Barbados', 'Belarus': 'Bielorrusia', 'Belgium': 'Bélgica',
        'Belize': 'Belice', 'Benin': 'Benín', 'Bhutan': 'Bután', 'Bolivia': 'Bolivia', 'Bosnia and Herzegovina': 'Bosnia y Herzegovina',
        'Botswana': 'Botsuana', 'Brazil': 'Brasil', 'Brunei': 'Brunéi', 'Bulgaria': 'Bulgaria', 'Burkina Faso': 'Burkina Faso',
        'Burundi': 'Burundi', 'Cambodia': 'Camboya', 'Cameroon': 'Camerún', 'Canada': 'Canadá', 'Cape Verde': 'Cabo Verde',
        'Central African Republic': 'República Centroafricana', 'Chad': 'Chad', 'Chile': 'Chile', 'China': 'China', 'Colombia': 'Colombia',
        'Comoros': 'Comoras', 'Congo': 'Congo', 'Cook Islands': 'Islas Cook', 'Costa Rica': 'Costa Rica', "Cote d'Ivoire": 'Costa de Marfil',
        'Croatia': 'Croacia', 'Cuba': 'Cuba', 'Cyprus': 'Chipre', 'Czechia': 'República Checa', 'Democratic Republic of Congo': 'República Democrática del Congo',
        'Denmark': 'Dinamarca', 'Djibouti': 'Yibuti', 'Dominica': 'Dominica', 'Dominican Republic': 'República Dominicana', 'East Timor': 'Timor Oriental',
        'Ecuador': 'Ecuador', 'Egypt': 'Egipto', 'El Salvador': 'El Salvador', 'Equatorial Guinea': 'Guinea Ecuatorial', 'Eritrea': 'Eritrea',
        'Estonia': 'Estonia', 'Eswatini': 'Eswatini', 'Ethiopia': 'Etiopía', 'Fiji': 'Fiyi', 'Finland': 'Finlandia', 'France': 'Francia',
        'Gabon': 'Gabón', 'Gambia': 'Gambia', 'Georgia': 'Georgia', 'Germany': 'Alemania', 'Ghana': 'Ghana', 'Greece': 'Grecia',
        'Grenada': 'Granada', 'Guatemala': 'Guatemala', 'Guinea': 'Guinea', 'Guinea-Bissau': 'Guinea-Bisáu', 'Guyana': 'Guyana', 'Haiti': 'Haití',
        'Honduras': 'Honduras', 'Hungary': 'Hungría', 'Iceland': 'Islandia', 'India': 'India', 'Indonesia': 'Indonesia', 'Iran': 'Irán',
        'Iraq': 'Irak', 'Ireland': 'Irlanda', 'Israel': 'Israel', 'Italy': 'Italia', 'Jamaica': 'Jamaica', 'Japan': 'Japón', 'Jordan': 'Jordania',
        'Kazakhstan': 'Kazajistán', 'Kenya': 'Kenia', 'Kiribati': 'Kiribati', 'Kosovo': 'Kosovo', 'Kuwait': 'Kuwait', 'Kyrgyzstan': 'Kirguistán',
        'Laos': 'Laos', 'Latvia': 'Letonia', 'Lebanon': 'Líbano', 'Lesotho': 'Lesoto', 'Liberia': 'Liberia', 'Libya': 'Libia', 'Lithuania': 'Lituania',
        'Luxembourg': 'Luxemburgo', 'Madagascar': 'Madagascar', 'Malawi': 'Malaui', 'Malaysia': 'Malasia', 'Maldives': 'Maldivas', 'Mali': 'Malí',
        'Malta': 'Malta', 'Marshall Islands': 'Islas Marshall', 'Mauritania': 'Mauritania', 'Mauritius': 'Mauricio', 'Mexico': 'México',
        'Micronesia (country)': 'Micronesia', 'Moldova': 'Moldavia', 'Monaco': 'Mónaco', 'Mongolia': 'Mongolia', 'Montenegro': 'Montenegro',
        'Montserrat': 'Montserrat', 'Morocco': 'Marruecos', 'Mozambique': 'Mozambique', 'Myanmar': 'Birmania', 'Namibia': 'Namibia', 'Nauru': 'Naurú',
        'Nepal': 'Nepal', 'Netherlands': 'Países Bajos', 'New Zealand': 'Nueva Zelanda', 'Nicaragua': 'Nicaragua', 'Niger': 'Níger', 'Nigeria': 'Nigeria',
        'Niue': 'Niue', 'North Korea': 'Corea del Norte', 'North Macedonia': 'Macedonia del Norte', 'Norway': 'Noruega', 'Oman': 'Omán', 'Pakistan': 'Pakistán',
        'Palau': 'Palau', 'Palestine': 'Palestina', 'Panama': 'Panamá', 'Papua New Guinea': 'Papúa Nueva Guinea', 'Paraguay': 'Paraguay', 'Peru': 'Perú',
        'Philippines': 'Filipinas', 'Poland': 'Polonia', 'Portugal': 'Portugal', 'Qatar': 'Catar', 'Romania': 'Rumanía', 'Russia': 'Rusia', 'Rwanda': 'Ruanda',
        'Saint Kitts and Nevis': 'San Cristóbal y Nieves', 'Saint Lucia': 'Santa Lucía', 'Saint Vincent and the Grenadines': 'San Vicente y las Granadinas',
        'Samoa': 'Samoa', 'San Marino': 'San Marino', 'Sao Tome and Principe': 'Santo Tomé y Príncipe', 'Saudi Arabia': 'Arabia Saudita', 'Senegal': 'Senegal',
        'Serbia': 'Serbia', 'Seychelles': 'Seychelles', 'Sierra Leone': 'Sierra Leona', 'Singapore': 'Singapur', 'Slovakia': 'Eslovaquia', 'Slovenia': 'Eslovenia',
        'Solomon Islands': 'Islas Salomón', 'Somalia': 'Somalia', 'South Africa': 'Sudáfrica', 'South Korea': 'Corea del Sur', 'South Sudan': 'Sudán del Sur',
        'Spain': 'España', 'Sri Lanka': 'Sri Lanka', 'Sudan': 'Sudán', 'Suriname': 'Surinam', 'Sweden': 'Suecia', 'Switzerland': 'Suiza', 'Syria': 'Siria',
        'Taiwan': 'Taiwán', 'Tajikistan': 'Tayikistán', 'Tanzania': 'Tanzania', 'Thailand': 'Tailandia', 'Togo': 'Togo', 'Tonga': 'Tonga',
        'Trinidad and Tobago': 'Trinidad y Tobago', 'Tunisia': 'Túnez', 'Turkey': 'Turquía', 'Turkmenistan': 'Turkmenistán', 'Turks and Caicos Islands': 'Islas Turcas y Caicos',
        'Tuvalu': 'Tuvalu', 'Uganda': 'Uganda', 'Ukraine': 'Ucrania', 'United Arab Emirates': 'Emiratos Árabes Unidos', 'United Kingdom': 'Reino Unido',
        'United States': 'Estados Unidos', 'Uruguay': 'Uruguay', 'Uzbekistan': 'Uzbekistán', 'Vanuatu': 'Vanuatu', 'Venezuela': 'Venezuela', 'Vietnam': 'Vietnam',
        'Yemen': 'Yemen', 'Zambia': 'Zambia', 'Zimbabwe': 'Zimbabue'
    }
    child_mortality['Entity'] = child_mortality['Entity'].replace(country_translation_dict) 

    # REEMPLAZO DE LOS NOMBRES DE LAS COLUMNAS POR NOMBRES EN ESPAÑOL
    child_mortality.columns= ['País', 'Año', 'Mortalidad infantil']

    # NUEVA EXPLORACIÓN DE CHILD_MORTALITY PARA CHEQUEAR QUE ESTÉ LIMPIO 
    print(child_mortality.head(10000)) 
    print(child_mortality.info()) 
    
    for column in child_mortality.columns: 
        print(f"Columna: {column}") 
        print(child_mortality[column].unique()) 
        print("-" * 40) # Separa entre columna y columna. 
    
    child_mortality.isna().sum() 

    return child_mortality