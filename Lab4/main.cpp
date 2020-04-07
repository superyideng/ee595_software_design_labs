#include <iostream>
#include <fstream>
#include <string>
#include "funcs.cpp"

using namespace std;

int main(int argc, const char* argv[]) {
	Matrix matrix("input.txt");
	matrix.linear_search();
	matrix.binary_search();
	matrix.output_result();
	return 0;
}
