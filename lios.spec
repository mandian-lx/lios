Summary:	Linux intelligent OCR solution
Name:		lios
Version:	2.0
Release:	0
License:	GPLv3+
Group:		Office
URL:		https://sourceforge.net/projects/%{name}
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick

Requires:	aspell-en
Requires:	espeak 
Requires:	imagemagick
Requires:	packagekit-gtk3-module
Requires:	poppler
Requires:	python-gi
Requires:	python-enchant
Requires:	python-speechd
Requires:	python-imaging
Requires:	python-sane
Requires:	tesseract

#Suggests:	cuneiform-linux

%description
# from README.md
Lios is a free and open source software for converting print in to text
using either scanner or a camera, It can also produce text out of scanned
images from other sources such as Pdf, Image, Folder containing Images or
screenshot. Program is given total accessibility for visually impaired.

Features include:
  · Import images from Scanner, PDFs, Folder or Webcam
  · Take and Recognize Screen-shot
  · Recognize Selected Areas(Rectangle selection)
  · Support two OCR Engines (Cuneiform,Tesseract)
  · 24 Language support (Given at the end), 30 more languages can be
    installed in Tesseract
  · Full Auto Rotation for any Language (if aspell installed for the
    language)
  · Side by side view of image and output
  · Advanced Scanner Brightness optimizer
  · Text Reader for low vision with Highlighting, With user selected 
    Color, Font, and Background Color
  · Audio converter(espeak)
  · Spell-checker(aspell)
  · Export as pdf (text/images)
  · Dictionary Support for English(Artha)
  · Options for save, load and reset settings
  · Other options - Find, Find-and-Replace, Go-To-Page, Go-To-Line,
    Append file, Punch File

Lios is written in python3.

%files -f FILELIST
%{_iconsdir}/hicolor/*/apps/%{name}.png
%doc README.md
%doc NEWS
%doc LICENSE
%doc COPYING

#----------------------------------------------------------------------------

%prep
%setup -q

# fix .desktop file name
mv share/applications/Lios.desktop share/applications/%{name}.desktop 
sed -i -e 's|Lios.desktop|%{name}.desktop|' setup.py

# fix premissions
chmod 0644 share/lios/%{name}
chmod 0644 share/lios/readme

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=%{buildroot} --record=FILELIST

# remove duplicates (by rpm5 point of view) from FILELIST
# (see http://wiki.rosalab.ru/ru/index.php/Python_policy#Automated_setup)
sed -i -e '{ /pyc$/d 
	     /pyo$/d 
	     /copyright$/d
	   }' FILELIST

# manpage uses xz compression
sed -i -e 's|%{name}.1.gz|%{name}.1.xz|' FILELIST

# set executable permissions (fix non-executable-script error)
find %{buildroot}%{python_sitelib} -name "*py" -exec %__chmod 0755 '{}' \;

# missing icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -scale ${d}x${d} share/%{name}/%{name} %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done

%check
# .desktop file
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

