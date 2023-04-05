import sys;
import io;
import molecule as m;
import MolDisplay;
from MolDisplay import Molecule;
from MolDisplay import Atom;
from MolDisplay import Bond;
from http.server import HTTPServer, BaseHTTPRequestHandler;
import urllib; 
import json;
from molsql import Database;

# svg string for storing svg data
the_svg = [];
svg = "";
svg_mol = MolDisplay.Molecule();
public_files = [ '/index.html', '/stylesheet.css', '/homepage.js', '/element.js', '/upload.html', '/upload.js', '/molecule.html', '/molecule.js' ];

class MyHandler( BaseHTTPRequestHandler ):

    db = Database(reset=True);
    # db = Database(reset=False);
    db.create_tables();
    db['Elements'] = (1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25);
    db['Elements'] = (6, 'C', 'Carbon', '808080', '010101', '000000', 40);
    db['Elements'] = (7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40);
    db['Elements'] = (8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40);
    MolDisplay.radius = db.radius();
    MolDisplay.element_name = db.element_name();
    MolDisplay.radial_gradients = db.radial_gradients();

    def do_GET(self):

        if self.path in public_files:   # make sure it's a valid file
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read();
            fp.close();

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/element.html":

            self.send_response( 200 );  # OK

            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:]  );

            data = fp.read();
            # print(data);

            fp.close();

            begin = """<select id="remove">""";
            end = """</select>""";

            replace = """<select id="remove">\n""";

            elements = self.db.get_elements();

            for element in elements:
                replace += f"""                <option value="{element[0]}">{element[0]}: {element[1]}</option>\n""";
            
            replace += "            </select>";

            # data = data.replace( toreplace, replace);

            idxbegin = data.find(begin);
            idxend = data.find(end) + 9;

            final = data[:idxbegin];
            final += replace;
            final += data[idxend:];

            # print(final);

            # create and send headers
            self.send_header( "Content-length", len(final) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( final, "utf-8" ) );

        elif self.path == "/molecules":

            molecules = self.db.get_molecules();

            if len(molecules) == 0:
                self.send_response( 210 );  # OK

                self.send_header( "Content-type", "application/json" );
                self.end_headers();
                molecules_json = json.dumps(molecules);
                self.wfile.write( bytes( molecules_json, "utf-8" ) );
            else:

                self.send_response( 200 );  # OK
                self.send_header( "Content-type", "application/json" );
                self.end_headers();
                molecules_json = json.dumps(molecules);
                self.wfile.write( bytes( molecules_json, "utf-8" ) );

        else:
            BaseHTTPRequestHandler.send_error(self, 404, 'not found');

    
    def do_POST(self):

        if self.path == "/add_element":

            message = "";

            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            elements = self.db.get_element_verification();

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            for element in elements:
                if int(postvars["element_number"][0]) == element[2]:
                    message = "Error, element number already taken";
                    self.send_response( 200 ); # OK
                    self.send_header( "Content-type", "text/plain" );
                    self.send_header( "Content-length", len(message) );
                    self.end_headers();
                    self.wfile.write( bytes(message, "utf-8") );
                    return;
                if postvars["element_code"][0] == element[0]:
                    message = "Error, element code already taken";
                    self.send_response( 200 ); # OK
                    self.send_header( "Content-type", "text/plain" );
                    self.send_header( "Content-length", len(message) );
                    self.end_headers();
                    self.wfile.write( bytes(message, "utf-8") );
                    return;
                if postvars["element_name"][0] == element[1]:
                    message = "Error, element name already taken";
                    self.send_response( 200 ); # OK
                    self.send_header( "Content-type", "text/plain" );
                    self.send_header( "Content-length", len(message) );
                    self.end_headers();
                    self.wfile.write( bytes(message, "utf-8") );
                    return;

            try:
                self.db['Elements'] = (int(postvars["element_number"][0]),
                                    postvars["element_code"][0], 
                                    postvars["element_name"][0], 
                                    postvars["colour1"][0][1:].upper(), 
                                    postvars["colour2"][0][1:].upper(), 
                                    postvars["colour3"][0][1:].upper(), 
                                    int (postvars["element_radius"][0]));
            except:
                message="Error, Element add not sucessful";
            else:
                message="Element added sucessfully";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes(message, "utf-8") );



        elif self.path == "/setmolecule":
            self.send_response( 200 ); # OK

            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            svg_mol = MolDisplay.Molecule();
            svg_mol = self.db.load_mol(postvars["name"][0]);

            if int(postvars["degrees"][0]) == 0:
                svg_mol.sort();

            else:
                if postvars["rotation"][0] == 'x':
                    mx = m.mx_wrapper(int(postvars["degrees"][0]),0,0);
                    svg_mol.xform( mx.xform_matrix );
                    svg_mol.sort();
                elif postvars["rotation"][0] == 'y':
                    my = m.mx_wrapper(0,int(postvars["degrees"][0]),0);
                    svg_mol.xform( my.xform_matrix );
                    svg_mol.sort();
                else:
                    mz = m.mx_wrapper(0,0,int(postvars["degrees"][0]));
                    svg_mol.xform( mz.xform_matrix );
                    svg_mol.sort();


            MolDisplay.radius = self.db.radius();
            MolDisplay.element_name = self.db.element_name();
            MolDisplay.radial_gradients = self.db.radial_gradients();

            svg = svg_mol.svg();

            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(svg) );
            self.end_headers();
            self.wfile.write( bytes(svg, "utf-8") );


        elif self.path == "/upload_file.html":

            message = "";

            self.send_response( 200 ); # OK

            line_counter = 0;
            molecules = self.db.get_molecules();

            # first convert file from byte to text IO
            length = int(self.headers['Content-Length']);
            filedata = self.rfile.read(length);
            parse_data = io.TextIOWrapper(io.BytesIO(filedata));
            fname_data = io.TextIOWrapper(io.BytesIO(filedata));

            Lines = fname_data.readlines();

            for line in Lines:
                line_counter = line_counter+1;
                # print(line);
                if """Content-Disposition: form-data; name="mol_name""""" in line:
                    break;

            # print("break");
            
            # print(Lines[line_counter+1]);
            mol_name = Lines[line_counter+1].split()[0];

            if len(molecules) > 0:
                for molecule in molecules:
                    if mol_name == molecule["name"]:
                        message = "Error, Molecule name already in use";

                        self.send_header( "Content-type", "text/plain" );
                        self.send_header( "Content-length", len(message) );
                        self.end_headers();
                        self.wfile.write( bytes(message, "utf-8") );
                        return;

            parse_data.readline();
            parse_data.readline();
            parse_data.readline();
            parse_data.readline();

            try:
                self.db.add_molecule(mol_name, parse_data);
            except:
                message = "Error, File Invalid";
            else:
                message = "File read sucessful";

            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes(message, "utf-8") );


        elif self.path == "/remove_element":

            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            self.db.remove_element(postvars["element_code"][0]);

            message = "Element "+postvars["element_code"][0]+" deleted sucessfully";

            # MolDisplay.radius = self.db.radius();
            # MolDisplay.element_name = self.db.element_name();
            # MolDisplay.radial_gradients = self.db.radial_gradients();

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes(message, "utf-8") );

        # else print error message
        else:
            BaseHTTPRequestHandler.send_error(self, 404, 'not found');

#setting up server and homepage
httpd = HTTPServer(( 'localhost', int(sys.argv[1]) ), MyHandler);
httpd.serve_forever();
