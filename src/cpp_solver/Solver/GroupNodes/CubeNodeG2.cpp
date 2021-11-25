#include "CubeNodeG2.h"

/**
  * Create a CubeNode from a Cube
  * @param cube base cube
  */
CubeNodeG2::CubeNodeG2 (const Cube& cube) : CubeNode(cube) {
}  

bool CubeNodeG2::isGoal()
{
  typedef Cube::FACE FACE;
  // IDEA: replace this->getColor with this->cube[idx]; in all CubeNode files
  
  // Corners, left and right facets.
  FACE LUB = this->getColor(FACE::L, 0, 0);
  FACE LUF = this->getColor(FACE::L, 0, 2);
  FACE LDB = this->getColor(FACE::L, 2, 0);
  FACE LDF = this->getColor(FACE::L, 2, 2);

  FACE RUB = this->getColor(FACE::R, 0, 2);
  FACE RUF = this->getColor(FACE::R, 0, 0);
  FACE RDB = this->getColor(FACE::R, 2, 2);
  FACE RDF = this->getColor(FACE::R, 2, 0);

  // Edges in the M slice (between R and L).
  FACE UF = this->getColor(FACE::U, 2, 1);
  FACE FU = this->getColor(FACE::F, 0, 1);

  FACE UB = this->getColor(FACE::U, 0, 1);
  FACE BU = this->getColor(FACE::B, 0, 1);

  FACE DF = this->getColor(FACE::D, 0, 1);
  FACE FD = this->getColor(FACE::F, 2, 1);

  FACE DB = this->getColor(FACE::D, 2, 1);
  FACE BD = this->getColor(FACE::B, 2, 1);

  return
    // All left/right corner facets either blue or green.
    (LUB == FACE::R || LUB == FACE::L) &&
    (LUF == FACE::R || LUF == FACE::L) &&
    (LDB == FACE::R || LDB == FACE::L) &&
    (LDF == FACE::R || LDF == FACE::L) &&
    (RUB == FACE::R || RUB == FACE::L) &&
    (RUF == FACE::R || RUF == FACE::L) &&
    (RDB == FACE::R || RDB == FACE::L) &&
    (RDF == FACE::R || RDF == FACE::L) &&

    // UF, UB, DF, DB in the M slice.  Note that the edges
    // are already oriented.
    (UF == FACE::F   || UF == FACE::B)  &&
    (FU == FACE::U   || FU == FACE::D)  &&

    (UB == FACE::F   || UB == FACE::B)  &&
    (BU == FACE::U   || BU == FACE::D)  &&

    (DF == FACE::F   || DF == FACE::B)  &&
    (FD == FACE::U   || FD == FACE::D)  &&

    (DB == FACE::F   || DB == FACE::B)  &&
    (BD == FACE::U   || BD == FACE::D);
}
