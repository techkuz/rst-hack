DOCKER_IMAGE_NODE = node:12-alpine

build: data
	@docker run --rm -it \
			--name build \
			-v $(CURDIR):/app \
			-w /app \
			$(DOCKER_IMAGE_NODE) \
			npm install && npm run build && npm run dataset

data:
	@mkdir -p data

.PHONY: data
