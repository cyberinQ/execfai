import unittest
import pandas as pd
from core.analyzer import AbsenceAnalyzer

class TestAbsenceAnalyzer(unittest.TestCase):
    def test_patterns_and_main(self):
        data = pd.DataFrame({
            'employee_id': ['EMP1']*5,
            'date': ['2025-01-06', '2025-01-13', '2025-01-20', '2025-02-03', '2025-02-10'],
            'pay_code_desc': ['Sick']*5
        })
        analyzer = AbsenceAnalyzer(data)
        results = analyzer.detect_patterns()
        self.assertTrue(any("Monday" in p for p in results['detected_patterns']))

    def test_weekend_adjacency(self):
        data = pd.DataFrame({
            'employee_id': ['EMP1']*2,
            'date': ['2025-01-06', '2025-01-10'],
            'pay_code_desc': ['Sick']*2
        })
        analyzer = AbsenceAnalyzer(data)
        results = analyzer.detect_patterns()
        self.assertTrue(any("60%+" in p for p in results['detected_patterns']))

    def test_payday_proximity(self):
        """Verify detection of absences near paydays."""
        paydays = ['2025-01-15', '2025-01-31']
        data = pd.DataFrame({
            'employee_id': ['EMP1', 'EMP1'],
            'date': ['2025-01-14', '2025-01-16'], # Both within 1 day of Jan 15
            'pay_code_desc': ['Sick', 'Sick']
        })
        analyzer = AbsenceAnalyzer(data)
        results = analyzer.detect_patterns(payday_dates=paydays)
        self.assertTrue(any("Payday Proximity" in p for p in results['detected_patterns']))
    
    def test_empty_data(self):
        """Line 30: Triggers the total_absences == 0 branch."""
        empty_data = pd.DataFrame(columns=['employee_id', 'date', 'pay_code_desc'])
        analyzer = AbsenceAnalyzer(empty_data)
        results = analyzer.detect_patterns()
        self.assertEqual(results['detected_patterns'], ["No data available."])

if __name__ == '__main__':
    unittest.main()