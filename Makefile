build:
	docker-compose up --build -d

migrate:
	docker-compose run backend python manage.py makemigrations
	docker-compose run backend python manage.py migrate