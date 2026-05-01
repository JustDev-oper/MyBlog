include .env
export


up:
	@docker compose up -d db
	docker compose up --build app

down:
	@docker compose down db
	docker compose down app

cleanup:
	@read -p "Вы уверены, что хотите удалить все данные? (y/n): " ans; \
	if [ "$$ans" = "y" ]; then \
	  		docker compose down db && \
	  		rm -rf out/pgdata && \
	  		echo "Данные удалены."; \
	else \
	  		echo "Операция отменена."; \
	fi

port-forward:
	@docker compose up -d port-forwarder

port-close:
	@docker compose down port-forwarder