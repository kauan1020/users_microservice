from enum import Enum
from dataclasses import dataclass

class PaymentStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

@dataclass
class Payment(object):
    order_id: int
    amount: float
    status: PaymentStatus
