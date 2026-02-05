import requests
import concurrent.futures
from typing import List, Dict, Any

class SecurityEnforcer:
    """Enforces Row-Level Security by injecting mandatory filters."""
    def __init__(self, user_context: Dict[str, Any]):
        self.permissions = user_context.get("scoped_departments", [])
        self.role = user_context.get("role", "USER")

    def apply_scope(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if self.role == "GLOBAL_ADMIN":
            return params
        # Inject department filter into the API parameters
        params["department"] = ",".join(self.permissions)
        return params

class UKGExecutionAgent:
    def __init__(self, base_url: str, api_key: str, auth_token: str, user_context: Dict[str, Any]):
        self.base_url = base_url
        self.headers = {
            "US-CUSTOMER-API-KEY": api_key,
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        self.enforcer = SecurityEnforcer(user_context)

    def get_department_financials(self, department: str) -> List[Dict]:
        # Step 1: Securely fetch IDs
        params = self.enforcer.apply_scope({"department": department})
        personnel_url = f"{self.base_url}/personnel/v1/person-details"
        response = requests.get(personnel_url, headers=self.headers, params=params)
        
        # FAIL LOUDLY: Ensure we don't proceed with bad data
        response.raise_for_status()
        employees = response.json()
        employee_ids = [emp['employeeId'] for emp in employees]

        # Step 2: Parallel Hydration
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self._fetch_comp, eid) for eid in employee_ids]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        return results

    def _fetch_comp(self, employee_id: str) -> Dict:
        url = f"{self.base_url}/personnel/v1/compensation-details/{employee_id}"
        return requests.get(url, headers=self.headers).json()