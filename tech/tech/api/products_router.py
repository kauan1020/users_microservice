from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.schemas.product_schema import ProductSchema, ProductPublic
from tech.interfaces.schemas.message_schema import Message
from tech.use_cases.products.create_product_use_case import CreateProductUseCase
from tech.use_cases.products.list_products_by_category_use_case import ListProductsByCategoryUseCase
from tech.use_cases.products.list_all_products_use_case import ListAllProductsUseCase
from tech.use_cases.products.update_product_use_case import UpdateProductUseCase
from tech.use_cases.products.delete_product_use_case import DeleteProductUseCase
from tech.infra.repositories.sql_alchemy_product_repository import SQLAlchemyProductRepository

router = APIRouter()

def get_product_repository(session: Session = Depends(get_session)) -> SQLAlchemyProductRepository:
    """
    Dependency injection for SQLAlchemyProductRepository.

    Args:
        session (Session): SQLAlchemy session for database operations.

    Returns:
        SQLAlchemyProductRepository: Repository instance for product-related operations.
    """
    return SQLAlchemyProductRepository(session)

@router.post('/', response_model=ProductPublic, status_code=201)
def create_product(product: ProductSchema, repo: SQLAlchemyProductRepository = Depends(get_product_repository)):
    """
    Create a new product.

    Args:
        product (ProductSchema): Product creation details.
        repo (SQLAlchemyProductRepository): Repository for product data operations.

    Returns:
        ProductPublic: Details of the newly created product.

    Raises:
        HTTPException: If a product with the same name already exists.
    """
    use_case = CreateProductUseCase(repo)
    try:
        created_product = use_case.execute(product)
        return created_product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/{category}', response_model=list[ProductPublic])
def list_products_by_category(category: str, repo: SQLAlchemyProductRepository = Depends(get_product_repository)):
    """
    Retrieve a list of products by category.

    Args:
        category (str): The category to filter products by.
        repo (SQLAlchemyProductRepository): Repository for product data operations.

    Returns:
        list[ProductPublic]: List of products in the specified category.

    Raises:
        HTTPException: If no products are found in the specified category.
    """
    use_case = ListProductsByCategoryUseCase(repo)
    products = use_case.execute(category)
    if not products:
        raise HTTPException(status_code=404, detail=f'No products found in category "{category}"')
    return products

@router.get('/', response_model=list[ProductPublic])
def list_all_products(repo: SQLAlchemyProductRepository = Depends(get_product_repository)):
    """
    Retrieve a list of all products.

    Args:
        repo (SQLAlchemyProductRepository): Repository for product data operations.

    Returns:
        list[ProductPublic]: List of all products.

    Raises:
        HTTPException: If no products are found.
    """
    use_case = ListAllProductsUseCase(repo)
    products = use_case.execute()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@router.put('/{product_id}', response_model=ProductPublic)
def update_product(product_id: int, product: ProductSchema, repo: SQLAlchemyProductRepository = Depends(get_product_repository)):
    """
    Update a product's information.

    Args:
        product_id (int): ID of the product to update.
        product (ProductSchema): Updated product information.
        repo (SQLAlchemyProductRepository): Repository for product data operations.

    Returns:
        ProductPublic: Details of the updated product.

    Raises:
        HTTPException: If the product is not found.
    """
    use_case = UpdateProductUseCase(repo)
    try:
        updated_product = use_case.execute(product_id, product)
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/{product_id}', response_model=Message)
def delete_product(product_id: int, repo: SQLAlchemyProductRepository = Depends(get_product_repository)):
    """
    Delete a product by ID.

    Args:
        product_id (int): ID of the product to delete.
        repo (SQLAlchemyProductRepository): Repository for product data operations.

    Returns:
        Message: A success message confirming deletion.

    Raises:
        HTTPException: If the product is not found.
    """
    use_case = DeleteProductUseCase(repo)
    try:
        return use_case.execute(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
