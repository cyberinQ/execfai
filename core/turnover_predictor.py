import pandas as pd

class TurnoverPredictor:
    def __init__(self, df):
        """
        Expects df with columns: ['employee_id', 'annualSalary', 'department']
        """
        self.df = df

    def predict_flight_risk(self):
        """
        Identifies employees with a salary 20% or more below their department average.
        """
        if self.df.empty:
            return []

        # Calculate department averages
        dept_avgs = self.df.groupby('department')['annualSalary'].transform('mean')
        self.df['salary_ratio'] = self.df['annualSalary'] / dept_avgs
        
        # Identify high-risk employees
        risks = self.df[self.df['salary_ratio'] <= 0.8]
        
        return risks[['employee_id', 'annualSalary', 'salary_ratio']].to_dict(orient='records')