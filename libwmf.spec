Summary:	libwmf, library to convert wmf files
Name:		libwmf
Version:	0.1.17
Release:	2
Serial:		2
License:	GPL
Group:		Utilities/Text
Group(fr):	Utilitaires/Texte
Group(pl):	Narzêdzia/Tekst
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Source0:	http://www.csn.ul.ie/~caolan/publink/libwmf/%{name}-%{version}.tar.gz
Patch0:		libwmf-DESTDIR.patch
URL:		http://www.csn.ul.ie/~caolan/docs/libwmf.html
Requires:	freetype
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libwmf is a library for unix like machines that can convert wmf files
into other formats, currently it supports a gd binding to convert to
gif, and an X one to draw direct to an X window or pixmap.

%prep
%setup -q -n %{name}
%patch -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf winepatches/* CHANGELOG CREDITS README libwmf.lsm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc examples notes winepatches {CHANGELOG,CREDITS,README,libwmf.lsm}.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
%{_includedir}/*
