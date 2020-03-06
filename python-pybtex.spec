Name:           python-pybtex
Version:        0.21
Release:        8
Summary:        Pybtex is a BibTeX-compatible bibliography processor
License:        MIT
URL:            http://pybtex.org/
Source0:        https://files.pythonhosted.org/packages/source/p/pybtex/pybtex-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python2-latexcodec python2-nose python2-pyglet python2-setuptools
BuildRequires:  python2-sphinx python2-yaml python3-devel python3-latexcodec python3-nose
BuildRequires:  python3-pyglet python3-setuptools python3-sphinx python3-yaml
# Fix stuff that 2to3 didn't catch
Patch0000:      python-pybtex-python36.patch

%description
The package is a BibTeX-compatible bibliography processor written in Python. You can simply type
pybtex instead of bibtex. Pybtex aims to be 100% compatible with BibTeX. It accepts the same command
line options, fully supports BibTeX’s .bst styles and produces byte-identical output.

%package -n     python2-pybtex
Summary:        BibTeX-compatible bibliography processor written in Python
Requires:       python2-latexcodec python2-pyglet python2-yaml
Provides:       bundled(jquery) bundled(js-underscore)
%{?python_provide:%python_provide python2-pybtex}

%description -n python2-pybtex
The package is a BibTeX-compatible bibliography processor written in Python. You can simply type
pybtex instead of bibtex. Pybtex aims to be 100% compatible with BibTeX. It accepts the same command
line options, fully supports BibTeX’s .bst styles and produces byte-identical output.

%package -n     python3-pybtex
Summary:        BibTeX-compatible bibliography processor written in Python
Requires:       python3-latexcodec python3-pyglet python3-yaml
Provides:       bundled(jquery) bundled(js-underscore)
%{?python_provide:%python_provide python3-pybtex}

%description -n python3-pybtex
The package is a BibTeX-compatible bibliography processor written in Python. You can simply type
pybtex instead of bibtex. Pybtex aims to be 100% compatible with BibTeX. It accepts the same command
line options, fully supports BibTeX’s .bst styles and produces byte-identical output.

%package        help
Summary:        Help documentation for python-pybtex
Provides:       python-pybtex-doc = %{version}-%{release}
Obsoletes:      python-pybtex-doc < %{version}-%{release}

%description    help
Help documentation for python-pybtex.

%prep
%setup -q -c
sed -i '\@/usr/bin/env python@d' pybtex-%{version}/pybtex/cmdline.py
cp -a pybtex-%{version} python3-pybtex-%{version}
cd pybtex-%{version}
for fil in pybtex/charwidths/make_charwidths.py pybtex/database/{convert,format}/__main__.py pybtex/__main__.py;
do
  sed -i 's/env python/python2/' $fil
done
cd -

cd python3-pybtex-%{version}
%patch0
for fil in pybtex/charwidths/make_charwidths.py pybtex/database/{convert,format}/__main__.py pybtex/__main__.py;
do
  sed -i 's/env python/python3/' $fil
done
cd -

%build
cd pybtex-%{version}
%py2_build
cd -
cd python3-pybtex-%{version}
%py3_build
cd -
pushd python3-pybtex-%{version}
PYTHONPATH=$PWD:$PWD/build/lib make -C docs html SPHINXBUILD=%{_bindir}/sphinx-build-%{python3_version}
rm -f docs/build/html/.buildinfo
cd -

%install
cd pybtex-%{version}
%py2_install
mkdir -p %{buildroot}%{_mandir}
cp -a docs/man1 %{buildroot}%{_mandir}
cd -
cd %{buildroot}%{python2_sitelib}
rm -fr custom_fixers pybtex/tests
chmod a+x pybtex/charwidths/make_charwidths.py pybtex/database/{convert,format}/__main__.py pybtex/__main__.py
cd -
cd python3-pybtex-%{version}
%py3_install
cd -
cd %{buildroot}%{python3_sitelib}
rm -fr custom_fixers pybtex/tests
chmod a+x pybtex/charwidths/make_charwidths.py pybtex/database/{convert,format}/__main__.py pybtex/__main__.py
cd -

%check
cd pybtex-%{version}
PYTHONPATH=$PWD:$PWD/build/lib nosetests-%{python2_version} -v
cd -
cd python3-pybtex-%{version}
cd build/lib; tar cBf - pybtex | (cd -; tar xBf -)
cd -
PYTHONPATH=$PWD:$PWD/build/lib nosetests-%{python3_version} -v
cd -

%files -n python2-pybtex
%doc pybtex-%{version}/README pybtex-%{version}/COPYING
%{python2_sitelib}/pybtex*

%files -n python3-pybtex
%doc python3-pybtex-%{version}/README python3-pybtex-%{version}/COPYING
%{python3_sitelib}/pybtex*
%{_bindir}/pybtex*

%files help
%doc python3-pybtex-%{version}/{CHANGES,docs/build/html}
%{_mandir}/man1/pybtex*

%changelog
* Fri Mar 6 2020 Ling Yang <lingyang2@huawei.com> - 0.21-8
- Package Init
