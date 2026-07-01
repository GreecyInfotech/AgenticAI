from __future__ import annotations

from ai_platform.infrastructure.crm import (
    check_crm_health,
    get_crm_client,
    lookup_crm_account,
    search_crm_accounts,
    update_crm_account,
)
from ai_platform.infrastructure.database import (
    acquire_connection,
    check_db_health,
    close_db_pool,
    execute_query,
    get_pool,
    init_db_pool,
    run_transaction,
)
from ai_platform.infrastructure.email import check_email_health, get_email_client, send_email
from ai_platform.infrastructure.kafka import check_kafka_health, ensure_topics
from ai_platform.infrastructure.qdrant_client import (
    check_qdrant_health,
    close_qdrant,
    ensure_collection,
    get_qdrant,
    init_qdrant,
)
from ai_platform.infrastructure.redis_client import (
    cache_get,
    cache_get_json,
    cache_set,
    cache_set_json,
    check_redis_health,
    close_redis,
    distributed_lock,
    get_redis,
    init_redis,
)

__all__ = [
    "acquire_connection",
    "cache_get",
    "cache_get_json",
    "cache_set",
    "cache_set_json",
    "check_crm_health",
    "check_db_health",
    "check_email_health",
    "check_kafka_health",
    "check_qdrant_health",
    "check_redis_health",
    "close_db_pool",
    "close_qdrant",
    "close_redis",
    "distributed_lock",
    "ensure_collection",
    "ensure_topics",
    "execute_query",
    "get_crm_client",
    "get_email_client",
    "get_pool",
    "get_qdrant",
    "get_redis",
    "init_db_pool",
    "init_qdrant",
    "init_redis",
    "lookup_crm_account",
    "run_transaction",
    "search_crm_accounts",
    "send_email",
    "update_crm_account",
]
