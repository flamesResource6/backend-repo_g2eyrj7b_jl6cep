import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Vendor, Newsletter, Vendorapplication

app = FastAPI(title="Multivendor Ecommerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Multivendor Ecommerce Backend Running"}

# Public endpoints for homepage content

@app.get("/api/products", response_model=List[Product])
def list_products(limit: int = 8, category: Optional[str] = None):
    if db is None:
        # Fallback sample data so the homepage loads even without DB
        sample: List[Product] = [
            Product(title=f"Premium Headphones {i+1}", description="Crystal clear sound.", price=99.99 + i, image_url=f"https://images.unsplash.com/photo-1518443871411-05f03d4d8e8b?auto=format&fit=crop&w=800&q=60", category="Audio", vendor_id=None, in_stock=True, rating=4.6)
            for i in range(limit)
        ]
        return sample

    query = {}
    if category:
        query["category"] = category
    docs = get_documents("product", query, limit)
    # Convert ObjectId and extra fields
    items: List[Product] = []
    for d in docs:
        d.pop("_id", None)
        items.append(Product(**d))
    return items

@app.get("/api/vendors", response_model=List[Vendor])
def list_vendors(limit: int = 6):
    if db is None:
        sample: List[Vendor] = [
            Vendor(name=f"Vendor {i+1}", logo_url="https://api.dicebear.com/7.x/initials/svg?seed=VV", description="Quality products from verified sellers.", rating=4.7, categories=["Electronics", "Home"], is_verified=True)
            for i in range(limit)
        ]
        return sample

    docs = get_documents("vendor", {}, limit)
    res: List[Vendor] = []
    for d in docs:
        d.pop("_id", None)
        res.append(Vendor(**d))
    return res

class SubscribePayload(BaseModel):
    email: str

@app.post("/api/newsletter")
def subscribe(payload: SubscribePayload):
    # If DB present, persist; else, accept for demo
    if db is not None:
        try:
            create_document("newsletter", Newsletter(email=payload.email))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}

class VendorApplyPayload(BaseModel):
    name: str
    email: str
    store_name: str
    message: Optional[str] = None

@app.post("/api/vendor/apply")
def vendor_apply(payload: VendorApplyPayload):
    if db is not None:
        try:
            create_document("vendorapplication", Vendorapplication(**payload.model_dump()))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available" if db is None else "✅ Connected",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "collections": []
    }

    if db is not None:
        try:
            response["collections"] = db.list_collection_names()[:10]
        except Exception as e:
            response["database"] = f"⚠️ Error: {str(e)[:50]}"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
