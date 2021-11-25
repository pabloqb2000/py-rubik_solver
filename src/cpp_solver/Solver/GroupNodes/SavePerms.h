#ifndef SAVEPERMS_H
#define SAVEPERMS_H

#include "CubeNode.h"
#include <set>
using std::set;
#include <array>
using std::array;
#include <cstdint>

class SavePerms : public CubeNode
{
    public:
        SavePerms(const Cube& cube, const string file_name="");
        bool isGoal();
        bool permutationExists(const Cube& cube) const;

    private:
        typedef array<Cube::FACE, 16> perm_t;

        // Fast comparator for a permutation.
        struct PermComp
        {
            bool operator()(const perm_t& lhs, const perm_t& rhs) const;
        };

        set<perm_t, PermComp> perms;
        string file_name;

        perm_t cubeToPerm(const Cube& cube) const;
        perm_t cubeToPerm() const;
        void save() const;
};


#endif