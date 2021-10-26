#include "Cube.h"
#include <iostream>
using namespace std;


/**
  * Initialize the cube array.
  */
Cube::Cube()
{
  array<FACE, 48>::iterator it  = this->cube.begin();
  array<FACE, 48>::iterator end = next(it, 8);

  // Up.
  fill(it, end, FACE::U);

  // Left.
  it = end;
  advance(end, 8);
  fill(it, end, FACE::L);

  // Front.
  it = end;
  advance(end, 8);
  fill(it, end, FACE::F);

  // Right.
  it = end;
  advance(end, 8);
  fill(it, end, FACE::R);

  // Back.
  it = end;
  advance(end, 8);
  fill(it, end, FACE::B);

  // Down.
  it = end;
  advance(end, 8);
  fill(it, end, FACE::D);
}



/**
  * Copy from another cube.
  */
Cube::Cube(const Cube& cube)
{
  memcpy(reinterpret_cast<void*>(&this->cube[0]),
    reinterpret_cast<const void*>(&cube.cube[0]), 48);
}

/**
  * Create cube from string
  */
Cube::Cube(const string cubeString) {
  for(uint8_t i = 0; i < 8*6; i++) {
    for(uint8_t j = 0; j < 6; j++) {
      if(cubeString[i] == face_names[j]) {
        this->cube[i] = (Cube::FACE)j;
        break;
      }
    }
  }
}

/**
  * Same as above, but using the equals operator.
  */
Cube& Cube::operator=(const Cube rhs)
{
  memcpy(reinterpret_cast<void*>(&this->cube[0]),
    reinterpret_cast<const void*>(&rhs.cube[0]), 48);

  return *this;
}

/**
  * Compare two cubes (integer comparison of each side).
  */
bool Cube::operator==(const Cube& rhs) const
{
  for (uint8_t i = 0; i < 6; ++i)
    if (this->getFace((FACE)i) != rhs.getFace((FACE)i))
      return false;

  return true;
}


/**
  * Check if the cube is in a solved state.  This is used by the solvers, and
  * the cube is expected to have red on top and white in the front.
  */
bool Cube::isSolved() const
{
  return
    this->getFace(FACE::U) == 0x0000000000000000 &&
    this->getFace(FACE::L) == 0x0101010101010101 &&
    this->getFace(FACE::F) == 0x0202020202020202 &&
    this->getFace(FACE::R) == 0x0303030303030303 &&
    this->getFace(FACE::B) == 0x0404040404040404 &&
    this->getFace(FACE::D) == 0x0505050505050505;
}


/**
  * Describe a move using an index.
  */
string Cube::getMove(MOVE ind) const
{
  switch (ind)
  {
    case MOVE::L:
      return "L";
    case MOVE::LP:
      return "L'";
    case MOVE::L2:
      return "L2";
    case MOVE::R:
      return "R";
    case MOVE::RP:
      return "R'";
    case MOVE::R2:
      return "R2";
    case MOVE::U:
      return "U";
    case MOVE::UP:
      return "U'";
    case MOVE::U2:
      return "U2";
    case MOVE::D:
      return "D";
    case MOVE::DP:
      return "D'";
    case MOVE::D2:
      return "D2";
    case MOVE::F:
      return "F";
    case MOVE::FP:
      return "F'";
    case MOVE::F2:
      return "F2";
    case MOVE::B:
      return "B";
    case MOVE::BP:
      return "B'";
    case MOVE::B2:
      return "B2";
    default:
      return "";
  }
}


/**
  * Get an entire face of the cube as a 64-bit int.
  * @param face The face to get.
  */
uint64_t Cube::getFace(FACE face) const
{
  return *(uint64_t*)&this->cube[(unsigned)face * 8];
}


void Cube::print() {
  cout << "\n    ";
  cout << face_names [(int)this->cube[0]];
  cout << face_names [(int)this->cube[1]];
  cout << face_names [(int)this->cube[2]];
  cout << "\n    ";
  cout << face_names [(int)this->cube[7]];
  cout << "U";
  cout << face_names [(int)this->cube[3]];
  cout << "\n    ";
  cout << face_names [(int)this->cube[6]];
  cout << face_names [(int)this->cube[5]];
  cout << face_names [(int)this->cube[4]];
  cout << "\n";

  for(uint8_t j = 0; j < 4; j++) {
    for(uint8_t k = 0; k < 3; k++) {
      cout << face_names [(int)this->cube[j*8 + k + 8]];
    }
    cout << " ";
  }
  cout << "\n";

  for(uint8_t j = 0; j < 4; j++) {
    cout << face_names [(int)this->cube[j*8 + 15]];
    cout << face_names [j+1];
    cout << face_names [(int)this->cube[j*8 + 11]];
    cout << " ";
  }
  cout << "\n";

  for(uint8_t j = 0; j < 4; j++) {
    for(uint8_t k = 0; k < 3; k++) {
      cout << face_names [(int)this->cube[j*8 - k + 14]];
    }
    cout << " ";
  }
  cout << "\n";

  cout << "\n    ";
  cout << face_names [(int)this->cube[40]];
  cout << face_names [(int)this->cube[41]];
  cout << face_names [(int)this->cube[42]];
  cout << "\n    ";
  cout << face_names [(int)this->cube[47]];
  cout << "D";
  cout << face_names [(int)this->cube[43]];
  cout << "\n    ";
  cout << face_names [(int)this->cube[46]];
  cout << face_names [(int)this->cube[45]];
  cout << face_names [(int)this->cube[44]];

  cout << "\n\n";
}

string Cube::toString() const {
  string cubeString = "";
  for(uint8_t i = 0; i < 8*6; i++) {
    cubeString += face_names[(int)this->cube[i]];
  }
  return cubeString;
}


/**
  * Move using a move index.
  */
Cube& Cube::move(MOVE ind)
{
  switch (ind)
  {
    case MOVE::L:
      return this->l();
    case MOVE::LP:
      return this->lp();
    case MOVE::L2:
      return this->l2();
    case MOVE::R:
      return this->r();
    case MOVE::RP:
      return this->rp();
    case MOVE::R2:
      return this->r2();
    case MOVE::U:
      return this->u();
    case MOVE::UP:
      return this->up();
    case MOVE::U2:
      return this->u2();
    case MOVE::D:
      return this->d();
    case MOVE::DP:
      return this->dp();
    case MOVE::D2:
      return this->d2();
    case MOVE::F:
      return this->f();
    case MOVE::FP:
      return this->fp();
    case MOVE::F2:
      return this->f2();
    case MOVE::B:
      return this->b();
    case MOVE::BP:
      return this->bp();
    case MOVE::B2:
      return this->b2();
  }
}

/**
   * Invert a move.
   * @param ind The move index.  The inverse will be applied.
   */
  Cube& Cube::invert(MOVE ind)
  {
    switch (ind)
    {
      case MOVE::L:
        return this->lp();
      case MOVE::LP:
        return this->l();
      case MOVE::L2:
        return this->l2();
      case MOVE::R:
        return this->rp();
      case MOVE::RP:
        return this->r();
      case MOVE::R2:
        return this->r2();
      case MOVE::U:
        return this->up();
      case MOVE::UP:
        return this->u();
      case MOVE::U2:
        return this->u2();
      case MOVE::D:
        return this->dp();
      case MOVE::DP:
        return this->d();
      case MOVE::D2:
        return this->d2();
      case MOVE::F:
        return this->fp();
      case MOVE::FP:
        return this->f();
      case MOVE::F2:
        return this->f2();
      case MOVE::B:
        return this->bp();
      case MOVE::BP:
        return this->b();
      case MOVE::B2:
        return this->b2();
    }
  }

/**
  * Make n_moves random moves in the cube
  */
Cube& Cube::scramble(uint8_t n_moves)
{
  srand(time(NULL));
  for(uint8_t i = 0; i < n_moves; i++) {
    Cube::MOVE mov = (Cube::MOVE)(rand() % 18);
    cout << getMove(mov) << " ";
    move(mov);
  }
  cout << endl;
}


/**
  * Move the up face clockwise.
  */
Cube& Cube::u()
{
  // Rotate the stickers on the face.
  this->roll90(FACE::U);

  // Update the sides.
  this->rotateSides90(8, 16, 24, 32, 10, 18, 26, 34);

  return *this;
}

/**
  * Move the up face counter clockwise.
  */
Cube& Cube::up()
{
  this->roll270(FACE::U);
  this->rotateSides90(32, 24, 16, 8, 34, 26, 18, 10);
  return *this;
}

/**
  * Move the up face twice
  */
Cube& Cube::u2()
{
  this->roll180(FACE::U);
  this->rotateSides180(8, 24, 16, 32, 10, 26, 18, 34);
  return *this;
}

/**
  * Move the left face clockwise.
  */
Cube& Cube::l()
{
  this->roll90(FACE::L);
  this->rotateSides90(6, 34, 46, 22, 0, 36, 40, 16);
  return *this;
}

/**
  * Move the left face counter clockwise.
  */
Cube& Cube::lp()
{
  this->roll270(FACE::L);
  this->rotateSides90(22, 46, 34, 6, 16, 40, 36, 0);
  return *this;
}

/**
  * Move the left face twice.
  */
Cube& Cube::l2()
{
  this->roll180(FACE::L);
  this->rotateSides180(6, 46, 34, 22, 0, 40, 36, 16);
  return *this;
}

/**
  * Move the front face clockwise.
  */
Cube& Cube::f()
{
  this->roll90(FACE::F);
  this->rotateSides90(4, 10, 40, 30, 6, 12, 42, 24);
  return *this;
}

/**
  * Move the front face counter clockwise.
  */
Cube& Cube::fp()
{
  this->roll270(FACE::F);
  this->rotateSides90(30, 40, 10, 4, 24, 42, 12, 6);
  return *this;
}

/**
  * Move the front face twice.
  */
Cube& Cube::f2()
{
  this->roll180(FACE::F);
  this->rotateSides180(4, 40, 10, 30, 6, 42, 12, 24);
  return *this;
}

/**
  * Move the right face clockwise.
  */
Cube& Cube::r()
{
  this->roll90(FACE::R);
  this->rotateSides90(2, 18, 42, 38, 4, 20, 44, 32);
  return *this;
}

/**
  * Move the right face counter clockwise.
  */
Cube& Cube::rp()
{
  this->roll270(FACE::R);
  this->rotateSides90(38, 42, 18, 2, 32, 44, 20, 4);
  return *this;
}

/**
  * Move the right face twice.
  */
Cube& Cube::r2()
{
  this->roll180(FACE::R);
  this->rotateSides180(2, 42, 18, 38, 4, 44, 20, 32);
  return *this;
}

/**
  * Move the back face clockwise.
  */
Cube& Cube::b()
{
  this->roll90(FACE::B);
  this->rotateSides90(0, 26, 44, 14, 2, 28, 46, 8);
  return *this;
}

/**
  * Move the back face counter clockwise.
  */
Cube& Cube::bp()
{
  this->roll270(FACE::B);
  this->rotateSides90(14, 44, 26, 0, 8, 46, 28, 2);
  return *this;
}

/**
  * Move the back face twice.
  */
Cube& Cube::b2()
{
  this->roll180(FACE::B);
  this->rotateSides180(0, 44, 26, 14, 2, 46, 28, 8);
  return *this;
}

/**
  * Move the down face clockwise.
  */
Cube& Cube::d()
{
  this->roll90(FACE::D);
  this->rotateSides90(12, 36, 28, 20, 14, 38, 30, 22);
  return *this;
}

/**
  * Move the down face counter clockwise.
  */
Cube& Cube::dp()
{
  this->roll270(FACE::D);
  this->rotateSides90(20, 28, 36, 12, 22, 30, 38, 14);
  return *this;
}

/**
  * Move the down face twice.
  */
Cube& Cube::d2()
{
  this->roll180(FACE::D);
  this->rotateSides180(12, 28, 36, 20, 14, 30, 38, 22);
  return *this;
}


/**
  * Roll an array right 2 places, and wrap around.  This is a 90-degree
  * rotation of a face.
  *
  * Input:  0 1 2 3 4 5 6 7 
  * Output: 6 7 0 1 2 3 4 5 
  *
  * @param f The face to roll.
  */
inline void Cube::roll90(FACE f)
{
  uint64_t face = *(uint64_t*)&this->cube[(unsigned)f * 8];
  asm volatile ("rolq $16, %[face]" : [face] "+r" (face) : );
  *(uint64_t*)&this->cube[(unsigned)f * 8] = face;
}

/**
  * Roll an array right 4 places, and wrap away.  This is a 180-degree
  * rotation of a face.
  *
  * Input:  0 1 2 3 4 5 6 7 
  * Output: 4 5 6 7 0 1 2 3 
  *
  * @param f The face to roll.
  */
inline void Cube::roll180(FACE f)
{
  uint64_t face = *(uint64_t*)&this->cube[(unsigned)f * 8];
  asm volatile ("rolq $32, %[face]" : [face] "+r" (face) : );
  *(uint64_t*)&this->cube[(unsigned)f * 8] = face;
}

/**
  * Roll an array right 6 places, and wrap away.  This is a 270-degree
  * rotation of a face.
  *
  * Input:  0 1 2 3 4 5 6 7 
  * Output: 2 3 4 5 6 7 0 1
  *
  * @param f The face to roll.
  */
inline void Cube::roll270(FACE f)
{
  uint64_t face = *(uint64_t*)&this->cube[(unsigned)f * 8];
  asm volatile ("rorq $16, %[face]" : [face] "+r" (face) : );
  *(uint64_t*)&this->cube[(unsigned)f * 8] = face;
}


/**
  * Rotate four sides 90 degrees.  Use roll to rotate the face.
  * @param s_i0 The first index, treated as a short.
  * @param s_i1 The second index, treated as a short.
  * @param s_i2 The third index, treated as a short.
  * @param s_i3 The fourth index, treated as a short.
  * @param c_i0 The first index, treated as a char.
  * @param c_i1 The second index, treated as a char.
  * @param c_i2 The third index, treated as a char.
  * @param c_i3 The fourth index, treated as a char.
  */
inline void Cube::rotateSides90(unsigned s_i0, unsigned s_i1, unsigned s_i2, unsigned s_i3,
  unsigned c_i0, unsigned c_i1, unsigned c_i2, unsigned c_i3)
{
  // The number of operations is reduced by moving two cubes at a time (e.g.
  // treating the cubes at index s_i0..s_i3 as 16-bit shorts).
  uint16_t hold_s_i0 = *((uint16_t*)&this->cube[s_i0]);

  *((uint16_t*)&this->cube[s_i0]) = *((uint16_t*)&this->cube[s_i1]);
  *((uint16_t*)&this->cube[s_i1]) = *((uint16_t*)&this->cube[s_i2]);
  *((uint16_t*)&this->cube[s_i2]) = *((uint16_t*)&this->cube[s_i3]);
  *((uint16_t*)&this->cube[s_i3]) = hold_s_i0;

  // The last four cubes need to be moved one at a time.
  FACE hold_c_i0 = this->cube[c_i0];

  this->cube[c_i0] = this->cube[c_i1];
  this->cube[c_i1] = this->cube[c_i2];
  this->cube[c_i2] = this->cube[c_i3];
  this->cube[c_i3] = hold_c_i0;
}

/**
  * Rotate four sides 180 degrees.  Use roll to rotate the face.
  * @param s_i0 The first index, treated as a short.
  * @param s_i1 The second index, treated as a short.
  * @param s_i2 The third index, treated as a short.
  * @param s_i3 The fourth index, treated as a short.
  * @param c_i0 The first index, treated as a char.
  * @param c_i1 The second index, treated as a char.
  * @param c_i2 The third index, treated as a char.
  * @param c_i3 The fourth index, treated as a char.
  */
inline void Cube::rotateSides180(
  unsigned s_i0, unsigned s_i1, unsigned s_i2, unsigned s_i3,
  unsigned c_i0, unsigned c_i1, unsigned c_i2, unsigned c_i3)
{
  swap(*((uint16_t*)&this->cube[s_i0]), *((uint16_t*)&this->cube[s_i1]));
  swap(*((uint16_t*)&this->cube[s_i2]), *((uint16_t*)&this->cube[s_i3]));
  swap(this->cube[c_i0], this->cube[c_i1]);
  swap(this->cube[c_i2], this->cube[c_i3]);
}

