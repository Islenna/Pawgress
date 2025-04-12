from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Category import Category as CategoryModel
from schemas.category_schema import Category as CategorySchema, CategoryCreate, CategoryWithSkills
from utils.dependencies import get_current_user  # Assuming you have a function to get the current user
from models.User import User as UserModel
from utils.logger import log_action

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

#Create a new category
@router.post("/", response_model=CategorySchema)
def create_category(category: CategoryCreate,
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    db_category = CategoryModel(**category.dict())

    # Check if the category already exists
    existing_category = db.query(CategoryModel).filter(CategoryModel.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    log_action(current_user, "create_category", extra={"category": category.name})
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

#Get all categories
@router.get("/", response_model=List[CategorySchema])
def get_categories(skip: int = 0, limit: int = 20, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    return db.query(CategoryModel).offset(skip).limit(limit).all()

#Get category by ID
@router.get("/{category_id}", response_model=CategoryWithSkills)
def get_category(category_id: int, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#Get category by name
@router.get("/name/{name}", response_model=CategorySchema)
def get_category_by_name(name: str, 
                        db: Session = Depends(get_db),
                        current_user: UserModel = Depends(get_current_user)):
    category = db.query(CategoryModel).filter(CategoryModel.name == name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#Update category
@router.put("/{category_id}", response_model=CategorySchema)
def update_category(category_id: int, 
                    category: CategoryCreate, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    log_action(current_user, "update_category", target=f"category {category_id}", extra={"updated_fields": category.dict()})
    db.commit()
    db.refresh(db_category)
    return db_category

#Delete category
@router.delete("/{category_id}", response_model=CategorySchema)
def delete_category(category_id: int, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    log_action(current_user, "delete_category", target=f"category {category_id}", extra={"category": db_category.name})
    db.delete(db_category)
    db.commit()
    return db_category


CategoryRouter = router
