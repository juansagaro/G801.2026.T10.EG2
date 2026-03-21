"""Module """
import re
from datetime import datetime
from .enterprise_management_exception import EnterpriseManagementException

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(_: str):
        """Returns True if CIF is valid"""
        return True

    @staticmethod
    def __validate_cif_algorithm(cif: str):
        """Validates the CIF control digit"""
        cif_letters = "JABCDEFGHI"
        digits = [int(d) for d in cif[1:8]]
        odd_sum = digits[0] + digits[2] + digits[4] + digits[6]
        even_sum = 0
        for d in digits[1::2]:
            double = d * 2
            even_sum += double if double < 10 else double - 9
        total = odd_sum + even_sum
        control_digit = (10 - (total % 10)) % 10
        control_char = cif_letters[control_digit]
        return cif[-1] in (str(control_digit), control_char)

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-branches
    def register_project(self, company_cif: str, project_acronym: str,
                         operation_name: str, department: str,
                         date: str, budget: float):
        """Registers a new project and returns its MD5 project_id"""

        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("CIF is not a valid string")

        if len(company_cif) != 9:
            raise EnterpriseManagementException("CIF length is not valid")

        if not company_cif[0].isalpha():
            raise EnterpriseManagementException("CIF must start with a letter")

        if not company_cif[1:8].isdigit():
            raise EnterpriseManagementException("Invalid CIF code")

        if not self.__validate_cif_algorithm(company_cif):
            raise EnterpriseManagementException("Invalid CIF code")

        if not isinstance(project_acronym, str):
            raise EnterpriseManagementException("project_acronym is not a valid string")

        if not 5 <= len(project_acronym) <= 10:
            raise EnterpriseManagementException("project_acronym length is not valid")

        if not project_acronym.isalnum() or not project_acronym.isupper():
            raise EnterpriseManagementException("project_acronym contains invalid characters")

        if not isinstance(operation_name, str):
            raise EnterpriseManagementException("operation_name is not a valid string")

        if not 10 <= len(operation_name) <= 30:
            raise EnterpriseManagementException("operation_name length is not valid")

        if not isinstance(department, str):
            raise EnterpriseManagementException("department is not a valid string")

        if department not in ("HR", "FINANCE", "LEGAL", "LOGISTICS"):
            raise EnterpriseManagementException("department value is not valid")

        if not isinstance(date, str):
            raise EnterpriseManagementException("date is not a valid string")

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", date):
            raise EnterpriseManagementException("date format is not valid")

        parts = date.split("/")
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])

        if not 1 <= day <= 31:
            raise EnterpriseManagementException("date day is not valid")

        if not 1 <= month <= 12:
            raise EnterpriseManagementException("date month is not valid")

        if not 2025 <= year <= 2027:
            raise EnterpriseManagementException("date year is not valid")

        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        except ValueError as exc:
            raise EnterpriseManagementException("date is not a valid date") from exc

        if date_obj < datetime.today().date():
            raise EnterpriseManagementException("date must be today or in the future")

    def register_document(self, input_file: str):
        """Registers a document associated to a project"""

    def check_project_budget(self, project_id: str):
        """Calculates the balance of a project"""
