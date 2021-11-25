#ifndef CUBENODE_G3_2_H
#define CUBENODE_G3_2_H

#include "CubeNodeG3_1.h"

class CubeNodeG3_2 : public CubeNodeG3_1
{
    public:
        CubeNodeG3_2(const Cube& cube);
        bool isGoal();
};


#endif