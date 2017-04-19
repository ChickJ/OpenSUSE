#
# spec file for package freetype2
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


#
%define doc_version 2.7.1
Name:           freetype2
Version:        2.7.1
Release:        1.1
Summary:        A TrueType Font Library
License:        SUSE-Freetype or GPL-2.0+
Group:          System/Libraries
Url:            http://www.freetype.org
Source0:        http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1:        http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{doc_version}.tar.bz2
Source3:        baselibs.conf
# PATCH-FIX-OPENSUSE don-t-mark-libpng-as-required-library.patch -- it is private in .pc
Patch202:       don-t-mark-libpng-as-required-library.patch
Patch308961:    bugzilla-308961-cmex-workaround.patch
Patch1000:	subpixel.patch
BuildRequires:  gawk
BuildRequires:  libbz2-devel
BuildRequires:  libpng-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# bug437293
%ifarch ppc64
Obsoletes:      freetype2-64bit
%endif

%description
This library features TrueType fonts for open source projects. This
version also contains an autohinter for producing improved output.

%package -n libfreetype6
Summary:        A TrueType Font Library
Group:          System/Libraries
Obsoletes:      freetype2 < %{version}
Provides:       freetype2 = %{version}

%description -n libfreetype6
This library features TrueType fonts for open source projects. This
version also contains an autohinter for producing improved output.

%package devel
Summary:        Development environment for the freetype2 TrueType font library
Group:          Development/Libraries/C and C++
Requires:       libfreetype6 = %{version}
Requires:       zlib-devel
# there is no freetype-devel on suse:
Provides:       freetype-devel
# Static library provides:
Provides:       libfreetype6-devel-static
# bug437293
%ifarch ppc64
Obsoletes:      freetype2-devel-64bit
%endif

%description devel
This package contains all necessary include files, libraries and
documentation needed to develop applications that require the freetype2
TrueType font library.

It also contains a small tutorial for using that library.

%prep

%setup -q -n freetype-%{version} -a 1
%patch308961 -p 1
%patch1000 -p1
%build
export CFLAGS="%{optflags} -std=gnu99 -D_GNU_SOURCE $(getconf LFS_CFLAGS)"
%configure \
	--with-bzip2 \
	--with-png \
	--with-zlib \
	--disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

# remove documentation that does not belong in an rpm
rm docs/INSTALL*

%post -n libfreetype6 -p /sbin/ldconfig

%postun -n libfreetype6 -p /sbin/ldconfig

%files -n libfreetype6
%defattr(-,root,root)
%{_libdir}/libfreetype.so.*
%doc ChangeLog README
%doc docs/{CHANGES,CUSTOMIZE,DEBUG,MAKEPP,PROBLEMS,TODO,*.txt}

%files devel
%defattr(-,root,root)
%doc docs/reference/*
%{_includedir}/*
%if 0%{?suse_version} >= 1140
%exclude %{_libdir}/libfreetype.*a
%else
%{_libdir}/libfreetype.*a
%endif
%{_libdir}/libfreetype.so
%{_libdir}/pkgconfig/freetype2.pc
%{_bindir}/*
%{_datadir}/aclocal
%{_mandir}/man1/freetype-config*

%changelog
* Sun Jan  1 2017 idonmez@suse.com
- Update to version 2.7.1:
  * IMPORTANT CHANGES
    + Support for the new CFF2 font format as introduced with
    OpenType 1.8 has been contributed by Dave Arnolds from Adobe.
    + Preliminary support for variation fonts as specified in
    OpenType 1.8 (in addition to the already existing support for
    Adobe's MM and Apple's GX formats). Dave Arnolds contributed
    handling of advance width change variation; more will come in
    the next version.
  * IMPORTANT BUG FIXES
    + Handling of raw CID fonts was partially broken (bug introduced
    in 2.6.4).
  * MISCELLANEOUS
    + Some limits for TrueType bytecode execution have been tightened
    to speed up FreeType's handling of malformed fonts, in
    particular to quickly abort endless loops.
    + The number of twilight points can no longer be set to an
    arbitrarily large value.
    + The total number of jump opcode instructions (like JMPR) with
    negative arguments is dynamically restricted; the same holds
    for the total number of iterations in LOOPCALL opcodes.
    + The dynamic limits are based on the number of points in a glyph
    and the number of CVT entries. Please report if you encounter a
    font where the selected values are not adequate.
    + PCF family names are made more `colourful'; they now include the
    foundry and information whether they contain wide characters.
    For example, you no longer get `Fixed' but rather `Sony Fixed'
    or `Misc Fixed Wide'.
    + A new function `FT_Get_Var_Blend_Coordinates' (with its alias
    name `FT_Get_MM_Blend_Coordinates') to retrieve the normalized
    blend coordinates of the currently selected variation instance
    has been added to the Multiple Masters interface.
    + A new function `FT_Get_Var_Design_Coordinates' to retrieve the
    design coordinates of the currently selected variation instance
    has been added to the Multiple Masters interface.
    + A new load flag `FT_LOAD_BITMAP_METRICS_ONLY' to retrieve bitmap
    information without loading the (embedded) bitmap itself.
    + Retrieving advance widths from bitmap strikes (using
    `FT_Get_Advance' and `FT_Get_Advances') have been sped up.
    + The usual round of fuzzer fixes to better reject malformed
    fonts.
- Drop freetype2-bitmap-foundry.patch, merged upstream.
* Fri Sep  9 2016 develop7@develop7.info
- update to version 2.7:
  * IMPORTANT CHANGES
    + As announced earlier, the 2.7.x series now uses the new subpixel
    hinting  mode as  the  default, emulating  a  modern version  of
    ClearType.
    This change inevitably leads to different rendering results, and
    you   might   change   the   `TT_CONFIG_OPTION_SUBPIXEL_HINTING'
    configuration option to  adapt it to your taste (or  use the new
    `FREETYPE_PROPERTIES'    environment    variable).    See    the
    corresponding entry  below for  version 2.6.4, which  gives more
    information.
    + A new option  `FT_CONFIG_OPTION_ENVIRONMENT_PROPERTIES' has been
    introduced.   If  set (which  is  the  default), an  environment
    variable  `FREETYPE_PROPERTIES' can  be used  to control  driver
    properties.  Example:
    FREETYPE_PROPERTIES=truetype:interpreter-version=35 \
    cff:no-stem-darkening=1 \
    autofitter:warping=1
    This allows to select, say, the subpixel hinting mode at runtime
    for a given application.  See file `ftoption.h' for more.
  * IMPORTANT BUG FIXES
    + After  loading a  named instance  of  a GX  variation font,  the
    `face_index'  value  in  the returned  `FT_Face'  structure  now
    correctly holds the named instance  index in the upper 16bits as
    documented.
  * MISCELLANEOUS
    + A new macro `FT_IS_NAMED_INSTANCE' to  test whether a given face
    is a named instance.
    + More fixes to GX font handling.
    + Apple's   `GETVARIATION'  bytecode   operator  (needed   for  GX
    variation font support) has been implemented.
    + Another round  of fuzzer fixes,  mainly to reject  invalid fonts
    faster.
    + Handling of raw CID fonts  was broken (bug introduced in version
    2.6.4).
    + The smooth rasterizer has been streamlined  to make it faster by
    approx. 20%%.
    + The `ftgrid'  demo program now  understands command  line option
    `-d' to give start-up design coordinates.
    + The `ftdump' demo program has  a new command line option `-p' to
    dump TrueType bytecode instructions.
- removed freetype2-subpixel.patch in favor of above
  FREETYPE_PROPERTIES environment variable
* Wed Jul 13 2016 dimstar@opensuse.org
- Update to version 2.6.5:
  + Compilation works again  on Mac OS X (bug introduced in version
    2.6.4).
  + The new  subpixel hinting  mode is now  disabled by  default; it
    will  be enabled  by default  in the  forthcoming 2.7.x  series.
    Main reason for reverting this feature is the principle of least
    surprise: a  sudden change in  appearance of all fonts  (even if
    the rendering improves  for almost all recent  fonts) should not
    be expected in a new micro version of a series.
- Rebase freetype2-subpixel.patch.
* Fri Jul  8 2016 dimstar@opensuse.org
- Upadte to version 2.6.4:
  * A new subpixel hinting mode, which is now the default rendering
    mode for TrueType fonts. It implements (almost everything of)
    version 40 of the bytecode engine. The existing code base in
    FreeType (the `Infinality code') was stripped to the bare
    minimum and all configurability removed in the name of speed
    and simplicity. The configurability was mainly aimed at legacy
    fonts like Arial, Times New Roman, or Courier. [Legacy fonts
    are fonts that modify vertical stems to achieve clean
    black-and-white bitmaps.] The new mode focuses on applying a
    minimal set of rules to all fonts indiscriminately so that
    modern and web fonts render well while legacy fonts render
    okay. Activation of the subpixel hinting support can be
    controlled with the `TT_CONFIG_OPTION_SUBPIXEL_HINTING'
    configuration option at compile time: If set to value 1, you
    get the old Infinality mode (which was never the default due to
    its slowness). Value 2 activates the new subpixel hinting mode,
    and value 3 activates both. The default is value 2. At run
    time, you can select the subpixel hinting mode with the
    `interpreter-version' property (provided you have compiled in
    the corresponding hinting mode); see `ftttdrv.h' for more.
  * Support for the following scripts has been added to the
    auto-hinter: Armenian, Cherokee, Ethiopic, Georgian, Gujarati,
    Gurmukhi, Malayalam, Sinhala, Tamil.
- Rebase freetype2-subpixel.patch.
* Mon Mar 28 2016 idonmez@suse.com
- Update to version 2.6.3
  * IMPORTANT CHANGES
  - Khmer,  Myanmar, Bengali,  and Kannada  script support  has been
    added to the auto-hinter.
  * MISCELLANEOUS
  - Better  support of  Indic  scripts like  Devanagari  by using  a
    top-to-bottom hinting flow.
  - All  FreeType macros  starting  with two  underscores have  been
    renamed to  avoid a violation of  both the C and  C++ standards.
    Example: Header  macros of the  form `__FOO_H__' are  now called
    `FOO_H_'.  In most cases,  this should be completely transparent
    to the user.   The exception to this  is `__FTERRORS_H__', which
    must be  sometimes undefined by  the user to get  FreeType error
    strings:  Both this  form and  the new  `FTERRORS_H_' macro  are
    accepted for backwards compatibility.
  - Minor improvements mainly to the Type 1 driver.
  - The  new CFF  engine now  supports all  Type 2  operators except
    `random'.
  - The macro `_STANDALONE_', used for  compiling the B/W and smooth
    rasterizers  as   stand-alone  modules,  has  been   renamed  to
    `STANDALONE_', since macro names starting with an underscore and
    followed by an uppercase letter are reserved in both C and C++.
  - Function  `FT_Library_SetLcdFilterWeights'  now  also  activates
    custom LCD filter weights (instead of just adjusting them).
  - Support for  `unpatented hinting'  has been  completely removed:
    Consequently,  the two  functions `FT_Face_CheckTrueTypePatents'
    and  `FT_Face_SetUnpatentedHinting'  now  return  always  false,
    doing nothing.
* Sun Nov 29 2015 idonmez@suse.com
- Update to version 2.6.2
  * IMPORTANT CHANGES
  - The auto-hinter now supports stem darkening, to be controlled by
    the    new   `no-stem-darkening'    and   `darkening-parameters'
    properties.   This is  an  experimental  feature contributed  by
    Nikolaus Waxweiler, and  the interface might change  in a future
    release.
  - By default, stem darkening is now switched off (for both the CFF
    engine and the  auto-hinter).  The main reason is  that you need
    linear  alpha  blending  and  gamma correction  to  get  correct
    rendering results, and  the latter is not yet  available in most
    freely  available  rendering  stacks like  X11.   Applying  stem
    darkening without proper gamma correction  leads to far too dark
    rendering results.
  - The   meaning  of   `FT_RENDER_MODE_LIGHT'  has   been  slightly
    modified.   It  now  essentially  means `no  hinting  along  the
    horizontal  axis'; in  particular,  no change  of glyph  advance
    widths.  Consequently, the auto-hinter  is used for all scalable
    font  formats  except  for  CFF.    It  is  planned  that  other
    font-specific rendering engines (TrueType, Type 1) will follow.
  * MISCELLANEOUS
  - The default  LCD filter  has been changed  to be  normalized and
    color-balanced.
  - For    better    compatibility   with    FontConfig,    function
    `FT_Library_SetLcdFilter'  accepts   a  new   enumeration  value
    `FT_LCD_FILTER_LEGACY1'   (which  has   the   same  meaning   as
    `FT_LCD_FILTER_LEGACY').
  - A large number of bugs have been detected by using the libFuzzer
    framework,  which should  further  improve  handling of  invalid
    fonts.  Thanks again to Kostya Serebryany and Bungeman!
  - `TT_CONFIG_OPTION_MAX_RUNNABLE_OPCODES',  a   new  configuration
    option, controls the maximum number of executed opcodes within a
    bytecode program.  You don't want to change this except for very
    special  situations (e.g.,  making a  library fuzzer  spend less
    time to handle broken fonts).
  - The smooth renderer has been made faster.
* Sun Oct  4 2015 baiduzhyi.devel@gmail.com
- Update to version 2.6.1
  * IMPORTANT BUG FIXES
  - It turned  out that for CFFs  only the advance widths  should be
    taken from the  `htmx' table, not the side  bearings.  This bug,
    introduced in  version 2.6.0, makes  it necessary to  upgrade if
    you are using  CFFs; otherwise, you get cropped  glyphs with GUI
    interfaces like GTK or Qt.
  - Accessing Type 42 fonts returned  incorrect results if the glyph
    order of the embedded TrueType font differs from the glyph order
    of the Type 42 charstrings table.
  * IMPORTANT CHANGES
  - The header  file layout  has been  changed (again),  moving  all
    header files except `ft2build.h' into a subdirectory tree.
    Doing so  reduces the  possibility of  header file  name clashes
    (e.g., FTGL's  `FTGlyph.h' with FreeType's `ftglyph.h')  on case
    insensitive file systems like Mac OS X or Windows.
    Applications  that  use  (a)  the  `freetype-config'  script  or
    FreeType's `freetype2.pc' file for pkg-config to get the include
    directory  for the  compiler,  and (b)  the  documented way  for
    header inclusion like
    [#]include <ft2build.h>
    [#]include FT_FREETYPE_H
    ...
    don't need any change to the source code.
  - Simple access  to named instances  in GX variation fonts  is now
    available (in addition to the  previous method via FreeType's MM
    interface).   In  the `FT_Face'  structure,  bits  16-30 of  the
    `face_index' field hold the current named instance index for the
    given face  index, and bits  16-30 of `style_flags'  contain the
    number of  instances for  the given face  index.  `FT_Open_Face'
    and friends also understand the  extended bits of the face index
    parameter.
    You need to enable  TT_CONFIG_OPTION_GX_VAR_SUPPORT for this new
    feature.  Otherwise, bits  16-30 of the two fields  are zero (or
    are ignored).
  - Lao script support has been added to the auto-hinter.
  * MISCELLANEOUS
  - The auto-hinter's Arabic script support has been enhanced.
  - Superscript-like and  subscript-like glyphs  as used  by various
    phonetic alphabets like the IPA  are now better supported by the
    auto-hinter.
  - The TrueType bytecode interpreter now runs slightly faster.
  - Improved support for builds with cmake.
  - The  function  `FT_CeilFix'  now   always  rounds  towards  plus
    infinity.
  - The  function  `FT_FloorFix'  now always  rounds  towards  minus
    infinity.
  - A  new load  flag `FT_LOAD_COMPUTE_METRICS'  has been  added; it
    makes FreeType  ignore pre-computed  metrics, as needed  by font
    validating  or  font  editing  programs.  Right  now,  only  the
    TrueType  module supports  it  to ignore  data  from the  `hdmx'
    table.
  - Another round of bug fixes  to better handle broken fonts, found
    by Kostya Serebryany <kcc@google.com>.
- Dropping upstreamed patch Dont-use-hmtx-table-for-LSB.patch.
* Fri Sep 11 2015 zaitor@opensuse.org
- Add Dont-use-hmtx-table-for-LSB.patch: Fixes gnu#45520, cut off
  fonts in gtk and qt. Taken from upstream git.
* Thu Jun 11 2015 idonmez@suse.com
- Update to version 2.6
  * Thread safety improvements
  * Thai script support has been added to the auto-hinter.
  * Arabic script support has been added to the auto-hinter.
  * Following OpenType version 1.7,  advance widths and side bearing
    values in  CFFs (wrapped  in an SFNT  structure) are  now always
    taken from the `hmtx' table.
  * Following OpenType  version 1.7, the  PostScript font name  of a
    CFF font (wrapped in an SFNT structure) is now always taken from
    the `name'  table.  This is  also true for  OpenType Collections
    (i.e., TTCs using  CFFs subfonts instead of TTFs),  where it may
    have a significant difference.
  * Fonts natively hinted for  ClearType are now supported, properly
    handling selector index 3 of the INSTCTRL bytecode instruction.
  * Major improvements to the GX TrueType variation font handling.
* Tue Jun  9 2015 fstrba@suse.com
- Merge with the version 2.5.5 from openSUSE:Factory
- Removed patches:
  * CVE-2014-9656.patch
  * CVE-2014-9657.patch
  * CVE-2014-9658.patch
  * CVE-2014-9659.patch
  * CVE-2014-9660.patch
  * CVE-2014-9661.patch
  * CVE-2014-9662.patch
  * CVE-2014-9663.patch
  * CVE-2014-9664.patch
  * CVE-2014-9665.patch
  * CVE-2014-9666.patch
  * CVE-2014-9667.patch
  * CVE-2014-9668.patch
  * CVE-2014-9669.patch
  * CVE-2014-9670.patch
  * CVE-2014-9671.patch
  * CVE-2014-9672.patch
  * CVE-2014-9673.patch
  * CVE-2014-9674.patch
  * CVE-2014-9675.patch
  - Integrated in the 2.5.5 release
- Modified patches:
  * don-t-mark-libpng-as-required-library.patch
  * bugzilla-308961-cmex-workaround.patch
  * freetype2-subpixel.patch
  * freetype2-bitmap-foundry.patch
  * overflow.patch
  - Adapt to the new version of sources
* Wed Jun  3 2015 fstrba@suse.com
- Modified patch:
  * CVE-2014-9671.patch
  - Adapt the code to correspond to the current git master of
    freetype2 (fixes bsc#933247)
* Fri Apr 10 2015 fstrba@suse.com
- Enable the bz2 compression in freetype2
- Remove patch overflow.patch from freetype2.spec where it is not
  applied.
- Run spec-cleaner on the spec file.
* Fri Feb 20 2015 nadvornik@suse.com
- fixed vulnerabilities (bnc#916847, bnc#916856, bnc#916857,
  bnc#916858, bnc#916859, bnc#916860, bnc#916861, bnc#916862,
  bnc#916863, bnc#916864, bnc#916865, bnc#916867, bnc#916868,
  bnc#916870, bnc#916871, bnc#916872, bnc#916873, bnc#916874,
  bnc#916879, bnc#916881)
  - CVE-2014-9656.patch
  - CVE-2014-9657.patch
  - CVE-2014-9658.patch
  - CVE-2014-9659.patch
  - CVE-2014-9660.patch
  - CVE-2014-9661.patch
  - CVE-2014-9662.patch
  - CVE-2014-9663.patch
  - CVE-2014-9664.patch
  - CVE-2014-9665.patch
  - CVE-2014-9666.patch
  - CVE-2014-9667.patch
  - CVE-2014-9668.patch
  - CVE-2014-9669.patch
  - CVE-2014-9670.patch
  - CVE-2014-9671.patch
  - CVE-2014-9672.patch
  - CVE-2014-9673.patch
  - CVE-2014-9674.patch
  - CVE-2014-9675.patch
* Sat Jan  3 2015 hrvoje.senjan@gmail.com
- Update to version 2.5.5
  * IMPORTANT BUG FIXES
  - Handling of  uncompressed PCF files works again (bug
    introduced in version 2.5.4).
- Drop freetype2-2.5.3-fix-pcf.patch, merged upstream
* Mon Dec  8 2014 hrvoje.senjan@gmail.com
- Update to version 2.5.4
  * IMPORTANT BUG FIXES
  - A variant of vulnerability CVE-2014-2240 was identified
    (cf.  http://savannah.nongnu.org/bugs/?43661) and fixed
    in  the new CFF driver.  All users should upgrade.
  - The new auto-hinter code using HarfBuzz crashed for some
    invalid fonts.
  - Many fixes to better protect against malformed input.
  * IMPORTANT CHANGES
  - Full auto-hinter support of the Devanagari script.
  - Experimental auto-hinter support of the Telugu script.
  - CFF stem darkening behaviour can now be controlled at
    build time using the eight macros
    CFF_CONFIG_OPTION_DARKENING_PARAMETER_{X,Y}{1,2,3,4}    .
  - Some fields in the `FT_Bitmap'  structure have been changed
    from signed to unsigned type, which better reflects
    the actual usage. It is also an additional means to
    protect against malformed input. This change doesn't break
    the ABI; however, it might cause compiler warnings.
  * MISCELLANEOUS
  - Improvements to  the auto-hinter's algorithm to recognize
    stems and local extrema.
  - Function `FT_Get_SubGlyph_Info' always returned an error
    even in case of success.
  - Version  2.5.1 introduced major bugs in the cjk part of
    the auto-hinter, which are now fixed.
  - The `FT_Sfnt_Tag' enumeration values have been changed to
    uppercase,  e.g.  `FT_SFNT_HEAD'. The lowercase variants
    are deprecated. This is for orthogonality with all other
    enumeration (and enumeration-like) values in FreeType.
  - `cmake' now supports builds of FreeType as an OS X framework
    and for iOS.
  - Improved project files for vc2010,
    introducing a property file
  - The documentation generator for the API reference has been
    updated to produce  better HTML code (with proper  CSS).
    At the same time, the documentation got a better structure.
  - The FT_LOAD_BITMAP_CROP flag is obsolete; it is not used
    by any driver.
  - The TrueType DELTAP[123] bytecode instructions now work in
    subpixel hinting mode as described in the ClearType
    whitepaper (i.e., for touched points in the
    non-subpixel direction).
  - Many small improvements to the internal arithmetic routines.
- Rebase don-t-mark-libpng-as-required-library.patch,
  bugzilla-308961-cmex-workaround.patch, freetype2-subpixel.patch,
  freetype2-bitmap-foundry.patch and overflow.patch
- Add freetype2-2.5.3-fix-pcf.patch from upstream to resolve
  http://savannah.nongnu.org/bugs/?43774, "Freetype 2.5.4 does not
  load ungzipped PCF fonts"
* Thu Mar 27 2014 nadvornik@suse.com
- get 2.5.3 from Factory as it fixes
  CVE-2014-2240 CVE-2014-2241 (bnc#867620)
* Thu Mar 13 2014 hrvoje.senjan@gmail.com
- Improve don-t-mark-libpng-as-required-library.patch: also handle
  Requires.private case (freetype does not include png headers)
* Sun Mar  9 2014 hrvoje.senjan@gmail.com
- Update to version 2.5.3
  * IMPORTANT BUG FIXES
  - A vulnerability was  identified and fixed in the  new CFF
    driver (cf. http://savannah.nongnu.org/bugs/?41697;  it
    doesn't have a CVE number yet).  All users should upgrade.
  - More  bug  fixes related  to  correct  positioning of
    composite glyphs.
  - Many fixes to better protect against malformed input.
  * IMPORTANT CHANGES
  - FreeType can now use the HarfBuzz library to greatly improve
    the auto-hinting of  fonts that  use OpenType features:
    Many glyphs that are part  of such features but don't have
    cmap entries are now handled  properly, for  example small
    caps or superscripts. Define the configuration  macro
    FT_CONFIG_OPTION_USE_HARFBUZZ to activate HarfBuzz support.
    You need HarfBuzz version 0.9.19 or newer. Note that HarfBuzz
    depends on  FreeType; this currently causes a chicken-and-egg
    problem  that can be  solved as follows  in case HarfBuzz
    is not yet installed on your system.
    1. Compile  and  install  FreeType without the configuration
    macro FT_CONFIG_OPTION_USE_HARFBUZZ.
    2. Compile and install HarfBuzz.
    3. Define  macro  FT_CONFIG_OPTION_USE_HARFBUZZ, then
    compile and install FreeType again.
    With FreeType's  `configure' script the procedure  boils
    down to configure, build, and install Freetype, then
    configure, compile, and  install  HarfBuzz,  then configure,
    compile,  and  install FreeType again (after executing
    `make distclean').
  - All  libraries FreeType  depends on  are now  checked
    using  the `pkg-config' configuration files  first,
    followed by alternative methods.
  - The  new  value  `auto'  for the  various  `--with-XXX'
    library options   (for   example   `--with-harfbuzz=auto')
    makes   the `configure' script automatically link to the
    libraries it finds. This is now the default.
  - In case FreeType's `configure' script  can't find a
    library, you can  pass environment  variables to  circumvent
    pkg-config,  and those variables  have been  harmonized as
    a consequence  of the changes mentioned above:
    LIBZ           -> removed; use LIBZ_CFLAGS and LIBZ_LIBS
    LIBBZ2         -> removed; use BZIP2_CFLAGS and BZIP2_LIBS
    LIBPNG_LDFLAGS -> LIBPNG_LIBS
    `./configure --help' shows all available environment variables.
  - The `freetype-config'  script now understands
    option `--static' to emit static linking information.
- Due to buildsystem changes, rename and rebase
  don-t-mark-libpng-as-required-library-in-freetype-co.patch to
  don-t-mark-libpng-as-required-library.patch
* Thu Dec 12 2013 hrvoje.senjan@gmail.com
- Added patches:
  * don-t-mark-libpng-as-required-library-in-freetype-co.patch: it's
    private in pkgconfig file, and causes issues in downstream
    packages
- As per patch, remove libpng-devel Requires from devel package
* Wed Dec 11 2013 arvidjaar@gmail.com
- freetype2 pkgconfig now includes -lpng16; make sure freetype2-devel
  Requires libpng-devel
* Tue Dec 10 2013 hrvoje.senjan@gmail.com
- Update to version 2.5.2
  * Fixed bug  that made  FreeType crash  on some  popular (but  not
    fully conformant) fonts like `ahronbd.ttf'
  * Another round of improvements to correct positioning and hinting
    of composite glyphs in TrueType fonts
  * Fixed bug introduced in version  2.5.1: handling embedded
    bitmap strikes of  TrueType fonts, caused garbage display
    under some circumstances
  * Fixed `ftgrid' demo program compilation in non-development
    builds
- Droped fix-compile-in-non-debug.patch, included in this release
* Wed Nov 27 2013 hrvoje.senjan@gmail.com
- Update to version 2.5.1
  * For  some WinFNT  files,  the last  glyph  wasn't displayed  but
    incorrectly marked as invalid.
  * The vertical size of glyphs was  incorrectly set after a call to
    `FT_GlyphSlot_Embolden', resulting in clipped glyphs.
  * Many fields of the `PCLT' table in SFNT based fonts (if accessed
    with `FT_Get_Sfnt_Table') were computed incorrectly.
  * In TrueType fonts,  hinting of composite glyphs  could sometimes
    deliver  incorrect positions  of  components or  even  distorted
    shapes.
  * WOFF font format support has been added.
  * The auto-hinter now supports Hebrew.  Greek and Cyrillic support
    has been improved.
  * Support for the forthcoming `OS/2'  SFNT table version 5, as can
    be found e.g. in the `Sitka' font family for Windows 8.1.
  * The header  file layout  has been changed.   After installation,
    all files are now located in `<prefix>/include/freetype2'.
    Applications  that  use   (a)  `freetype-config'  or  FreeType's
    `pkg-config' file to get the include directory for the compiler,
    and (b) the documented way for header inclusion like
    [#]include <ft2build.h> or #include FT_FREETYPE_H
    don't need any change to the source code.
  * The stem  darkening feature  of the  new CFF  engine can  now be
    fine-tuned with the new `darkening-parameters' property.
  * `ftgrid' has been updated to toggle various engines with the `H'
    key, similar to `ftview' and `ftdiff'.
  * The functionality of `ttdebug' has been greatly enhanced.
  . It now displays twilight, storage, and control value data; key
  * Better support of ARMv7 and x86_64 processors.
  * Apple's `sbix' color bitmap format is now supported.
  * Improved   auto-hinter  rendering   for  many   TrueType  fonts,
    especially in the range 20-40ppem.
  * A  new face  flag  `FT_FACE_FLAG_COLOR' has  been  added (to  be
    accessed with the macro `FT_HAS_COLOR').
  * `FT_Gzip_Uncompress'   (modeled    after   zlib's   `uncompress'
    function)  has been  added; this  is a  by-product of  the newly
    added WOFF support.
  * Support for  a build with  `cmake' has been contributed  by John
    Cary <cary@txcorp.com>.
  * Support for x64  builds with Visual C++ has  been contributed by
    Kenneth Miller <kennethadammiller@yahoo.com>
  * Manual pages for most demo programs have been added.
  * The GETINFO bytecode instruction for TrueType fonts was buggy if
    used to retrieve subpixel hinting information.  It was necessary
    to set  selector bit 6  to get  results for selector  bits 7-10,
    which is wrong.
  * Improved computation  of emulated vertical metrics  for TrueType
    fonts.
  * Fixed horizontal start-up position of vertical phantom points in
    TrueType bytecode.
- Rebase freetype2-subpixel.patch to current release
- Added fix-compile-in-non-debug.patch, fixes release build of ftdemos
- Added overflow.patch for resolving post-build-check detected error:
  I: Statement is overflowing a buffer
* Wed Jul  3 2013 idonmez@suse.com
- Update to version 2.5.0.1
  * The cache manager function `FTC_Manager_Reset'  didn't flush the
    cache.
  * Behdad Esfahbod  (on behalf  of Google) contributed  support for
    color embedded bitmaps (eg. color emoji).
  * The  old FreeType  CFF engine  is now  disabled by  default.
  * All code related to macro FT_CONFIG_OPTION_OLD_INTERNALS
    has been removed.
  * The  property API  (`FT_Property_Get' and  `FT_Property_Set') is
    now declared as stable.
  * Another round of TrueType subpixel hinting fixes.
  * 64bit compilation of the new CFF engine was buggy.
  * Some fixes to improve robustness in memory-tight situations.
- Add dependency on libpng-devel for color emoji support.
- Drop freetype-new-cff-engine.patch, upstream now.
* Sun Jun  9 2013 crrodriguez@opensuse.org
- Library and tools must be compiled with large file
  support in 32 bit archs just like the rest of system.
* Fri May 10 2013 idonmez@suse.com
- Update to version 2.4.12
  * A new CFF rendering engine from Adobe
  * The  macro FT_CONFIG_OPTION_OLD_INTERNALS  is no  longer set  by
    default.
- freetype-new-cff-engine.patch: Enable the new CFF engine by default.
- Drop freetype2-no_rpath.patch, not needed.
* Fri Jan 11 2013 jw@suse.com
- Rediffed patches.
- CVE-2012-5668.patch, CVE-2012-5669.patch, CVE-2012-5670.patch nothing to do.
* Thu Dec 20 2012 idonmez@suse.com
- Update to version 2.4.11
  * Some vulnerabilities in the  BDF implementation have been fixed.
  * Support for OpenType collections (OTC) has been added.
  * Pure CFF fonts within an SFNT wrapper are now supported.
  * Minor rendering improvements to the auto-hinter.
  * `FT_GlyphSlot_Oblique' now uses a shear angle of 12°.
- Modify freetype2-subpixel.patch for new subpixel hinting option.
- Drop fix-build.patch: no longer needed
* Sun Jun 17 2012 idonmez@suse.com
- Update to version 2.4.10
  * Incremental glyph loading as needed by ghostscript was broken.
  * A new  function `FT_Outline_EmboldenXY'
  * The glyph  spacing computation  in `FT_GlyphSlot_Embolden'  (and
    similar code in `ftview') has been improved.
  * Minor  improvements to  the TrueType  bytecode  interpreter  and
    glyph loader, the auto-hinter, and the B/W rasterizer.
* Wed May  9 2012 crrodriguez@opensuse.org
- USe -std=gnu99 in all targets not only on ARM
* Fri Mar 30 2012 idonmez@suse.com
- Unbreak SLE builds
* Thu Mar  8 2012 idonmez@suse.com
- Update to version 2.4.9
  * Fixes CVE-2012-1126, CVE-2012-1127, CVE-2012-1128, CVE-2012-1129,
    CVE-2012-1130, CVE-2012-1131, CVE-2012-1132, CVE-2012-1133,
    CVE-2012-1134, CVE-2012-1135, CVE-2012-1136, CVE-2012-1137,
    CVE-2012-1138, CVE-2012-1139, CVE-2012-1140, CVE-2012-1141,
    CVE-2012-1142, CVE-2012-1143, CVE-2012-1144
  * The `ENCODING -1 <n>' format of BDF fonts is now supported.
  * For BDF fonts,  support for the whole Unicode encoding range has
    been added.
  * Better TTF support for x_ppem != y_ppem.
  * `FT_Get_Advances' sometimes returned bogus values.
* Tue Feb 14 2012 cfarrell@suse.com
- license update: SUSE-Freetype or GPL-2.0+
  Use SUSE- proprietary prefix until upstream spdx.org accepts Freetype as
  official license
* Tue Feb 14 2012 saschpe@suse.de
- Ran spec-cleaner
- Add devel-static provides to devel package (shared library policy)
* Thu Dec 22 2011 tiwai@suse.de
- provide libfreetype.la for older distros; otherwise it breaks
  too many package builds in M17N repo
- fix build on FACTORY by owning aclocal dir
* Tue Nov 15 2011 idonmez@suse.com
- Update to version 2.4.8
  * Some vulnerabilities in handling CID-keyed PostScript fonts have
    been fixed; see CVE-2011-3439
  * Chris Liddell contributed a new API, `FT_Get_PS_Font_Value',  to
    retrieve most of the dictionary keys in Type 1 fonts.
* Tue Oct 18 2011 idonmez@suse.com
- Update to version 2.4.7
  * Some  vulnerabilities in handling Type 1 fonts  have been fixed;
    see CVE-2011-3256.
  * FreeType  now properly  handles ZapfDingbats  glyph names  while
    constructing a Unicode character map (for fonts which don't have
    one).
* Fri Jul 29 2011 idonmez@novell.com
- Update to version 2.4.6
  * For TrueType based fonts, the ascender and descender values were
    incorrect sometimes  (off by a pixel if the ppem value was not a
    multiple of 5).   Depending on the use you might now  experience
    a different  layout; the  change should  result in  better, more
    consistent line spacing.
  * Fix CVE-2011-0226  which causes a  vulnerability while  handling
    Type 1 fonts.
  * BDF fonts  containing  glyphs with negative values  for ENCODING
    were  incorrectly  rejected.  This  bug has  been introduced  in
    FreeType version 2.2.0.
  * The behaviour of FT_STROKER_LINEJOIN_BEVEL has been corrected.
  * A new  line join style,  FT_STROKER_LINEJOIN_MITER_FIXED,  has
    been introduced to support PostScript and PDF miter joins.
  * FT_STROKER_LINEJOIN_MITER_VARIABLE  has been introduced  as an
    alias for FT_STROKER_LINEJOIN_MITER.
  * Various stroking glitches has been fixed
  * SFNT bitmap fonts which contain an outline glyph for `.notdef'
    only no longer set the FT_FACE_FLAG_SCALABLE flag.
- Drop bnc704612_othersubr.diff, applied upstream
* Fri Jul 22 2011 ke@suse.de
- added bnc704612_othersubr.diff, CVE-2011-0226, bnc#704612.
* Thu Jul  7 2011 idonmez@novell.com
- Clean spec file
- Disable static libraries
- Drop unneeded use_unix.diff
- Disable newly introduced bzip2 support, it seems to create
  problems with subpixel rendering
* Sat Jun 25 2011 idonmez@novell.com
- Update to version 2.4.5
  * A rendering regression  for second-order Bézier curves  has been
    fixed, introduced in 2.4.3.
  * If autohinting  is not  explicitly disabled,  FreeType now  uses
    the autohinter if  a TrueType based font doesn't  contain native
    hints.
  * The load flag FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH  has been made
    redundant and  is simply ignored;  this means that FreeType  now
    ignores the global advance width value in TrueType fonts.
  * `FT_Sfnt_Table_Info' can now return the number of SFNT tables of
    a font.
  * Support for PCF files compressed with bzip2 has been contributed
    by Joel  Klinghed.  To  make this  work, the  OS must  provide a
    bzip2 library.
  * Again some fixes to better handle broken fonts.
  * Some improvements to the B/W rasterizer.
  * Fixes to the cache module to improve robustness.
  * Just  Fill Bugs contributed (experimental) code to compute  blue
    zones for CJK Ideographs, improving the alignment of  horizontal
    stems at the top or bottom edges.
- Dropped the following patches:
  * bnc628213_1797.diff (fixed upstream)
  * bnc641580_CVE-2010-3311.diff (fixed upstream)
  * ft2-stream-compat.diff (only needed for SLE8->SLE9 update)
- Add libbz2-devel to BuildRequires to enable bzip2 support
* Mon Feb 28 2011 jw@novell.com
- bnc#647375: CVE-2010-3855.diff already fixed upstream.
- bnc#647375: CVE-2010-3814.diff already fixed upstream.
* Tue Dec  7 2010 jw@novell.com
- several old patches got lost, reapplying:
  * added bnc641580_CVE-2010-3311.diff for bnc#641580
  * bnc633943_CVE-2010-3054 nothing to do.
  * bnc633938_CVE-2010-3053 nothing to do.
* Mon Dec  6 2010 cristian.rodriguez@opensuse.org
- exclude *.a *.la files from -devel package
* Sat Dec  4 2010 pascal.bleser@opensuse.org
- Updated to version 2.4.4:
  * [truetype] better multi-threading support
  * [truetype] identify the tricky fonts by cvt/fpgm/prep checksums; some Latin TrueType fonts are still expected to be unhinted
  * [type1] fix matrix normalization
  * [type1] improve guard against malformed data
  * [ftsmooth] improve rendering
  * [ftraster] fix rendering
* Fri Oct 29 2010 fisiu@opensuse.org
- Updated to version 2.4.3:
  + Fix rendering of certain cubic, S-shaped arcs. This regression
    has been introduced in version 2.4.0.
  + Handling of broken fonts has been further improved.
* Thu Aug 12 2010 jw@novell.com
- bnc#628213: added bnc628213_1797.diff
- bnc#629447: CVE-2010-2805..8 are already fixed in upstream 2.4.2
- bnc#619562: CVE-2010-2497,2498,2499,2500,2519,2520 dito.
* Mon Aug  9 2010 tiwai@suse.de
- updated to version 2.4.2:
  Another serious bug in the CFF font module has been found,
  together with more exploitable vulnerabilities in the T42 font
  driver.
* Tue Jul 20 2010 tiwai@suse.de
- updated to version 2.4.1:
  * major version up
  * bytecode interpreter is enabled as default in the upstream
  * doc-reference is redundant, removed
* Fri Jun  4 2010 coolo@novell.com
- reenable bitmap foundaries (bnc#596559)
* Sat Apr 24 2010 coolo@novell.com
- buildrequire pkg-config to fix provides
* Tue Apr  6 2010 aj@suse.de
- Adjust baselibs.conf for changes
* Tue Apr  6 2010 coolo@novell.com
- fix obsoletes/provides
* Mon Apr  5 2010 coolo@novell.com
- leave freetype2 behind and only go with shared library package
* Sun Apr  4 2010 aj@suse.de
- Fix baselibs.conf for renamed libs
* Wed Mar 31 2010 coolo@novell.com
- update to version 2.3.12:
  brings considerable improvements for b/w rasterizing of hinted
  TrueType fonts at small sizes, see NEWS for more details
- fixed build without sysvinit in the build system
- disable no longer compiling patch that should be upstream or dead
- split out shared library policy package
- remove old patches
* Mon Dec 14 2009 jengelh@medozas.de
- add baselibs.conf as a source
* Fri Nov  6 2009 tiwai@suse.de
- make -std=gnu99 cfalgs to be ARM-specific
* Tue Nov  3 2009 coolo@novell.com
- updated patches to apply with fuzz=0
* Sun Aug  2 2009 jansimon.moeller@opensuse.org
- ARM build needs -std=gnu99 in CFLAGS
* Mon Jul 27 2009 tiwai@suse.de
- updated to version 2.3.8:
  * see URLs below
    http://www.freetype.org/index2.html#release-freetype-2.3.8
    http://sourceforge.net/project/shownotes.php?group_id=3157&release_id=653641
- updated to version 2.3.9:
  * see URLs below
    http://www.freetype.org/index2.html#release-freetype-2.3.9
    http://sourceforge.net/project/shownotes.php?group_id=3157&release_id=667610
- fix builds with older distros
* Tue Jul  7 2009 meissner@novell.com
- require zlib-devel-<targettype> from freetype2-devel-<targettype>
  bnc#519192
* Thu Apr 16 2009 nadvornik@suse.cz
- fixed integer overflows [bnc#485889] CVE-2009-0946
* Mon Mar  9 2009 crrodriguez@suse.de
- freetype2 has subpixel rendering enabled [bnc#478407]
* Wed Dec 10 2008 olh@suse.de
- use Obsoletes: -XXbit only for ppc64 to help solver during distupgrade
  (bnc#437293)
* Wed Nov  5 2008 mfabian@suse.de
- bnc#441638: use fix from upstream CVS to fix the return value
  of FT_Get_TrueType_Engine_Type (and make it work as documented).
  Thanks to Werner Lemberg for fixing and Krzysztof Kotlenga for
  reporting the issue.
* Thu Oct 30 2008 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Mon Aug 18 2008 mfabian@suse.de
- fix uninitialized pointer "FT_STREAM stream" in function
  FT_Open_Face() which made fontforge crash while trying to apply
  a workaround to the sazanami-fonts because fontforge called
  FT_Open_Face() with 0 for the FT_Library argument and
  then freetype crashed in FT_Stream_Free().
* Wed Jul 23 2008 mfabian@suse.de
- update to 2.3.7. Extract from the docs/CHANGES file:
  • If the library was compiled on an i386 platform using gcc, and
    compiler option -O3 was given, `FT_MulFix' sometimes returned
    incorrect results which could have caused problems with
    `FT_Request_Metrics' and `FT_Select_Metrics', returning an
    incorrect descender size.
  • Pure CFFs without subfonts were scaled incorrectly if the font
    matrix was non-standard.  This bug has been introduced in
    version 2.3.6.
  • The `style_name' field in the `FT_FaceRec' structure often
    contained a wrong value for Type 1 fonts.  This misbehaviour
    has been introduced in version 2.3.6 while trying to fix
    another problem.  [Note, however, that this value is
    informative only since the used algorithm to extract it is
    very simplistic.]
  • Two new macros, FT_OUTLINE_SMART_DROPOUTS and
    FT_OUTLINE_EXCLUDE_STUBS, have been introduced.  Together with
    FT_OUTLINE_IGNORE_DROPOUTS (which was ignored previously) it is
    now possible to control the dropout mode of the `raster' module
    (for B&W rasterization), using the `flags' field in the
    `FT_Outline' structure.
  • The TrueType bytecode interpreter now passes the dropout mode to
    the B&W rasterizer.  This greatly increases the output for small
    ppem values of many fonts like `pala.ttf'.
  • A bunch of potential security problems have been found.  All
    users should update.
  • Microsoft Unicode cmaps in TrueType fonts are now always
    preferred over Apple cmaps.  This is not a bug per se, but there
    exist some buggy fonts created for MS which have broken Apple
    cmaps.  This affects only the automatic selection of FreeType;
    it's always possible to manually select an Apple Unicode cmap if
    desired.
  • Many bug fixes to the TrueType bytecode interpreter.
  • Improved Mac support.
  • Subsetted CID-keyed CFFs are now supported correctly.
  • CID-keyed CFFs with subfonts which are scaled in a non-standard
    way are now handled correctly.
  • A call to FT_Open_Face with `face_index' < 0 crashed FreeType if
    the font was a Windows (bitmap) FNT/FON.
  • The new function `FT_Get_CID_Registry_Ordering_Supplement' gives
    access to those fields in a CID-keyed font.  The code has been
    contributed by Derek Clegg.
  • George Williams contributed code to validate the new `MATH'
    OpenType table (within the `otvalid' module).  The `ftvalid'
    demo program has been extended accordingly.
  • An API for cmap 14 support (for Unicode Variant Selectors, UVS)
    has been contributed by George Williams.
  • A new face flag FT_FACE_FLAG_CID_KEYED has been added, together
    with a macro FT_IS_CID_KEYED which evaluates to 1 if the font is
    CID-keyed.
  • Build support for symbian has been contributed.
  • Better WGL4 glyph name support, contributed by Sergey Tolstov.
  • Debugging output of the various FT_TRACEX macros is now sent to
    stderr.
  • The `ftview' demo program now provides artificial slanting too.
  • The `ftvalid' demo program has a new option `-f' to select the
    font index.
- remove patch for bnc#399169 (came from upstream).
* Fri Jun 13 2008 mfabian@suse.de
- bnc#399169: fix multiple vulnerabilities.
* Mon Apr 14 2008 schwab@suse.de
- Make sure config.guess and config.sub exist.
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Thu Oct 18 2007 mfabian@suse.de
- Bugzilla #334565: avoid crash in xpdf caused by a bug in the
  workaround patch for bug #308961
  (fixed by Peng Wu <pwu@novell.com>).
* Mon Oct  8 2007 mfabian@suse.de
- Bugzilla #308961: improve workaround patch for the broken
  underlining in the CMEX fonts
  (again by Peng Wu <pwu@novell.com>).
* Tue Oct  2 2007 mfabian@suse.de
- Bugzilla #308961: add workaround for broken underlining
  when using the CMEX fonts (by Peng Wu <pwu@novell.com>).
* Tue Jul  3 2007 mfabian@suse.de
- update to 2.3.5. Extract from the doc/CHANGES file:
  • Some subglyphs in TrueType fonts were handled incorrectly due
  to a missing graphics state reinitialization.
  • Large .Z files  (as distributed with some X11  packages)
    weren't handled correctly, making FreeType increase the heap
    stack in an endless loop.
  • A large number of bugs have been fixed to avoid crashes and
    endless loops with invalid fonts.
  • The two new cache functions  `FTC_ImageCache_LookupScaler' and
    `FTC_SBit_Cache_LookupScaler' have been added to allow lookup of
    glyphs using an  `FTC_Scaler' object;  this makes it possible to
    use fractional pixel sizes in the cache.  The demo programs have
    been updated accordingly to use this feature.
  • A new API  `FT_Get_CMap_Format' has been added to  get the
    cmap format  of a  TrueType font.   This  is useful  in handling
    PDF files. The code has been contributed by Derek Clegg.
  • The  auto-hinter now  produces better output by default for
    non-Latin scripts like Indic.  This was done by using the CJK
    hinting module as the default instead of the Latin one. Thanks
    to Rahul Bhalerao for this suggestion.
  • A new API `FT_Face_CheckTrueTypePatents' has been added to find
    out whether a given TrueType font uses patented bytecode
    instructions.  The `ft2demos' bundle contains a new program
    called `ftpatchk' which demonstrates its usage.
  • A new API `FT_Face_SetUnpatentedHinting' has been added to
    enable or disable the unpatented hinter.
  • Support for Windows FON files in PE format has been contributed
    by Dmitry Timoshkov.
* Mon Jun  4 2007 mfabian@suse.de
-  Bugzilla #275072: (from upstream CVS):
  Check for negative number of points in contours. Problem
  reported by Victor Stinner <victor.stinner@haypocalc.com>.
* Tue May 22 2007 mfabian@suse.de
- fix last patch to avoid crashes when loader->exec == NULL.
  (caused crashes in xpdf, kpdf, acroread for me for many
  .pdf files).
* Mon May 21 2007 mfabian@suse.de
- Bugzilla #273714: ('¼', '½', and  '¾' in "Albany AMT" are
  rendered very badly): apply fix from upstream CVS, thanks
  to Werner LEMBERG.
* Tue Apr 10 2007 mfabian@suse.de
- update to 2.3.4. Extract from the doc/CHANGES file:
  • A serious bug in the handling of bitmap fonts (and bitmap
    strikes of outline fonts) has been introduced in 2.3.3.
  • Remove a serious regression in the TrueType bytecode
    interpreter that was introduced in version 2.3.2.  Note that
    this does not disable the improvements introduced to the
    interpreter in version 2.3.2, only some ill cases that occurred
    with certain fonts (though a few popular ones).
  • The auto-hinter now ignores single-point contours for
    computing blue zones.  This bug created `wavy' baselines when
    rendering text with various fonts that use these contours to
    model mark-attach points (these are points that are never
    rasterized and are placed outside of the glyph's real
    outline).
  • The `rsb_delta' and `lsb_delta' glyph slot fields are now set
    to 0 for mono-spaced fonts.  Otherwise code that uses them
    would essentially ruin the fixed-advance property.
  • Fix CVE-2007-1351 which can cause an integer overflow while
    parsing BDF fonts, leading to a potentially exploitable heap
    overflow condition.
  • FreeType returned incorrect kerning information from TrueType
    fonts when the bytecode interpreter was enabled.  This
    happened due to a typo introduced in version 2.3.0.
  • Negative kerning values from PFM files are now reported
    correctly (they were read as 16-bit unsigned values from the
    file).
  • Fixed a small memory leak when `FT_Init_FreeType' failed for
    some reason.
  • The Postscript hinter placed and sized very thin and ghost
    stems incorrectly.
  • The TrueType bytecode interpreter has been fixed to get rid
    of most of the rare differences seen in comparison to the
    Windows font loader.
  • A new demo program `ftdiff' has been added to compare
    TrueType hinting, FreeType's auto hinting, and rendering
    without hinting in three columns.
  • The auto-hinter now better deals with serifs and corner cases
    (e.g., glyph '9' in Arial at 9pt, 96dpi).  It also improves
    spacing adjustments and doesn't change widths for non-spacing
    glyphs.
* Mon Apr  2 2007 rguenther@suse.de
- add zlib-devel BuildRequires
* Wed Mar 28 2007 mfabian@suse.de
- Bugzilla #258335: fix buffer overflow in handling of bdf fonts.
* Mon Feb  5 2007 mfabian@suse.de
- update to 2.3.1.
  • The TrueType interpreter sometimes returned incorrect
    horizontal metrics due to a bug in the handling of the SHZ
    instruction.
  • A typo  in  a  security  check  introduced  after
    version 2.2.1 prevented FreeType to render some glyphs in CFF
    fonts.
* Sun Jan 21 2007 mfabian@suse.de
- update to 2.3.0 (from rc1 to final release)
* Fri Jan 12 2007 mfabian@suse.de
- update to 2.2.1.20070112 (= 2.3.0rc1).
  • bugzilla #231417 fixed, see ChangeLog:
    2007-01-10  David Turner  <david at freetype.org>
    [...]
  * src/pshinter/pshalgo.c (psh_glyph_compute_inflections):
    fixed a typo which created an endless loop with some malformed
    font files
* Wed Jan 10 2007 mfabian@suse.de
- update to 2.2.1.20070110.
- remove bugzilla-216793-local-variable-used-before-set.patch,
  bugzilla-217388-fix-advance-handling-in-FT_GlyphSlot_Embolden.patch
  (included upstream).
* Wed Nov 22 2006 mfabian@suse.de
- Bugzilla #222693: disable bugzilla-159166-reduce-embolden-distance.patch
* Thu Nov  9 2006 mfabian@suse.de
- Bugzilla #216793: "local variable used before set"
* Tue Nov  7 2006 mfabian@suse.de
- Bugzilla #217388: fix advance handling in FT_GlyphSlot_Embolden()
* Fri Oct 27 2006 mfabian@suse.de
- Bugzilla #158573: update to 2.2.1.20061027.
* Fri Oct 20 2006 mfabian@suse.de
- disable the recent fixes of the byte code interpreter because
  if breaks the rendering of "Luxi Mono"
  (/usr/share/fonts/truetype/luximr.ttf) See also:
  http://lists.gnu.org/archive/html/freetype/2006-10/msg00034.html
* Fri Oct 13 2006 mfabian@suse.de
- update to 2.2.1.20061013
  • fixes bugzilla #207959.
  • autohinter improved
* Fri Aug  4 2006 mfabian@suse.de
- Bugzilla #196931: add zlib-devel to Requires of freetype2-devel.
* Mon Jul 10 2006 mfabian@suse.de
- Bugzilla #190902: add patch from upstream CVS to handle
  bad PCF files.
* Mon Jun 26 2006 mfabian@suse.de
- Bugzilla #188210: move development documents of into -devel
  package.
* Tue Jun 20 2006 mfabian@suse.de
- update to 2.2.1:
  + remove bugzilla-97202-fix-x-crash.patch
  + remove bugzilla-157441-autofit-cjk-cvs.patch
    (was from upstream CVS).
  + remove bugzilla-158156-memory-leak.patch
    (was from upstream CVS).
  + remove bugzilla-158573-fix-orientation-detection.patch
    (included upstream).
  + remove bugzilla-133086-enable-kerning.patch
    (was from upstream).
  + remove bugzilla-154928-integer-overflows.patch
    (was from upstream).
  + remove bugzilla-159304-fix-ftview-glyph-index.patch
    (fixed upstream).
  + remove enable_ft_optimize_memory.patch (is already enabled by
    default now).
  + adapt bugzilla-159166-reduce-embolden-distance.patch a little
    bit to achieve the same boldness effect as with the last
    package.
* Thu Jun  1 2006 mfabian@suse.de
- Bugzilla #154928: fix several integer overflows.
* Mon Apr 24 2006 mfabian@suse.de
- Bugzilla #133086: enable kerning, see
  http://lists.nongnu.org/archive/html/freetype-devel/2005-09/msg00027.html
* Tue Mar 21 2006 dmueller@suse.de
- build parallel
* Mon Mar 20 2006 zsu@suse.de
- Bugzilla #158573: fix corrupt embolden glyphs issue for CJK fonts.
- Bugzilla #159166: reduce embolden strength to get better rendering
  effect.
* Wed Mar 15 2006 mfabian@suse.de
- Bugzilla #157441:  remove 0x0100-0xFFFF from CJK Unicode range,
  as it might cause side effects for non-CJK scripts.
* Wed Mar 15 2006 mfabian@suse.de
- Bugzilla #158156: fix a memory leak (by Zhe Su <zsu@novell.com>).
* Tue Mar 14 2006 mfabian@suse.de
- Bugzilla #157441: instead of Takashi's patches, use a patch
  from upstream CVS which renders slightly better.
* Tue Mar 14 2006 mfabian@suse.de
- Bugzilla #157441: FZSongTi.ttf contains a lot more (CJK)-glyphs
  than most other fonts, therefore we have to expand the cjk range
  in Takashi Iwai's "ft2-autofit-02-cjk.diff" to render these
  glyphs correctly as well.
- Bugzilla #157441: don't apply ft2-autofit-03-latin-baseline.diff
  as it has some side effects.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan  9 2006 mfabian@suse.de
- Bugzilla #105626: add patches by Takashi IWAI <tiwai@suse.de>
  to improve the autohinting (mainly for CJK fonts).
* Wed Jul 20 2005 mfabian@suse.de
- Bugzilla #97202: apply workaround to avoid crashing the Xserver.
  I need to disable FT_OPTIMIZE_MEMORY again to apply that
  workaround.
* Tue Jul 19 2005 mfabian@suse.de
- enable FT_OPTIMIZE_MEMORY.
- enable the byte code interpreter again.
* Tue Jul 12 2005 mfabian@suse.de
- update to 2.1.10.
  + fixes serious bug introduced in 2.1.8 which caused many
    distortions for TrueType fonts
  + amount of heap memory used is drastically reduced
  For more details see /usr/share/doc/packages/freetype2/CHANGES.
- disable freetype-autohint-cjkfonts.patch for the moment, the
  auto-hinter has been replaced with a new module called the
  'auto-fitter' which is "prepared better to support non-latin1
  scripts in next releases". Currently the rendering quality of
  CJK fonts seems to have suffered though compared to 2.1.9
  with the freetype-autohint-cjkfonts.patch.
* Mon Jul  4 2005 meissner@suse.de
- Use system zlib.
* Wed Aug 25 2004 kukuk@suse.de
- Avoid /bin/sh as PreRequires
* Tue Jul  6 2004 mfabian@suse.de
- update to 2.1.9.
* Mon May 10 2004 mfabian@suse.de
- update to 2.1.8.
  remove the bdf-pcf fixes for bitmap font metric issues which
  were backported from CVS, they are included in this release
* Fri Apr 16 2004 mfabian@suse.de
- Bugzilla #38205:
  add patch from http://www.kde.gr.jp/~akito/patch/freetype2/2.1.7
  to improve the hinting results (mainly for CJK fonts).
* Wed Mar 24 2004 mfabian@suse.de
- Add ft2-stream-compat.diff for binary compatibility when
  upgrading from SLES8 to SLES9.
  The FT_Stream functions have been renamed and although these
  functions were declared for internal use only by the freetype
  developers, they have been used in Qt (and possibly elsewhere).
  Therefore, 3rd party which linked statically against Qt might
  not work after upgrading from SLES8 to SLES9.
  Fix this problem with a patch by Kurt Garloff <garloff@suse.de>
  which defines appropriate weak symbols.
* Tue Mar 16 2004 mfabian@suse.de
- fix Bugzilla# 36143: backport fixes for bitmap font metric issues
  from CVS to fix  crashes when using bitmap fonts caused by the
  new libXft-2.1.5 from the X.org tree.
* Mon Jan 12 2004 adrian@suse.de
- add %%defattr and %%run_ldconfig
* Fri Jan  9 2004 mfabian@suse.de
- add "-fno-strict-aliasing" compile option to prevent crashes
  for example in ftdump and mkfontscale.
* Tue Dec 16 2003 mfabian@suse.de
- update to 2.1.7.
- remove freetype2-type1.patch (included upstream)
- add documentation.
* Wed Oct  8 2003 schwab@suse.de
- Fix invalid free.
* Fri Sep 26 2003 mfabian@suse.de
- update to 2.1.5.
- remove freetype-bdf-pcf-drivr.patch, freetype2-bitmap-style.patch
  (included upstream).
- remove gzip-eof.patch.
* Mon Sep  1 2003 mfabian@suse.de
- add gzip-eof.patch to fix the problem that some gzipped bitmap
  fonts could not be opened by freetype2.
  See also:
  http://marc.theaimsgroup.com/?l=freetype-devel&m=105505219505600&w=2
  and followups.
* Tue Aug 26 2003 mfabian@suse.de
- add freetype2-bitmap-style.patch: check the bdf properties
  WEIGHT_NAME and SLANT case insensitively. Without that,
  these properties are not correctly recognized when the fonts
  specify them in lower case.
* Tue Apr  8 2003 mfabian@suse.de
- update to 2.1.4
* Fri Apr  4 2003 mfabian@suse.de
- update to 2.1.4rc2
- freetype2-gzip-header.patch is obsolete -> removed
* Fri Mar  7 2003 mfabian@suse.de
- Bug #24755: further improvement: add " Wide" to the family name
  for fonts which have an average width >= point size, i.e. fonts
  which have glyphs which are at least square (or maybe even
  wider). This makes fonts which contain only double width
  characters (for example the "misc-fixed" 18x18ja.bdf) clearly
  distinct from single width fonts of the same family and
  avoids that they get accidentally selected via freetype2/Xft2.
* Fri Mar  7 2003 mfabian@suse.de
- Bug #24775: partly fixed by a patch to freetype which returns
  "FOUNDRY FAMILY_NAME" as the family_name for bitmap fonts.
  Without that change, all bitmap fonts which have "Fixed"
  in FAMILY_NAME also had the same family_name "Fixed" via
  freetype/Xft2 and it was not possible to distinguish between
  them, therefore the selection of "Fixed" bitmap fonts produced
  quite surprising results. After this change, the fonts show
  up for example as "Misc Fixed", "Etl Fixed", etc. via
  freetype2/Xft2, which makes it easy to select the right one.
* Mon Mar  3 2003 mfabian@suse.de
- fix for the bug that caused FreeType to loop endlessly when
  trying to read certain compressed gzip files. The following test
  could be used to reveal the bug:
  touch 0123456789 ; gzip 0123456789 ; ftdump 0123456789.gz
  (from upstream CVS)
* Fri Feb 14 2003 mfabian@suse.de
- freetype-bdf-pcf-drivr.patch: use FT_UShort instead of FT_Short
  for the glyph number of bitmap fonts. The GNU Unicode font
  has 34725 glyphs and because of the usage of signed short
  all glyphs with an index above 2^15 couldn't be displayed.
  Thanks to Gerd Knorr <kraxel@suse.de>.
* Thu Jan 30 2003 mfabian@suse.de
- disable freetype2-bc.patch, see
  http://www.freetype.org/freetype2/2.1.3-explained.html
* Wed Jan 29 2003 mfabian@suse.de
- add freetype2-bc.patch
* Mon Jan 13 2003 mfabian@suse.de
- split out ft2demos into extra package to avoid adding
  x-devel-packages to '# neededforbuild' (XFree86 needs freetype2,
  this would be a loop in the requirements)
- add doc files and license texts.
* Fri Jan 10 2003 mfabian@suse.de
- fix checking of .gz header (fixes Bug #22712, i.e. fixes
  the problem that freetype2 couldn't open .pcf.gz files which
  contain the original file name or extra fields)
- add programs from ft2demos-2.1.3.
* Thu Nov 21 2002 mfabian@suse.de
- update to 2.1.3.
* Tue Nov  5 2002 mfabian@suse.de
- add /usr/share/aclocal/* to filelist
  (thanks to <adrian@suse.de> for noticing the omission)
* Thu Oct 24 2002 mfabian@suse.de
- update to 2.1.2. From the release notes:
  That's probably the first release of FreeType in the 2.1.x
  development branch that can safely replace 2.0.9 on any
  system.
* Fri Aug  9 2002 mfabian@suse.de
- freetype2-devel package should require freetype2 package
* Tue Apr  2 2002 mfabian@suse.de
- upgrade to 2.0.9 (considerably improved rendering of Type1 fonts)
* Wed Mar  6 2002 mfabian@suse.de
- use the byte code interpreter
* Mon Feb 11 2002 mfabian@suse.de
- upgrade to 2.0.8
- remove freetype-config.patch (included upstream)
* Tue Feb  5 2002 adrian@suse.de
- enable debug informations to debug a sig11 in inst-sys
* Tue Feb  5 2002 pmladek@suse.cz
- fixed missing 'fi' in freetype-config
* Mon Feb  4 2002 mfabian@suse.de
- update to 2.0.7
- remove freetype-2.0.6-gsf-segv.patch (included in 2.0.7 already)
* Tue Jan 29 2002 mfabian@suse.de
- add freetype-2.0.6-gsf-segv.patch from upstream CVS to prevent
  SEGV caused by gsf files.
* Tue Jan 22 2002 mfabian@suse.de
- use %%{_libdir} instead of /usr/lib
* Wed Jan 16 2002 adrian@suse.de
- updated to 2.0.6
  * important fixes which causes crashes with pfb fonts
  * improved rendering
* Fri Nov  9 2001 mfabian@suse.de
- updated to 2.0.5
* Sat Jul 21 2001 egger@suse.de
- Updated to version 2.0.4.
- Use RPM_OPT_FLAGS.
* Wed Jun  6 2001 egger@suse.de
- Fix filelist.
* Mon Jun  4 2001 egger@suse.de
- Updated to version 2.0.3.
* Mon Mar 26 2001 ro@suse.de
- fix build-rooting
* Thu Dec 14 2000 kukuk@suse.de
- split devel package
* Mon Dec 11 2000 egger@suse.de
- Updated to version 2.0.1.
* Fri Nov 10 2000 egger@suse.de
- Initial SuSE package.
