# create read update delete get one
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from api_v1.products.schemas import ProductCreate
from core.models import Product
from .schemas import ProductUpdate, ProductUpdatePartial


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)

    await session.commit()
    await session.refresh(product)

    return product


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(
        session: AsyncSession,
        product: Product
) -> None:
    await session.delete(product)
    await session.commit()
