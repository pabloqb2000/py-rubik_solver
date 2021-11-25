#include "CubeNodeG1.h"
#include <iostream>

/**
  * Create a CubeNode from a Cube
  * @param cube base cube
  */
CubeNodeG1::CubeNodeG1 (const Cube& cube) : CubeNode(cube) {
}

bool CubeNodeG1::isGoal()
{
  typedef Cube::FACE FACE;
  // IDEA: replace this->getColor with this->cube[idx]; in all CubeNode files
  FACE UB = this->getColor(FACE::U, 0, 1);
  FACE UL = this->getColor(FACE::U, 1, 0);
  FACE UR = this->getColor(FACE::U, 1, 2);
  FACE UF = this->getColor(FACE::U, 2, 1);

  FACE LU = this->getColor(FACE::L, 0, 1);
  FACE LB = this->getColor(FACE::L, 1, 0);
  FACE LF = this->getColor(FACE::L, 1, 2);
  FACE LD = this->getColor(FACE::L, 2, 1);

  FACE FU = this->getColor(FACE::F, 0, 1);
  FACE FL = this->getColor(FACE::F, 1, 0);
  FACE FR = this->getColor(FACE::F, 1, 2);
  FACE FD = this->getColor(FACE::F, 2, 1);

  FACE RU = this->getColor(FACE::R, 0, 1);
  FACE RF = this->getColor(FACE::R, 1, 0);
  FACE RB = this->getColor(FACE::R, 1, 2);
  FACE RD = this->getColor(FACE::R, 2, 1);

  FACE BU = this->getColor(FACE::B, 0, 1);
  FACE BL = this->getColor(FACE::B, 1, 0);
  FACE BR = this->getColor(FACE::B, 1, 2);
  FACE BD = this->getColor(FACE::B, 2, 1);

  FACE DF = this->getColor(FACE::D, 0, 1);
  FACE DL = this->getColor(FACE::D, 1, 0);
  FACE DR = this->getColor(FACE::D, 1, 2);
  FACE DB = this->getColor(FACE::D, 2, 1);

  // See the spreadsheet in this directory for possible "good" edges.  Each
  // should be movable to its solved position without using U, U', D, or D'.
  return
    (UF == FACE::R  || UF == FACE::L || FU == FACE::U || FU == FACE::D) &&
    (UB == FACE::R  || UB == FACE::L || BU == FACE::U || BU == FACE::D) &&
    (DF == FACE::R  || DF == FACE::L || FD == FACE::U || FD == FACE::D) &&
    (DB == FACE::R  || DB == FACE::L || BD == FACE::U || BD == FACE::D) &&
    (LU == FACE::R  || LU == FACE::L || UL == FACE::U || UL == FACE::D) &&
    (LD == FACE::R  || LD == FACE::L || DL == FACE::U || DL == FACE::D) &&
    (RU == FACE::R  || RU == FACE::L || UR == FACE::U || UR == FACE::D) &&
    (RD == FACE::R  || RD == FACE::L || DR == FACE::U || DR == FACE::D) &&
    (LF == FACE::R  || LF == FACE::L || FL == FACE::U || FL == FACE::D) &&
    (LB == FACE::R  || LB == FACE::L || BL == FACE::U || BL == FACE::D) &&
    (RF == FACE::R  || RF == FACE::L || FR == FACE::U || FR == FACE::D) &&
    (RB == FACE::R  || RB == FACE::L || BR == FACE::U || BR == FACE::D);
}
