#include <string>
#include <fstream>

using namespace std;

class Matrix {
	private:
		int value[20][10];
		int first_num;
		int iter_linear;// to record iteration time in linear search
		int iter_binary;// to record iteration time in binary search
		int target_row_idx;// index of next row where first_num appears
		int binary_idx;//the column index of fisrt_num obtained by binary search
		int target_sorted_row[10];// the sorted version of row where first_num appears

	public:
		// constructor
    	Matrix(const string& file_name);
		int linear_search();
		int binary_search();
		int* sort_row(int idx);
		void output_result();
};