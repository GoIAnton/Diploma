# Diploma
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
winpty docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input