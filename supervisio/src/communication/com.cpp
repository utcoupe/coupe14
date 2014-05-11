#include <string>
#include <iostream>

#include "com.h"
#include "../traitement/traitement.h"

using namespace std;

void communication(int index, string path_to_conf, bool save) {
	Visio visio(index, path_to_conf, save);
	if (!visio.isOpened()) {
		cerr << "Failed to initialize vision on index " << index << endl;
		cout << "FAILED" << endl;
		return;
	}
	if (!visio.isCalibrated()) {
		cerr << "ERROR : Uncalibrated on index " << index << endl;
		return;
	}
	if (visio.getDistortMode() != none) {
		cerr << "INFO : Starting visio WITH distortion correction on index " << index << endl;
	} else {
		cerr << "INFO : Starting visio WITHOUT distortion correction on index " << index << endl;
	}
	comLoop(visio);
}

void comLoop(Visio& visio) {
	string order;
	while (!visio.isReady()) {}
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

