#ifndef THISTLETHWAITE_H
#define THISTLETHWAITE_H

#include "IDDFSSolver.h"
#include "../CubeModel/Cube.h"
#include "GroupNodes/CubeNode.h"
#include "GroupNodes/CubeNodeG1.h"
#include "GroupNodes/CubeNodeG2.h"
#include "GroupNodes/CubeNodeG3_1.h"
#include "GroupNodes/CubeNodeG3_2.h"

class ThistlethwaitesSolver : public IDDFSSolver
{
    public:
        stack<Cube::MOVE> solve(const Cube& cube);
};

#endif