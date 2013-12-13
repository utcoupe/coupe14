#ifndef PROTOCOLCODES_H_INCLUDED
#define PROTOCOLCODES_H_INCLUDED

/*
 *
 * bit organization:
 * 0: error code for Robot-> response, unused in the other way
 * 1: direction (0=IA->Robot) (+64)
 * 2: Robot (GroBot=0, PtiBot=1) (+32)
 * 3->7 : Command (0->31 available)
 *
 * Utiliser uniquement des commentaires sur une seul ligne '//' pour le parseur python
 */
//////////////////////////////
/////////// PtiBot ///////////
//////////////////////////////
#define EMERGENCY_STOP_P			0x00
#define EMERGENCY_STOP_P_SIZE		0x0

#define INIT_P						0x01
#define INIT_P_SIZE					0x0

#define PUSH_GOAL_P					0x02
#define PUSH_GOAL_P_SIZE			0x8 //(x:uint_16, y:uint_16, theta:float(4o))

#define DROP_GOALS_P				0x03
#define DROP_GOALS_P_SIZE			0x0

#define GET_POS						0x04
#define GET_POS_SIZE				0x8

#define FIRE_BALL					0x05
#define FIRE_BALL_SIZE				0x0

#define FIRE_NET					0x06
#define FIRE_NET_SIZE				0x0



//////////////////////////////
/////////// GroBot ///////////
//////////////////////////////
#define EMERGENCY_STOP_G			0x00+0x32
#define EMERGENCY_STOP_G_SIZE		0x0

#define INIT_G						0x01+0x32
#define INIT_G_SIZE					0x0

#define PUSH_GOAL_G					0x02+0x32
#define PUSH_GOAL_G_SIZE			0x0

#define DROP_GOALS_G				0x03+0x32
#define DROP_GOALS_G_SIZE			0x0

#define GET_POS						0x04+0x32
#define GET_POS_SIZE				0x8

// Triangles
#define PICK_TRIANGLE				0x05+0x32
#define PICK_TRIANGLE_SIZE			0x0

#define RETURN_TRIANGLE				0x06+0x32
#define RETURN_TRIANGLE_SIZE		0x0

#define DROP_TRIANGLE				0x07+0x32
#define DROP_TRIANGLE_SIZE			0x0

#define DROP_RETURNED_TRIANGLE		0x08+0x32
#define DROP_RETURNED_TRIANGLE_SIZE	0x0



//#define DROP_GOALS_G				0x03 +0x32
//#define DROP_GOALS_G_SIZE			0x0

//#define DROP_GOALS_G				0x03 +0x32
//#define DROP_GOALS_G_SIZE			0x0






#endif // PROTOCOLCODES_H_INCLUDED