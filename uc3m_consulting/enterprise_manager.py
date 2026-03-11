"""Module for enterprise_manager """

# import json
# import os
import re
from datetime import datetime
# from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str) -> bool:
        """Validate basic structure of a Spanish CIF"""

        if not isinstance(cif, str):
            return False

        if len(cif) != 9:
            return False

        if not cif[0].isalpha():
            return False

        if not cif[1:8].isdigit():
            return False

        if not cif[8].isalnum():
            return False

        return True

    def register_project(
            self,
            company_cif: str,
            project_acronym: str,
            operation_name: str,
            department: str,
            date: str,
            budget: float):

        """Register a new enterprise project."""
        # CM-FR-01-I1 company_cif
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid CIF")

        # CM-FR-01-I2 project_acronym
        if not isinstance(project_acronym, str):
            raise EnterpriseManagementException("Invalid project acronym")

        if not 5 <= len(project_acronym) <= 10:
            raise EnterpriseManagementException("Invalid project acronym length")

        if not re.fullmatch(r"[A-Z0-9]+", project_acronym):
            raise EnterpriseManagementException("Invalid project acronym characters")

        # CM-FR-01-I3 operation_name
        if not isinstance(operation_name, str):
            raise EnterpriseManagementException("Invalid operation name")

        if not 10 <= len(operation_name) <= 30:
            raise EnterpriseManagementException("Invalid operation name length")

        # CM-FR-01-I4 department
        if not isinstance(department, str):
            raise EnterpriseManagementException("Invalid department type")

        valid_departments = ["HR", "FINANCE", "LEGAL", "LOGISTICS"]

        if department not in valid_departments:
            raise EnterpriseManagementException("Invalid department")

        # CM-FR-01-I5 date (DD/MM/YY)

        if not isinstance(date, str):
            raise EnterpriseManagementException("Invalid date")

        try:
            parsed_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise EnterpriseManagementException("Invalid date format") from None

        if not 2025 <= parsed_date.year <= 2027:
            raise EnterpriseManagementException("Invalid year")

        # CM-FR-01-I6 budget

        if not isinstance(budget, float):
            raise EnterpriseManagementException("Invalid budget type")

        if not 50000.00 <= budget <= 1000000.00:
            raise EnterpriseManagementException("Budget out of range")

        if round(budget, 2) != budget:
            raise EnterpriseManagementException("Budget must have 2 decimals")
