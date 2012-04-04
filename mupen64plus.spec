Name:			mupen64plus
Version:		1.99.5
Release:		%mkrel 1

Summary:	Nintendo 64 Emulator (GTK Gui)
License:	GPLv2+
Group:		Emulators
URL:		http://code.google.com/p/mupen64plus/
Source0:	mupen64plus-bundle-src-%{version}.tar.gz

BuildRequires:	SDL-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	gtk2-devel
BuildRequires:	lirc-devel
BuildRequires:	libsamplerate-devel 
BuildRoot:	%{_tmppath}/%{name}-%{version}

Conflicts:	mupen64plus-qt
Conflicts:	mupen64plus-cli

%description
Mupen64plus is a Nintendo 64 Emulator.
This package includes a GTK front-end and all the plug-ins.

This package is in PLF as Mandriva Linux policy forbids emulators.

%prep
%setup -q -n mupen64plus-bundle-src-%{version}

%build
./m64p_build.sh

%install
rm -rf %{buildroot}
make -C source/mupen64plus-core/projects/unix install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir}/mupen64plus MANDIR=%{buildroot}%{_mandir}
make -C source/mupen64plus-ui-console/projects/unix install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir}/mupen64plus MANDIR=%{buildroot}%{_mandir}
make -C source/mupen64plus-audio-sdl/projects/unix install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir}/mupen64plus MANDIR=%{buildroot}%{_mandir}
make -C source/mupen64plus-input-sdl/projects/unix install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir}/mupen64plus MANDIR=%{buildroot}%{_mandir}
make -C source/mupen64plus-rsp-hle/projects/unix install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir}/mupen64plus MANDIR=%{buildroot}%{_mandir}
make -C source/mupen64plus-video-rice/projects/unix install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir}/mupen64plus MANDIR=%{buildroot}%{_mandir}/man1
# ln -s libmupen64plus.so.2.0.0 %{buildroot}%{_libdir}/%{name}/libmupen64plus.so.2
pushd %{buildroot}%{_prefix}
# ln -s %{_libdir}/mupen64plus  %{buildroot}%{_datadir}/mupen64plus/plugins
popd

# desktop-file-install --vendor="" \
# --remove-category="Game" \
# --add-category="X-MandrivaLinux-MoreApplications-Emulators" \
# --add-category="Emulator" \
# --dir=%{buildroot}%{_datadir}/applications \
#  %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}

%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root)
%{_bindir}/mupen64plus
%{_libdir}/mupen64plus
%{_datadir}/mupen64plus
# %{_datadir}/applications/mupen64plus.desktop
%{_mandir}/*
%{_includedir}/%{name}/*.h

%changelog
* Tue Jan  6 2009 Guillaume Bedot <littletux@zarb.org> 1.5-1plf2009.1
- First package of mupen64plus for PLF, requested by Zombie Ryushu
