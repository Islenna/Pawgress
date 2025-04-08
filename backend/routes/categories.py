from fastAPI import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Category import Category as CategoryModel

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

#Create a new category
@router.post("/", response_model=CategoryModel)
def create_category(category: CategoryModel, db: Session = Depends(get_db)):
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

#View all categories
@router.get("/", response_model=List[CategoryModel])
def get_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(CategoryModel).offset(skip).limit(limit).all()
    return categories

#View one category by ID
@router.get("/{category_id}", response_model=CategoryModel)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#View one category by name
@router.get("/name/{name}", response_model=CategoryModel)
def get_category_by_name(name: str, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.name == name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#Delete a category
@router.delete("/{category_id}", response_model=CategoryModel)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return db_category
