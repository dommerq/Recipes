from sqlalchemy import create_engine
from models.RecipeModel import Base
from settings.settings import DB_URI

engine = create_engine(DB_URI)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
