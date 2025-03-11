WEIGHT_KG = 80

DAILY_ENERGY_RECOMMENDATION_KCAL = 1650
DAILY_ENERGY_RECOMMENDATION_MJ = 1650 * 1_000 * 4.18 / 1_000_000
DAILY_PROT_G = WEIGHT_KG

# https://www.anses.fr/fr/content/les-references-nutritionnelles-en-vitamines-et-mineraux
DAILY_NUTRIMENT_RECOMMENDATION = {
    "vit_a_ug": 750,
    "vit_b1_mg": 0.1 * DAILY_ENERGY_RECOMMENDATION_MJ,  # ANSES : 0.1mg/MJ absorbée. Donc pour 1650kcal = 6.7MJ
    "vit_b2_mg": 1.6,
    "vit_b3_mg": 1.6 * DAILY_ENERGY_RECOMMENDATION_MJ,  # ANSES : 1.6mg/MJ absorbée. Donc 1650kcal = 6.7MJ
    "vit_b5_mg": 5,
    "vit_b6_mg": 1.6,
    "vit_b8_ug": 40,
    "vit_b9_ug": 330,
    "vit_b12_ug": 4,
    "vit_c_mg": 110,
    "vit_d_ug": 15,
    "vit_e_mg": 10,
    "vit_k_ug": 79,
    "calcium_mg": 1000,
    "iron_mg": 11,
    "mg_mg": 375,
    "sodium_mg": 1500,
    "phosphore_mg": 550,
    "selenium_µg": 70,
    "zinc_mg": 10,
    "chlorure_mg": 2300,
    "cu_mg": 1.9,
    "mn_mg": 2,
}

DAILY_RECOMMENDATION = {
    **DAILY_NUTRIMENT_RECOMMENDATION,
    "energy_kcal": DAILY_ENERGY_RECOMMENDATION_KCAL,
    "prot_g": DAILY_PROT_G,
}
