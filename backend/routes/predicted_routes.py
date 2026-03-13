from fastapi import APIRouter

router = APIRouter()

@router.get("/test-route")
def test_route():
    return {"message": "Predict routes working"}