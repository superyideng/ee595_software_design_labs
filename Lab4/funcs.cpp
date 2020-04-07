//
// funcs.cpp
//
#include "class.h"
#include <fstream>
#include <algorithm>

// constructor
Matrix::Matrix(const string& file_name) {
    // open a stream to the Matrix file
    ifstream f_in;
    f_in.open(file_name.c_str());

    string str;

	int cur_row = 0;
	bool is_firstnum = true;
	while (!f_in.eof()) {
		getline(f_in, str);
		if (str.length() == 0) continue;
		int cur_col = 0;
		string cur_num = "";
		for (int i = 0; i < str.length(); i++) {
			if (str[i] == ' ' && cur_num.length() != 0) {
				value[cur_row][cur_col] = stoi(cur_num);
				cur_col++;
				cur_num = "";
			} else if (i == str.length() - 1 && cur_num.length() != 0) {
				cur_num += str[i];
				value[cur_row][cur_col] = stoi(cur_num);
			} else {
				cur_num += str[i];
			}
		}
		cur_row++;
	}
 
    // close the stream
    f_in.close();

    first_num = value[0][0];
    //cout << first_num << endl;
}

// return the nest row where first_num appears using linear search
int Matrix::linear_search() {
	int iter = 0;
	for (int r = 1; r < 20; r++) {
		for (int c = 0; c < 10; c++) {
			iter++;
			if (value[r][c] == first_num) {
				iter_linear = iter;
				cout << r << c << endl;
				return r;
			}
		}
	}
	iter_linear = iter;
	return -1;
}

// return the next row where first_num appears using binary search
int Matrix::binary_search() {
	int iter = 0;
	for (int r = 1; r < 20; r++) {
		int* p;
		p = sort_row(r);
		int lo = 0;
		int hi = 9;
		// do binary search
		while (lo <= hi) {
			iter++;
			if (first_num < p[lo] || first_num > p[hi]) break;
			int mid = lo + (hi - lo) / 2;
			if (first_num < p[mid]) {
				hi = mid - 1;
			} else if (first_num > p[mid]) {
				lo = mid + 1;
			} else {
				iter_binary = iter;
				for (int i = 0; i < 10; i++) {
					target_sorted_row[i] = p[i];
					cout << target_sorted_row[i] << endl;
				}
				target_row_idx = r;
				binary_idx = mid;
				return r;
			}
		}
	}
	iter_binary = iter;
	target_row_idx = -1;
	return -1;
}

// return the sorted array of idx-th row of value matrix
int* Matrix::sort_row(int idx) {
	static int result[10];
	for (int i = 0; i < 10; i++) {
		result[i] = value[idx][i];
	}
	sort(result, result + 10, less<int>());
	return result;
}

// write results to output.txt file
void Matrix::output_result() {
	ofstream output("output.txt");
	output << "the iteration number of linear search for FirstNum: " << iter_linear << endl;
	output << "the sorted row including FirstNum: ";
	for (int i = 0; i < 10; i++) {
		if (i < 9) {
			output << target_sorted_row[i] << ",";
		} else {
			output << target_sorted_row[i] << endl;
		}
	}
	output << "the index of FirstNum obtained by binary search: " << binary_idx << endl;
	output << "the iteration number of binary search for FirstNum: " << iter_binary << endl;
	output.close();
}


