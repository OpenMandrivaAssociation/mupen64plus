Name:			mupen64plus
Version:		1.5
Release:		%mkrel 2

Summary:	Nintendo 64 Emulator (GTK Gui)
License:	GPLv2+
Group:		Emulators
URL:		http://code.google.com/p/mupen64plus/
Source0:	Mupen64Plus-1-5-src.tar.gz
Patch0:		ftbfs-gvariant-type-conflicts.patch
Patch1:		ftbfs-glibc210.patch
Patch2:		fix-7z-subfolder.patch
Patch3:		fix_readpng.patch
Patch4:		gtk-open-filter.patch
Patch5:		jttl_fix_romclosed.patch
Patch6:		load_aidacrate.patch
Patch7:		load_vistatus.patch
Patch8:		noexecstack.patch
Patch9:		osd-pause-crash.patch
Patch10:	plugin-searchpath.patch
Patch11:	resume_on_start.patch
Patch12:	rice-ati-symbols.patch
Patch13:	rice-crash-vendorstring.patch
Patch14:	rice-screenflickering.patch
Patch15:	rice-texturepack-crash.patch
Patch16:	rice_fog.patch
Patch17:	rsp_ucode2_reset.patch
Patch18:	version-string.patch
Patch19:	mupen64plus-keys.patch

BuildRequires:	SDL-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	gtk2-devel
BuildRequires:	lirc-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}

Conflicts:	mupen64plus-qt
Conflicts:	mupen64plus-cli

%description
Mupen64plus is a Nintendo 64 Emulator.
This package includes a GTK front-end and all the plug-ins.

%prep
%setup -q -n Mupen64Plus-1-5-src
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1


%build
make VCR=1 LIRC=1 GUI=GTK2 DBGSYM=1 PREFIX=%{_prefix} LIBDIR=%{_libdir}/mupen64plus all

%install
rm -rf %{buildroot}
make install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir}/mupen64plus MANDIR=%{buildroot}%{_mandir}/man1
pushd %{buildroot}%{_prefix}
ln -s %{_libdir}/mupen64plus  %{buildroot}%{_datadir}/mupen64plus/plugins
popd

desktop-file-install --vendor="" \
 --add-category="X-MandrivaLinux-MoreApplications-Emulators" \
 --add-category="Emulator" \
 --dir=%{buildroot}%{_datadir}/applications \
 %{buildroot}%{_datadir}/applications/%{name}.desktop

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
%doc README RELEASE TODO
%{_bindir}/mupen64plus
%{_libdir}/mupen64plus
%{_datadir}/mupen64plus
%{_datadir}/applications/mupen64plus.desktop
%{_mandir}/man1/*

