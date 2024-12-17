from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlmodel import Session, select

from app.models import Hero, HeroCreate, HeroResponse, HeroUpdate, HeroResponseWithTeam
from app.database import get_session
from app.utils.hashing import generate_hashed_password

router = APIRouter()

@router.post("/heroes/", response_model=HeroResponse, status_code=
              status.HTTP_201_CREATED, summary="Create a hero")
async def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    """Create a hero"""
    hashed_password = generate_hashed_password(hero.password)
    extra_data = {"hashed_password": hashed_password}
    db_hero = Hero.model_validate(hero, update=extra_data)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get("/heroes/{hero_id}", response_model=HeroResponseWithTeam, status_code=
              status.HTTP_200_OK, summary="Read a hero")
async def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    """Read a hero"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero
        


@router.get("/heroes/", response_model=list[HeroResponse], status_code=
              status.HTTP_200_OK, summary="Reads all heroes")
async def read_heroes(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(40, le=40)):
    """Reads all heroes"""
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
        
    
@router.patch("/heroes/{hero_id}", response_model=HeroResponse, status_code=
              status.HTTP_200_OK, summary="Update a hero")
async def update_hero(*, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate):
    """Update a hero"""
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in hero_data:
        password = hero_data["password"]
        hashed_password = generate_hashed_password(password)
        extra_data["hashed_password"] = hashed_password
    db_hero.sqlmodel_update(hero_data, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
        
    
@router.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a hero")
async def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    """Delete a hero"""
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    session.delete(db_hero)
    session.commit()
    return None
        