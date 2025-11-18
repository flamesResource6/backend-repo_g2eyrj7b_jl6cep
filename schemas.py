"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- Vendor -> "vendor" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Vendor(BaseModel):
    """
    Vendors collection schema
    Collection name: "vendor"
    """
    name: str = Field(..., description="Vendor name")
    logo_url: Optional[str] = Field(None, description="Logo image URL")
    description: Optional[str] = Field(None, description="Short bio or tagline")
    rating: float = Field(4.5, ge=0, le=5, description="Average rating out of 5")
    categories: List[str] = Field(default_factory=list, description="Categories this vendor sells")
    is_verified: bool = Field(False, description="Whether vendor is verified")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product"
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    image_url: Optional[str] = Field(None, description="Product image URL")
    category: str = Field(..., description="Product category")
    vendor_id: Optional[str] = Field(None, description="Owning vendor id")
    in_stock: bool = Field(True, description="Whether product is in stock")
    rating: float = Field(4.6, ge=0, le=5, description="Average rating")

class Newsletter(BaseModel):
    """
    Newsletter subscriptions collection
    Collection name: "newsletter"
    """
    email: EmailStr = Field(..., description="Subscriber email")

class Vendorapplication(BaseModel):
    """
    Vendor applications collection
    Collection name: "vendorapplication"
    """
    name: str = Field(..., description="Applicant name or brand")
    email: EmailStr = Field(..., description="Contact email")
    store_name: str = Field(..., description="Desired store name")
    message: Optional[str] = Field(None, description="Additional details")
