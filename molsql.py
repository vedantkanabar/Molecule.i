import sqlite3;
import os;
from MolDisplay import Molecule;
from MolDisplay import Atom;
from MolDisplay import Bond;
import MolDisplay;


# Database class
class Database:


    # Constructor function to establish connection
    def __init__ ( self, reset = False ):

        # if reset is True then reset the file if it exists
        if (reset == True):
            if os.path.exists( 'molecules.db' ):
                os.remove( 'molecules.db' );
        
        # set up connection
        self.conn = sqlite3.connect( 'molecules.db' );



    # Creat tables function to create tables
    def create_tables( self ):

        # Elements table creation
        self.conn.execute(   """CREATE TABLE IF NOT EXISTS Elements (
                                ELEMENT_NO INTEGER PRIMARY KEY NOT NULL,
                                ELEMENT_CODE VARCHAR(3) NOT NULL,
                                ELEMENT_NAME VARCHAR(32) NOT NULL,
                                COLOUR1 CHAR(6) NOT NULL,
                                COLOUR2 CHAR(6) NOT NULL,
                                COLOUR3 CHAR(6) NOT NULL,
                                RADIUS DECIMAL(3) NOT NULL);""" );

        # Atoms table creation
        self.conn.execute(   """CREATE TABLE IF NOT EXISTS Atoms (
                                ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                ELEMENT_CODE VARCHAR(3) NOT NULL,
                                X DECIMAL(7,4) NOT NULL,
                                Y DECIMAL(7,4) NOT NULL,
                                Z DECIMAL(7,4) NOT NULL,
                                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements );""" );

        # Bonds table creation
        self.conn.execute(   """CREATE TABLE IF NOT EXISTS Bonds (
                                BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                A1 INTEGER NOT NULL,
                                A2 INTEGER NOT NULL,
                                EPAIRS INTEGER NOT NULL);""" );

        # Molecules table creation
        self.conn.execute(   """CREATE TABLE IF NOT EXISTS Molecules (
                                MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                NAME TEXT NOT NULL,
                                UNIQUE (NAME) );""" );

        # MoleculeAtom table creation
        self.conn.execute(   """CREATE TABLE IF NOT EXISTS MoleculeAtom (
                                MOLECULE_ID INTEGER NOT NULL,
                                ATOM_ID INTEGER NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, ATOM_ID) 
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""" );

        # MoleculeBond table creation
        self.conn.execute(   """CREATE TABLE IF NOT EXISTS MoleculeBond (
                                MOLECULE_ID INTEGER NOT NULL,
                                BOND_ID INTEGER NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, BOND_ID) 
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY (BOND_ID) REFERENCES Bonds );""" );



    # Set Item funciton to add to table givne values tuple
    def __setitem__( self, table, values ):

        # tuples_string = str(values);

        query = f"""INSERT
                    INTO   {table}
                    VALUES   (?,?,?,?,?,?,?);""" 

        self.conn.execute(query, values);
        self.conn.commit();

    

    # Add atom function to add an atom
    def add_atom( self, molname, atom ):

        # Adding to Atoms table
        self.conn.execute(  """INSERT
                                INTO   Atoms ( ELEMENT_CODE,  X, Y, Z )
                                VALUES    ( ?, ?, ?, ? );""", (atom.atom.element, atom.atom.x, atom.atom.y, atom.atom.z) );
        self.conn.commit();

        # Extracting atom id of added atom
        data = self.conn.execute( """SELECT last_insert_rowid();""");
        record = data.fetchone();
        atom_id = record[0];

        # Getting mol id of molecule wih the molname
        data = self.conn.execute( """SELECT Molecules.MOLECULE_ID FROM Molecules 
                                        WHERE NAME=?""", (molname,) );
        record = data.fetchone();
        mol_id = record[0];

        # Inserting to MoleculeAtom table
        self.conn.execute(  """INSERT
                                INTO   MoleculeAtom ( MOLECULE_ID, ATOM_ID )
                                VALUES    ( ?, ? );""", (mol_id, atom_id) );
        self.conn.commit();



    # Add bond function to add a bond
    def add_bond( self, molname, bond ):

        # Adding to Bonds table
        self.conn.execute(  """INSERT
                                INTO   Bonds ( A1, A2, EPAIRS )
                                VALUES    ( ?, ?, ? );""", (bond.bond.a1, bond.bond.a2, bond.bond.epairs) );
        self.conn.commit();

        # Extracting bond id of added atom
        data = self.conn.execute( """SELECT last_insert_rowid();""");
        record = data.fetchone();
        bond_id = record[0];

        # Getting mol id of molecule wih the molname
        data = self.conn.execute( """SELECT Molecules.MOLECULE_ID FROM Molecules 
                                        WHERE (NAME=?);""", (molname,) );
        record = data.fetchone();
        mol_id = record[0];

        # Inserting to MoleculeBond table
        self.conn.execute(  """INSERT
                                INTO   MoleculeBond ( MOLECULE_ID, BOND_ID )
                                VALUES    ( ?, ? );""",(mol_id, bond_id) );
        self.conn.commit();



    # Add Molecule to add a molecule from .sdf file
    def add_molecule( self, name, fp ):

        # creating Molecule to read from
        mol = Molecule();

        # parsing .sdf file
        mol.parse(fp);

        # setting up Mol ID
        self.conn.execute(  """INSERT
                                INTO   Molecules ( NAME )
                                VALUES    (?);""", (name,) );
        self.conn.commit();

        # going though atoms
        for i in range(mol.atom_no):
            atom = mol.get_atom(i);
            Atom = MolDisplay.Atom(atom);
            self.add_atom(name,Atom);

        # going through bonds
        for i in range(mol.bond_no):
            bond = mol.get_bond(i);
            Bond = MolDisplay.Bond(bond);
            self.add_bond(name,Bond);



    # Load Mol to get Molecule from the database
    def load_mol( self, name ):

        # setting up molecule to return
        mol = Molecule();

        # Join to get the Atoms table
        data = self.conn.execute( f"""SELECT Atoms.ATOM_ID, Atoms.ELEMENT_CODE, Atoms.X, Atoms.Y, Atoms.Z FROM Atoms 
                                        INNER JOIN MoleculeAtom
                                        ON (Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
                                            AND MoleculeAtom.MOLECULE_ID=Molecules.MOLECULE_ID)
                                        INNER JOIN Molecules
                                        ON (Molecules.NAME=?)
                                        ORDER BY Atoms.ATOM_ID;""", (name,) );
        records = data.fetchall();

        # addting all atoms found
        for row in records:
            mol.append_atom( row[1], row[2], row[3], row[4] );

        # Join to get the Bonds table
        data = self.conn.execute( f"""SELECT Bonds.BOND_ID, Bonds.A1, Bonds.A2, Bonds.EPAIRS FROM Bonds 
                                        INNER JOIN MoleculeBond
                                        ON (Bonds.BOND_ID = MoleculeBond.BOND_ID
                                            AND MoleculeBond.MOLECULE_ID=Molecules.MOLECULE_ID)
                                        INNER JOIN Molecules
                                        ON (Molecules.NAME=?)
                                        ORDER BY Bonds.BOND_ID;""", (name,) );
        records = data.fetchall();

        # addting all bonds found
        for row in records:
            mol.append_bond( row[1], row[2], row[3] );

        # return the MolDisplay Molecule
        return mol;

    

    # Radius funtion to return Radius dictionary
    def radius( self ):

        # set up the dictionary
        radius_dictionary = {}

        # query for corresponding records
        data = self.conn.execute( """SELECT Elements.ELEMENT_CODE,Elements.RADIUS FROM Elements;""" );
        records = data.fetchall();

        # adding every entry found
        for row in records:
            radius_dictionary.update({row[0]:row[1]});

        # returns a python dictionary
        return radius_dictionary;



    # Radius funtion to return Element name dictionary
    def element_name( self ):

        # set up the dictionary
        element_name_dictionary = {}

        # query for corresponding records
        data = self.conn.execute( """SELECT Elements.ELEMENT_CODE,Elements.ELEMENT_NAME FROM Elements;""" );
        records = data.fetchall();

        # adding every entry found
        for row in records:
            element_name_dictionary.update({row[0]:row[1]});

        # returns a python dictionary
        return element_name_dictionary;



    # Radical Gradients function to set up gradient ids for svg
    def radial_gradients( self ):

        # set up final retuen
        final_result = "";

        # query to select the rows
        data = self.conn.execute( """SELECT Elements.ELEMENT_NAME,Elements.COLOUR1,Elements.COLOUR2,Elements.COLOUR3 FROM Elements;""" );
        records = data.fetchall();

        # for every row found, set up radialGradient ID then add to final string
        for row in records:

            # setting up radialGradient
            radialGradientSVG = """
  <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
    <stop offset="0%%" stop-color="#%s"/>
    <stop offset="50%%" stop-color="#%s"/>
    <stop offset="100%%" stop-color="#%s"/>
  </radialGradient>""" % (row[0], row[1], row[2], row[3]);

            # add to final string
            final_result = final_result + radialGradientSVG;


        # returns string as a final result
        return final_result;


    def get_elements( self ):
        
        # set up the dictionary
        elements = []

        # query for corresponding records
        data = self.conn.execute( """SELECT Elements.ELEMENT_CODE,Elements.ELEMENT_NAME FROM Elements;""" );
        records = data.fetchall();

        for row in records:
            elements.append((row[0], row[1]));

        return elements;

    def remove_element( self, element_code ):

        # query for deleteing element
        self.conn.execute( f"""DELETE FROM Elements WHERE (Elements.ELEMENT_CODE=?);""", (element_code,) );
        self.conn.commit();

    def get_molecules( self ):
        
        # set up the dictionary
        molecules = []

        # query for corresponding records
        data = self.conn.execute( """SELECT Molecules.NAME FROM Molecules;""" );
        records = data.fetchall();

        for row in records:
            mol = self.load_mol(row[0]);
            
            molecules.append({"name":row[0],
                               "atom_no":mol.atom_no, 
                               "bond_no":mol.bond_no});

        return molecules;

    def get_element_verification( self ):
        
        # set up the dictionary
        elements = []

        # query for corresponding records
        data = self.conn.execute( """SELECT Elements.ELEMENT_CODE,Elements.ELEMENT_NAME,Elements.ELEMENT_NO FROM Elements;""" );
        records = data.fetchall();

        for row in records:
            elements.append((row[0], row[1], row[2]));

        return elements;
