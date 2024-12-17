from sqlmodel import Field, SQLModel, Relationship


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()

    team: Team | None = Relationship(back_populates="heroes")
    


class HeroCreate(HeroBase):
    password: str


class HeroResponse(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None
    team_id: int | None = None

class HeroResponseWithTeam(HeroResponse):
    team: TeamResponse | None = None


class TeamResponseWithHeroes(TeamResponse):
    heroes: list[HeroResponse] = []