Summary:	libwmf, library to convert wmf files.
Name:		libwmf
Version:	0.1.11
Release:	1
Serial:		2
Copyright:	GPL
Group:		Utilities/Text
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Source:		http://www.csn.ul.ie/~caolan/publink/libwmf/%{name}-%{version}.tar.gz
URL:		http://www.csn.ul.ie/~caolan/docs/libwmf.html
Requires:	freetype
BuildRoot:	/tmp/%{name}-%{version}-root

%description
libwmf is a library for unix like machines that can convert wmf files into
other formats, currently it supports a gd binding to convert to gif, and an
X one to draw direct to an X window or pixmap.

%prep
%setup -q -n %{name}
LDFLAGS="-s"; export LDFLAGS
%configure

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc examples notes winepatches CHANGELOG CREDITS README TODO libwmf.lsm
%{_bindir}/*
%{_libdir}/*
%{_includedir}/*

%changelog
* Mon May 24 1999 Ryan Weaver <ryanw@infohwy.com>
  [libwmf-0.1.10-1]
- removed c++ comment
- stripped ^M's out
- cast a few things to void pointers before assigning
  them to userdata.

* Wed May 19 1999 Ryan Weaver <ryanw@infohwy.com>
  [libwmf-0.1.9-2]
- New source tgz, same version, recompiling.
- Some changes to configure script and other files.

* Wed Apr 28 1999 Ryan Weaver <ryanw@infohwy.com>
  [libwmf-0.1.9-1]
- v 0.1.9
- added more bullet proofing against the sort of nightmare wmf's
  that come out of mswordview.
- some better error checking for missing fonts, (doh !)
- broke tt, fixed tt
- removd debugging messages.

* Fri Apr 23 1999 Ryan Weaver <ryanw@infohwy.com>
  [libwmf-0.1.8-1]
- v 0.1.8
- trivial change to wmfapi.h to make life easier with blip
  handling in mswordview
- made configure script get heroic when searching for components,
  checks for for includes and libs both below a --with-stuff dir, and
  also inside it as well.

* Tue Apr 13 1999 Ryan Weaver <ryanw@infohwy.com>
  [libwmf-0.1.7-1]
- Initial RPM Build
- 0.1.7
- added ability to gd to read xbm's from data, rather than file,
  changed source accordingly, dont need to carry xbm's around
  anymore.
- changed configure script to agressively find the xpm header file,
- tested to work under aix (of all things :-))
- tested to work under solaris.
- checked that it reports lack of xpm lib, and fails to go any
  further.
- fiddled a bit more, and libwmf now works cleanly with mswordview,
  all cheer.
