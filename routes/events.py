from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from database.connection import Database
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(tags=["Events"])
event_database = Database(Event)

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return await event_database.get_all()

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено.")
    return event

@event_router.post("/new")
async def create_event(body: Event) -> dict:
    await event_database.save(body)
    return {"message": "Событие успешно создано в MongoDB Искандера!"}

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    updated = await event_database.update(id, body)
    if not updated:
        raise HTTPException(status_code=404, detail="Событие не найдено.")
    return updated

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    if not await event_database.delete(id):
        raise HTTPException(status_code=404, detail="Событие не найдено.")
    return {"message": "Событие успешно удалено из MongoDB."}
