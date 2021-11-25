#ifndef CUBE_H
#define CUBE_H

#include <string>
using std::string;
#include <array>
using std::array;
#include <algorithm>
using std::fill;
using std::next;
using std::swap;
#include <iterator>
using std::advance;
#include <cstdint>
#include <cstring>
using std::memcpy;
#include <stdlib.h>
#include <time.h>

/*
  * Index wise:
   *
   *
   *              0  1  2
   *              7  U  3
   *              6  5  4
   *
   *   8  9 10   16 17 18   24 25 26   32 33 34
   *  15 L  11   23 F  19   31 R  27   39 B  35
   *  14 13 12   22 21 20   30 29 28   38 37 36
   *
   *             40 41 42
   *             47 D  43
   *             46 45 44
   */

const char face_names[6] = {'U', 'L', 'F', 'R', 'B', 'D'};
const string move_names[19] = {
  "U", "UP", "D", "DP",
  "F", "FP", "B", "BP",
  "R", "RP", "L", "LP",
  "U2", "R2", "F2",
  "D2", "L2", "B2",
  "NONE"
};

class Cube
{
public:
    enum class FACE : uint8_t {U, L, F, R, B, D};
    enum class MOVE : uint8_t
    {
      U, UP, D, DP,
      F, FP, B, BP,
      R, RP, L, LP,
      U2, R2, F2,
      D2, L2, B2,
      NONE
    };
    
    // Constructors
    Cube();
    Cube(const Cube& cube);
    Cube(const string cubeString);

    // Copy and compare
    Cube& operator=(const Cube rhs);
    bool operator==(const Cube& rhs) const;
    
    // Others
    bool isSolved() const;
    uint64_t getFace(FACE face) const;
    FACE getColor(FACE f, unsigned row, unsigned col) const;
    
    void print();
    string getMove(MOVE ind) const;
    string toString() const;

    Cube& move(MOVE ind);
    Cube& invert(MOVE ind);
    Cube& scramble(uint8_t n_moves);

private:
    array<FACE, 48> cube;

    // Face moves.
    Cube& u();
    Cube& up();
    Cube& u2();

    Cube& l();
    Cube& lp();
    Cube& l2();

    Cube& f();
    Cube& fp();
    Cube& f2();

    Cube& r();
    Cube& rp();
    Cube& r2();

    Cube& b();
    Cube& bp();
    Cube& b2();

    Cube& d();
    Cube& dp();
    Cube& d2();

    // Move methods
    inline void roll90(FACE f);
    inline void roll180(FACE f);
    inline void roll270(FACE f);

    inline void rotateSides90(
      unsigned s_i0, unsigned s_i1, unsigned s_i2, unsigned s_i3,
      unsigned c_i0, unsigned c_i1, unsigned c_i2, unsigned c_i3);
    inline void rotateSides180(
      unsigned s_i0, unsigned s_i1, unsigned s_i2, unsigned s_i3,
      unsigned c_i0, unsigned c_i1, unsigned c_i2, unsigned c_i3);

    void print_face(FACE f);
};

#endif