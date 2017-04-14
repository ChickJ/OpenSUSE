# Tips and Tricks

Even though I have been using Linux for more than twenty years I still learn
new things everyday. But mostly I just forget how to do something so I make
little notes.

## Command line interface
These are some command lines that I use to help me with this project.


1. I use the following command to create the files list for the %files section
   in SPEC files.

        find . -type f | sed 's|./||

2. The following command will list missing shared libraries for all executables
   in a directory.

        find /opt/dotnet -name '*.so' -type f -print | xargs ldd | grep 'not found'
