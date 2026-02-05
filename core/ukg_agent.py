import requests
import concurrent.futures
from typing import List, Dict

class UKGExecutionAgent:
    def __init__(self, base_url: str, api_key: str, auth_token: str):
        self.base_url = base_url
        self.headers = {
            "US-CUSTOMER-API-KEY": api_key,
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    def get_department_financials(self, department: str) -> List[Dict]:
        """
        Answering: 'What is the salary spend for [Department]?'
        Requires a two-step join: Personnel -> Compensation.
        """
        # STEP 1: Get Employee IDs for the department
        personnel_url = f"{self.base_url}/personnel/v1/person-details?department={department}"
        employees = requests.get(personnel_url, headers=self.headers).json()
        
        # Row-Level Security: Filter out any IDs the user isn't allowed to see
        # (This would call your SecurityEnforcer here)
        employee_ids = [emp['employeeId'] for emp in employees]

        # STEP 2: Hydrate with Compensation data in parallel
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_comp = {
                executor.submit(self._fetch_comp, eid): eid for eid in employee_ids
            }
            for future in concurrent.futures.as_completed(future_to_comp):
                results.append(future.result())
        
        return results

    def _fetch_comp(self, employee_id: str) -> Dict:
        url = f"{self.base_url}/personnel/v1/compensation-details/{employee_id}"
        return requests.get(url, headers=self.headers).json()

# Example usage for the POC
# agent = UKGExecutionAgent(base_url="https://tenant123.ultipro.com", api_key="KEY", auth_token="TOKEN")
# data = agent.get_department_financials("Engineering")