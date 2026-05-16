from flask import Blueprint, render_template, request, redirect, url_for
from models.parental import ParentalSuggestion, db

# ✅ Rename blueprint to parental_bp so app.py can import it directly
parental_bp = Blueprint('parental', __name__, url_prefix="/parental")

@parental_bp.route("/", methods=['GET', 'POST'])
def parental():
    if request.method == 'POST':
        new_suggestion = ParentalSuggestion(
            parent_name=request.form['parent_name'],
            student_name=request.form['student_name'],
            student_class=request.form['student_class'],
            student_stream=request.form['student_stream'],
            contact_number=request.form['contact_number'],
            gmail=request.form['gmail'],
            comment=request.form['comment'],
            approved=False
        )
        db.session.add(new_suggestion)
        db.session.commit()   # ✅ ensure data is saved
        return redirect(url_for('parental.recent_suggestions'))

    return render_template('parental_form.html')


@parental_bp.route("/recent_suggestions")
def recent_suggestions():
    # ✅ Only show approved suggestions for users
    suggestions = ParentalSuggestion.query.filter_by(approved=True).order_by(
        ParentalSuggestion.created_at.desc()
    ).all()
    return render_template('recent_suggestions.html', suggestions=suggestions)
