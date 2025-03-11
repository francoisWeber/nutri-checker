from dataclasses import dataclass, asdict
from loguru import logger
import pandas as pd
from nutri_checker.data.loader import COLUMNS_QUANTI, COLUMNS_QUALI
from nutri_checker.search.bm25 import NutriIndex
from uuid import uuid4
from typing import List


@dataclass
class Aliment:
    grp_name_fr: str
    ssgrp_name_fr: str
    ssssgrp_name_fr: str
    name_fr: str
    grp_code: int
    ssgrp_code: int
    ssssgrp_code: int
    code: int
    # spec
    energy_kcal: float
    water_g: float
    prot_g: float
    glucid_g: float
    lipid_g: float
    sugar_g: float
    sugar_fructose_g: float
    sugar_galactose_g: float
    sugar_glucose_g: float
    sugar_lactose_g: float
    sugar_maltose_g: float
    sugar_saccharose_g: float
    amidon_g: float
    fiber_g: float
    alcool_g: float
    acid_sat_g: float
    acid_monoinsat_g: float
    acid_polyinsat_g: float
    cholesterol_g: float
    salt_g: float
    calcium_mg: float
    iron_mg: float
    mg_mg: float
    vit_a_ug: float
    vit_d_ug: float
    vit_e_mg: float
    vit_k1_ug: float
    vit_k2_ug: float
    vit_c_mg: float
    vit_b1_mg: float
    vit_b2_mg: float
    vit_b3_mg: float
    vit_b5_mg: float
    vit_b6_mg: float
    vit_b9_ug: float
    vit_b12_ug: float
    sodium_mg: float
    phosphore_mg: float
    selenium_ug: float
    zinc_mg: float
    chlorure_mg: float
    cu_mg: float
    mn_mg: float
    # technical
    raw_food: bool

    def __post_init__(self):
        if not self.raw_food:
            logger.warning(f"Aliment {self.name_fr} is not raw food")
        self._id = str(uuid4())

    @classmethod
    def from_row(cls, row):
        return cls(**row.to_dict())

    @classmethod
    def from_name_in_nutridata(cls, name: str, nutri_index: NutriIndex):
        if not any(cook_mode in name.lower() for cook_mode in ["cuit", "cuite", "cuisiné", "cuisinée"]):
            name = name + " " + "cru"

        aliment = nutri_index.retrieve(name, k=1).iloc[0].to_dict()
        return cls(**aliment)

    def get_nutritive_spec(self) -> pd.Series:
        return pd.Series(asdict(self))


@dataclass
class Ingredient:
    aliment: Aliment
    quantity_g: float

    def __post_init__(self):
        self._id = str(uuid4())

    def get_nutritive_spec(self) -> pd.Series:
        nutritive_unit_row = self.aliment.get_nutritive_spec()
        return pd.concat([nutritive_unit_row[COLUMNS_QUALI], nutritive_unit_row[COLUMNS_QUANTI] * self.quantity_g])



class Dish:
    def __init__(self, name: str | None = None, ingredients: List[Ingredient] = [], total_weight_g: int | None = None, already_taken_g: int=0):
        self.name = name
        self.ingredients = ingredients
        self.total_weight_g = total_weight_g
        self.already_taken_g = already_taken_g

        self._id = str(uuid4())

    def get_total_weight_g(self):
        return self.total_weight_g if self.total_weight_g else sum(ing.quantity_g for ing in self.ingredients)

    @property
    def final_weight_g(self):
        return self.get_total_weight_g()

    def __str__(self):
        return f"{self.name} ({len(self.ingredients)} ingredients)"

    def __repr__(self):
        return f"{self.name} ({len(self.ingredients)} ingredients)"

    def get_portion(self, portion_g):
        fraction = portion_g / self.get_total_weight_g()
        return Dish(
            self.name,
            [Ingredient(ing.aliment, ing.quantity_g * fraction) for ing in self.ingredients],
            total_weight_g=portion_g,
        )

    def get_nutri(self):
        return pd.DataFrame(data=[ing.get_nutritive_spec() for ing in self.ingredients])
