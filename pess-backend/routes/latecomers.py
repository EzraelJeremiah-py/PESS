from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.latecomer import LateComer

late_bp = Blueprint('late', __name__, url_prefix='/late')

@late_bp.route('/admin', methods=['GET', 'POST'])
def manage_latecomers():
    if request.method == 'POST':
        student = request.form['student_name']
        class_name = request.form['class_name']
        stream = request.form['stream']
        reason = request.form['reason']
        db.session.add(LateComer(student_name=student, class_name=class_name, stream=stream, reason=reason))
        db.session.commit()
    latecomers = LateComer.query.order_by(LateComer.created_at.desc()).all()
    return render_template('admin/latecomers.html', latecomers=latecomers)

@late_bp.route('/')
def list_latecomers():
    latecomers = LateComer.query.order_by(LateComer.created_at.desc()).all()
    return render_template('latecomers.html', latecomers=latecomers)

@late_bp.route('/update/<int:id>/<string:status>')
def update_status(id, status):
    lc = LateComer.query.get_or_404(id)
    lc.status = status
    db.session.commit()
    return redirect(url_for('late.manage_latecomers'))

@late_bp.route('/delete/<int:id>')
def delete_latecomer(id):
    lc = LateComer.query.get_or_404(id)
    db.session.delete(lc)
    db.session.commit()
    return redirect(url_for('late.manage_latecomers'))
