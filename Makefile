install:
	cd project/backend && pip install -r requirements.txt
	cd project/frontend && npm i

dev:
	$(MAKE) dev-back & $(MAKE) dev-front

dev-back:
	cd project/backend && flask run --port=5000

dev-front:
	cd project/frontend && npm run dev

build:
	cd project/frontend && npm run build:prod

deploy:
	@echo "Add docker-compose in deploy/ to enable this target"