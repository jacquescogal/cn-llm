run_build:
	chmod +x ./database/hanzi_scripts/1-schema.sql
	chmod +x ./database/hanzi_scripts/2-prepopulate.sql
	docker-compose up --build
	
run:
	chmod +x ./database/hanzi_scripts/1-schema.sql
	chmod +x ./database/hanzi_scripts/2-prepopulate.sql
	docker-compose up

stop:
	docker-compose down

reset:
	docker-compose down -v