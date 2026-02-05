import unittest
import pandas as pd
from core.analyzer import AbsenceAnalyzer

class TestAbsenceAnalyzer(unittest.TestCase):
    def test_monday_friday_pattern(self):
        # Sample data where all absences are on Mondays
        data = pd.DataFrame({
            'employee_id': ['EMP1'] * 3,
            'date': ['2025-01-06', '2025-01-13', '2025-01-20'], # All Mondays
            'pay_code_desc': ['Sick'] * 3
        })
        analyzer = AbsenceAnalyzer(data)
        results = analyzer.detect_patterns()
        
        # Verify the pattern was detected
        self.assertTrue(any("High concentration" in p for p in results['detected_patterns']))

if __name__ == '__main__':
    unittest.main()