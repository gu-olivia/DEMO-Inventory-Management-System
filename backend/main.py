from fastapi import FastAPI
from sqlalchemy import text
from fastapi import Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .database import get_db
from .database import SessionLocal
from . import models, schemas
from fastapi.staticfiles import StaticFiles
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
print("BASE DIR:", BASE_DIR)
print("STATIC EXISTS:", (BASE_DIR / "static").exists())

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/api/fluorophores")
def get_fluorophores(db: Session = Depends(get_db)):
    fluorophores = db.query(models.Fluorophore).all()

    return [
        {
            "fluorophore_id": f.fluorophore_id,
            "fluorophore_name": f.fluorophore_name
        }
        for f in fluorophores
    ]

@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html"
    )

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):

    products = db.query(models.Product).all()

    return [
        {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "ab_name": product.ab_name,
            "fluorophore_id": product.fluorophore_id,
            "fluorophore_name": product.fluorophore.fluorophore_name if product.fluorophore else None,
            "host_isotype_name": product.host_isotype_name,
            "part_number": product.part_number,
            "clone_name": product.clone_name,
            "product_category": product.product_category,
            "top_products": product.top_products
        }
        for product in products
    ]

@app.post("/api/products", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    fluorophore = None

    if product.fluorophore_name:
        fluorophore = (
            db.query(models.Fluorophore)
            .filter(models.Fluorophore.fluorophore_name == product.fluorophore_name)
            .first()
        )

        if not fluorophore:
            raise HTTPException(status_code=404, detail="Fluorophore not found")

    db_product = models.Product(
        product_name=product.product_name,
        ab_name=product.ab_name,
        fluorophore_id=fluorophore.fluorophore_id if fluorophore else None,
        host_isotype_name=product.host_isotype_name or None,
        part_number=product.part_number,
        clone_name=product.clone_name,
        product_category=product.product_category or None,
        top_products=product.top_products or "NO"
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

    return {
        "product_id": db_product.product_id,
        "product_name": db_product.product_name,
        "ab_name": db_product.ab_name,
        "fluorophore_id": db_product.fluorophore_id,
        "fluorophore_name": fluorophore.fluorophore_name,  
        "host_isotype_name": db_product.host_isotype_name,
        "part_number": db_product.part_number,
        "clone_name": db_product.clone_name,
        "product_category": db_product.product_category,
        "top_products": db_product.top_products
    }

@app.get("/api/products/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product)
        .filter(models.Product.product_id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@app.put("/api/products/{product_id}")
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):

    db_product = db.query(models.Product).filter(
        models.Product.product_id == product_id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.product_name = product.product_name
    db_product.ab_name = product.ab_name
    db_product.part_number = product.part_number
    db_product.clone_name = product.clone_name
    db_product.product_category = product.product_category
    db_product.top_products = product.top_products

    # fluorophore lookup again (same logic as POST)
    fluorophore = db.query(models.Fluorophore).filter(
        models.Fluorophore.fluorophore_name == product.fluorophore_name
    ).first()

    if fluorophore:
        db_product.fluorophore_id = fluorophore.fluorophore_id

    db.commit()
    db.refresh(db_product)

    return db_product

@app.patch("/api/products/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):

    product = (
        db.query(models.Product)
        .filter(models.Product.product_id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_data = product_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.product_id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Deleted successfully"}

# lot endpoints

@app.get("/lots", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="lots.html"
    )

@app.get("/api/lots")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Lot).join(models.Product).all()

@app.get("/api/lots/{lot_id}")
def get_lot(
    lot_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(models.Lot)
        .filter(models.Lot.lot_id == lot_id)
        .first()
    )

    return product

@app.post("/api/lots", response_model=schemas.LotRead)
def create_lot(lot: schemas.LotCreate, db: Session = Depends(get_db)):
    # first verify that corresponding product exists first
    product = db.query(models.Product).filter(
        models.Product.product_id == lot.product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_lot = models.Lot(
        product_id=lot.product_id,
        lot_number=lot.lot_number,
        creation_date=lot.creation_date,
        expiration_date=lot.expiration_date,
        product_state=lot.product_state,
        test_5uL_concentration_ug_mL=lot.test_5uL_concentration_ug_mL,
        initial_volume_mL=lot.initial_volume_mL,
        remarks=lot.remarks
    )

    db.add(new_lot)
    db.commit()
    db.refresh(new_lot)

    return new_lot

@app.patch("/api/lots/{lot_id}", response_model=schemas.LotRead)
def update_lot(
    lot_id: int,
    lot_update: schemas.LotUpdate,
    db: Session = Depends(get_db)
):

    lot = (
        db.query(models.Lot)
        .filter(models.Lot.lot_id == lot_id)
        .first()
    )

    if lot is None:
        raise HTTPException(
            status_code=404,
            detail="Lot not found"
        )

    update_data = lot_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(lot, field, value)

    db.commit()
    db.refresh(lot)

    return lot

@app.put("/api/lots/{lot_id}")
def update_lot(lot_id: int, updated_lot: schemas.LotUpdate, db: Session = Depends(get_db)):

    lot = db.query(models.Lot).filter(models.Lot.lot_id == lot_id).first()

    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")

    for key, value in updated_lot.dict(exclude_unset=True).items(): # preserves existing values
        setattr(lot, key, value) 

    db.commit()
    db.refresh(lot)

    return lot

@app.delete("/api/lots/{lot_id}")
def delete_lot(lot_id: int, db: Session = Depends(get_db)):

    lot = db.query(models.Lot).filter(models.Lot.lot_id == lot_id).first()

    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")

    db.delete(lot)
    db.commit()

    return {"message": "Lot deleted"}

# bulk endpoints

@app.get("/bulk_inventory", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="bulk_inventory.html"
    )

#@app.get("/api/bulk_inventory")
#def get_products(db: Session = Depends(get_db)):
    #return db.query(models.Bulk_Product).all()

@app.get("/api/bulk_inventory")
def get_bulk_inventory(db: Session = Depends(get_db)):

    bulk_products = db.query(models.Bulk_Product).all()

    return [
        {
            "lot_id": bp.lot_id,
            "product_id": bp.product_id,
            "product_name": bp.product.product_name if bp.product else None,
            "ab_name": bp.product.ab_name if bp.product else None,
            "fluorophore_name": bp.product.fluorophore.fluorophore_name if bp.product and bp.product.fluorophore else None,
            "host_isotype_name": bp.product.host_isotype_name if bp.product and bp.product.host_isotype_name else None,
            "part_number": bp.product.part_number if bp.product and bp.product.part_number else None,
            "clone_name": bp.product.clone_name if bp.product else None,
            "lot_number": bp.lot_number if bp.lot_number else None,
            "creation_date": bp.lot.creation_date if bp.lot else None,
            "expiration_date": bp.lot.expiration_date if bp.lot else None,
            "initial_volume_mL": bp.lot.initial_volume_mL if bp.lot else None,
            "current_volume_ml": bp.current_volume_ml,
            "storage_concentration_ug_ml": bp.storage_concentration_ug_ml if bp.lot else None,
            "location": bp.location,
            "buffer": bp.buffer,
            "remarks": bp.remarks,
            "top_products": bp.product.top_products if bp.product and bp.product.top_products else None,
        }   
        for bp in bulk_products
    ]


@app.get("/api/bulk_inventory/{lot_id}")
def get_bulk_product(
    lot_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(models.Bulk_Product)
        .filter(models.Bulk_Product.lot_id == lot_id)
        .first()
    )

    return product

@app.post("/api/bulk_inventory")
def create_bulk(bulk: schemas.BulkCreate, db: Session = Depends(get_db)):

    new_bulk = models.Bulk_Product(
        lot_id=bulk.lot_id,
        product_id=bulk.product_id,
        clone_name=bulk.clone_name,
        lot_number=bulk.lot_number,
        buffer=bulk.buffer,
        storage_concentration_ug_ml=bulk.storage_concentration_ug_ml,
        current_volume_ml=bulk.current_volume_ml,
        location=bulk.location,
        remarks=bulk.remarks
    )

    db.add(new_bulk)
    db.commit()
    db.refresh(new_bulk)

    return new_bulk

@app.put("/api/bulk_inventory/{lot_id}")
def update_lot(lot_id: int, updated_lot: schemas.BulkUpdate, db: Session = Depends(get_db)):

    lot = db.query(models.Bulk_Product).filter(models.Bulk_Product.lot_id == lot_id).first()

    if not lot:
        raise HTTPException(status_code=404, detail="Bulk not found")

    for key, value in updated_lot.dict(exclude_unset=True).items(): # preserves existing values
        setattr(lot, key, value) 

    db.commit()
    db.refresh(lot)

    return lot

@app.patch("/api/bulk_inventory/{lot_id}")
def update_bulk(
    lot_id: int,
    bulk_update: schemas.BulkUpdate,
    db: Session = Depends(get_db)
):

    bulk = db.query(models.Bulk_Product).filter(
        models.Bulk_Product.lot_id == lot_id
    ).first()

    if not bulk:
        raise HTTPException(
            status_code=404,
            detail="Bulk product not found"
        )

    update_data = bulk_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(bulk, field, value)

    db.commit()
    db.refresh(bulk)

    return bulk

@app.delete("/api/bulk_inventory/{lot_id}")
def delete_bulk(
    lot_id: int,
    db: Session = Depends(get_db)
):

    bulk = db.query(models.Bulk_Product).filter(
        models.Bulk_Product.lot_id == lot_id
    ).first()

    if not bulk:
        raise HTTPException(
            status_code=404,
            detail="Bulk product not found"
        )

    db.delete(bulk)
    db.commit()

    return {
        "message": f"Bulk product with lot_id {lot_id} deleted"
    }


# packaged product endpoints

@app.get("/packaged_inventory", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="packaged_inventory.html"
    )

@app.get("/api/packaged_inventory")
def get_packaged_products(db: Session = Depends(get_db)):
    packaged_products = db.query(models.Packaged_Product).all()

    return [
        {
            "packaged_id": pp.packaged_id,
            "product_catalog_number": pp.product_catalog_number,
            "unit_price": pp.unit_price,
            "product_name": pp.product.product_name if pp.product else None,
            "clone_name": pp.product.clone_name if pp.product else None,
            "size": pp.size,
            "lot_number": pp.lot.lot_number if pp.lot else None,
            "packaging_date": pp.packaging_date,
            "packaging_concentration_ug_mL": pp.packaging_concentration_ug_mL,
            "location": pp.location,
            "qty_remaining": pp.qty_remaining,
            "buffer": pp.buffer,
            "cost_of_goods": pp.cost_of_goods,
            "remarks": pp.remarks
        }   
        for pp in packaged_products
    ]


@app.get("/api/packaged_inventory/{packaged_id}")
def get_packaged_product(
    packaged_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(models.Packaged_Product)
        .filter(models.Packaged_Product.packaged_id == packaged_id)
        .first()
    )

    return product

@app.put("/api/packaged_inventory/{packaged_id}")
def update_packaged_product(
    packaged_id: int,
    updated_packaged: schemas.PackagedUpdate,
    db: Session = Depends(get_db)
):
    packaged = (
        db.query(models.Packaged_Product)
        .filter(models.Packaged_Product.packaged_id == packaged_id)
        .first()
    )

    if not packaged:
        raise HTTPException(status_code=404, detail="Packaged product not found")

    for key, value in updated_packaged.dict(exclude_unset=True).items():
        setattr(packaged, key, value)

    db.commit()
    db.refresh(packaged)

    return packaged

@app.post("/api/packaged_inventory")
def create_packaged_product(
    packaged: schemas.PackagedCreate,
    db: Session = Depends(get_db)
):

    new_packaged = models.Packaged_Product(
        lot_id=packaged.lot_id,
        product_id=packaged.product_id,
        #clone_name=packaged.clone_name,
        unit_price=packaged.unit_price,
        packaging_date=packaged.packaging_date,
        packaging_concentration_ug_mL=packaged.packaging_concentration_ug_mL,
        qty_remaining=packaged.qty_remaining,
        product_catalog_number=packaged.product_catalog_number,
        size=packaged.size,
        location=packaged.location,
        buffer=packaged.buffer,
        cost_of_goods=packaged.cost_of_goods,
        remarks=packaged.remarks
    )

    db.add(new_packaged)
    db.commit()
    db.refresh(new_packaged)

    return new_packaged

@app.patch("/api/packaged_inventory/{packaged_id}")
def update_packaged_product(
    packaged_id: int,
    packaged_update: schemas.PackagedUpdate,
    db: Session = Depends(get_db)
):

    packaged = db.query(models.PackagedProduct).filter(
        PackagedProduct.packaged_id == packaged_id
    ).first()

    if not packaged:
        raise HTTPException(
            status_code=404,
            detail="Packaged product not found"
        )

    update_data = packaged_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(packaged, field, value)

    db.commit()
    db.refresh(packaged)

    return packaged

@app.delete("/api/packaged_inventory/{packaged_id}")
def delete_packaged_product(
    packaged_id: int,
    db: Session = Depends(get_db)
):

    packaged = db.query(models.Packaged_Product).filter(
        models.Packaged_Product.packaged_id == packaged_id
    ).first()

    if not packaged:
        raise HTTPException(
            status_code=404,
            detail="Packaged product not found"
        )

    db.delete(packaged)
    db.commit()

    return {
        "message": f"Packaged product {packaged_id} deleted"
    }

@app.get("/test-db")
def test_db():
    db = SessionLocal()
    result = db.execute(text("SELECT 1 AS test"))
    row = result.fetchone()
    db.close()
    return {"result": row.test}

