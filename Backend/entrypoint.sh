#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic

# Add this block to create a superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); user_exists = User.objects.filter(username='$DJANGO_SU_NAME').exists(); User.objects.create_superuser('$DJANGO_SU_NAME', '$DJANGO_SU_EMAIL', '$DJANGO_SU_PASSWORD') if not user_exists else None" | python3 manage.py shell

exec "$@"
