from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date


class Fluorophore(Base):
    __tablename__ = "fluorophores"

    fluorophore_id = Column(Integer, primary_key=True, index=True)
    fluorophore_name = Column(String)
    fluorophore_group = Column(String)
    display_name = Column(String)

    products = relationship(
        "Product", # name of the other model class
        back_populates="fluorophore" # corresponding attribute
    )

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    ab_name = Column(String)
    fluorophore_id = Column(
        Integer,
        ForeignKey("fluorophores.fluorophore_id")
    )
    host_isotype_name = Column(String)
    part_number = Column(String)
    clone_name = Column(String)
    product_category = Column(String)
    top_products = Column(String)

    fluorophore = relationship(
        "Fluorophore",
        back_populates="products"
    )

    lots = relationship("Lot", back_populates="product")
    # shows that multiple lots belong to a product

    bulk_products = relationship("Bulk_Product", back_populates="product")
    packaged_products = relationship("Packaged_Product", back_populates="product")
    

class Lot(Base):
    __tablename__ = "lots"

    lot_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.product_id")
    )
    lot_number = Column(String)
    creation_date = Column(Date)
    expiration_date = Column(Date)
    product_state = Column(String)
    test_5ul_concentration_ug_ml = Column(Float)
    initial_volume_ml = Column(Float)
    remarks = Column(String)
    product = relationship(
        "Product",
        back_populates="lots",
    )
    bulk_products = relationship(
    "Bulk_Product",
    back_populates="lot"
    )  
    packaged_products = relationship(
    "Packaged_Product",
    back_populates="lot"
    )    
    bulk_products = relationship(
    "Bulk_Product",
    back_populates="lot",
    cascade="all, delete-orphan"
    )
    packaged_products = relationship(
    "Packaged_Product",
    back_populates="lot",
    cascade="all, delete-orphan"
    )    


class Bulk_Product(Base):
    __tablename__ = "bulk_products"

    lot_id = Column(
        Integer,
        ForeignKey("lots.lot_id"),
        primary_key=True
    )
    #bulk_id = Column(Integer, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    clone_name = Column(String)
    lot_number = Column(String)
    storage_concentration_ug_mL = Column(Float)
    current_volume_mL = Column(Float)
    @property
    def amount_remaining_ug(self):
        return self.storage_concentration_ug_mL * self.current_volume_mL
    location = Column(String)
    buffer = Column(String)
    remarks = Column(String)
    lot = relationship("Lot", back_populates="bulk_products")
    product = relationship("Product", back_populates="bulk_products")

class Packaged_Product(Base):
    __tablename__ = "packaged_products"

    packaged_id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(
        Integer,
        ForeignKey("lots.lot_id"),
        primary_key=True
    )
    product_id = Column(Integer, ForeignKey("products.product_id"))
    clone_name = Column(String)
    unit_price = Column(Float)
    packaging_date = Column(Date)
    packaging_concentration_ug_mL = Column(Float)
    qty_remaining = Column(Integer)
    product_catalog_number = Column(String)
    size = Column(String)
    location = Column(String)
    buffer = Column(String)
    cost_of_goods = Column(Float)
    remarks = Column(String)
    lot = relationship("Lot", back_populates="packaged_products")
    product = relationship("Product", back_populates="packaged_products")
