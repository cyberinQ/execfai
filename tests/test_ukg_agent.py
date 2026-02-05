import unittest
from core.ukg_agent import SecurityEnforcer

class TestSecurity(unittest.TestCase):
    def test_enforcer_injects_department(self):
        user_ctx = {"role": "DEPT_HEAD", "scoped_departments": ["Engineering"]}
        enforcer = SecurityEnforcer(user_ctx)
        params = enforcer.apply_scope({"other_param": "test"})
        
        self.assertEqual(params["department"], "Engineering")

    def test_admin_bypass(self):
        user_ctx = {"role": "GLOBAL_ADMIN"}
        enforcer = SecurityEnforcer(user_ctx)
        params = enforcer.apply_scope({"other_param": "test"})
        
        self.assertNotIn("department", params)

if __name__ == '__main__':
    unittest.main()