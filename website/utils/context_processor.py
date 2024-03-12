from website import db
from website.models import Attorney
from flask import current_app as app


@app.context_processor
def inject_employees():
    """
    :return: dict object containing all employees from database in {id: employee,...} format
    """
    # employees = db.session.query(Attorney).all()
    employees = Attorney.query.order_by(Attorney.id).all()

    return dict(employees=employees)
