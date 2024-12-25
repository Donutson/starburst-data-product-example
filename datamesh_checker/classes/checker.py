"""
Module to make differents check on domains and data products in the context
of OCI datamesh
"""
import starburst_api

from datamesh_checker.helpers.checker import is_valid_domain_product_name
from datamesh_checker.helpers.string import to_snake_case, is_snake_case


class Checker:
    """
    A class to validate and check various properties of domains and data products
    in the Starburst data catalog.

    Attributes:
        starburst_client (Starburst): An instance of the Starburst client to interact
                                      with the Starburst API.

    Methods:
        check_domain(domain_name: str) -> dict:
            Check the validity of a domain's properties.

        check_data_product_info(data_product: DataProduct, valid_catalogs: dict=["minio", "minio_robin"]) -> dict:
            Check the validity of a data product's properties.

        check_data_product_dataset(dataset: DatasetView) -> dict:
            Check the validity of a dataset's properties.

        check_data_product_all_datasets(data_product: DataProduct) -> list:
            Check all datasets of a data product.

        check_domain_data_product(domain_name: str, data_product_name: str) -> dict:
            Check the validity of a specific data product within a domain.

        check_domain_all_data_products(domain_name: str) -> list:
            Check the validity of all data products within a domain.
    """

    pass