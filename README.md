# Diploma
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
winpty docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py load_tags
docker-compose exec web python manage.py load_users
docker-compose exec web python manage.py load_publications
docker-compose exec web python manage.py load_likes
# Tests
docker-compose exec web python manage.py test pages.tests.test_for_anon
docker-compose exec web python manage.py test pages.tests.test_for_auth
docker-compose exec web python manage.py test pages.tests.test_for_moder
docker-compose exec web python manage.py test pages.tests.test_for_safe