WEIGHT_KG = 80

DAILY_NUTRIMENT_RECOMMENDATION = {
    "vit_a_ug": 800,
    "vit_b1_mg": 1.1,
    "vit_b2_mg": 1.4,
    "vit_b3_mg": 16,
    "vit_b5_mg": 6,
    "vit_b6_mg": 1.4,
    "vit_b8_ug": 50,
    "vit_b9_ug": 200,
    "vit_b12_ug": 2.5,
    "vit_c_mg": 80,
    "vit_d_ug": 5,
    "vit_e_mg": 12,
    "vit_k_ug": 75,
    "calcium_mg": 800,
    "iron_mg": 14,
    "mg_mg": 375,
    "phosphore_mg": 700,
    "selenium_µg": 55,
    "zinc_mg": 10,
    "chlorure_mg": 800,
    "cu_mg": 1,
    "mn_mg": 2,
}

DAILY_ENERGY_RECOMMENDATION_KCAL = 1650
DAILY_PROT_G = WEIGHT_KG

DAILY_RECOMMENDATION = {
    **DAILY_NUTRIMENT_RECOMMENDATION,
    "energy_kcal": DAILY_ENERGY_RECOMMENDATION_KCAL,
    "prot_g": DAILY_PROT_G,
}
