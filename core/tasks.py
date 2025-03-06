import os
from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
import requests


@shared_task
def send_generic_email_test(subject, txt_, from_email, recipient_list, html_):
    pass


@shared_task
def send_generic_email(subject, txt_, from_email, recipient_list, html_):
    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )






@shared_task
def send_user_data_email_task(subject, message, from_email, recipient_list):
    send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )



@shared_task
def send_telegram_user_data_task(app_settings, message, ):
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





@shared_task
def save_data_to_file_task(email, message):
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
