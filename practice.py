"""from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    balance: float

# correct data
user1 = User(name="DR4VEN", age=17, balance=1000.0)
print(user1)
print(user1.name)
print(user1.age)

# wrong type — what happens?
user2 = User(name="Alice", age="25", balance=500.0)

print(user2)
print(user2.name)
print(user2.age)"""


from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int
    balance: float

    @field_validator('age')
    @classmethod
    def age_must_be_valid(cls, v):
        if v < 0:
            raise ValueError("age cannot be negative")
        if v > 150:
            raise ValueError("age cannot be over 150")
        return v


user1 = User(name="DR4VEN", age=-5, balance=1000.0)
user2 = User(name="Alice", age=200, balance=500.0)
user3 = User(name="Bob", age=17, balance=500.0)
