.PHONY: all migrate up down runcommand build 

APPNAME="Commerce-fm"
APPSLUG=commerce_fm
command=createsuperuser

# target: all - Display help
all:
	@echo -e "\nMakefile for $(APPNAME)\nSyntax:\n"
	@echo -e "make <option>\n"
	@egrep -o "^# target:.*" [Mm]akefile | sed 's/# target: /    /'
	@echo ""


# target: up - Start the server
up:
	docker-compose up

# target: build - Build the docker
build:
	docker-compose build

# target: down - Stop the server
down:
	docker-compose down

# target: migrate - Migrate django models
migrate:
	docker-compose run --rm backend python3 manage.py migrate

# target: runcommand - Run a django command.
runcommand:
	docker-compose run --rm backend python3 manage.py $(command)


