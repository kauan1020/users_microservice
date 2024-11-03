from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from tech.core.domain.models import Products
from tech.core.app.repositories.product_repository import ProductRepository
from tech.adapters.driven.infra.repositories.sql_alchemy_models import SQLAlchemyProduct

class SQLAlchemyProductRepository(ProductRepository):
    """Repository for managing Products entity interactions with the database using SQLAlchemy."""

    def __init__(self, session: Session):
        """Initializes the repository with a SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self.session = session

    def add(self, product: Products) -> Products:
        """Adds a new product to the database."""
        db_product = SQLAlchemyProduct(
            name=product.name,
            price=product.price,
            category=product.category,
        )
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        product.id = db_product.id
        return product

    def get_by_id(self, product_id: int) -> Optional[Products]:
        """Fetches a product by its unique ID."""
        db_product = self.session.scalar(select(SQLAlchemyProduct).where(SQLAlchemyProduct.id == product_id))
        if db_product:
            return Products(
                id=db_product.id,
                name=db_product.name,
                price=db_product.price,
                category=db_product.category,
            )
        return None

    def get_by_name(self, name: str) -> Optional[Products]:
        """Fetches a product by its name."""
        db_product = self.session.scalar(select(SQLAlchemyProduct).where(SQLAlchemyProduct.name == name))
        if db_product:
            return Products(
                id=db_product.id,
                name=db_product.name,
                price=db_product.price,
                category=db_product.category,
            )
        return None

    def list_by_category(self, category: str) -> List[Products]:
        """Retrieves a list of products by category."""
        db_products = self.session.scalars(select(SQLAlchemyProduct).where(SQLAlchemyProduct.category == category)).all()
        return [
            Products(
                id=db_product.id,
                name=db_product.name,
                price=db_product.price,
                category=db_product.category,
            )
            for db_product in db_products
        ]

    def list_all_products(self) -> List[Products]:
        """Retrieves all products from the database."""
        db_products = self.session.scalars(select(SQLAlchemyProduct)).all()
        return [
            Products(
                id=db_product.id,
                name=db_product.name,
                price=db_product.price,
                category=db_product.category,
            )
            for db_product in db_products
        ]

    def update(self, product: Products) -> Products:
        """Updates an existing product's information."""
        db_product = self.session.scalar(select(SQLAlchemyProduct).where(SQLAlchemyProduct.id == product.id))
        if not db_product:
            raise ValueError("Product not found")

        db_product.name = product.name
        db_product.price = product.price
        db_product.category = product.category
        self.session.commit()
        self.session.refresh(db_product)
        return product

    def delete(self, product: Products) -> None:
        """Deletes a product from the database."""
        db_product = self.session.scalar(select(SQLAlchemyProduct).where(SQLAlchemyProduct.id == product.id))
        if db_product:
            self.session.delete(db_product)
            self.session.commit()
