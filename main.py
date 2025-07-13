from fastapi import FastAPI
from routers import areas, trucks, assignments

app = FastAPI(root_path="/api")

app.include_router(areas.router)
app.include_router(trucks.router)
app.include_router(assignments.router)