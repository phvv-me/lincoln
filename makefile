install:
	python3 -m pip install \
		-r src/services/backend/requirements.txt \
		-t src/services/backend/deploy/lambda_layer/python/lib/python3.8/site-packages/.

deploy:
	terraform apply --auto-approve