$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {
  
        $('#loading').hide();

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

          $("#upload_form").submit(
            function(event){

                event.preventDefault();

                $('#upload_file_button').prop('disabled', true);
                $('#loading').show();

                var formdata = new FormData();
                formdata.append("file", $("#sdf_file")[0].files[0]);
                formdata.append("mol_name", $("#mol_name").val());

                $.ajax({
                    url: "/upload_file.html",
                    data: formdata,
                    processData: false,
                    contentType: false,
                    type: 'POST',
                    success: function(data){
                        console.log("SUCESS");
                        alert("Data: " + data);
                        $("#mol_name").val("");
                        $("#sdf_file").val("");
                        $('#loading').hide();
                        $("#upload_file_button").prop('disabled', false);
                    },
                    error: function(){
                        console.log("ERROR");
                        alert("Error");
                        $("#mol_name").val("");
                        $("#sdf_file").val("");
                        $('#loading').hide();
                        $("#upload_file_button").prop('disabled', false);
                    }
                });

            }
        );
  
    }
  );
  