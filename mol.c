#include "mol.h"


// FUNCTION atomset to set the variables in a given atom structure
void atomset( atom * atom, char element[3], double *x, double *y, double *z ){

    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    
}



// FUNCTION atomget to get the variables data from a given atom structure
void atomget( atom *atom, char element[3], double *x, double *y, double *z ){

    strcpy(element, atom->element);

    *x = atom->x;
    *y = atom->y;
    *z = atom->z;

}


// FUNCTION bondset to set the variables in a given bond structure
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){

    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = *atoms;
    compute_coords (bond);

}



// FUNCTION bondget to get the variables data from a given bond structure
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){

    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;

}




// FUNCTION compute_coords to compute the other attributes of bond
void compute_coords( bond *bond ){

    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z)/2;
    bond->len = sqrt((bond->x1-bond->x2)*(bond->x1-bond->x2) + (bond->y1-bond->y2)*(bond->y1-bond->y2));
    bond->dx = (bond->x2 - bond->x1)/bond->len;
    bond->dy = (bond->y2 - bond->y1)/bond->len;

}



// FUNCTION bond_comp to compare two bonds for the sort function
int bond_comp( const void *a, const void *b ){

    bond * aa = *(bond**)a;
    bond * bb = *(bond**)b;

    if(aa->z > bb->z){
        return 1;
    } else if(aa->z < bb->z){
        return -1;
    } else{
        return 0;
    }

}


// FUNCTION molmalloc to return a pointer to point to memory location for space assigned for molecule
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){
    
    molecule * mol = NULL;

    // allocating space for molecule and checking if malloc fails
    mol = malloc(sizeof(molecule));
    if(mol == NULL){
        return NULL;
    }

    // setting up atom parameters
    mol->atom_max = atom_max;
    mol->atom_no = 0;

    // allocating space for atoms array and checking if malloc fails
    mol->atoms = malloc(sizeof(atom)*atom_max);
    if(mol->atoms == NULL){
        free(mol);
        return NULL;
    }

    // allocating space for atom pointers array and checking if malloc fails
    mol->atom_ptrs = malloc(sizeof(atom*)*atom_max);
    if(mol->atom_ptrs == NULL){
        free(mol->atoms);
        free(mol);
        return NULL;
    }

    // setting up bond parameters
    mol->bond_max = bond_max;
    mol->bond_no = 0;

    // allocating space for bonds array and checking if malloc fails
    mol->bonds = malloc(sizeof(bond)*bond_max);
    if(mol->bonds == NULL){
        free(mol->atoms);
        free(mol->atom_ptrs);
        free(mol);
        return NULL;
    }

    // allocating space for bond pointers array and checking if malloc fails
    mol->bond_ptrs = malloc(sizeof(bond*)*bond_max);
    if(mol->bond_ptrs == NULL){
        free(mol->atoms);
        free(mol->atom_ptrs);
        free(mol->bonds);
        free(mol);
        return NULL;
    }

    return mol;

}



// FUNCTION molcopy to return a pointer to a new copy of given molecule
molecule *molcopy( molecule *src ){

    // allocating space for copy mol and checking if malloc fails
    molecule * mol = NULL;
    mol = molmalloc(src->atom_max, src->bond_max);
    if(mol == NULL){
        return NULL;
    }

    // adding atoms to the molecule copy
    for(int i=0; i< src->atom_no; i++){
        molappend_atom(mol, &src->atoms[i]);
    }

    // adding bonds to the molecule copy
    for(int i=0; i< src->bond_no; i++){
        molappend_bond(mol, &src->bonds[i]);
    }

    return mol;

}



// FUNCTION molfree to free memory used by a molecule pointer
void molfree( molecule *ptr ){

    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);

}



// FUNCTION molappend_atom to add a new atom to given molecule
void molappend_atom( molecule *molecule, atom *atom ){

    // case where no space is there in the arrays
    if(molecule->atom_max == 0){

        molecule->atom_max = 1;

        // reallocating space for atoms array and checking if realloc fails
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * (molecule->atom_max) );
        if(molecule->atoms == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reallocating space for atom pointers array and checking if realloc fails
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * (molecule->atom_max) );
        if(molecule->atom_ptrs == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reassigning the pointers to new rallocated memonory
        for(int i=0; i<molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }

    } else if(molecule->atom_max == molecule-> atom_no){ // else if arrays are full

        molecule->atom_max = molecule->atom_max*2;

        // reallocating space for atoms array and checking if realloc fails
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * (molecule->atom_max) );
        if(molecule->atoms == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reallocating space for atom pointers array and checking if realloc fails
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * (molecule->atom_max));
        if(molecule->atom_ptrs == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reassigning the pointers to new rallocated memonory
        for(int i=0; i<molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }

    }

    // adding the new atom to the correct memory location after confirming existence
    strcpy(molecule->atoms[molecule->atom_no].element, atom->element);
    molecule->atoms[molecule->atom_no].x = atom->x;
    molecule->atoms[molecule->atom_no].y = atom->y;
    molecule->atoms[molecule->atom_no].z = atom->z;

    // adding location of new atom to the atom pointers array
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    molecule->atom_no++;

}



// FUNCTION molappend_bond to add a new bond to given molecule
void molappend_bond( molecule *molecule, bond *bond ){

    // case where no space is there in the arrays
    if(molecule->bond_max == 0){

        molecule->bond_max = 1;

        // reallocating space for bonds array and checking if realloc fails
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond)*molecule->bond_max);
        if(molecule->bonds  == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reallocating space for bond pointers array and checking if realloc fails
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*)*molecule->bond_max);
        if(molecule->bond_ptrs == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reassigning the pointers to new rallocated memonory
        for(int i=0; i<molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }

    } else if(molecule->bond_max ==  molecule-> bond_no){ // else if arrays are full

        molecule->bond_max = molecule->bond_max*2;

        // reallocating space for bonds array and checking if realloc fails
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond)*molecule->bond_max);
        if(molecule->bonds == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reallocating space for bond pointers array and checking if realloc fails
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*)*molecule->bond_max);
        if(molecule->bond_ptrs == NULL){
            fprintf(stderr, "Realloc for molecule failed\n");
            exit(-1);
        }

        // reassigning the pointers to new rallocated memonory
        for(int i=0; i<molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }

    }

    // adding the new bond to the correct memory location after confirming existence
    molecule->bonds[molecule->bond_no].a1 = bond->a1;
    molecule->bonds[molecule->bond_no].a2 = bond->a2;
    molecule->bonds[molecule->bond_no].atoms = molecule->atoms;
    molecule->bonds[molecule->bond_no].epairs = bond->epairs;
    compute_coords(&molecule->bonds[molecule->bond_no]);

    // adding location of new bond to the bond pointers array
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    molecule->bond_no++;

}



// FUNCTION molsort to sort pointers array in molecule by z values for atom and average z values in bonds
void molsort( molecule *molecule ){

    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom*), &compare_atom);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond*), &bond_comp);

}



// FUNCTION xrotation to set up xform_matrix for rotation in x direction by deg angle
void xrotation( xform_matrix xform_matrix, unsigned short deg ){

    double rad = deg_to_rad(deg);

    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);

}



// FUNCTION yrotation to set up xform_matrix for rotation in y direction by deg angle
void yrotation( xform_matrix xform_matrix, unsigned short deg ){

    double rad = deg_to_rad(deg);

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
    
}



// FUNCTION zrotation to set up xform_matrix for rotation in z direction by deg angle
void zrotation( xform_matrix xform_matrix, unsigned short deg ){

    double rad = deg_to_rad(deg);

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
    
}



// FUNCTION mol_xform to transform all atoms in a molecule by the xform_matrix
void mol_xform( molecule *molecule, xform_matrix matrix ){

    for(int i=0; i<molecule->atom_no; i++){
        atom_transformation(matrix, &molecule->atoms[i]);
    }

    for(int i=0; i<molecule->bond_no; i++){
        compute_coords(&molecule->bonds[i]);
    }

}



// HELPER FUNCTIONS



// FUNCTION compare_atom for quick sort funciton in molsort function to sort atoms
int compare_atom(const void *a, const void *b){

    atom * aa = *(atom**)a;
    atom * bb = *(atom**)b;
    
    if(aa->z > bb->z){
        return 1;
    } else if(aa->z < bb->z){
        return -1;
    } else {
        return 0;
    }

}



// FUNCITON deg_to_rad to convert an unsigned short deg to a double radian
double deg_to_rad(unsigned short deg){

    double rad = (double) deg;
    rad = rad * M_PI / 180.0;
    return rad;

}



// FUNCTION atom_transformation to transform a specific atom using a xform_matrix
void atom_transformation( xform_matrix xform_matrix, atom *curr ){

    double res[3] = { 0.0, 0.0, 0.0 };
    double temp[3] = { curr->x, curr->y, curr->z };

    for(int i=0; i<3; i++){
        for(int j=0; j<3; j++){
            res[i] = res[i] + (temp[j] * xform_matrix[i][j]);
        }
    }

    curr->x = res[0];
    curr->y = res[1];
    curr->z = res[2];

}

