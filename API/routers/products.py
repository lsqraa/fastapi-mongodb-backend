from fastapi import APIRouter,HTTPException, status

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={status.HTTP_404_NOT_FOUND:{"description": "Not found"}}
                    )

products_list = ["salsa_amarilla",
                  "salsa_roja",
                    "salsa_verde",
                    "salsa_morada"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id:int):
    return products_list[id]