import pandas as pd
from typing import Tuple, List

class WaterQualityEvaluator:
    def __init__(self, ph_range: Tuple[float, float] = (6.5, 8.5), turbidity_threshold: float = 1.0):
        # store min and max for easy access
        self.ph_min, self.ph_max = ph_range
        self.turbidity_threshold = turbidity_threshold

    def is_safe(self, row: pd.Series) -> Tuple[bool, str]:

        reasons: List[str] = []

        ph = row.get('ph')
        turbidity = row.get('turbidity')

        # pH checks
        if pd.isna(ph):
            reasons.append('missing pH')
        else:
            if ph < self.ph_min:
                reasons.append('pH too low')
            elif ph > self.ph_max:
                    reasons.append('pH too high')

        # Turbidity checks
        if pd.isna(turbidity):
            reasons.append('missing turbidity')
        else:
            if turbidity > self.turbidity_threshold:
                reasons.append('turbidity too high')

        is_safe = len(reasons) == 0
        reason_text = '' if is_safe else '; '.join(reasons)
        return is_safe, reason_text

    def evaluate_all(self, df: pd.DataFrame) -> pd.DataFrame:
        is_safe_list: List[bool] = []
        reason_list: List[str] = []
        for _, row in df.iterrows():
            safe, reason = self.is_safe(row)
            is_safe_list.append(safe)
            reason_list.append(reason)

        return pd.DataFrame({
            'is_safe': is_safe_list,
            'reason': reason_list
        }, index=df.index)
