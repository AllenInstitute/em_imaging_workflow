APP_PACKAGE = at_em_imaging_workflow
PROJECTNAME = $(APP_PACKAGE)
DISTDIR = dist
BUILDDIR = build
RELEASEDIR = $(PROJECTNAME)-$(VERSION)$(RELEASE)
EGGINFODIR = $(PROJECTNAME).egg-info
DOCDIR = doc
COVDIR = htmlcov

DOC_URL=http://alleninstitute.github.io/AtEmImagingWorkflow

build:
	mkdir -p $(DISTDIR)/$(PROJECTNAME) 
	cp -r at_em_imaging_workflow setup.py README.md $(DISTDIR)/$(PROJECTNAME)/
	cd $(DISTDIR); tar czvf $(PROJECTNAME).tgz --exclude .git $(PROJECTNAME)
	

distutils_build: clean
	python setup.py build

sdist: distutils_build
	python setup.py sdist

pypi_deploy:
	python setup.py sdist upload --repository local

# see pytest.ini for additional configuration
pytest_lax:
	rm database.db || exit 0
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
	python setup.py test 

pytest: pytest_lax

test: pytest

pytest_pep8:
	find -L . -name "test_*.py" -exec py.test --boxed --pep8 --cov-config coveragerc --cov=$(APP_PACKAGE) --cov-report html --junitxml=test-reports/test.xml {} \+

pytest_lite:
	find -L . -name "test_*.py" -exec py.test --boxed --assert=reinterp --junitxml=test-reports/test.xml {} \+

prospector:
	prospector > htmlcov/pylint.txt || exit 0
	grep import htmlcov/pylint.txt > htmlcov/pylint_imports.txt

pylint:
	pylint --disable=C $(APP_PACKAGE) > htmlcov/pylint.txt || exit 0
	grep import-error htmlcov/pylint.txt > htmlcov/pylint_imports.txt

flake8:
	flake8 --ignore=E201,E202,E226 --max-line-length=200 --filename 'at_em_imaging_workflow/**/*.py' at_em_imaging_workflow | grep -v "local variable '_' is assigned to but never used" > htmlcov/flake8.txt
	grep -i "import" htmlcov/flake8.txt > htmlcov/imports.txt || exit 0

EXAMPLES=doc/_static/examples

fsm_figures:
	python -m manage graph_transitions -o doc_template/aibs_sphinx/static/reference_set_states.png at_em_imaging_workflow.ReferenceSet
	python -m manage graph_transitions -o doc_template/aibs_sphinx/static/chunk_states.png at_em_imaging_workflow.Chunk
	python -m manage graph_transitions -o doc_template/aibs_sphinx/static/load_states.png at_em_imaging_workflow.Load
	python -m manage graph_transitions -o doc_template/aibs_sphinx/static/e_m_montage_set_states.png at_em_imaging_workflow.EMMontageSet


doc: FORCE
	sphinx-apidoc -d 4 --force -H "AT EM Imaging Workflow" -A "Allen Institute for Brain Science" -V $(VERSION) -R $(VERSION)$(RELEASE) --full -o doc --module-first $(PROJECTNAME)
	cp doc_template/*.rst doc_template/conf.py doc
	# cp -R doc_template/examples $(EXAMPLES)
	cp -R htmlcov doc/_static
	sed -i --expression "s/|version|/${VERSION}/g" doc/conf.py
	cp -R doc_template/aibs_sphinx/static/* doc/_static
	cp -R doc_template/aibs_sphinx/templates/* doc/_templates
ifdef STATIC
	sed -i --expression "s/\/_static\/external_assets/${STATIC}\/external_assets/g" doc/_templates/layout.html
	sed -i --expression "s/\/_static\/external_assets/${STATIC}\/external_assets/g" doc/_templates/portalHeader.html
	sed -i --expression "s/\/_static\/external_assets/${STATIC}\/external_assets/g" doc/_templates/portalFooter.html
endif
	cd doc && make html || true

FORCE:

clean:
	rm -rf $(DISTDIR)
	rm -rf $(BUILDDIR)
	rm -rf $(RELEASEDIR)
	rm -rf $(EGGINFODIR)
	rm -rf $(DOCDIR)
