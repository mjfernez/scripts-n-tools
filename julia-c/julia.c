#include <stdio.h>
#include <math.h>
#include <complex.h>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

const char *HELP = "julia usage:\n" 
	"julia <complex num>[a+bj] <resolution>[integer] <depth>[integer] <bounds>[x-,x+,y-,y+]\n"
	"\n"
	"\tcomplex_num: a complex number in the form a + bj where j is the "
	"imaginary unit.\n"
	"\tresolution: resolution (in pixels) of the image\n"
	"\tdepth: iteration count for the julia function, warning: slow at high values >100\n"
	"\tbounds: the bounds of the graphs as a comma separated list without spaces "
	"in the form: minX,maxX,minY,maxY.\n"
	"\tBounds above 2 are generally not interesting.\n"
	"\n"
	"All arguments are required. This command prints bitmap directly to stdout which is "
	"(probably) not what you want. You should always pipe the output somewhere like:\n"
	"julia 1+1j 300 -1,1,-1,1 > file.bmp";
const int RGB_MODE = 3; // don't care about transparency, so we go for 8 bit channel

int julia(double complex z, double complex c, int d) {
	// z: coordinate
	// c: complex seed
	// d: depth, iteration count
	int ic = 0; // iteration count
	while(ic < d){
		if(cabs(z) > 2)
		       break;
		z = z * z + c;
		ic++;	
	}
	return ic;
}

int write_image(double complex seed, int r, int depth, float bounds[4]) {
	float x, y;
	int pixels = r * r;
	int cur_pixel = 3 * pixels - 1;
	char const *filename = "/dev/stdout";
	// In a bitmap: 3 bytes makes a pixel (RGB)
	uint8_t *img_data = (uint8_t *) STBI_MALLOC(pixels * 3 * sizeof(uint8_t));
	// In this image library, data is stored in a 
	// 1-D array separated by row, so you need to fill
	// the pixels horizontally first
	
	float dx = bounds[1] - bounds[0];
	float dy = bounds[3] - bounds[2];
	if (dx <= 0 || dy <= 0)
		return 0; // failure (to match stbi_write)	

	for(y = bounds[2]; y < bounds[3]; y += dy/((float) r - 1)) {
		for(x = bounds[0]; x < bounds[1]; x += dx/((float) r - 1)) {
			double complex z = x + y * I;
			int out = julia(z, seed, depth);
			img_data[cur_pixel - 2] = out % 32 * 8;
			img_data[cur_pixel - 1] = out % 16 * 16;
			img_data[cur_pixel] = out % 8 * 32;
			cur_pixel -= 3;	
		}
	}
	// returns 0 on failure	
	return stbi_write_bmp(filename, r, r, RGB_MODE, img_data);
}

int main(int argc, char *argv[]) {
	double complex seed;
	int res, depth;
	float b[4];
	
	if(argc != 5) {
		printf("%s\n", HELP);
		return 1;
	}
	else {
		float re, img;
		sscanf(argv[1], "%f+%fj", &re, &img);
		sscanf(argv[2], "%d", &res);
		sscanf(argv[3], "%d", &depth);
		sscanf(argv[4], "%f,%f,%f,%f", &b[0], &b[1], &b[2], &b[3]);
		seed = re + img * I;
		if (!write_image(seed, res, depth, b)) {
			printf("Error in arguments, could not make image\n");
			return 1;
		}
	}
	return 0;
}
