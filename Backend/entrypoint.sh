#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_MAP_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python3 manage.py makemigrations
python3 manage.py migrate
#python3 manage.py collectstatic --noinput

# Add this block to create a superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); user_exists = User.objects.filter(username='$SUPER_USER_USERNAME').exists(); User.objects.create_superuser('$SUPER_USER_NAME', '$SUPER_USER_EMAIL', '$SUPER_USER_PASSWORD') if not user_exists else None" | python3 manage.py shell

exec "$@"
