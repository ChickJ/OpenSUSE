%define _topdir /home/jon.chick/Code/packages/rpm
%define name microsoft-consolas-truetype-fonts
%define release 1
%define version 0.0.1
%define buildroot %{_topdir}/BUILD/%{name}-%{version}
%define source %{name}-%{version}.tar.gz
%define files_dir /home/jon.chick/Code/packages/files

BuildArch: noarch
BuildRoot: %{buildroot}
Group: System/X11/Fonts
License: Proprietary
Name: %{name}
Prefix: /usr
Release: %{release}
Source: %{source}
Summary: Microsoft Consolas Font
Vendor: Microsoft
Version: %{version}

%description
Consolas is a monospaced (non-proportional) typeface, designed by Luc(as) de Groot. It is a part of a suite of fonts that take advantage of Microsoft's ClearType font rendering technology. It is included with Windows since Windows Vista, Microsoft Office 2007 and Microsoft Visual Studio 2010, and is available for download from Microsoft. It is the only standard Windows Vista font with a slash through the zero character.

%prep
%setup -q

%clean
if [ -d $RPM_BUILD_ROOT ]; then
  rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
/usr/share/fonts/truetype/consola.ttf
/usr/share/fonts/truetype/consolab.ttf
/usr/share/fonts/truetype/consolai.ttf
/usr/share/fonts/truetype/consolaz.ttf

