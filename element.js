$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {
        // $.get("/get_elements");
        // window.location.href = 'element.html';

        // $("#add_element").prop('disabled', true);

        $("#mode_remove_element").hide();

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

        $("#change_remove").click(
            function(){
                $("#mode_add_element").hide();
                $("#mode_remove_element").show();
            }
        );

        $("#change_add").click(
            function(){
                $("#mode_add_element").show();
                $("#mode_remove_element").hide();
            }
        );

        // $("#add_element").click(
        //     function()
        //     {
        //   /* ajax post */
        //   $.post("/add_element.html",
        //     /* pass a JavaScript dictionary */
        //     {
        //         element_number: $("#element_number").val(),
        //         element_name: $("#element_name").val(),
        //         element_code: $("#element_code").val(),
        //         colour1: $("#colour1").val(),
        //         colour2: $("#colour2").val(),
        //         colour3: $("#colour3").val(),
        //         element_radius: $("#element_radius").val()
        //     },
        //     function( data, status )
        //     {
        //       alert( "Data: " + data + "\nStatus: " + status );
        //     }
        //   );
        //     }
        //   );

        // $("form#element_form").blur(function(event) {
        //     event.target.validate().checkForm();
        //     event.target.reportValidity();
        // }).bind('invalid', function() {
        //         // setTimeout(function() { $(event.target).focus();}, 50);
        //         $("#add_element").prop('disabled', true);
        //     });

        // if($("element_form").validate().checkForm()){
        //     $('#add_element').removeAttr("disabled");
        // } else {
        //     $("#add_element").prop('disabled', true);
        // }

        $("#submit_element_form").submit(
            function(event){

                event.preventDefault();

                $('#add_element').prop('disabled', true);

                $.ajax({
                    url: "/add_element",
                    data: {
                        element_number: $("#element_number").val(),
                        element_name: $("#element_name").val(),
                        element_code: $("#element_code").val(),
                        colour1: $("#colour1").val(),
                        colour2: $("#colour2").val(),
                        colour3: $("#colour3").val(),
                        element_radius: $("#element_radius").val()
    
                    },
                    type: 'POST',
                    success: function(data){
                        console.log("SUCESS");
                        alert("Data: " + data);
                        $("#element_number").val("");
                        $("#element_name").val("");
                        $("#element_code").val("");
                        $("#element_radius").val("");
                        $('#add_element').prop('disabled', false);
                    },
                    error: function(){
                        console.log("ERROR");
                        alert("Error");
                        $("#element_number").val("");
                        $("#element_name").val("");
                        $("#element_code").val("");
                        $("#element_radius").val("");
                        $('#add_element').prop('disabled', false);
                    }
                });

                window.location.reload();

            }
        );

        $("#form_remove_element").submit(
            function(event){

                event.preventDefault();

                $('#remove_element').prop('disabled', true);

                $.ajax({
                    url: "/remove_element",
                    data: {
                        element_code: $("#remove").val(),
                    },
                    type: 'POST',
                    success: function(data){
                        console.log("SUCESS");
                        alert("Data: " + data);
                        $('#remove_element').prop('disabled', false);
                    },
                    error: function(){
                        console.log("ERROR");
                        alert("Error");
                        $('#remove_element').prop('disabled', false);
                    }
                });

                window.location.reload();

            }
        );

        // $("#remove_element").click(
        //     function(){

        //         $.post("/remove_element",
        //         {
        //             element_code: $("#remove").val(),

        //         },
        //         function( data, status )
        //         {
        //         alert( "Data: " + data + "\nStatus: " + status );
        //         });

        //         // window.location.reload();
        //     }
        // );

          
          
    }
  );
  