#include <string>
#include <fstream>

using namespace std;

struct Profit
{
	// dollar amount
	float amount;

	// time duration
	int time;
};

class KWP {
	private:
		Profit profit_KWP;
		float initial[4];
		static int numObj;
		float percentage;
		string path;

	public:
		// constructor: init at least one data attribute
		KWP(string filename);

		// destructor
		~KWP();

		void getInputInfo(const string& file_name);
		float computeAvgProfit(int Z);
		float computeTotalProfit(int Z);
		// int totalTimes(int Z);
		float computeProfitOfKY(int Z);
		void setProfit(int Z, float pro);
		float getProfit();
		float getPercentage();
};

class KYP {
	private:
		Profit profit_KYP;
		int numObj;
		ofstream output;
		string path;

	public:
		// constructor
		KYP(string filename);

		// destructor
		~KYP();

		void setProfit(int Z, float pro);

		float getProfit();
};