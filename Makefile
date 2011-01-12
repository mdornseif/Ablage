deploy: dependencies
	# check
	# index must be clean
	git diff-index --quiet --cached HEAD
	# no uncomitted changes
	git diff-files --quiet
	git branch -f deploy_`grep -E '^version: ' app.yaml | cut -d ' ' -f 2`
	git push -f . deploy_`grep -E '^version: ' app.yaml | cut -d ' ' -f 2`
	appcfg.py update .

check: lib/google_appengine/google/__init__.py
	pep8 -r --ignore=E501 ablage/ *.py
	sh -c 'PYTHONPATH=`python ./config.py` pyflakes ablage/ *.py'
	-sh -c 'PYTHONPATH=`python ./config.py` pylint -iy --max-line-length=110 ablage/ *.py' # -rn

lib/google_appengine/google/__init__.py:
	curl -O http://googleappengine.googlecode.com/files/google_appengine_1.3.8.zip
	unzip google_appengine_1.3.8.zip
	rm -Rf lib/google_appengine
	mv google_appengine lib/
	rm google_appengine_1.3.8.zip

dependencies:
	git submodule update --init lib/huTools
	git submodule update --init lib/gaetk
	git submodule update --init lib/jinja2

clean:
	rm -Rf pythonenv/
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: deploy pylint dependencies_for_check_target clean check dependencies
