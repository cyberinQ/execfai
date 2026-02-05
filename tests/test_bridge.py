import unittest
import json
from unittest.mock import MagicMock, patch
from ai_studio.bridge import AnalyticalBridge

class TestAnalyticalBridge(unittest.TestCase):
    def setUp(self):
        self.config = {
            'base_url': 'https://test.ultipro.com',
            'api_key': 'test_key',
            'auth_token': 'test_token'
        }
        self.user_ctx = {
            'role': 'DEPT_HEAD',
            'scoped_departments': ['Engineering']
        }
        self.bridge = AnalyticalBridge(self.config, self.user_ctx)

    @patch('core.ukg_agent.UKGExecutionAgent.get_department_financials')
    def test_route_get_financials(self, mock_financials):
        mock_financials.return_value = [{"annualSalary": 100000}]
        intent = json.dumps({"action": "get_financials", "department": "Engineering"})
        
        result = self.bridge.route_query(intent)
        self.assertEqual(result[0]["annualSalary"], 100000)

    @patch('core.ukg_agent.UKGExecutionAgent.get_department_financials')
    @patch('core.analyzer.AbsenceAnalyzer.detect_patterns')
    def test_route_analyze_absences(self, mock_detect, mock_financials):
        # FIX: Provide the 'date' column that AbsenceAnalyzer requires
        mock_financials.return_value = [
            {"employeeId": "EEID1", "date": "2025-01-06"},
            {"employeeId": "EEID1", "date": "2025-01-13"}
        ]
        mock_detect.return_value = {"detected_patterns": ["High concentration on Mondays"]}
        
        intent = json.dumps({"action": "analyze_absences", "department": "Engineering"})
        result = self.bridge.route_query(intent)
        self.assertIn("High concentration on Mondays", result["detected_patterns"])


    def test_route_unrecognized_intent(self):
        intent = json.dumps({"action": "invalid_action"})
        result = self.bridge.route_query(intent)
        self.assertIn("error", result)

if __name__ == '__main__':
    unittest.main()