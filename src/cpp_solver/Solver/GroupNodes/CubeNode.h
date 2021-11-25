#ifndef CUBENODE_H
#define CUBENODE_H

#include "../../CubeModel/Cube.h"
#include <stack>
using namespace std;

class CubeNode : public Cube
{
    public:
        CubeNode(const Cube& cube);
        Cube& move(MOVE ind);
        Cube& invert();
        virtual bool isGoal();
        stack<MOVE> getStack();

    private:
        stack<MOVE> moveStack;
};


#endif