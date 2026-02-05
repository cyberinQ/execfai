import unittest
from unittest.mock import patch, MagicMock
from core.ukg_agent import SecurityEnforcer, UKGExecutionAgent

class TestUKGAgent(unittest.TestCase):
    def setUp(self):
        self.ctx = {"role": "DEPT_HEAD", "scoped_departments": ["Engineering"]}
        self.agent = UKGExecutionAgent("https://test.com", "key", "token", self.ctx)

    def test_admin_bypass(self):
        """Line 13: Triggers the GLOBAL_ADMIN branch."""
        admin_ctx = {"role": "GLOBAL_ADMIN"}
        enforcer = SecurityEnforcer(admin_ctx)
        params = enforcer.apply_scope({"test": "data"})
        self.assertEqual(params, {"test": "data"})
        self.assertNotIn("department", params)

    def test_security_enforcer(self):
        enforcer = SecurityEnforcer(self.ctx)
        params = enforcer.apply_scope({})
        self.assertEqual(params["department"], "Engineering")

    @patch('requests.get')
    def test_get_department_financials(self, mock_get):
        # Mock Personnel Response
        mock_personnel = MagicMock()
        mock_personnel.json.return_value = [{"employeeId": "EEID1"}]
        mock_personnel.status_code = 200
        
        # Mock Compensation Response
        mock_comp = MagicMock()
        mock_comp.json.return_value = {"annualSalary": 100000}
        
        mock_get.side_effect = [mock_personnel, mock_comp]

        results = self.agent.get_department_financials("Engineering")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["annualSalary"], 100000)

if __name__ == '__main__':
    unittest.main()