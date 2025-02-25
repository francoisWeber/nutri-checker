import pandas as pd


DEFAULT_TABLE = "data/table_Ciqual_2020_FR_20200707.xls"

COLUMNS_TO_DROP = [
    "alim_nom_sci",
    "Energie, Règlement UE N° 1169/2011 (kJ/100 g)",
    "Energie, N x facteur Jones, avec fibres  (kJ/100 g)",
    "Protéines, N x facteur de Jones (g/100 g)",
    "Polyols totaux (g/100 g)",
    "Cendres (g/100 g)",
    "AG 4:0, butyrique (g/100 g)",
    "AG 6:0, caproïque (g/100 g)",
    "AG 8:0, caprylique (g/100 g)",
    "AG 10:0, caprique (g/100 g)",
    "AG 12:0, laurique (g/100 g)",
    "AG 14:0, myristique (g/100 g)",
    "AG 16:0, palmitique (g/100 g)",
    "AG 18:0, stéarique (g/100 g)",
    "AG 18:1 9c (n-9), oléique (g/100 g)",
    "AG 18:2 9c,12c (n-6), linoléique (g/100 g)",
    "AG 18:3 c9,c12,c15 (n-3), alpha-linolénique (g/100 g)",
    "AG 20:4 5c,8c,11c,14c (n-6), arachidonique (g/100 g)",
    "AG 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100 g)",
    "AG 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100 g)",
    "Acides organiques (g/100 g)",
    "Chlorure (mg/100 g)",
    "Cuivre (mg/100 g)",
    "Iode (µg/100 g)",
    "Phosphore (mg/100 g)",
    "Manganèse (mg/100 g)",
    "Potassium (mg/100 g)",
    "Beta-Carotène (µg/100 g)",
    "Sélénium (µg/100 g)",
    "Sodium (mg/100 g)",
    "Zinc (mg/100 g)",
    "Energie, N x facteur Jones, avec fibres  (kcal/100 g)",
]
COLUMNS_RENAMER = {
    "alim_grp_code": "grp_code",
    "alim_ssgrp_code": "ssgrp_code",
    "alim_ssssgrp_code": "ssssgrp_code",
    "alim_grp_nom_fr": "grp_name_fr",
    "alim_ssgrp_nom_fr": "ssgrp_name_fr",
    "alim_ssssgrp_nom_fr": "ssssgrp_name_fr",
    "alim_code": "code",
    "alim_nom_fr": "name_fr",
    "Energie, Règlement UE N° 1169/2011 (kcal/100 g)": "energy_kcal",
    "Eau (g/100 g)": "water_g",
    "Protéines, N x 6.25 (g/100 g)": "prot_g",
    "Glucides (g/100 g)": "glucid_g",
    "Lipides (g/100 g)": "lipid_g",
    "Sucres (g/100 g)": "sugar_g",
    "Fructose (g/100 g)": "sugar_fructose_g",
    "Galactose (g/100 g)": "sugar_galactose_g",
    "Glucose (g/100 g)": "sugar_glucose_g",
    "Lactose (g/100 g)": "sugar_lactose_g",
    "Maltose (g/100 g)": "sugar_maltose_g",
    "Saccharose (g/100 g)": "sugar_saccharose_g",
    "Amidon (g/100 g)": "amidon_g",
    "Fibres alimentaires (g/100 g)": "fiber_g",
    "Alcool (g/100 g)": "alcool_g",
    "AG saturés (g/100 g)": "acid_sat_g",
    "AG monoinsaturés (g/100 g)": "acid_monoinsat_g",
    "AG polyinsaturés (g/100 g)": "acid_polyinsat_g",
    "Cholestérol (mg/100 g)": "cholesterol_g",
    "Sel chlorure de sodium (g/100 g)": "salt_g",
    "Calcium (mg/100 g)": "calcium_g",
    "Fer (mg/100 g)": "iron_mg",
    "Magnésium (mg/100 g)": "mg_mg",
    "Rétinol (µg/100 g)": "vit_a_ug",
    "Vitamine D (µg/100 g)": "vit_d_ug",
    "Vitamine E (mg/100 g)": "vit_e_ug",
    "Vitamine K1 (µg/100 g)": "vit_k1_ug",
    "Vitamine K2 (µg/100 g)": "vit_k2_ug",
    "Vitamine C (mg/100 g)": "vit_c_mg",
    "Vitamine B1 ou Thiamine (mg/100 g)": "vit_b1_mg",
    "Vitamine B2 ou Riboflavine (mg/100 g)": "vit_b2_mg",
    "Vitamine B3 ou PP ou Niacine (mg/100 g)": "vit_b3_mg",
    "Vitamine B5 ou Acide pantothénique (mg/100 g)": "vit_b5_mg",
    "Vitamine B6 (mg/100 g)": "vit_b6_mg",
    "Vitamine B9 ou Folates totaux (µg/100 g)": "vit_b9_ug",
    "Vitamine B12 (µg/100 g)": "vit_b12_ug",
}

COLUMNS_STRINGS = [
    "grp_name_fr",
    "ssgrp_name_fr",
    "ssssgrp_name_fr",
    "name_fr",
]

COLUMNS_QUALI_NON_STRINGS = [
    "grp_code",
    "ssgrp_code",
    "ssssgrp_code",
    "code",
]

COLUMNS_QUALI = COLUMNS_STRINGS + COLUMNS_QUALI_NON_STRINGS

COLUMNS_QUANTI = [
    "energy_kcal",
    "water_g",
    "prot_g",
    "glucid_g",
    "lipid_g",
    "sugar_g",
    "sugar_fructose_g",
    "sugar_galactose_g",
    "sugar_glucose_g",
    "sugar_lactose_g",
    "sugar_maltose_g",
    "sugar_saccharose_g",
    "amidon_g",
    "fiber_g",
    "alcool_g",
    "acid_sat_g",
    "acid_monoinsat_g",
    "acid_polyinsat_g",
    "cholesterol_g",
    "salt_g",
    "calcium_g",
    "iron_mg",
    "mg_mg",
    "vit_a_ug",
    "vit_d_ug",
    "vit_e_ug",
    "vit_k1_ug",
    "vit_k2_ug",
    "vit_c_mg",
    "vit_b1_mg",
    "vit_b2_mg",
    "vit_b3_mg",
    "vit_b5_mg",
    "vit_b6_mg",
    "vit_b9_ug",
    "vit_b12_ug",
]

FINAL_COLUMNS = COLUMNS_QUALI + COLUMNS_QUANTI


def load_nutri_data(table_path: str = DEFAULT_TABLE):
    data = pd.read_excel(table_path)
    data = columns_filter_and_rename(data)
    data = normalize_quanti_and_quali_columns(data)
    data = add_features(data)
    data = restore_missing_information(data)
    return data.reset_index(drop=True)


def columns_filter_and_rename(data: pd.DataFrame) -> pd.DataFrame:
    data.drop(columns=COLUMNS_TO_DROP, inplace=True)
    data.rename(columns=COLUMNS_RENAMER, inplace=True)
    return data


def add_features(data: pd.DataFrame) -> pd.DataFrame:
    return data.assign(raw_food=data.grp_code.isin([10, 2, 3, 4, 6, 8, 10]))


def normalize_quanti_and_quali_columns(data: pd.DataFrame) -> pd.DataFrame:
    df_quali = data[COLUMNS_QUALI]
    df_quanti = data[COLUMNS_QUANTI]
    return pd.concat(
        [normalize_quali_columns(df_quali), normalize_quanti_columns(df_quanti)], axis=1
    )


def normalize_quanti_columns(df_quanti: pd.DataFrame) -> pd.DataFrame:
    df_quanti = df_quanti.map(lambda x: str(x).replace(",", "."))
    df_quanti = df_quanti.map(lambda x: 0 if "<" in x else x)
    df_quanti = df_quanti.replace("Traces", 0)
    df_quanti = df_quanti.replace("traces", 0)
    df_quanti = df_quanti.replace("-", 0)
    df_quanti = df_quanti.astype(float)
    return df_quanti


def normalize_quali_columns(df_quali: pd.DataFrame) -> pd.DataFrame:
    df_quali_str = df_quali[COLUMNS_STRINGS]
    df_quali_nonstr = df_quali[COLUMNS_QUALI_NON_STRINGS]
    df_quali_str = df_quali_str.fillna("").map(lambda x: x.lower())
    return pd.concat([df_quali_str, df_quali_nonstr], axis=1)


SUGAR_AVG_KCAL_PER_G = 375 / 100

def restore_missing_information(data: pd.DataFrame) -> pd.DataFrame:
    data = restore_missing_kcal_from_sugar(data)
    return data

def restore_missing_kcal_from_sugar(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[data["energy_kcal"] == 0, "energy_kcal"] = data.loc[data["energy_kcal"] == 0, "sugar_g"] * SUGAR_AVG_KCAL_PER_G
    return data