#ifndef CUBENODE_G1_H
#define CUBENODE_G1_H

#include "CubeNode.h"

class CubeNodeG1 : public CubeNode
{
    public:
        CubeNodeG1(const Cube& cube);
        bool isGoal();
};


#endif