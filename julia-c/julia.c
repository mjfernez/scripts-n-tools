#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <complex.h>
#define STB_IMAGE_IMPLEMENTATION
#include "stb/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb/stb_image_write.h"

const char *HELP = "julia usage:\n" 
        "julia <function>[string] <complex num>[a+bj] <resolution>[intxint] "
        "<depth>[integer] <bounds>[x-,x+,y-,y+]\n"
        "\n"
        "\tfunction: the function (in complex.h) to use, (i.e. sin(x), pow(z, 3))\n"
        "\tOptionally, a power can be appended, like 'sin2' for sin^2(z).\n"
        "\tSee README for available functions\n"
        "\tcomplex_num: a complex number in the form a + bj where j is the "
        "imaginary unit.\n"
        "\tresolution: resolution (in pixels) of the image\n"
        "\tdepth: iteration count for the julia function, warning: slow at high values >100\n"
        "\tbounds: the bounds of the graphs as a comma separated list without spaces "
        "in the form: minX,maxX,minY,maxY.\n"
        "\tBounds above 2 are generally not interesting.\n"
        "\n"
        "All arguments are required. This command prints bitmap directly to stdout. "
        "You should always pipe the output somewhere like:\n"
        "\n./julia pow^2 -0.0567+0.678j 300x300 64 -1.5,1.5,-1.5,1.5 > file.bmp\n"
        "With Imagemagick, you can just do:\n"
        "\n"
        "./julia pow^2 -0.0567+0.678j 300x300 64 -1.5,1.5,-1.5,1.5 | display";

const char *FUNCTION_LIST[16] = { "acos" , "acosh" , "asin" , "asinh", "atan" , "atanh" , 
        "cos" , "cosh" , "exp" , "log" , "sin" , "sinh" , "sqrt" , "tan" , "tanh" , "pow" };
const int RGB_MODE = 3; // I don't care about transparency, so we go for 8 bit channel
const int FSIZE = 10; // 10 is the max function size (acosh^9999, or acosh^1.125).
const double EPSILON = 0.000025; // for accounting for rounding error

typedef struct {
        uint8_t R;
        uint8_t G;
        uint8_t B;
} pixel_t;

double complex func(char f[FSIZE], double complex z) {
        int i = 0;
        double complex e;
        char copy[FSIZE], fname[5];// max would be acosh\0, as in acosh^5
        char *parser;
        strcpy(copy, f);
        parser = strtok(copy, "^");
        
        strcpy(fname, parser);
        parser = strtok(NULL, "^"); // second will be exponent
        
        if (parser == NULL) // No ^ was found
                e = 1;
        else
                e = (double complex) atof(parser); 
        
        for ( ; i < 16; i++)
                if (!strcmp(fname, FUNCTION_LIST[i]))
                        break;
        
        switch (i) {
                case 0: return cpow(cacos(z), e);
                case 1: return cpow(cacosh(z), e);
                case 2: return cpow(casin(z), e);
                case 3: return cpow(casinh(z), e);
                case 4: return cpow(catan(z), e);
                case 5: return cpow(catanh(z), e);
                case 6: return cpow(ccos(z), e);
                case 7: return cpow(ccosh(z), e);
                case 8: return cpow(cexp(z), e);
                case 9: return cpow(clog(z), e);
                case 10: return cpow(csin(z), e);
                case 11: return cpow(csinh(z), e);
                case 12: return cpow(csqrt(z), e);
                case 13: return cpow(ctan(z), e);
                case 14: return cpow(ctanh(z), e);
                case 15: return cpow(z, e);
                default: return z * z; // if function can't be parsed, just z^2
        }
}

int julia(char f[FSIZE], double complex z, double complex c, int d) {
        // f: function keyword
        // z: coordinate
        // c: complex seed
        // d: depth, iteration count
        int ic = 0; // iteration count
        
        while(ic < d){
                if(cabs(z) > 2)
                       break;
                z = func(f, z) + c;
                ic++;
        }
        return ic;
}

int write_image(char f[FSIZE], double complex seed, int r[2], int depth, double bounds[4]) {
        // writes the image to stdout according to function parameters
        // f: the function keyword
        // seed: a complex number a+bj
        // r[]: the XxY resolution of the image
        // depth: the iteration count to use
        // bounds: the grid on which to plot

        double x, y;
        int pixels = r[1] * r[0];
        int cur_pixel = pixels;
        char const *filename = "/dev/stdout";
        pixel_t *img_data = (pixel_t *) STBI_MALLOC(pixels * sizeof(pixel_t));
        
        // In this image library, data is stored in a 
        // 1-D array separated by row, so you need to fill
        // the pixels horizontally first, and *backwards* if
        // we want the grid right side up
        
        double dx = bounds[1] - bounds[0];
        double dy = bounds[3] - bounds[2];
        if (dx <= 0 || dy <= 0)
                return 0; // failure (to match stbi_write)        
        
        for(y = bounds[2]; y <= bounds[3]; y += dy/((double) r[1])) {
                for(x = bounds[0]; x <= bounds[1]; x += dx/((double) r[0])) {
                        double complex z = x + y * I;
                        int out = julia(f, z, seed, depth);
                        img_data[cur_pixel].R = out % 32 * 8;
                        img_data[cur_pixel].G = out % 16 * 16;
                        img_data[cur_pixel].B = out % 8 * 32;
                        cur_pixel -= 1; 
                        fprintf(stderr, "x: %5f, y: %5f p: %d\n", x, y, cur_pixel); 
                }
                if (cur_pixel < 300)
                        break;
                
        }
        // returns 0 on failure        
        return stbi_write_bmp(filename, r[0], r[1], RGB_MODE, img_data);
}

int main(int argc, char *argv[]) {
        double complex seed;
        char f[FSIZE]; // 10 is the max function size (acosh^9999)
        int depth;
        int res[2];
        double b[4];
        if(argc != 6) {
                fprintf(stderr, "%s\n", HELP);
                return 1;
        }
        else {
                double re, img;
                sscanf(argv[1], "%8s", f);
                sscanf(argv[2], "%10lf+%10lfj", &re, &img);
                sscanf(argv[3], "%10dx%10d", &res[0], &res[1]);
                sscanf(argv[4], "%4d", &depth);
                sscanf(argv[5], "%10lf,%10lf,%10lf,%10lf", &b[0], &b[1], &b[2], &b[3]);
                seed = re + img * I;
                if (!write_image(f, seed, res, depth, b)) {
                        fprintf(stderr, "Error in arguments, could not make image\n");
                        return 1;
                }
        }
        return 0;
}
