from __future__ import annotations

from functools import lru_cache

from ai_platform.infrastructure.crm import get_crm_client
from ai_platform.infrastructure.email import get_email_client
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


@lru_cache
def get_crm() -> object:
    return get_crm_client()


@lru_cache
def get_email() -> object:
    return get_email_client()
