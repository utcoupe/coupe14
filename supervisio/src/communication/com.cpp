#include <string>
#include <iostream>

#include "com.h"
#include "../traitement/traitement.h"

using namespace std;

void comLoop(Visio& visio) {
	string order;
	cout << "READY" << endl;
	//On lit les ordres sur l'entrée standard
	cin >> order;
	while (order != "EXIT") {
		if (order == "ASK_DATA") {
			vector<Triangle> tri;
			try {
				visio.triangles(tri);
				for (int i=0; i<tri.size(); i++) {
					cout << tri[i].coords.x<<":"<<tri[i].coords.y<<" "<<tri[i].angle<<" "<<tri[i].size<<" "<<tri[i].color<<" "<<tri[i].isDown << endl;
				}
				cout << "END" << endl;
			} catch (const std::exception &e) {
				cerr << "Exception in visio.triangles() : " << e.what() << endl;
				cout << "ERROR" << endl;
			} catch (...) {
				cerr << "Unknown exception in visio.triangles()" << endl;
				cout << "ERROR" << endl;
			}
			order = "";
		}
		else {
			//cerr << "Unexpected order : " << order << endl;
			continue;
		}
		cin >> order;
	}
	cout << "exit" << endl;

}

