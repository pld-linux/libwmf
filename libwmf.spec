Summary:	libwmf, library to convert wmf files.
Name:		libwmf
Version:	0.1.11
Release:	1
Serial:		2
Copyright:	GPL
Group:		Utilities/Text
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Source:		http://www.csn.ul.ie/~caolan/publink/libwmf/%{name}-%{version}.tar.gz
Patch:		libwmf-DESTDIR.patch
URL:		http://www.csn.ul.ie/~caolan/docs/libwmf.html
Requires:	freetype
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libwmf is a library for unix like machines that can convert wmf files into
other formats, currently it supports a gd binding to convert to gif, and an
X one to draw direct to an X window or pixmap.

%prep
%setup -q -n %{name}
%patch -p1

%build
LDFLAGS="-s"; export LDFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

make install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf winepatches/* CHANGELOG CREDITS README TODO libwmf.lsm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc examples notes winepatches {CHANGELOG,CREDITS,README,TODO,libwmf.lsm}.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
%{_includedir}/*
