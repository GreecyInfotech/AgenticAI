from __future__ import annotations

from functools import lru_cache

from ai_platform.infrastructure.repositories import (
    CustomerRepository,
    InventoryRepository,
    OrderRepository,
    ProductRepository,
)


@lru_cache
def get_order_repository() -> OrderRepository:
    return OrderRepository()


@lru_cache
def get_customer_repository() -> CustomerRepository:
    return CustomerRepository()


@lru_cache
def get_inventory_repository() -> InventoryRepository:
    return InventoryRepository()


@lru_cache
def get_product_repository() -> ProductRepository:
    return ProductRepository()
