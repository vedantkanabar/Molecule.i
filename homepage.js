$(document).ready( 
  /* this defines a function that gets called after the document is in memory */
  function()
  {

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

  }
);
