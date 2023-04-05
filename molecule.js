$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {

        var molecules;
        var svgfile;
        var empty = true;

        $("#display").prop('disabled', true);
        $("#no_mol").hide();
        $("#has_mol").hide();
  
          $("#home").click(
              function(){
                  $.get("/index.html");
              }
          );
  
          $("#element").click(
              function(){
                  $.get("/element.html");
              }
          );
  
          $("#upload").click(
              function(){
                  $.get("/upload.html");
              }
          );
  
          $("#molecule").click(
              function(){
                  $.get("/molecule.html");
              }
          );


          
            $.ajax({
                url: "/molecules",
                type: 'GET',
                success: function(data, status, xhr){
                    console.log("SUCESS");
                    // var label = $('<label>Select Molecule to Display</label>');
                    // var selectoptions = $('<select id="selection"></select>');
                    if(xhr.status == 210){
                        console.log("210");
                        empty = true;
                        $("#no_mol").show();
                    }
                    else{

                        $("#has_mol").show();

                        $("#display").prop('disabled', false);
                        molecules = data;
                        empty = false;

                        for(var i=0; i<molecules.length; i++){
                            var string = '<option id="'+molecules[i].name+'" value="'+molecules[i].name+'">'+molecules[i].name+'  |  Atom No:'+molecules[i].atom_no+', Bond No:'+molecules[i].bond_no+' </option>';
                            $("#selection").append(string);
                        }
                        // $("#dropbox").append(label);
                        // $("#dropbox").append(selectoptions);
                    }
                },
                error: function(xhr){
                    console.log("ERROR");
                    console.log(xhr);

                }
            });

            $("#display").click(function(){

                $.ajax({
                    url: "/setmolecule",
                    type: 'POST',
                    data: {
                        name: $("#selection").val(),
                        rotation: $("#rotation").val(),
                        degrees: $("#degrees").val()
                    },
                    success: function(data){
                        $("#image_div").html(data);
                        $("html, body").animate({scrollTop:$(document).height()},1000);
                    }
                });
            });

  
    }
  );
  