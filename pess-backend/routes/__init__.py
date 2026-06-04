from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from routes.fees import fees_bp
from routes.meeting import meeting_bp
from routes.late import late_bp
from routes.suspensions import suspensions_bp
from routes.parental import parental_bp



# This makes it easy to import all blueprints at once
blueprints = [
  auth_bp, 
  admin_bp,
  user_bp, 
  fees_bp, 
  meeting_bp, 
  late_bp, 
  suspensions_bp,
  parental_bp
]
