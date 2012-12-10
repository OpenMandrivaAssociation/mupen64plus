%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:		mupen64plus
Version:	1.99.5
Release:	3
Summary:	Plugin-Based Nintendo 64 Emulator
Group:		Emulators
License:	GPLv2+
Url:		http://code.google.com/p/mupen64plus/
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	lirc-devel
Source:		%{name}-bundle-src-%{version}.tar.gz
Source100:	%{name}-rpmlintrc
Patch0:		mupen64plus-zlib.patch

%description
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games. It includes four MIPS R4300 CPU emulators, with dynamic
recompilers for 32-bit x86 and 64-bit amd64 systems.  It supports plugins for
audio, graphical rendering (RDP), the signal co-processor (RSP), and input.

%package -n %{libname}
Summary:	Shared Library Interface to Mupen64plus
Group:		System/Libraries
Requires:	fonts-ttf-dejavu

%description -n %{libname}
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games. It includes four MIPS R4300 CPU emulators, with dynamic
recompilers for 32-bit x86 and 64-bit amd64 systems.  It supports plugins for
audio, graphical rendering (RDP), the signal co-processor (RSP), and input.

This package contains the shared library interface for frontends.

%package -n %{develname}
Summary:	Include Files for Mupen64plus Development
License:	GPLv2+
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains all necessary include files to develop frontends against
the Mupen64plus shared library interface.

%package ui-console
Summary:	Command Line Frontend for the Mupen64plus Nintendo 64 Emulator
Group:		Emulators
Provides:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	mupen64plus-plugin-audio
Requires:	mupen64plus-plugin-video
Requires:	mupen64plus-plugin-input
Requires:	mupen64plus-plugin-rsp-hle

%description ui-console
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games.

This package contains a command line frontend.

%package plugin-audio-sdl
Summary:	SDL Audio Plugin for the Mupen64plus Nintendo 64 Emulator
Group:		Emulators
Provides:	mupen64plus-plugin-audio

%description plugin-audio-sdl
This package contains the SDL audio plugin for the Mupen64plus Nintendo 64
Emulator.

%package plugin-input-sdl
Summary:	SDL Input Plugin for the Mupen64plus Nintendo 64 Emulator
Group:		Emulators
Provides:	mupen64plus-plugin-input

%description plugin-input-sdl
This package contains the SDL input plugin for the Mupen64plus Nintendo 64
Emulator. It has LIRC Infrared remote control interface and Rumble Pak support.

%package plugin-rsp-hle
Summary:	RSP High-Level Emulation Plugin For the Mupen64plus
Group:		Emulators
Provides:	mupen64plus-plugin-rsp-hle

%description plugin-rsp-hle
This package contains the RSP High-Level emulation plugin for the Mupen64plus
Nintendo 64 Emulator.

%package plugin-video-rice
Summary:	Rice Video Plugin for the Mupen64plus Nintendo 64 Emulator
License:	GPLv2+
Group:		Emulators
Provides:	mupen64plus-plugin-video

%description plugin-video-rice
This package contains the Rice Video Plugin for the Mupen64plus Nintendo 64
Emulator. It provides Hi-resolution texture support.

%prep
%setup -q -n %{name}-bundle-src-%{version}
%patch0 -p1

%build
export CFLAGS="%{optflags}"
%make -C source/mupen64plus-core/projects/unix all SHAREDIR=%{_datadir}/mupen64plus2/ LIRC=1 V=1
%make -C source/mupen64plus-ui-console/projects/unix all COREDIR=%{_libdir}/ SHAREDIR=%{_datadir}/mupen64plus2/ PLUGINDIR=%{_libdir}/mupen64plus2/ V=1
%make -C source/mupen64plus-audio-sdl/projects/unix all V=1
%make -C source/mupen64plus-input-sdl/projects/unix all V=1
%make -C source/mupen64plus-rsp-hle/projects/unix all V=1
%make -C source/mupen64plus-video-rice/projects/unix all V=1

%install
make -C source/mupen64plus-core/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" SHAREDIR=%{_datadir}/mupen64plus2/ LIBDIR=%{_libdir}/ INCDIR=%{_includedir}/mupen64plus/ LIRC=1
pushd %{buildroot}%{_libdir}
ln -sf libmupen64plus.so.2.0.0 libmupen64plus.so.2
ln -sf libmupen64plus.so.2.0.0 libmupen64plus.so
popd
make -C source/mupen64plus-ui-console/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" BINDIR=/usr/bin/ MANDIR=%{_mandir}/man6/ NO_ASM=1
# rm %{buildroot}%{_datadir}/mupen64plus2/font.ttf
make -C source/mupen64plus-audio-sdl/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" LIBDIR=%{_libdir}/mupen64plus2/
make -C source/mupen64plus-input-sdl/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" SHAREDIR=%{_datadir}/mupen64plus2/ LIBDIR=%{_libdir}/mupen64plus2/
make -C source/mupen64plus-rsp-hle/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" LIBDIR=%{_libdir}/mupen64plus2/
make -C source/mupen64plus-video-rice/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" SHAREDIR=%{_datadir}/mupen64plus2/ LIBDIR=%{_libdir}/mupen64plus2/

chmod -R 0755 %{buildroot}%{_libdir}

mv %{buildroot}/%{_libdir}/mupen64plus2/%{name}/mupen64plus*.so %{buildroot}/%{_libdir}/mupen64plus2/
rmdir %{buildroot}/%{_libdir}/mupen64plus2/%{name}

%files -n %{libname}
%dir %{_datadir}/mupen64plus2
%dir %{_libdir}/mupen64plus2
%{_libdir}/libmupen64plus.so.*
%{_datadir}/mupen64plus2/mupen64plus.cht
%{_datadir}/mupen64plus2/mupencheat.txt
%{_datadir}/mupen64plus2/mupen64plus.ini
%{_datadir}/mupen64plus2/font.ttf

%files -n %{develname}
%doc source/mupen64plus-core/INSTALL
%doc source/mupen64plus-core/LICENSES
%doc source/mupen64plus-core/README
%doc source/mupen64plus-core/RELEASE
%dir %{_includedir}/mupen64plus
%{_includedir}/mupen64plus/*
%{_libdir}/libmupen64plus.so

%files ui-console
%doc source/mupen64plus-ui-console/INSTALL
%doc source/mupen64plus-ui-console/LICENSES
%doc source/mupen64plus-ui-console/README
%doc source/mupen64plus-ui-console/RELEASE
%doc %{_mandir}/man6/man6/mupen64plus.*
%{_bindir}/mupen64plus

%files plugin-audio-sdl
%doc source/mupen64plus-audio-sdl/INSTALL
%doc source/mupen64plus-audio-sdl/LICENSES
%doc source/mupen64plus-audio-sdl/RELEASE
%{_libdir}/mupen64plus2/mupen64plus-audio-sdl.so

%files plugin-input-sdl
%doc source/mupen64plus-input-sdl/AUTHORS
%doc source/mupen64plus-input-sdl/COPYING
%doc source/mupen64plus-input-sdl/INSTALL
%doc source/mupen64plus-input-sdl/LICENSES
%doc source/mupen64plus-input-sdl/README
%doc source/mupen64plus-input-sdl/RELEASE
%{_datadir}/mupen64plus2/InputAutoCfg.ini
%{_libdir}/mupen64plus2/mupen64plus-input-sdl.so

%files plugin-rsp-hle
%doc source/mupen64plus-rsp-hle/INSTALL
%doc source/mupen64plus-rsp-hle/LICENSES
%doc source/mupen64plus-rsp-hle/RELEASE
%{_libdir}/mupen64plus2/mupen64plus-rsp-hle.so

%files plugin-video-rice
%doc source/mupen64plus-video-rice/INSTALL
%doc source/mupen64plus-video-rice/LICENSES
%doc source/mupen64plus-video-rice/README
%doc source/mupen64plus-video-rice/RELEASE
%{_datadir}/mupen64plus2/RiceVideoLinux.ini
%{_libdir}/mupen64plus2/mupen64plus-video-rice.so



%changelog
* Sat Apr 21 2012 Zombie Ryushu <ryushu@mandriva.org> 1.99.5-1.5mdv2012.0
+ Revision: 792592
- mupen64plus has no api tag only a major tag

* Fri Apr 20 2012 Zombie Ryushu <ryushu@mandriva.org> 1.99.5-1.4
+ Revision: 792478
- add support for arachnoid

* Thu Apr 05 2012 Zombie Ryushu <ryushu@mandriva.org> 1.99.5-1.3
+ Revision: 789467
- fix a typo
- fix a typo
- move plugins up one directory so executable can find them
- move plugins up one directory so executable can find them

* Thu Apr 05 2012 Zombie Ryushu <ryushu@mandriva.org> 1.99.5-1.2
+ Revision: 789310
- fix my man page screwup
- fix my man page screwup
- fix my screwup wrong spec file
- fix my screwup wrong spec file
- fix my screwup wrong spec file
- fix my screwup wrong spec file
- fix my screwup wrong spec file
- Patch for zlib detection
- Patch for zlib detection
- zlib support

* Wed Apr 04 2012 Zombie Ryushu <ryushu@mandriva.org> 1.99.5-1
+ Revision: 789223
- zlib support
- remove PLF tag
- Fix redundant symlinking
- Update to 1.99.5

* Sun Jul 31 2011 Andrey Bondrov <abondrov@mandriva.org> 1.5-3
+ Revision: 692528
- Rebuild
- Drop patch 10 as it breaks 64 bit version

* Wed Jul 27 2011 Andrey Bondrov <abondrov@mandriva.org> 1.5-2
+ Revision: 691880
- Add desktop-file-utils to BuildRequires
- Fix group
- imported package mupen64plus


* Sun Jul 23 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 1.5-2mdv2011.0
- Add patches from Debian
- Add keyboard default config patch from MIB
- Import from PLF
- Remove PLF reference

* Tue Jan  6 2009 Guillaume Bedot <littletux@zarb.org> 1.5-1plf2009.1
- First package of mupen64plus for PLF, requested by Zombie Ryushu
