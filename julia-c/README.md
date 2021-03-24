# julia.c

### Simple CLI for efficient Julia Set fractal parsing in C

The motivation for this tool was to improve upon my earlier Julia Set code 
with a cleaner web app interface. But usingPython/numpy/PIL as the driver for 
image rendering was just too slow. This is supposed to be a better driver program 
meant to be lightweight, and easy to be called from another application with 
not-so complicated syntax. 

If for some reason you use it in anything important, *you shoud also sanitize the input*
with another programming/scripting language to esnure the syntax doesn't break anything.
You'll notice immediately you can mess with the inputs a bit but still get an image 
-- assume it is NOT secure on it's own

I make use of the STB Image library avaliable [here](https://github.com/nothings/stb) for image
rendering.

Call `./julia` without options for a help menu. Functions come from complex.h
documented [here](https://code-reference.com/c/complex.h) with some
simplifications and subtractions. Supported arguments are:

- acos 
- acosh 
- asin 
- asinh 
- atan 
- atanh 
- cos 
- cosh 
- exp 
- log (natural log, only) 
- sin 
- sinh 
- sqrt 
- tan 
- tanh
- pow 

All functions can optionally be appended with a number (up to and including 9999) 
to raise them to a power, with '^'. As an example: `pow^3`, is "z^3. Decimal powers are
also usable, such as `cos^.5` as long as it's less than 4 digits. You can optionally 
just pass any string to get the default z^2 Julia Sets for example, `./julia nil ...`

The executable was compiled on Debian sid so it won't work on Windows, or certain other
operating systems. If you have gcc installed, you can just run `make` and then `./julia`
to run. 

If you're on Windows, you'll need to [install GCC](https://gcc.gnu.org/install/binaries.html)
to do the same
