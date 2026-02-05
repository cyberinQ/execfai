import json
from core.ukg_agent import UKGExecutionAgent
from core.analyzer import AbsenceAnalyzer
import pandas as pd

class AnalyticalBridge:
    def __init__(self, ukg_config: dict, user_context: dict):
        """
        ukg_config: Contains base_url, api_key, auth_token
        user_context: Contains role and scoped_departments for RLS
        """
        self.agent = UKGExecutionAgent(
            ukg_config['base_url'], 
            ukg_config['api_key'], 
            ukg_config['auth_token'],
            user_context
        )
        self.user_context = user_context

    def route_query(self, intent_json: str):
        """
        Routes the LLM's parsed intent to the correct execution path.
        Example Intent: {"action": "analyze_absences", "department": "Sales"}
        """
        intent = json.loads(intent_json)
        action = intent.get("action")
        
        if action == "analyze_absences":
            return self._handle_absence_analysis(intent.get("department"))
        elif action == "get_financials":
            return self.agent.get_department_financials(intent.get("department"))
        else:
            return {"error": "Intent not recognized by the Analytical Fabric."}

    def _handle_absence_analysis(self, department: str):
        # Fetch raw data via the agent
        raw_data = self.agent.get_department_financials(department)
        
        if not raw_data:
            return {"detected_patterns": ["No data retrieved for this department."]}

        df = pd.DataFrame(raw_data)
        
        # ALIGNMENT: The UKG API uses 'employeeId', but the Analyzer expects 'employee_id'
        if 'employeeId' in df.columns and 'employee_id' not in df.columns:
            df = df.rename(columns={'employeeId': 'employee_id'})
            
        # Defensive Check: Ensure required columns exist
        if 'date' not in df.columns:
            return {"error": "Retrieved data missing required 'date' field for analysis."}
            
        analyzer = AbsenceAnalyzer(df)
        return analyzer.detect_patterns()