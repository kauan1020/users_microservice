from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech.adapters.driven.infra.database import get_session
from tech.core.domain.schemas import ProductSchema, ProductPublic, Message
from tech.core.app.use_cases.products_use_cases import ProductUseCase
from tech.adapters.driven.infra.repositories.sql_alchemy_product_repository import SQLAlchemyProductRepository

router = APIRouter()

def get_product_use_case(session: Session = Depends(get_session)) -> ProductUseCase:
    """Dependency injection for ProductUseCase using the SQLAlchemyProductRepository."""
    product_repository = SQLAlchemyProductRepository(session)
    return ProductUseCase(product_repository)

@router.post('/', response_model=ProductPublic, status_code=201)
def create_product(product: ProductSchema, use_case: ProductUseCase = Depends(get_product_use_case)):
    """Create a new product."""
    try:
        created_product = use_case.create_product(product)
        return created_product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/{category}', response_model=list[ProductPublic])
def list_products_by_category(category: str, use_case: ProductUseCase = Depends(get_product_use_case)):
    """Retrieve a list of products by category."""
    products = use_case.list_products_by_category(category)
    if not products:
        raise HTTPException(status_code=404, detail=f'No products found in category "{category}"')
    return products

@router.get('/', response_model=list[ProductPublic])
def list_all_products(use_case: ProductUseCase = Depends(get_product_use_case)):
    """Retrieve a list of all products."""
    products = use_case.list_all_products()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@router.put('/{product_id}', response_model=ProductPublic)
def update_product(product_id: int, product: ProductSchema, use_case: ProductUseCase = Depends(get_product_use_case)):
    """Update a product's information."""
    try:
        updated_product = use_case.update_product(product_id, product)
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/{product_id}', response_model=Message)
def delete_product(product_id: int, use_case: ProductUseCase = Depends(get_product_use_case)):
    """Delete a product by ID."""
    try:
        return use_case.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
