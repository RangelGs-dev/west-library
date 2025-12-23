#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [[ "$CREATE_SUPERUSER" == "true" ]]; then
    echo "Verificando superusuário..."

    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

username = "${DJANGO_SUPERUSER_USERNAME}"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
    print("Superusuário criado.")
else:
    print("Superusuário já existe, pulando.")
END
else
    echo "CREATE_SUPERUSER=false, pulando criação."
fi