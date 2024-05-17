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


@app.context_processor
def camel_case_formatter():
    """
    :return: dict object containing function that turns a string into CamelCase for use in templates
    """
    def to_camel_case(string):
        camel_case_string = ''
        upper_case_next = False
        for letter in string:
            if letter == '_' or letter == " ":
                upper_case_next = True
            else:
                if upper_case_next:
                    camel_case_string += letter.upper()
                else:
                    camel_case_string += letter
                upper_case_next = False
        return camel_case_string

    return dict(to_camel_case=to_camel_case)
