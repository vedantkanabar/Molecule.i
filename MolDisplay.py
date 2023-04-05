import molecule;
import io;

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""";

radial_gradients = "";

default = """
  <radialGradient id="Default" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
    <stop offset="0%" stop-color="#FF0000"/>
    <stop offset="50%" stop-color="#00FF00"/>
    <stop offset="100%" stop-color="#0000FF"/>
  </radialGradient>""";

footer = """</svg>""";

offsetx = 500;
offsety = 500;

# Atom Wrapper class
class Atom:

    # Constructor function
    def __init__ ( self, c_atom ):
        self.atom = c_atom;
        self.z = c_atom.z;


    # svg function
    def svg ( self ):

        # calculating cx, cy, radius and the colour
        xtr = self.atom.x * 100 + offsetx;
        ytr = self.atom.y * 100 + offsety;

        if self.atom.element in element_name:
            radtr = radius.get(self.atom.element);
            colour = element_name.get(self.atom.element);
        else:
            radtr = 40;
            colour = "Default";
        
        # returns the svg string
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (xtr, ytr, radtr, colour);
    

    # str testing function
    def __str__ ( self ):
        return 'Element = %s, x=%.2f, y=%.2f, z=%.2f' % (self.atom.element, self.atom.x, self.atom.y, self.z);



# Bond Wrapper class
class Bond:


    # Constructor function
    def __init__ ( self, c_bond ):
        self.bond = c_bond;
        self.z = c_bond.z;


    # svg function
    def svg ( self ):

        # calculating the polygon corners
        corner_top_left_x = (self.bond.x1*100 + offsetx) + self.bond.dy*10;
        corner_top_left_y = (self.bond.y1*100 + offsety) - self.bond.dx*10;

        corner_bottom_left_x = (self.bond.x1*100 + offsetx) - self.bond.dy*10;
        corner_bottom_left_y = (self.bond.y1*100 + offsety) + self.bond.dx*10;

        corner_top_right_x = (self.bond.x2*100 + offsetx) + self.bond.dy*10;
        corner_top_right_y = (self.bond.y2*100 + offsety) - self.bond.dx*10;
        
        corner_bottom_right_x = (self.bond.x2*100 + offsetx) - self.bond.dy*10;
        corner_bottom_right_y = (self.bond.y2*100 + offsety) + self.bond.dx*10;

        # returns the svg string
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (corner_top_left_x, corner_top_left_y, corner_bottom_left_x, corner_bottom_left_y, corner_bottom_right_x, corner_bottom_right_y, corner_top_right_x, corner_top_right_y); 


    # str testing function
    def __str__ ( self ):
        return 'A1=%d, A2=%d, epairs=%d, x1=%.2f, y1=%.2f, x2=%.2f, y2=%.2f, z=%.2f, len=%.2f, dx=%.2f, dy=%.2f' % (self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.z, self.bond.len, self.bond.dx, self.bond.dy);



# Molecule wrapper subclass
class Molecule (molecule.molecule):


    # str testing function
    def __str__ ( self ):

        result = 'Atom no = %d\n' % (self.atom_no);

        for i in range(self.atom_no):
            atom = self.get_atom(i);
            the_Atom = Atom(atom);
            result += the_Atom.__str__() + '\n';

        result += 'Bond no = %d\n' % (self.bond_no);

        for i in range(self.bond_no):
            bond = self.get_bond(i);
            the_Bond = Bond(bond);
            result += the_Bond.__str__() + '\n';

        return result;


    # svg function
    def svg ( self ):

        # setting up result str
        result = header;

        result += radial_gradients;

        result += default;

        i = 0;
        j = 0;

        while i < self.atom_no and j < self.bond_no:
            atom = self.get_atom(i);
            the_Atom = Atom(atom);
            bond = self.get_bond(j);
            the_Bond = Bond(bond);

            if the_Atom.z < the_Bond.z:
                result += the_Atom.svg();
                i = i+1;
            else:
                result += the_Bond.svg();
                j = j+1;
        
        while i < self.atom_no:
            atom = self.get_atom(i);
            the_Atom = Atom(atom);
            result += the_Atom.svg();
            i = i+1;

        while j < self.bond_no:
            bond = self.get_bond(j);
            the_Bond = Bond(bond);
            result += the_Bond.svg();
            j = j+1;

        result += footer;

        return result;


    # parse function
    def parse ( self, file ):

        # skipping first 3 lines
        file.readline();
        file.readline();
        file.readline();

        # getting atom no and bond no
        intial = [int(s) for s in file.readline().split() if s.isdigit()];
        atom_no = intial[0];
        bond_no = intial[1];

        # reading atoms
        for i in range(atom_no):
            atom = [str(s) for s in file.readline().split()];
            x = float(atom[0]);
            y = float(atom[1]);
            z = float(atom[2]);
            element = atom[3];

            self.append_atom(element,x,y,z);

        # reading bonds
        for i in range(bond_no):
            bond = [int(s) for s in file.readline().split() if s.isdigit()];
            a1 = bond[0] - 1;
            a2 = bond[1] - 1;
            epairs = bond[2];

            self.append_bond(a1,a2,epairs);
        

