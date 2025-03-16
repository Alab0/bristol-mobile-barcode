from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Product():
    barcode: str
    id: int
    name: str

@dataclass(frozen=True, slots=True)
class RequestStatus:
    barcode: str
    status: str