Checker
======================================================

.. autoclass:: classes.checker.Checker
    :members:

Usage Example
-------------

.. code-block:: python

    from classes.checker import Checker
    from starburst_api.classes.class_starburst import Starburst
    from starburst_api.classes.class_starburst_connection_info import StarburstConnectionInfo

    # Initialize the Starburst client
    connection_info = StarburstConnectionInfo(
        user="username", 
        password="password", 
        host="your-starburst-host", 
        port=8080, 
        catalog="your_catalog", 
        schema="your_schema"
    )
    starburst_client = Starburst(connection_info)

    # Create a Checker instance
    checker = Checker(starburst_client=starburst_client)

    # Example 1: Validate a specific domain
    domain_name = "finance"
    domain_validation = checker.check_domain(domain_name)
    print("Domain Validation Results:", domain_validation)

    # Example 2: Validate a specific data product within a domain
    data_product_name = "financial_reports"
    data_product_validation = checker.check_domain_data_product(domain_name, data_product_name)
    print(f"Validation Results for Data Product '{data_product_name}':", data_product_validation)

    # Example 3: Validate all data products in a domain
    all_data_products_validation = checker.check_domain_all_data_products(domain_name)
    print(f"Validation Results for All Data Products in Domain '{domain_name}':", all_data_products_validation)

    # Example 4: Validate a specific data product object
    data_product = starburst_client.get_data_product(domain_name, data_product_name, as_class=True)
    data_product_info_validation = checker.check_data_product_info(data_product)
    print("Data Product Info Validation Results:", data_product_info_validation)

    # Example 5: Validate all datasets within a data product
    data_product_datasets_validation = checker.check_data_product_all_datasets(data_product)
    print("Validation Results for All Datasets in the Data Product:", data_product_datasets_validation)


    checker = Checker()
    checker.run_checks()