class ProductPresenter:
    """
    Handles the formatting of product-related responses.

    This class provides methods to transform product entities into a structured response format
    that is suitable for API responses.
    """

    @staticmethod
    def present_product(product: object) -> dict:
        """
        Formats a single product response.

        Args:
            product (object): The product entity to format.

        Returns:
            dict: A dictionary containing the formatted product details.
        """
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category": product.category
        }

    @staticmethod
    def present_product_list(products: list) -> list:
        """
        Formats a list of products.

        Args:
            products (list): A list of product entities.

        Returns:
            list: A list of dictionaries containing formatted product details.
        """
        return [ProductPresenter.present_product(product) for product in products]
