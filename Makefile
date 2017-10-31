bumpversion:
	bumpversion $(bump)

push:
	git push && git push --tags

sdist:
	python setup.py sdist

upload:
	twine upload dist/uspto-opendata-python-*.tar.gz

# make release bump=minor  (major,minor,patch)
release: bumpversion push sdist upload


mkvar:
	mkdir -p var/lib

redis-start: mkvar
	echo 'dir ./var/lib' | redis-server -

celery-start: mkvar
	@# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#starting-the-scheduler
	celery worker --app uspto.celery.tasks --beat --schedule-filename var/lib/celerybeat-schedule --loglevel=info


docs-virtualenv:
	$(eval venvpath := ".venv_sphinx")
	@test -e $(venvpath)/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages $(venvpath)
	@$(venvpath)/bin/pip --quiet install --requirement requirements-docs.txt

docs-html: docs-virtualenv
	$(eval venvpath := ".venv_sphinx")
	touch docs/index.rst
	export SPHINXBUILD="`pwd`/$(venvpath)/bin/sphinx-build"; cd docs; make html
