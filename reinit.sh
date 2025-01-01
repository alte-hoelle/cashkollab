rm db.sqlite3
poetry run python src/manage.py migrate
poetry run python src/manage.py import
echo "from hellusers.models import HellUser; HellUser.objects.create_superuser('admin', 'admin@example.com', '12345')" | poetry run python src/manage.py shell 
#python src/manage.py runserver