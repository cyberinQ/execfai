"""
Author: Sunil Jain with Gemini
Role: Strategic Analyst / 90-day Operator
Function: Deterministic Absence Pattern Detection for UKG Data
"""

import pandas as pd
import numpy as np
from datetime import timedelta

class AbsenceAnalyzer:
    def __init__(self, df):
        """
        Expects df with columns: ['employee_id', 'date', 'pay_code_desc']
        'date' should be datetime objects.
        """
        self.df = df
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        self.df['is_weekend'] = self.df['date'].dt.dayofweek >= 5

    def detect_patterns(self):
        patterns = []
        
        # 1. Day-of-Week Concentration (e.g., "Monday/Friday Syndrome")
        dow_counts = self.df['day_of_week'].value_counts()
        total_absences = len(self.df)
        
        for day, count in dow_counts.items():
            if count / total_absences > 0.4:  # Threshold: 40% of absences on one day
                patterns.append(f"High concentration of absences on {day}s ({count}/{total_absences}).")

        # 2. Weekend Adjacency (Mondays or Fridays)
        weekend_adjacent = self.df[self.df['day_of_week'].isin(['Monday', 'Friday'])]
        if len(weekend_adjacent) / total_absences > 0.6:
            patterns.append("Pattern detected: 60%+ of absences occur adjacent to weekends.")

        # 3. Proximity to Payday or Holidays (Placeholder for logic)
        # Logic: if abs_date - holiday_date == 1 day...
        
        return {
            "dates": self.df['date'].dt.strftime('%Y-%m-%d').tolist(),
            "detected_patterns": patterns if patterns else ["No statistically significant patterns found."]
        }

# Use the pragma comment to tell the coverage reporter to ignore this block
if __name__ == "__main__":  # pragma: no cover
    sample_data = pd.DataFrame({
        'employee_id': ['EMP001']*5,
        'date': ['2025-01-06', '2025-01-13', '2025-01-20', '2025-02-03', '2025-02-05'],
        'pay_code_desc': ['Sick', 'Sick', 'Sick', 'Sick', 'Personal']
    })
    analyzer = AbsenceAnalyzer(sample_data)
    print(analyzer.detect_patterns())