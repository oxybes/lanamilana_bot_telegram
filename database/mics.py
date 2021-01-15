import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# if (os.name == "nt"):
#     filename_bd = 'sqlite:///database/database.db'
# else:
#     filename_bd = 'sqlite://///root//lanamilana_bot_telegram//database/database.db'

# engine = create_engine(filename_bd, echo = False)
engine = create_engine('postgresql://postgres:7104501784329@193.122.111.95:5432/lanamilana', echo = False)
metadata = Base.metadata
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
