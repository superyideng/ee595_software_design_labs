#include <iostream>
#include <fstream>
#include <string>
#include "funcs.cpp"

using namespace std;

int KWP::numObj = 0;

int main(int argc, const char* argv[]) {
	// ofstream output("output.txt");

	string filename = "output.txt";

	KWP kwp(filename);
	kwp.getInputInfo("input.txt");

	int Z;
	cout << "Enter a time duration (eg: 1 for 1 week) that you want to check: " << endl;
	cin >> Z;

	float kwpInZ = kwp.computeAvgProfit(Z); // compute the profit that KW gets during Z weeks

	kwp.setProfit(Z, kwpInZ);

	// KYP kyp(output);
	KYP kyp(filename);

	float kypInZFromKwp = kwp.computeProfitOfKY(Z);
	kyp.setProfit(Z, kypInZFromKwp);

	cout << "KW's profit for " << Z << " number of weeks in average is estimated $";
	cout << kwp.getProfit() << ", out of which " << kwp.getPercentage();
	cout << "%, i.e., $" << kyp.getProfit() << " is KY's." << endl;

	// ofstream mycout(filename,ios::app);


	// mycout << "KW's profit for " << Z << " number of weeks in average is estimated $";
	// mycout << kwp.getProfit() << ", out of which " << kwp.getPercentage();
	// mycout << "%, i.e., $" << kyp.getProfit() << " is KY's." << endl;

	// mycout.close();

	return 0;
}
