#ifndef CUBENODE
#define CUBENODE

#include "../CubeModel/Cube.h"
#include <stack>
using namespace std;

class CubeNode : public Cube
{
    public:
        CubeNode(const Cube& cube);
        Cube& move(MOVE ind);
        Cube& invert();
        bool isGoal() const;
        stack<Cube::MOVE> getStack();

    private:
        stack<Cube::MOVE> moveStack;
};


#endif