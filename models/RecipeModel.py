from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('recipes_id', Integer, ForeignKey('recipes.id')),
                          Column('ingredients_id', Integer, ForeignKey('ingredients.id'))
                          )


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    image_url = Column(String)
    primary_ingredient = Column(String)
    rating = Column(Float)
    yielding_number = Column(Integer)
    yielding_unit = Column(String)
    ingredients = relationship('Ingredient', secondary=association_table, backref=backref('pages', lazy='dynamic'), lazy='joined')

    def __repr__(self):
        return '<Recipe %r>' % self.title


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    metric_display_quantity = Column(String)
    metric_unit = Column(String)
    preparation_notes = Column(String)

    def __repr__(self):
        return '<Ingredient %r>' % self.name


