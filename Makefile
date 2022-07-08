test:
	@coverage run --source=diegorocha manage.py test
	@coverage html --omit=*/migrations/*,*/wsgi.py,*/tests.py,*/apps.py,*/settings.py -d coverage

ecr-login:
	aws ecr get-login-password --region us-east-1  | docker login --username AWS --password-stdin 215758104365.dkr.ecr.us-east-1.amazonaws.com

build:
	echo "Cleaning dist"
	rm -rf dist/*

	echo "Copying statics"
	cp -r src/static dist/

	FLASK_SKIP_DOTENV=1 FLASK_ENV=development FLASK_APP=src/app.py flask generate_static_html --directory dist

release: build
	aws s3 sync dist/ s3://diegorocha.com.br/
