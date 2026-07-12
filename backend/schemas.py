from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date

# classes for products table create, read, update
class ProductCreate(BaseModel):
    product_name: str # does not have product_id since this is data going "into" the database
    ab_name: str | None = None
    fluorophore_name: str | None = None
    #fluorophore_id: int
    host_isotype_name: str | None = None
    part_number: str
    clone_name: str | None = None
    product_category: str
    top_products: str = "NO"

class ProductRead(BaseModel):
    product_id: int # does have product_id since this is data going "out" of the database
    product_name: str
    ab_name: str | None = None
    fluorophore_id: int
    host_isotype_name: str | None = None
    part_number: str
    clone_name: str | None = None
    product_category: str
    top_products: str

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    product_name: str | None = None
    ab_name: str | None = None
    fluorophore_id: int | None = None
    host_isotype_name: str | None = None
    part_number: str | None = None
    clone_name: str | None = None
    product_category: str | None = None
    top_products: str | None = None

# classes for lots table create, read, update
class LotCreate(BaseModel):
    product_id: int
    clone_name: str | None = None
    lot_number: str
    creation_date: date
    expiration_date: date
    product_state: str
    test_5uL_concentration_ug_mL: Decimal
    initial_volume_mL: Decimal
    remarks: str | None = None

class LotRead(BaseModel):
    lot_id: int
    product_id: int
    clone_name: str | None
    lot_number: str
    creation_date: date
    expiration_date: date
    product_state: str
    test_5uL_concentration_ug_mL: Decimal
    initial_volume_mL: Decimal
    remarks: str | None

    model_config = ConfigDict(from_attributes=True)

class LotUpdate(BaseModel):
    product_id: int | None = None
    clone_name: str | None = None
    lot_number: str | None = None
    creation_date: date | None = None
    expiration_date: date | None = None
    product_state: str | None = None
    test_5uL_concentration_ug_mL: Decimal | None = None
    initial_volume_mL: Decimal | None = None
    remarks: str | None = None

# classes for bulk table create, read, update
class BulkCreate(BaseModel):
    lot_id: int
    product_id: int
    clone_name: str | None = None
    lot_number: str
    buffer: str | None = None
    storage_concentration_ug_mL: Decimal
    current_volume_mL: Decimal
    location: str | None = None
    remarks: str | None = None

class BulkRead(BaseModel):
    bulk_id: int
    lot_id: int
    product_id: int
    clone_name: str | None
    lot_number: str
    buffer: str | None
    storage_concentration_ug_mL: Decimal
    current_volume_mL: Decimal
    amount_remaining_ug: Decimal
    location: str | None
    remarks: str | None

    model_config = ConfigDict(from_attributes=True)

class BulkUpdate(BaseModel):
    lot_id: int | None = None
    product_id: int | None = None
    #clone_name: str | None = None
    lot_number: str | None = None
    buffer: str | None = None
    storage_concentration_ug_mL: Decimal | None = None
    current_volume_mL: Decimal | None = None
    location: str | None = None
    remarks: str | None = None
    
# classes for packaged table create, read, update
class PackagedCreate(BaseModel):
    lot_id: int
    product_id: int
    #clone_name: str | None = None
    unit_price: float | None = None
    packaging_date: date | None = None
    packaging_concentration_ug_mL: float | None = None
    qty_remaining: int | None = None
    product_catalog_number: str | None = None
    size: str | None = None
    location: str | None = None
    buffer: str | None = None
    cost_of_goods: float | None = None
    remarks: str | None = None

class PackagedRead(BaseModel):
    packaged_id: int
    lot_id: int
    product_id: int
    clone_name: str | None
    unit_price: Decimal | None
    packaging_date: date | None
    packaging_concentration_ug_mL: Decimal | None
    qty_remaining: int
    product_catalog_number: str | None
    size: str | None
    location: str | None
    buffer: str | None
    cost_of_goods: Decimal | None
    remarks: str | None

    model_config = ConfigDict(from_attributes=True)

class PackagedUpdate(BaseModel):
    lot_id: int | None = None
    product_id: int | None = None
    clone_name: str | None = None
    unit_price: Decimal | None = None
    packaging_date: date | None = None
    packaging_concentration_ug_mL: Decimal | None = None
    qty_remaining: int | None = None
    product_catalog_number: str | None = None
    size: str | None = None
    location: str | None = None
    buffer: str | None = None
    cost_of_goods: Decimal | None = None
    remarks: str | None = None
