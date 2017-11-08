from classes.db_queries import ConnectionInstance
from flask import Flask, request, flash, render_template
from funcs.logIn import check_password, hash_password

def reset_password(email):
    new_password = request.form.get("new_password", None)
    repeat_password = request.form.get("repeat_password", None)
    if not new_password or not repeat_password:
        flash("Please fill in both fields")
    elif len(new_password) < 6:
        flash("Minimum 6 characters.")
    elif new_password == repeat_password:
        if check_password(new_password, email):
            flash("You cannot use your old password.")
        else:
            with ConnectionInstance() as queries:
                queries.set_new_password(email,hash_password(new_password))
                return True
    else:
        flash("Your inputs do not match")
    return False
