import numpy as np
import pandas as pd
from nutri_checker.data.ajr import DAILY_RECOMMENDATION
from nutri_checker.data.loader import COLUMNS_QUANTI
from nutri_checker.search.bm25 import NutriIndex

class SupplementFinder:
    def __init__(self, food_df: pd.DataFrame, drop_nan_threshold: int = 3, raw_food_only: bool = True):
        if raw_food_only:
            food_df = food_df.copy()[food_df["raw_food"]]
        nan_counts = food_df.isna().sum(axis=1)
        self.food_df = food_df[nan_counts < drop_nan_threshold].set_index("name_fr")[COLUMNS_QUANTI]
        self.food_ajr_df = self.food_df.div(pd.Series(DAILY_RECOMMENDATION)).dropna(axis=1, how="all")
        self.food_ajr_profile = self.food_ajr_df.div(self.food_ajr_df.max(axis=1), axis=0)
        
    def retrieve_supplement_for_needs_ajr_pct(self, needs_ajr_pct: pd.Series):
        needs_profile = needs_ajr_pct.clip(upper=1.0) / needs_ajr_pct.clip(upper=1.0).max()
        lack_profiles = needs_profile - self.food_ajr_profile
        lack_profiles_scores = self._compute_lack_profile_scores(lack_profiles)
        best_supplement_profile = lack_profiles_scores.nlargest(1, "score").iloc[0]
        best_supplement_ajr = self.food_ajr_df[best_supplement_profile.name]
        opt_quantity = self._compute_optimal_quantity_of_supplement_knowing_needs(best_supplement_ajr, needs_ajr_pct)
        return best_supplement_ajr, opt_quantity
        
        
    def _compute_lack_profile_scores(self, lack_profiles: pd.DataFrame) -> pd.DataFrame:
        return lack_profiles.apply(lambda row: -self._loss_fn(row), axis=1).to_frame(name="score")
    
    @staticmethod
    def _loss_fn(row: pd.Series, seek_low_energy:  bool = True, overflow_tol: int = 2) -> float:
        nutri_row = row.copy()
        # treat energy - highest lack is the best
        energy_loss = 0.0
        if seek_low_energy:
            energy_lack = nutri_row.pop("energy_kcal")
            energy_loss = 0.0 if np.isnan(energy_lack) else - 1.0 * energy_lack
            
        # rest of nutriments
        nutri_discrepancy = nutri_row.to_numpy() if overflow_tol == 0 else np.where(nutri_row < 0, -nutri_row/overflow_tol, nutri_row) 
        nutri_loss = np.nansum(np.power(nutri_discrepancy, 2))
        
        return energy_loss + nutri_loss
    
    @staticmethod
    def _compute_optimal_quantity_of_supplement_knowing_needs(best_supplement_ajr, needs_ajr_pct):
        """Solve every linear equation about 'what quantity supplement should have to fullfill the need in nutriment N ?'"""
        opt_qt = (needs_ajr_pct/best_supplement_ajr.fillna(0)).quantile(0.1)
        return opt_qt