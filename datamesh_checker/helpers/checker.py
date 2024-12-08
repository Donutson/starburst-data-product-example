"""
Checkers functions
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

from datamesh_checker.helpers.string import is_upper_camel_case


def is_valid_domain_product_name(name: str):
    """
    Validate a domain or product name based on specific criteria.

    This function checks if the name is valid by ensuring that:
    - Each word in the name contains only alphabetic characters.
    - Each word is in UpperCamelCase format, or if it is 5 characters or shorter, it must be in uppercase.

    Args:
        name (str): The name to validate.

    Returns:
        bool: True if the name is valid, False otherwise.

    Examples:
        >>> is_valid_domain_product_name("ValidName")
        True

        >>> is_valid_domain_product_name("invalid name")
        False

        >>> is_valid_domain_product_name("ShortNAME")
        True

        >>> is_valid_domain_product_name("ShortNAME withInvalid")
        False
    """
    for word in name.split(" "):
        if not word.isalpha():
            return False

        if not (is_upper_camel_case(word) or (len(word) <= 5 and word.isupper())):
            return False

    return True


def validate_report(report: dict) -> bool:
    """
    Validate a report by checking the validity of its sections.

    This function checks if all elements within the sections of the given report are valid.
    A section or item is considered invalid if it contains a dictionary with an 'is_valid'
    key set to False.

    Args:
        report (dict): The report to validate, expected to contain 'data_product_info'
                       and 'data_product_datasets' sections.

    Returns:
        bool: True if all sections and items within the report are valid, False otherwise.

    Examples:
        >>> report = {
                'data_product_info': {
                    'data_product_name': {'value': 'ValidName', 'is_valid': True},
                    'data_product_summary': {'value': 'Some summary', 'is_valid': True}
                },
                'data_product_datasets': [
                    {'dataset_name': {'value': 'ValidDataset', 'is_valid': True}},
                    {'dataset_name': {'value': 'InvalidDataset', 'is_valid': False}}
                ]
            }
        >>> validate_report(report)
        False

        >>> report = {
                'data_product_info': {
                    'data_product_name': {'value': 'ValidName', 'is_valid': True},
                    'data_product_summary': {'value': 'Some summary', 'is_valid': True}
                },
                'data_product_datasets': [
                    {'dataset_name': {'value': 'ValidDataset', 'is_valid': True}},
                    {'dataset_name': {'value': 'AnotherValidDataset', 'is_valid': True}}
                ]
            }
        >>> validate_report(report)
        True
    """
    # Check if an element is invalid in a specific section
    def check_validity(section):
        for _, value in section.items():
            if isinstance(value, dict):
                if "is_valid" in value and not value["is_valid"]:
                    return False
            elif isinstance(value, list):
                for item in value:
                    if (
                        isinstance(item, dict)
                        and "is_valid" in item
                        and not item["is_valid"]
                    ):
                        return False
        return True

    if report.get("message"):
        return False

    if not report.get("data_product_datasets"):
        return False

    # Check every section of the report
    if not check_validity(report["data_product_info"]):
        return False

    for dataset in report["data_product_datasets"]:
        if not check_validity(dataset):
            return False

    return True


def create_pdf_from_domain_product_report(report: dict, filename: str):
    """
    Create a PDF report from a domain product validation report.

    This function generates a PDF document that summarizes the validation report
    of a domain product. The report includes information on the data product and
    its datasets, indicating whether each piece of information is valid or not.
    Invalid entries are highlighted in red.

    Args:
        report (dict): The validation report containing information on the domain product.
                       It includes sections like 'data_product_info' and 'data_product_datasets'.
        filename (str): The name of the file to save the generated PDF document.

    Returns:
        None

    Examples:
        >>> report = {
                'data_product_info': {
                    'data_product_name': {'value': 'ValidName', 'is_valid': True},
                    'data_product_summary': {'value': 'Some summary', 'is_valid': True}
                },
                'data_product_datasets': [
                    {'dataset_name': {'value': 'ValidDataset', 'is_valid': True}},
                    {'dataset_name': {'value': 'InvalidDataset', 'is_valid': False}}
                ]
            }
        >>> create_pdf_from_domain_product_report(report, 'report.pdf')
    """

    def add_paragraph(content, is_valid):
        style = normal_style if is_valid else invalid_style
        story.append(Paragraph(content, style))
        story.append(Spacer(1, 0.1 * inch))

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    invalid_style = ParagraphStyle("Invalid", parent=normal_style, textColor=colors.red)

    story = []
    doc = SimpleDocTemplate(filename, pagesize=letter)

    if "message" in report and "domain_name" in report:
        # Cas 1 : Affichage du message en rouge
        story.append(Paragraph(report["message"], invalid_style))
    else:
        # Cas 2 : Traitement détaillé du rapport
        story.append(Paragraph("Rapport de validation des données", styles["Title"]))
        story.append(Spacer(1, 0.2 * inch))

        # Ajout de la section data_product_info
        story.append(
            Paragraph("Informations sur le produit de données", styles["Heading2"])
        )
        for key, value in report["data_product_info"].items():
            content = (
                f"{key.replace('_', ' ').capitalize()}: {value.get('value', 'None')}"
            )
            add_paragraph(content, value.get("is_valid", True))

        # Ajout de la section data_product_datasets
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Jeux de données", styles["Heading2"]))
        if not report["data_product_datasets"]:
            add_paragraph(
                "Des datasets de type materialized view ont été détecté", False
            )
        else:
            for dataset in report["data_product_datasets"]:
                story.append(Spacer(1, 0.1 * inch))
                for key, value in dataset.items():
                    if key == "dataset_columns":
                        story.append(
                            Paragraph("Colonnes du jeu de données", styles["Heading3"])
                        )
                        columns_data = [["Colonne", "Type", "Description"]]
                        for column in value["value"]:
                            column_parts = column[1:-1].split(";")
                            column_name = column_parts[0]
                            column_type = column_parts[1]
                            column_description = column_parts[2]
                            columns_data.append(
                                [column_name, column_type, column_description]
                            )

                        t = Table(columns_data)
                        t.setStyle(
                            TableStyle(
                                [
                                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                                ]
                            )
                        )

                        for row_num, row in enumerate(columns_data):
                            if row_num > 0 and (row[2].strip(" ") == ""):
                                t.setStyle(
                                    TableStyle(
                                        [
                                            (
                                                "TEXTCOLOR",
                                                (0, row_num),
                                                (-1, row_num),
                                                colors.red,
                                            )
                                        ]
                                    )
                                )

                        story.append(t)
                        story.append(Spacer(1, 0.1 * inch))
                    else:
                        content = f"{key.replace('_', ' ').capitalize()}: {value.get('value', 'None')}"
                        add_paragraph(content, value.get("is_valid", True))

    # Génération du PDF
    doc.build(story)
