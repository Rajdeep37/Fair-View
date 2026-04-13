from database import Base, engine
from models import Interview, Room, User

Base.metadata.create_all(bind=engine)

print("DB Ready.")