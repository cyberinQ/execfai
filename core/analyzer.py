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

    def detect_patterns(self, payday_dates=None):
        """
        Detects anomalies including Day-of-Week concentration and Payday Proximity.
        payday_dates: List of strings ['YYYY-MM-DD']
        """
        patterns = []
        total_absences = len(self.df)
        if total_absences == 0:
            return {"dates": [], "detected_patterns": ["No data available."]}

        # 1. Day-of-Week Concentration
        dow_counts = self.df['day_of_week'].value_counts()
        for day, count in dow_counts.items():
            if count / total_absences >= 0.4:
                patterns.append(f"High concentration on {day}s ({count}/{total_absences}).")

        # 2. Weekend Adjacency
        weekend_adjacent = self.df[self.df['day_of_week'].isin(['Monday', 'Friday'])]
        if len(weekend_adjacent) / total_absences >= 0.6:
            patterns.append("Pattern detected: 60%+ of absences occur adjacent to weekends.")

        # 3. Payday Proximity (New Logic)
        if payday_dates:
            paydays = pd.to_datetime(payday_dates)
            proximity_count = 0
            for abs_date in self.df['date']:
                # Calculate absolute days from nearest payday
                days_diff = min(abs(paydays - abs_date)).days
                if days_diff <= 1:
                    proximity_count += 1
            
            if proximity_count / total_absences >= 0.4:
                patterns.append(f"Payday Proximity: {proximity_count}/{total_absences} absences occurred +/- 1 day of payday.")

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