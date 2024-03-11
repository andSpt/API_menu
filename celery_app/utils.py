from email.message import EmailMessage


SMTP_HOST = "smtp.yandex.ru"
SMTP_PORT = 465
SMTP_USER = "Antestov1@yandex.ru"
SMTP_PASSWORD = "wrxvmwjjazkqltgj"


def generate_confirmation_email(
    username: str, confirmation_token: str, user_email: str
) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Подтверждение регистрации"
    email["From"] = SMTP_USER
    email["To"] = user_email

    confirmation_link: str = (
        f"http://127.0.0.1:8040/api/v1/user/confirm/{confirmation_token}"
    )

    email.set_content(
        f"Здравствуйте, {username}\n\n"
        f"Спасибо за регистрацию на нашем сайте. Для завершения регистрации, пожалуйста, перейдите по следующей ссылке:\n"
        f"{confirmation_link}\n\n"
        f"Если вы не регистрировались на нашем сайте, пожалуйста, проигнорируйте это сообщение.\n\n"
        f"С уважением,\n"
        f"Команда нашего сайта"
    )

    return email
