#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	The Jupyter Notebook Format
Summary(pl.UTF-8):	Format Jupyter Notebook
Name:		python-nbformat
Version:	4.4.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/nbformat/
Source0:	https://files.pythonhosted.org/packages/source/n/nbformat/nbformat-%{version}.tar.gz
# Source0-md5:	2d5f873138d9fbc2a3f9eaaebca3b8a1
Patch0:		%{name}-use_setuptools.patch
URL:		https://pypi.org/project/nbformat/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-ipython_genutils
BuildRequires:	python-jsonschema >= 2.5.1
BuildRequires:	python-jupyter_core
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
BuildRequires:	python-testpath
BuildRequires:	python-traitlets >= 4.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-jsonschema >= 2.5.1
BuildRequires:	python3-jupyter_core
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-testpath
BuildRequires:	python3-traitlets >= 4.1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-jsonschema >= 2.5.1
#BuildRequires:	python3-jupyter_core
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nbformat contains the reference implementation of the Jupyter Notebook
format and Python APIs for working with notebooks.

%description -l pl.UTF-8
nbformat zawiera wzorcową implementację formatu Jupyter Notebook oraz
API Pythona do pracy z takimi notatnikami.

%package -n python3-nbformat
Summary:	The Jupyter Notebook Format
Summary(pl.UTF-8):	Format Jupyter Notebook
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-nbformat
nbformat contains the reference implementation of the Jupyter Notebook
format and Python APIs for working with notebooks.

%description -n python3-nbformat -l pl.UTF-8
nbformat zawiera wzorcową implementację formatu Jupyter Notebook oraz
API Pythona do pracy z takimi notatnikami.

%package apidocs
Summary:	API documentation for Python nbformat module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona nbformat
Group:		Documentation

%description apidocs
API documentation for Python nbformat module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona nbformat.

%prep
%setup -q -n nbformat-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest nbformat/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest nbformat/tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jupyter-trust{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jupyter-trust{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/jupyter-trust-2
%{py_sitescriptdir}/nbformat
%{py_sitescriptdir}/nbformat-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-nbformat
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/jupyter-trust-3
%{py3_sitescriptdir}/nbformat
%{py3_sitescriptdir}/nbformat-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
