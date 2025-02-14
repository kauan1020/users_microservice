from fastapi import HTTPException
from tech.use_cases.products.create_product_use_case import CreateProductUseCase
from tech.use_cases.products.list_products_by_category_use_case import ListProductsByCategoryUseCase
from tech.use_cases.products.list_all_products_use_case import ListAllProductsUseCase
from tech.use_cases.products.update_product_use_case import UpdateProductUseCase
from tech.use_cases.products.delete_product_use_case import DeleteProductUseCase
from tech.interfaces.presenters.product_presenter import ProductPresenter
from tech.interfaces.schemas.product_schema import ProductSchema

class ProductController:
    """
    Controller responsible for managing product-related operations.

    This class acts as an intermediary between the API and the business logic, ensuring proper
    use of the use cases and handling exceptions.
    """

    def __init__(
        self,
        create_product_use_case: CreateProductUseCase,
        list_products_by_category_use_case: ListProductsByCategoryUseCase,
        list_all_products_use_case: ListAllProductsUseCase,
        update_product_use_case: UpdateProductUseCase,
        delete_product_use_case: DeleteProductUseCase
    ):
        """
        Initializes the ProductController with the required use cases.

        Args:
            create_product_use_case (CreateProductUseCase): Use case for creating a product.
            list_products_by_category_use_case (ListProductsByCategoryUseCase): Use case for listing products by category.
            list_all_products_use_case (ListAllProductsUseCase): Use case for retrieving all products.
            update_product_use_case (UpdateProductUseCase): Use case for updating a product.
            delete_product_use_case (DeleteProductUseCase): Use case for deleting a product.
        """
        self.create_product_use_case = create_product_use_case
        self.list_products_by_category_use_case = list_products_by_category_use_case
        self.list_all_products_use_case = list_all_products_use_case
        self.update_product_use_case = update_product_use_case
        self.delete_product_use_case = delete_product_use_case

    def create_product(self, product_data: ProductSchema) -> dict:
        """
        Creates a new product and returns a formatted response.

        Args:
            product_data (ProductSchema): Data required to create a new product.

        Returns:
            dict: The formatted response containing product details.

        Raises:
            HTTPException: If a product with the same name already exists.
        """
        try:
            product = self.create_product_use_case.execute(product_data)
            return ProductPresenter.present_product(product)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def list_products_by_category(self, category: str) -> list:
        """
        Retrieves a list of products filtered by category.

        Args:
            category (str): The category to filter products by.

        Returns:
            list: A list of formatted product data.

        Raises:
            HTTPException: If no products are found in the specified category.
        """
        products = self.list_products_by_category_use_case.execute(category)
        if not products:
            raise HTTPException(status_code=404, detail=f'No products found in category "{category}"')
        return ProductPresenter.present_product_list(products)

    def list_all_products(self) -> list:
        """
        Retrieves all available products.

        Returns:
            list: A list of formatted product data.

        Raises:
            HTTPException: If no products are found.
        """
        products = self.list_all_products_use_case.execute()
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return ProductPresenter.present_product_list(products)

    def update_product(self, product_id: int, product_data: ProductSchema) -> dict:
        """
        Updates a product by its ID.

        Args:
            product_id (int): The ID of the product to update.
            product_data (ProductSchema): The updated product data.

        Returns:
            dict: The formatted response containing the updated product details.

        Raises:
            HTTPException: If the product is not found.
        """
        try:
            updated_product = self.update_product_use_case.execute(product_id, product_data)
            return ProductPresenter.present_product(updated_product)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def delete_product(self, product_id: int) -> dict:
        """
        Deletes a product by its ID.

        Args:
            product_id (int): The ID of the product to delete.

        Returns:
            dict: A success message confirming deletion.

        Raises:
            HTTPException: If the product is not found.
        """
        try:
            return self.delete_product_use_case.execute(product_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
