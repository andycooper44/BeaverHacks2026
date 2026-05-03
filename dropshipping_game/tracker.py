from dataclasses import dataclass, field


@dataclass
class SaleRecord:
    product: str = ""
    quantity: int = 0
    revenue: float = 0.0
    cost: float = 0.0
    profit: float = 0.0


@dataclass
class SalesTracker:
    money: float = 0.0
    total_sales: int = 0
    total_revenue: float = 0.0
    total_profit: float = 0.0
    sales: list[SaleRecord] = field(default_factory=list)
