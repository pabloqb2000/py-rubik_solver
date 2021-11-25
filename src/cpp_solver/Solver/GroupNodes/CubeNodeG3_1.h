#ifndef CUBENODE_G3_1_H
#define CUBENODE_G3_1_H

#include "CubeNode.h"
#include "SavePerms.h"

class CubeNodeG3_1 : public CubeNode
{
    public:
        CubeNodeG3_1(const Cube& cube);
        bool isGoal();
    protected:
        SavePerms perms;
};


#endif