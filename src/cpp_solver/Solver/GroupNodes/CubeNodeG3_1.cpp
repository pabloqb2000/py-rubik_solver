#include "CubeNodeG3_1.h"

/**
  * Create a CubeNode from a Cube
  * @param cube base cube
  */
CubeNodeG3_1::CubeNodeG3_1 (const Cube& cube) : 
  CubeNode(cube),
  perms(Cube())
{

}

bool CubeNodeG3_1::isGoal()
{
  return this->perms.permutationExists(*(Cube *)this);
}
