"""
Module to make differents check on domains and data products in the context
of OCI datamesh
"""


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

    def __init__(self, starburst_client: Starburst):
        """
        Initialize the Checker with a Starburst client.

        Args:
            starburst_client (Starburst): An instance of the Starburst client.
        """
        self.starburst_client = starburst_client

    def check_domain(self, domain_name: str) -> dict:
        """
        Check the validity of a domain's properties.

        Args:
            domain_name (str): The name of the domain to check.

        Returns:
            dict: A dictionary containing the validation results of the domain's properties.
            None if the domain doesn't exists
        """
        domain = self.starburst_client.get_domain_by_name(domain_name, as_class=True)

        if not domain:
            return None

        return {
            "domain_name": {
                "value": domain.name,
                "is_valid": is_valid_domain_product_name(domain.name),
            },
            "domain_description": {
                "value": domain.description,
                "is_valid": domain.description != "",
            },
            "domain_schema_location": {
                "value": domain.schema_location,
                "is_valid": (
                    domain.schema_location.startswith("s3://starburst/")
                    and domain.schema_location[15:].startswith(
                        to_snake_case(domain.name)
                    )
                ),
            },
        }

    def check_data_product_info(
        self, data_product: DataProduct, valid_catalogs: dict = ["minio", "minio_robin"]
    ) -> dict:
        """
        Check the validity of a data product's properties.

        Args:
            data_product (DataProduct): The data product to check.
            valid_catalogs (dict, optional): A list of valid catalog names. Default is ["minio", "minio_robin"].

        Returns:
            dict: A dictionary containing the validation results of the data product's properties.
        """
        domain = self.starburst_client.get_domain_by_id(
            domain_id=data_product.data_domain_id, as_class=True
        )
        tags = self.starburst_client.get_data_product_tags(
            domain_name=domain.name, data_product_name=data_product.name, as_class=True
        )
        return {
            "data_product_name": {
                "value": data_product.name,
                "is_valid": is_valid_domain_product_name(data_product.name),
            },
            "data_product_summary": {
                "value": data_product.summary,
                "is_valid": data_product.summary != "",
            },
            "data_product_catalog_name": {
                "value": data_product.catalog_name,
                "is_valid": data_product.catalog_name in valid_catalogs,
            },
            "data_product_owners": {
                "value": [str(owner) for owner in data_product.owners],
                "is_valid": len(data_product.owners) >= 1,
            },
            "data_product_tags": {
                "value": [str(tag) for tag in tags],
                "is_valid": len(tags) >= 1,
            },
        }

    def check_data_product_dataset(self, dataset: DatasetView) -> dict:
        """
        Check the validity of a dataset's properties.

        Args:
            dataset (DatasetView): The dataset to check.

        Returns:
            dict: A dictionary containing the validation results of the dataset's properties.
        """
        is_columns_valid = True
        for column in dataset.columns:
            if column.description == "":
                is_columns_valid = False
                break

        return {
            "dataset_name": {
                "value": dataset.name,
                "is_valid": is_snake_case(dataset.name),
            },
            "dataset_description": {
                "value": dataset.description,
                "is_valid": dataset.description != "",
            },
            "dataset_columns": {
                "value": [str(column) for column in dataset.columns],
                "is_valid": is_columns_valid,
            },
        }

    def check_data_product_all_datasets(self, data_product: DataProduct) -> list:
        """
        Check all datasets of a data product.

        Args:
            data_product (DataProduct): The data product whose datasets are to be checked.

        Returns:
            list: A list of dictionaries containing the validation results of each dataset.
        """
        if not data_product.materialized_views:
            return [
                self.check_data_product_dataset(dataset)
                for dataset in data_product.views
            ]

    def check_domain_data_product(
        self, domain_name: str, data_product_name: str
    ) -> dict:
        """
        Check the validity of a specific data product within a domain.

        Args:
            domain_name (str): The name of the domain.
            data_product_name (str): The name of the data product to check.

        Returns:
            dict: A dictionary containing the validation results of the data product and its datasets.
            None if the data product doesn't exists
        """
        data_product = self.starburst_client.get_data_product(
            domain_name, data_product_name, as_class=True
        )

        if not data_product:
            return None

        return {
            "domain_name": domain_name,
            "data_product_info": self.check_data_product_info(data_product),
            "data_product_datasets": self.check_data_product_all_datasets(data_product),
        }

    def check_domain_all_data_products(self, domain_name: str) -> list:
        """
        Check the validity of all data products within a domain.

        Args:
            domain_name (str): The name of the domain.

        Returns:
            list: A list of dictionaries containing the validation results of each data product in the domain.
        """
        domain = self.starburst_client.get_domain_by_name(domain_name)

        if not domain:
            return None

        return [
            self.check_domain_data_product(
                domain_name=domain_name, data_product_name=data_product.get("name")
            )
            for data_product in domain.get("assignedDataProducts")
        ]
