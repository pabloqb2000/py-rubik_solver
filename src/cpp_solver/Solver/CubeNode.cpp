#include "CubeNode.h"

/**
  * Create a CubeNode from a Cube
  * @param cube base cube
  */
CubeNode::CubeNode (const Cube& cube) : Cube(cube) {
  this->moveStack.push(Cube::MOVE::NONE);
}

/**
  * Store move in stack
  * Move using a move index.
  */
Cube& CubeNode::move(MOVE ind)
{
  this->moveStack.push(ind);
  return Cube::move(ind);
}

/**
  * Undo last move in the stack
  */
Cube& CubeNode::invert()
{
  Cube::MOVE move = this->moveStack.top();
  this->moveStack.pop();
  return Cube::invert(move);
}

/**
  * Check if the cube is solved
  */
bool CubeNode::isGoal() const
{
  return this->isSolved();
}

/**
  * Return this cubes move stack
  */
stack<Cube::MOVE>  CubeNode::getStack()
{
  return this->moveStack;
}
