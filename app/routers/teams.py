from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlmodel import Session, select

from app.models import Team, TeamCreate, TeamResponse, TeamUpdate, TeamResponseWithHeroes
from app.database import get_session


router = APIRouter()

@router.post("/teams/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED, summary="Create a team")
async def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    """Create a team"""
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@router.get("/teams/{team_id}", response_model=TeamResponseWithHeroes, status_code=status.HTTP_200_OK, summary="Read a team")
async def read_team(*, session: Session = Depends(get_session), team_id: int):
    """Read a team"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team

@router.get("/teams/", response_model=list[TeamResponse], status_code=status.HTTP_200_OK, summary="Reads all teams")
async def read_teams(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(15, le=15)):
    """Reads all teams"""
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.patch("/teams/{team_id}", response_model=TeamResponse, status_code=status.HTTP_200_OK, summary="Update a team")
async def update_team(*, session: Session = Depends(get_session), team_id: int, team: TeamUpdate):
    """Update a team"""
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    # db_team.sqlmodel_update(team_data) # This the same as the for loop below
    for key, value in team_data.items():
        setattr(db_team, key,value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a team")
async def delete_team(*, session: Session = Depends(get_session), team_id: int):
    """Delete a team"""
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    session.delete(db_team)
    session.commit()
    return None