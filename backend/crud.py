from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate

def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        quantity=product.quantity
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def get_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()
