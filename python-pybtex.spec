%define oname   pybtex
Name:           python-pybtex
Version:        0.24.0
Release:        1
Summary:        Pybtex is a BibTeX-compatible bibliography processor
License:        MIT
URL:            http://pybtex.org/
Source0:        https://files.pythonhosted.org/packages/source/p/pybtex/pybtex-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel python3-latexcodec python3-pytest
BuildRequires:  python3-setuptools python3-sphinx python3-yaml

%description
The package is a BibTeX-compatible bibliography processor written in Python. You can simply type
pybtex instead of bibtex. Pybtex aims to be 100% compatible with BibTeX. It accepts the same command
line options, fully supports BibTeX’s .bst styles and produces byte-identical output.

%package -n     python3-pybtex
Summary:        BibTeX-compatible bibliography processor written in Python
Requires:       python3-latexcodec python3-yaml
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

%build
cd pybtex-%{version}
%py3_build
cd -
pushd pybtex-%{version}
PYTHONPATH=$PWD:$PWD/build/lib make -C docs html SPHINXBUILD=%{_bindir}/sphinx-build-%{python3_version}
rm -f docs/build/html/.buildinfo
cd -

%install
cd pybtex-%{version}
%py3_install
cd -
cd %{buildroot}%{python3_sitelib}
rm -fr custom_fixers tests
chmod a+x pybtex/charwidths/make_charwidths.py pybtex/database/{convert,format}/__main__.py pybtex/__main__.py
# install man
cd -
cd pybtex-%{version}
for man in %{oname} %{oname}-convert %{oname}-format ; do
  install -Dpm 0644 docs/man1/${man}.1 %{buildroot}%{_mandir}/man1/${man}.1
done

%check
cd pybtex-%{version}
cd build/lib; tar cBf - pybtex | (cd -; tar xBf -)
cd -
pytest
cd -

%files -n python3-pybtex
%doc pybtex-%{version}/README pybtex-%{version}/COPYING
%{python3_sitelib}/pybtex*
%{_bindir}/pybtex*

%files help
%doc pybtex-%{version}/{CHANGES,docs/build/html}
%{_mandir}/man1/pybtex*

%changelog
* Tue May 31 2022 lvxiaoqian <xiaoqian@nj.iscas.ac.cn> - 0.24.0-1
- update to 0.24.0

* Fri Mar 6 2020 Ling Yang <lingyang2@huawei.com> - 0.21-8
- Package Init
