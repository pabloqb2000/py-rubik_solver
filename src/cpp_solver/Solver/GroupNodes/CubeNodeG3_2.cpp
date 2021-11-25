#include "CubeNodeG3_2.h"

/**
  * Create a CubeNode from a Cube
  * @param cube base cube
  */
CubeNodeG3_2::CubeNodeG3_2 (const Cube& cube) : CubeNodeG3_1(cube) {
}

bool CubeNodeG3_2::isGoal()
{
  typedef Cube::FACE FACE;

  // Edges.  Note that the edge pieces in the M slice were taken care
  // of in the G1->G2 goal.
  FACE UL = this->getColor(FACE::U, 1, 0);
  FACE LU = this->getColor(FACE::L, 0, 1);

  FACE UR = this->getColor(FACE::U, 1, 2);
  FACE RU = this->getColor(FACE::R, 0, 1);

  FACE DL = this->getColor(FACE::D, 1, 0);
  FACE LD = this->getColor(FACE::L, 2, 1);

  FACE DR = this->getColor(FACE::D, 1, 2);
  FACE RD = this->getColor(FACE::R, 2, 1);

  FACE LB = this->getColor(FACE::L, 1, 0);
  FACE BL = this->getColor(FACE::B, 1, 2);

  FACE LF = this->getColor(FACE::L, 1, 2);
  FACE FL = this->getColor(FACE::F, 1, 0);

  FACE RB = this->getColor(FACE::R, 1, 2);
  FACE BR = this->getColor(FACE::B, 1, 0);

  FACE RF = this->getColor(FACE::R, 1, 0);
  FACE FR = this->getColor(FACE::F, 1, 2);


  // After this goal, the cube will be solvable with only 180-degree turns.
  return
    // All corners in a permutation that is achievable from the solved
    // state in only 180-degree turns.
    this->perms.permutationExists(*(Cube *)this) &&
      
    // Edges in their slices.
    (UL == FACE::F || UL == FACE::B) && (LU == FACE::R || LU == FACE::L)  &&
    (UR == FACE::F || UR == FACE::B) && (RU == FACE::R || RU == FACE::L)  &&
    (DL == FACE::F || DL == FACE::B) && (LD == FACE::R || LD == FACE::L)  &&
    (DR == FACE::F || DR == FACE::B) && (RD == FACE::R || RD == FACE::L)  &&
    (BL == FACE::U || BL == FACE::D) && (LB == FACE::R || LB == FACE::L)  &&
    (FL == FACE::U || FL == FACE::D) && (LF == FACE::R || LF == FACE::L)  &&
    (BR == FACE::U || BR == FACE::D) && (RB == FACE::R || RB == FACE::L)  &&
    (FR == FACE::U || FR == FACE::D) && (RF == FACE::R || RF == FACE::L);
}
