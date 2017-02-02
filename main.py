#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a>Signup</a>
    </h1>
"""

page_footer = """
</body>
</html>
"""

def create_form(username, error_username, error_password, error_verify, email, error_email):
    signup_form = '''
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username: </label></td>
                    <td><input name="username" type="text" value="{0}"></td>
                    <td class="error">{1}</td>
                </tr>
                <tr>
                    <td><label for="password">Password: </label></td>
                    <td><input name="password" type="password"></td>
                    <td class="error">{2}</td>
                </tr>
                <tr>
                    <td><label for="verify_password">Verify Password: </label></td>
                    <td><input name="verify_password" type="password"></td>
                    <td class="error">{3}</td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional): </label></td>
                    <td><input name="email" type="text" value="{4}"></td>
                    <td class="error">{5}</td>
                </tr>
            </table>
            <input type="submit">
        </form>'''.format(username, error_username, error_password, error_verify, email, error_email)
    return signup_form



user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and user_re.match(username)

pass_re = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and pass_re.match(password)

email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and email_re.match(email)


class Signup(webapp2.RequestHandler):
    
    def get(self):

        signup_form = create_form("","","","","","")
        content = page_header + signup_form + page_footer
        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify_password = self.request.get('verify_password')
        email = self.request.get('email')

        error_username = ""
        error_password= ""
        error_verify= ""
        error_email= ""

        if not valid_username(username):
            error_username = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            error_password = "That's not a valid password."
            have_error = True
        elif password != verify_password:
            error_verify = "Your passwords didn't match."
            have_error = True

        if email:    
            if not valid_email(email):
                error_email = "That's not a valid email."
                have_error = True

        if have_error:
            signup_form = create_form(username, error_username, error_password, error_verify, email, error_email)
            content = page_header + signup_form + page_footer
            self.response.write(content)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        content = page_header + "<h2> Welcome, " + username + "!</h2>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
