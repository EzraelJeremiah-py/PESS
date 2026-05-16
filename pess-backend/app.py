import os
from flask import Flask, session, render_template, send_from_directory, redirect, url_for, flash
from models import db
from models.library import BookResource, PastPaper   # ✅ import models
from models.meeting import Meeting
from models.regulations import RegulationFile        # ✅ import RegulationFile model
from flask_migrate import Migrate
from models.parental import ParentalSuggestion


def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"
    # ✅ point to the actual DB in /instance
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/pess_project/instance/pess.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Uploads folder
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize DB + Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprints
    from routes.login import login_bp
    from routes.dashboard import dashboard_bp
    from routes.admin.dashboard import admin_bp
    from routes.admin.guidelines import admin_guidelines_bp
    from routes.guidelines import guidelines_bp
    from routes.register import register_bp
    from routes.admin.library import admin_library_bp
    from routes.meeting_routes import meeting_bp
    from routes.public_meeting_routes import public_meeting_bp
    from routes.admin.suspensions import admin_suspensions_bp
    from routes.public_suspensions import public_suspensions_bp
    from routes.regulations import regulations_bp
    from routes.admin.regulations import admin_regulations_bp
    from routes.parental import parental_bp
    from routes.admin.parental import admin_parental_bp
    from routes.latecomers import late_bp
    from routes.forgot_password import forgot_password_bp
    from routes.admin.fees import admin_fees_bp
    from routes.public.fees import public_fees_bp





    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_guidelines_bp)
    app.register_blueprint(guidelines_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(admin_library_bp)
    app.register_blueprint(meeting_bp)
    app.register_blueprint(public_meeting_bp)
    app.register_blueprint(admin_suspensions_bp)
    app.register_blueprint(public_suspensions_bp)
    app.register_blueprint(regulations_bp)        # User-facing regulations
    app.register_blueprint(admin_regulations_bp) 
    app.register_blueprint(parental_bp)
    app.register_blueprint(admin_parental_bp)
    app.register_blueprint(late_bp)
    app.register_blueprint(forgot_password_bp)
    app.register_blueprint(admin_fees_bp)   # /admin/fees
    app.register_blueprint(public_fees_bp)  # /fees


    # ✅ Home route
    @app.route("/")
    def home():
        if "user_id" in session:
            return redirect("/dashboard")
        return render_template("home.html")

    # ✅ Logout
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    # ✅ Admin redirect
    @app.route("/admin")
    def admin_redirect():
        if not session.get("is_admin"):
            return redirect(url_for("dashboard.dashboard"))
        return redirect(url_for("admin.dashboard"))

    @app.route("/uploads/library/<filename>")
    def uploaded_library_file(filename):
        return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], "library"), filename)

    # ✅ Public Library route
    @app.route("/library")
    def library():
        books = BookResource.query.all()
        papers = PastPaper.query.all()
        return render_template("library.html", books=books, papers=papers)

    @app.route("/admin/library/delete/<int:id>", methods=["POST"])
    def delete_resource(id):
        resource = BookResource.query.get(id) or PastPaper.query.get(id)
        if resource:
            db.session.delete(resource)
            db.session.commit()
            flash("Resource deleted successfully!", "success")
        return redirect(url_for("manage_library"))

    return app

if __name__ == "__main__":
    app = create_app()
    # ✅ force-create missing tables like regulation_files
    with app.app_context():
        db.create_all()
    app.run(debug=True)
