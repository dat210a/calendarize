Requirement:
- Flask, python
- pip install Flask-Mail


So far:
- Checking if the input email is registered in database:
- Yes > Send an email with reset password link ( still need to work with reset-link)
- No > Flash an error message.
- When user enter the reset-link (http://localhost:5000/reset/<resetlink>
- With valid reset-key --> Reset password page. --> Store new password in database.
- Invalid key --> error message.

TODO:
- Generate unique reset-key and store in database.
- Make the link 1 time usable within 24 hours
