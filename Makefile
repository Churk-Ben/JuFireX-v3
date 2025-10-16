install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm i

dev:
	$(MAKE) dev-back & $(MAKE) dev-front

dev-back:
	cd backend && flask run --port=5000

dev-front:
	cd frontend && npm run dev -- --host 0.0.0.0

build:
	cd frontend && npm run build:prod

deploy:
	@echo "Add docker-compose in deploy/ to enable this target"