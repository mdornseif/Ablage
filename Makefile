dependencies: update_templates
	virtualenv pythonenv
	pip -q install -E pythonenv -r requirements.txt
	find pythonenv/ -name 'settings.py*' -delete

generic_templates:
	git clone git@github.com:hudora/html.git generic_templates

update_templates: generic_templates
	cd generic_templates ; git pull ; cd -
