from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Relationship
    restaurant_pizzas = relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")
    pizzas = relationship("Pizza", secondary="restaurant_pizzas", back_populates="restaurants")

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # Relationship
    restaurant_pizzas = relationship("RestaurantPizza", back_populates="pizza", cascade="all, delete-orphan")
    restaurants = relationship("Restaurant", secondary="restaurant_pizzas", back_populates="pizzas")

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza',)

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    
    # Foreign Keys
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, ForeignKey('pizzas.id'), nullable=False)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza = relationship("Pizza", back_populates="restaurant_pizzas")

    # Serialization rules
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')

    # Validation
    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
