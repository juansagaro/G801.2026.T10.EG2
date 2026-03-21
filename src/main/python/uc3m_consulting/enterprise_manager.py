"""Module """
from .enterprise_management_exception import EnterpriseManagementException

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(_: str):
        """Returns True if CIF is valid"""
        return True

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
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

    def register_document(self, input_file: str):
        """Registers a document associated to a project"""

    def check_project_budget(self, project_id: str):
        """Calculates the balance of a project"""
