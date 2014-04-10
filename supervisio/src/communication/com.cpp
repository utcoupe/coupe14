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
	while (order != "END") {
		if (order == "ASK_DATA") {
			vector<Triangle> tri;
			try {
				visio.triangles(tri);
				for (int i=0; i<tri.size(); i++) {
					cout << tri[i].coords.x<<":"<<tri[i].coords.y<<" "<<tri[i].angle<<" "<<tri[i].color<<" "<<tri[i].isDown << endl;
				}
				cout << "END" << endl;
			} catch (const std::exception &e) {
				cerr << "Exception in visio.triangles() : " << e.what() << endl;
			} catch (...) {
				cerr << "Unknown exception in visio.triangles()" << endl;
			}
			order = "";
		}
		else {
			cerr << "Unexpected answer : " << order << endl;
		}
		cin >> order;
		//}
		/*else {
			cerr << "ERROR : Ordre inconnu" << endl;
		}*/
	}
	cout << "exit" << endl;

}

