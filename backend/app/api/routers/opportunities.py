from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_opportunities():
    return {"message": "Opportunities Endpoint"}
