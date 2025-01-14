from typing import Annotated, Literal
from common.models import BaseSchemas
from fastapi import Query


class OrderCreated(BaseSchemas):
    order_id: Annotated[str, Query(
        description = "Order ID",
        regex = '^woo[0-9]{1,}$')]
    amount: Annotated[float, Query(
        description="Amount of order",
        ge = 20000,
    )]
    description: Annotated[str, Query(
        description = "Description of order",
    )]
    ip_address : Annotated[str, Query(
        description = "IP Address",
        regex = '^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    )]
    limit_time: Annotated[int, Query(
        description = "Limit time to pay",
        ge = 5,
        le = 15
    )]
    locale : Annotated[Literal["en", "vn"], Query(
        description = "Locale",
        regex = '^(vn|en)$'
    )]