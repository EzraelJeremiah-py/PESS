from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models AFTER db is defined
from .user import User
from .library import BookResource, PastPaper
from .meeting import Meeting
from .regulations import RegulationFile
from .parental import ParentalSuggestion
from .latecomer import LateComer   # ✅ add LateComer here
