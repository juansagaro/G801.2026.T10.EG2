"""Tests for the register_project function (Function 1)"""
import json
import os
import unittest
from pathlib import Path

from uc3m_consulting import EnterpriseManager
from uc3m_consulting import EnterpriseManagementException

# pylint: disable=too-many-public-methods
# pylint: disable=assignment-from-no-return
class TestRegisterProject(unittest.TestCase):
    """All test cases for register_project will be here"""

    __path_data = str(Path.home()) + "/PycharmProjects/G801.2026.T10.EG2/src/unittest/data/"
    __path_output = (str(Path.home()) +
                     "/PycharmProjects/G801.2026.T10.EG2/src/main/python/uc3m_consulting/data/")

    @classmethod
    def setUpClass(cls):
        """Opens and returns a variable with the JSON file test data"""
        try:
            with open(cls.__path_data + "f1_test_data.json",
                      encoding="UTF-8", mode="r") as json_file:
                cls.__f1_test_data = json.load(json_file)
                print("Data read is: " + str(cls.__f1_test_data))
        except FileNotFoundError as exc:
            raise EnterpriseManagementException("Wrong file or path") from exc
        except json.JSONDecodeError:
            cls.__f1_test_data = []

    def setUp(self):
        """Remove output JSON before each test to avoid side effects"""
        output_file = self.__path_output + "corporate_operations.json"
        if os.path.isfile(output_file):
            os.remove(output_file)

    def test_register_project_tc_f1_01(self):
        """TC-F1-01. Input is correct. Project_ID returned and JSON output stored."""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-01":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)
                patron_md5 = r"^[a-f0-9]{32}$"
                self.assertRegex(result.lower(), patron_md5,
                                 f"'{result}' not a valid MD5 code")
                output_file = self.__path_output + "corporate_operations.json"
                self.assertTrue(os.path.isfile(output_file))
                with open(output_file, encoding="UTF-8", mode="r") as f_out:
                    all_ops = json.load(f_out)
                found = any(op.get("project_id") == result for op in all_ops)
                self.assertTrue(found)

    def test_register_project_tc_f1_02(self):
        """TC-F1-02. CIF is not a valid string. Covers: CENV1"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-02":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "CIF is not a valid string")

    def test_register_project_tc_f1_03(self):
        """TC-F1-03. CIF length < 9. Covers: CENV3, VLNV1"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-03":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "CIF length is not valid")

    def test_register_project_tc_f1_04(self):
        """TC-F1-04. CIF length > 9. Covers: CENV4, VLNV2"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-04":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "CIF length is not valid")

    def test_register_project_tc_f1_05(self):
        """TC-F1-05. CIF length exactly 9 (valid boundary). Covers: VLV1"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-05":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_06(self):
        """TC-F1-06. CIF must start with a letter. Covers: CENV5"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-06":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "CIF must start with a letter")

    def test_register_project_tc_f1_07(self):
        """TC-F1-07. CIF digits 2-8 contain a letter. Covers: CENV6"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-07":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "Invalid CIF code")

    def test_register_project_tc_f1_08(self):
        """TC-F1-08. CIF control digit is incorrect. Covers: CENV2"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-08":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "Invalid CIF code")

    def test_register_project_tc_f1_09(self):
        """TC-F1-09. project_acronym is not a string. Covers: CENV7"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-09":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "project_acronym is not a valid string")

    def test_register_project_tc_f1_10(self):
        """TC-F1-10. project_acronym length < 5. Covers: CENV8, VLNV3"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-10":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "project_acronym length is not valid")

    def test_register_project_tc_f1_11(self):
        """TC-F1-11. project_acronym length > 10. Covers: CENV9, VLNV4"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-11":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "project_acronym length is not valid")

    def test_register_project_tc_f1_12(self):
        """TC-F1-12. project_acronym length exactly 5 (valid min). Covers: VLV2"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-12":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_13(self):
        """TC-F1-13. project_acronym length exactly 10 (valid max). Covers: VLV3"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-13":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_14(self):
        """TC-F1-14. project_acronym contains lowercase letters. Covers: CENV10"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-14":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "project_acronym contains invalid characters")

    def test_register_project_tc_f1_15(self):
        """TC-F1-15. project_acronym contains special characters. Covers: CENV10"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-15":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "project_acronym contains invalid characters")

    def test_register_project_tc_f1_16(self):
        """TC-F1-16. operation_name is not a string. Covers: CENV11"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-16":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "operation_name is not a valid string")

    def test_register_project_tc_f1_17(self):
        """TC-F1-17. operation_name length < 10. Covers: CENV12, VLNV5"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-17":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "operation_name length is not valid")

    def test_register_project_tc_f1_18(self):
        """TC-F1-18. operation_name length > 30. Covers: CENV13, VLNV6"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-18":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "operation_name length is not valid")

    def test_register_project_tc_f1_19(self):
        """TC-F1-19. operation_name length exactly 10 (valid min). Covers: VLV6"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-19":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_20(self):
        """TC-F1-20. operation_name length exactly 30 (valid max). Covers: VLV7"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-20":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_21(self):
        """TC-F1-21. department is not a string. Covers: CENV14"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-21":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "department is not a valid string")

    def test_register_project_tc_f1_22(self):
        """TC-F1-22. department value not allowed. Covers: CENV15"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-22":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "department value is not valid")

    def test_register_project_tc_f1_23(self):
        """TC-F1-23. department in lowercase. Covers: CENV15"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-23":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "department value is not valid")

    def test_register_project_tc_f1_24(self):
        """TC-F1-24. department = FINANCE (valid). Covers: CEV13"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-24":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_25(self):
        """TC-F1-25. department = LEGAL (valid). Covers: CEV14"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-25":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_26(self):
        """TC-F1-26. department = LOGISTICS (valid). Covers: CEV15"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-26":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_27(self):
        """TC-F1-27. date is not a string. Covers: CENV16"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-27":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date is not a valid string")

    def test_register_project_tc_f1_28(self):
        """TC-F1-28. date format is incorrect. Covers: CENV17"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-28":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date format is not valid")

    def test_register_project_tc_f1_29(self):
        """TC-F1-29. date DD = 00 (invalid). Covers: CENV18, VLNV7"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-29":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date day is not valid")

    def test_register_project_tc_f1_30(self):
        """TC-F1-30. date DD = 32 (invalid). Covers: CENV19, VLNV8"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-30":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date day is not valid")

    def test_register_project_tc_f1_31(self):
        """TC-F1-31. date DD = 01 (valid min). Covers: VLV10"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-31":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_32(self):
        """TC-F1-32. date DD = 31 (valid max). Covers: VLV11"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-32":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_33(self):
        """TC-F1-33. date MM = 00 (invalid). Covers: CENV20, VLNV9"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-33":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date month is not valid")

    def test_register_project_tc_f1_34(self):
        """TC-F1-34. date MM = 13 (invalid). Covers: CENV20, VLNV10"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-34":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date month is not valid")

    def test_register_project_tc_f1_35(self):
        """TC-F1-35. date MM = 01 (valid min). Covers: VLV14"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-35":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_36(self):
        """TC-F1-36. date MM = 12 (valid max). Covers: VLV15"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-36":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_37(self):
        """TC-F1-37. date YYYY = 2024 (invalid). Covers: CENV22, VLNV11"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-37":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date year is not valid")

    def test_register_project_tc_f1_38(self):
        """TC-F1-38. date YYYY = 2028 (invalid). Covers: CENV23, VLNV12"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-38":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date year is not valid")

    def test_register_project_tc_f1_39(self):
        """TC-F1-39. date YYYY = 2025 (valid min). Covers: VLV18"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-39":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_40(self):
        """TC-F1-40. date YYYY = 2027 (valid max). Covers: VLV19"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-40":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_41(self):
        """TC-F1-41. date is not a valid calendar date (31/02/2026). Covers: CENV24"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-41":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "date is not a valid date")

    def test_register_project_tc_f1_42(self):
        """TC-F1-42. date is in the past. Covers: CENV25"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-42":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "date must be today or in the future")

    def test_register_project_tc_f1_43(self):
        """TC-F1-43. budget is an integer (no decimals). Covers: CENV26, CENV29"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-43":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "budget is not a valid float")

    def test_register_project_tc_f1_44(self):
        """TC-F1-44. budget has only 1 decimal. Covers: CENV29"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-44":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message,
                                 "budget must have exactly 2 decimal places")

    def test_register_project_tc_f1_45(self):
        """TC-F1-45. budget < 50000.00. Covers: CENV27, VLNV13"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-45":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "budget is out of range")

    def test_register_project_tc_f1_46(self):
        """TC-F1-46. budget > 1000000.00. Covers: CENV28, VLNV14"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-46":
                manager = EnterpriseManager()
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "budget is out of range")

    def test_register_project_tc_f1_47(self):
        """TC-F1-47. budget = 50000.00 (valid min). Covers: VLV21"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-47":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_48(self):
        """TC-F1-48. budget = 1000000.00 (valid max). Covers: VLV22"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-48":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_49(self):
        """TC-F1-49. Duplicate project raises exception. Covers: CENV30"""
        manager = EnterpriseManager()
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-01":
                manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-49":
                with self.assertRaises(EnterpriseManagementException) as result:
                    manager.register_project(
                        input_data["companyCIF"], input_data["projectAcronym"],
                        input_data["operationName"], input_data["department"],
                        input_data["date"], input_data["budget"])
                self.assertEqual(result.exception.message, "project already exists")

    def test_register_project_tc_f1_50(self):
        """TC-F1-50. project_acronym length exactly 6 (valid). Covers: VLV4"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-50":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_51(self):
        """TC-F1-51. project_acronym length exactly 9 (valid). Covers: VLV5"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-51":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_52(self):
        """TC-F1-52. operation_name length exactly 11 (valid). Covers: VLV8"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-52":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_53(self):
        """TC-F1-53. operation_name length exactly 29 (valid). Covers: VLV9"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-53":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_54(self):
        """TC-F1-54. date DD = 02 (valid). Covers: VLV12"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-54":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_55(self):
        """TC-F1-55. date DD = 30 (valid). Covers: VLV13"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-55":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_56(self):
        """TC-F1-56. date MM = 02 (valid). Covers: VLV16"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-56":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_57(self):
        """TC-F1-57. date MM = 11 (valid). Covers: VLV17"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-57":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_58(self):
        """TC-F1-58. budget = 50000.01 (valid). Covers: VLV23"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-58":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)

    def test_register_project_tc_f1_59(self):
        """TC-F1-59. budget = 999999.99 (valid). Covers: VLV24"""
        for input_data in self.__f1_test_data:
            if input_data["idTest"] == "TC-F1-59":
                manager = EnterpriseManager()
                result = manager.register_project(
                    input_data["companyCIF"], input_data["projectAcronym"],
                    input_data["operationName"], input_data["department"],
                    input_data["date"], input_data["budget"])
                self.assertEqual(len(result), 32)


if __name__ == "__main__":
    unittest.main()
