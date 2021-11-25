#ifndef CUBENODE_G2_H
#define CUBENODE_G2_H

#include "CubeNode.h"

class CubeNodeG2 : public CubeNode
{
    public:
        CubeNodeG2(const Cube& cube);
        bool isGoal();
};


#endif