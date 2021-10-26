#ifndef IDDFSSOLVER
#define IDDFSSOLVER

#include "CubeNode.h"
#include <stack>
#include <tuple> 
using namespace std;

#define MAXDEPTH 14

class IDDFSSolver
{
    private:
        bool prune(Cube::MOVE move, Cube::MOVE lastMove) const;

    public:
        stack<Cube::MOVE> findGoal(
            CubeNode& cube, 
            uint8_t maxDepth=MAXDEPTH+1
        );

        void printSolution(stack<Cube::MOVE> solution, int maxMovesPerLine=16);
};


#endif