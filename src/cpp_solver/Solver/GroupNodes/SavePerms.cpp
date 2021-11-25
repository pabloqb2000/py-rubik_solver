#include "SavePerms.h"
#include "../IDDFSSolver.h"

#include<iostream>
#include<fstream>
using namespace std;

/**
  * Create a CubeNode from a Cube
  * @param cube base cube
  */
SavePerms::SavePerms (const Cube& cube, const string file_name) : CubeNode(cube) {
    this->file_name = file_name;
    IDDFSSolver solver(12);
    cout << "Creating corner permutation database" << endl;
    solver.findGoal(*(CubeNode*)this);
}

/**
* Convert a permutation of the corners to a string.
*/
SavePerms::perm_t SavePerms::cubeToPerm(const Cube& cube) const
{
    // Note that two facets of a corner dictate the orientation of a corner.
    // The third facet doesn't need to be stored, therefore.  For example,
    // there are two corner cubies with red and blue facets: RBW, and RBY.
    // With red up top and blue on the left, the RBW cubie occupies the top,
    // left, front position.  There's no possible way to get the RBY cubie to
    // occupy that same position such that red is on top and blue is on the
    // left.  Indexing top, left, front, the RBY corner cubie can be in three
    // permutations: RYB, YBR, BRY, but never RBY.
    perm_t perm =
    {  // IDEA: substitute this getColor functions
        cube.getColor(FACE::U, 0, 0),
        cube.getColor(FACE::L, 0, 0),

        cube.getColor(FACE::U, 2, 0),
        cube.getColor(FACE::L, 0, 2),

        cube.getColor(FACE::U, 0, 2),
        cube.getColor(FACE::R, 0, 2),

        cube.getColor(FACE::U, 2, 2),
        cube.getColor(FACE::R, 0, 0),

        cube.getColor(FACE::D, 2, 0),
        cube.getColor(FACE::L, 2, 0),

        cube.getColor(FACE::D, 0, 0),
        cube.getColor(FACE::L, 2, 2),

        cube.getColor(FACE::D, 2, 2),
        cube.getColor(FACE::R, 2, 2),

        cube.getColor(FACE::D, 0, 2),
        cube.getColor(FACE::R, 2, 0),
    };

    return perm;
}

/**
* Convert a permutation of the corners to a string.
*/
SavePerms::perm_t SavePerms::cubeToPerm() const
{
    // Note that two facets of a corner dictate the orientation of a corner.
    // The third facet doesn't need to be stored, therefore.  For example,
    // there are two corner cubies with red and blue facets: RBW, and RBY.
    // With red up top and blue on the left, the RBW cubie occupies the top,
    // left, front position.  There's no possible way to get the RBY cubie to
    // occupy that same position such that red is on top and blue is on the
    // left.  Indexing top, left, front, the RBY corner cubie can be in three
    // permutations: RYB, YBR, BRY, but never RBY.
    perm_t perm =
    {  // IDEA: substitute this getColor functions
        this->getColor(FACE::U, 0, 0),
        this->getColor(FACE::L, 0, 0),

        this->getColor(FACE::U, 2, 0),
        this->getColor(FACE::L, 0, 2),

        this->getColor(FACE::U, 0, 2),
        this->getColor(FACE::R, 0, 2),

        this->getColor(FACE::U, 2, 2),
        this->getColor(FACE::R, 0, 0),

        this->getColor(FACE::D, 2, 0),
        this->getColor(FACE::L, 2, 0),

        this->getColor(FACE::D, 0, 0),
        this->getColor(FACE::L, 2, 2),

        this->getColor(FACE::D, 2, 2),
        this->getColor(FACE::R, 2, 2),

        this->getColor(FACE::D, 0, 2),
        this->getColor(FACE::R, 2, 0),
    };

    return perm;
}

/**
* If the corner permutation is unique, save it in a set.  There are a
* total of 96 possible corner permutations that can be achieved from the
* solved state using only 180-degree turns.
*/
bool SavePerms::isGoal()
{
    perm_t perm = this->cubeToPerm();

    if (this->perms.count(perm) == 0)
    {
        this->perms.insert(perm);

        // There are 96 total permutations.
        if (this->perms.size() == 96)
        {
            return true;
        }
    }

    return false;
}

/**
* Check if the permutation of the cube's corners is one that can be achieved
* by only 180-degree twists.
* @cube The cube.
*/
bool SavePerms::permutationExists(const Cube& cube) const
{
    return this->perms.count(this->cubeToPerm(cube)) == 1;
}

/**
* Quick compare for two permutation arrays.
* @param lhs The left array.
* @param rhs The right array.
*/
bool SavePerms::PermComp::operator()(const perm_t& lhs, const perm_t& rhs) const
{
    // 16 corner facets are stored (see note in the ctor).  Each facet is an
    // 8-bit char (a COLOR), so the array of corners can be treated as two
    // 64-bit ints.  This is quite a bit faster than the default
    // set comparator.
    int64_t lDiff = *(int64_t*)&lhs[0] - *(int64_t*)&rhs[0];

    if (lDiff < 0)
        return true;
    else if (lDiff == 0)
    {
        return *(int64_t*)&lhs[8] < *(int64_t*)&rhs[8];
    }

    return false;
}

void SavePerms::save() const
{
    ofstream wf(this->file_name, ios::out | ios::binary);
    if(!wf) cout << "Cannot open file!" << endl;

    for(perm_t perm : perms) {
        wf.write((char *) &perm, 16*sizeof(Cube::FACE));
    }
    
    wf.close();
    if(!wf.good()) cout << "Error occurred at writing time!" << endl;    
}
