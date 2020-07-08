%ifarch %{ix86} %{x8664} x32
%define		with_gl		1
%endif

%define		qtver	5.7
Summary:	Screen recorder for Linux
Summary(pl.UTF-8):	Nagrywarka ekranu dla Linuksa
Name:		simplescreenrecorder
Version:	0.4.2
Release:	1
License:	GPL v3
Group:		Applications
Source0:	https://github.com/MaartenBaert/ssr/archive/%{version}/ssr-%{version}.tar.gz
# Source0-md5:	c43eb407d13006e0173f087ba5111214
Patch0:		build.patch
URL:		http://www.maartenbaert.be/simplescreenrecorder/
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake >= 3.1
BuildRequires:	ffmpeg-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5Gui >= %{qtver}
Requires:	Qt5Gui-platform-xcb
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5X11Extras >= %{qtver}
%if %{with gl}
Suggests:	%{name}-glinject = %{version}-%{release}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SimpleScreenRecorder is a screen recorder for Linux. Despite the name,
this program is actually quite complex. It's 'simple' in the sense
that it's easier to use than ffmpeg/avconv or VLC :).

%package glinject
Summary:	SimpleScreenRecorder - wrapper library for recording OpenGL
Group:		Applications

%description glinject
A wrapper library and a script to inject screen recording calls into
OpenGL applications, for use with the SimpleScreenRecorder.

%prep
%setup -q -n ssr-%{version}
%patch0 -p1

%build
%cmake \
	-DLRELEASE=/usr/bin/lrelease-qt5 \
	%{cmake_on_off gl WITH_GLINJECT} \
	%{cmake_on_off gl WITH_OPENGL_RECORDING} \
	-DWITH_JACK=ON \
	-DWITH_PULSEAUDIO=ON \
	-DWITH_QT5=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md *.txt
%attr(755,root,root) %{_bindir}/simplescreenrecorder
%dir %{_datadir}/simplescreenrecorder
%{_datadir}/simplescreenrecorder/output-profiles
%dir %{_datadir}/simplescreenrecorder/translations
%{_mandir}/man1/simplescreenrecorder.1*
%{_iconsdir}/*/*/apps/simplescreenrecorder*.png
%{_iconsdir}/hicolor/scalable/apps/simplescreenrecorder*.svg
%{_desktopdir}/simplescreenrecorder.desktop
%{_datadir}/metainfo/simplescreenrecorder.metainfo.xml

%if %{with glinject}
%files glinject
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ssr-glinject
%attr(755,root,root) %{_libdir}/libssr-glinject.so
%{_mandir}/man1/ssr-glinject.1*
%endif
