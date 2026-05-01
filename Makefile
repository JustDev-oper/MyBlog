include .env
export


env-up:
	@docker compose up -d db
	docker compose up app

env-down:
	@docker compose down db
	docker compose down app

env-cleanup:
	@read -p "Вы уверены, что хотите удалить все данные? (y/n): " ans; \
	if [ "$$ans" = "y" ]; then \
	  		docker compose down db && \
	  		rm -rf out/pgdata && \
	  		echo "Данные удалены."; \
	else \
	  		echo "Операция отменена."; \
	fi

env-port-forward:
	@docker compose up -d port-forwarder

env-port-close:
	@docker compose down port-forwarder