<!DOCTYPE html>
<!-- BEGIN inicio -->
<html lang="en">
    <head>

        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Robik - Un robot imprimible que puede mover el cubo de Rubik</title>

        <!-- Bootstrap -->
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">

        <link href="css/custom.css" rel="stylesheet">


        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
            <script src="http//cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>script>
            <script src="http//cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>script>
        <![endif]-->
    </head>
    <body>

        <!-- Modal pagina en construccion -->
        <div id="enconstruccion" class="modal show" tabindex="-1" role="dialog">
          <div class="modal-dialog">

            <!-- Modal content-->
            <div class="modal-content panel-danger">
              <div id="kaka" class="modal-header panel-heading">
                <button type="button" onclick="$('div#enconstruccion').removeClass('show')" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">P&aacute;gina en construcci&oacute;n!</h4>
              </div>
              <div class="modal-body">
                  <p>El material que aparece en esta p&aacute;gina est&aacute; incompleto y sujeto a muchos cambios.</p>
                  <p>Estamos trabajando para tener lista la documentaci&oacute;n de Robik el d&iacute;a en Abril de 2016.</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" onclick="$('div#enconstruccion').removeClass('show')" data-dismiss="modal">Cerrar</button>
              </div>
            </div>

          </div>
        </div>        

        <nav class="navbar navbar-default" role="navigation">
            <div class="container">
                <!-- Brand and toggle get grouped for better mobile display -->
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="index.html">Robik</a>
                </div>
        
                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="index.html">Inicio</a></li>
                    <li><a href="materiales.html">Materiales</a></li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Construcci&oacute;n<b class="caret"></b></a>
                        <ul class="dropdown-menu">
                            <li><a href="construccion.html">Mec&aacute;nica</a></li>
                            <li><a href="electronica.html">Electr&oacute;nica</a></li>
                        </ul>
                    </li>
                    <li><a href="firmware.html">Firmware</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Enlaces <b class="caret"></b></a>
                        <ul class="dropdown-menu">
                            <li><a href="https://facebook.com/recunchomaker">Facebook</a></li>
                            <li><a href="https://twitter.com/RecunchoMaker">Twitter</a>
                            <li><a href="https://flickr.com/recunchomaker">Flickr</a>
                        </ul>
                    </li>
                </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>
            
<!-- END inicio -->
