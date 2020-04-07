//
// funcs.cpp
//
#include "class.h"
#include <fstream>
#include <string>

// default constructor
KWP::KWP(string filename) {
	// keep track of the number of objs created
	numObj++;
	//initial[0] = 0;
	path = filename;

	// if (numObj == 1){
 //        ofstream mycout(path);
 //        mycout << "KWP objects No."<< count << " is constructed." <<  endl;
 //        mycout.close();}
 //    else {
 //        ofstream mycout(path,ios::app);
 //        mycout << "KWP objects No."<< count << " is constructed." <<  endl;
 //        mycout.close();}
	// cout << "KWP Object No."<< numObj << " is constructed." <<  endl;
	ofstream mycout(path);
	mycout << "KWP Object No."<< numObj << " is constructed." <<  endl;
	mycout.close();
}

// destructor
KWP::~KWP() {
	// print one line for testing method
	ofstream mycout(path,ios::app);
    mycout << "One KWP object is destructed." << endl;
    // mycout.close();
    // cout << "One KWP object is destructed." << endl;
	//output << "One KWP object is destructed" << endl;
}

// read input.txt file and put base case into profit_KWP
void KWP::getInputInfo(const string& file_name) {
	ifstream f_in;
	f_in.open(file_name.c_str());

	string str;
	int line_ind = 0;
	while (line_ind < 6) {
		getline(f_in, str);
		if (1 <= line_ind && line_ind <= 3) {
			string cur_num = "";
			int cur_duration;
			float cur_prof;
			for (int i = 0; i < str.length(); i++) {
				if (str[i] == ' ' && cur_num.length() != 0 && i != str.length() - 1) {
					cur_duration = stoi(cur_num);
					cur_num = "";
				} else if (i == str.length() - 1 && cur_num.length() != 0) {
					cur_num += str[i];
					cur_prof = stof(cur_num);
					initial[cur_duration] = cur_prof;
				} else if (str[i] != ' ') {
					cur_num += str[i];
				}
			}	
		}
		if (line_ind == 5) {
			percentage = stof(str);
		}
		line_ind++;
	}
	f_in.close();
}

// accessor to get average profit for Z number of weeks



float KWP::computeAvgProfit(int Z) {

	if (Z <= 3) return initial[Z];
	else return (computeAvgProfit(Z-1) + initial[1] + computeAvgProfit(Z-2) + initial[2] + computeAvgProfit(Z-3) + initial[3]) / 3;
}

float KWP::computeTotalProfit(int Z) {
	if (Z <= 3) return initial[Z];
	return computeTotalProfit(Z - 1) + initial[1] + computeTotalProfit(Z - 2) + initial[2] + computeTotalProfit(Z - 3) + initial[3];
}

// to get the profit that sould go to KY
float KWP::computeProfitOfKY(int Z) {
	return percentage / 100 * KWP::computeAvgProfit(Z);
}

// mutator to set profit for Z number of weeks
void KWP::setProfit(int Z, float pro) {
	profit_KWP.amount = pro;
	profit_KWP.time = Z;
}

float KWP::getProfit() {
	return profit_KWP.amount;
}

float KWP::getPercentage() {
	return percentage;
}


// default constructor
KYP::KYP(string filename) {
	//output = out;

	// keep track of the number of objs created
	numObj++;
	//initial[0] = 0;
	path = filename;

	// if (numObj == 1){
 //        ofstream mycout(path);
 //        mycout << "KWP objects No."<< count << " is constructed." <<  endl;
 //        mycout.close();}
 //    else {
 //        ofstream mycout(path,ios::app);
 //        mycout << "KWP objects No."<< count << " is constructed." <<  endl;
 //        mycout.close();}
	ofstream mycout(path,ios::app);
	mycout << "KYP Object No."<< numObj << " is constructed." << endl;

	// print one line for testing method
	// cout << "KYP Object No."<< numObj << " is constructed." << endl;
	//output << "A KWP Object is constructed" << endl;
}

// destructor
KYP::~KYP() {
	// print one line for testing method
	// cout << "One KYP object is destructed." << endl;
	//output << "KYP Object No." << numObj << " is constructed" << endl;
	ofstream mycout(path,ios::app);
    mycout << "One KYP object is destructed." << endl;
    mycout.close();
}

// mutator to set profit for Z number of weeks
void KYP::setProfit(int Z, float pro) {
	profit_KYP.amount = pro;
	profit_KYP.time = Z;
}

float KYP::getProfit() {
	return profit_KYP.amount;
}