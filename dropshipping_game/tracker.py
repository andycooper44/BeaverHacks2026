from dataclasses import dataclass, field


@dataclass
class SaleRecord:
    product: str = ""
    quantity: int = 0
    revenue: float = 0.0
    cost: float = 0.0
    profit: float = 0.0
    day: int = 0


@dataclass
class SalesTracker:
    money: float = 0.0
    total_sales: int = 0
    total_revenue: float = 0.0
    total_profit: float = 0.0
    sales: list[SaleRecord] = field(default_factory=list)

    def spend_money(self, amount: float) -> None:
        self.money -= amount

    def record_sale(self, sale: SaleRecord) -> None:
        self.money += sale.profit
        self.total_sales += sale.quantity
        self.total_revenue += sale.revenue
        self.total_profit += sale.profit
        self.sales.append(sale)
