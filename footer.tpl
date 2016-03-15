            <!-- BEGIN footer -->
            <div id="footer">
                <div class="row">
                    <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6 text-center">
                        <p>2016 · <a href="recunchomaker.org">recunchomaker.com</a> · Santiago de Compostela · Galicia · Espa&ntilde;a</p>
<a href="http://creativecommons.org/licenses/by-sa/4.0/" rel="license">Licencia Creative Commons Attribution-ShareAlike 4.0</a>

</p>

                    </div>
                    <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6 text-right">
                <a href="https://facebook.com/recunchomaker"><i id="social-fb" class="fa fa-facebook-square fa-3x social"></i></a>
                <a href="https://twitter.com/RecunchoMaker"><i id="social-tw" class="fa fa-twitter-square fa-3x social"></i></a>
                <a href="https://flickr.com/recunchomaker"><i id="social-fl" class="fa fa-flickr fa-3x social"></i></a>
                    </div>
                </div>
            </div>
                                  
        </div>
            
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
        <script>
            $(function() {
                var pgurl = window.location.href.substr(window.location.href
                        .lastIndexOf("/")+1);
                $("nav div li a").each(function(){
                    if($(this).attr("href") == pgurl || $(this).attr("href") == '' ) {
                        if($(this).parent().parent().attr('class')=="dropdown-menu") {
                            $(this).parent().parent().parent().addClass("active");
                            $(this).parent().addClass("active");
                        } else {
                            $(this).parent().addClass("active");
                    }
                    }
                })
            });
        </script>
    </body>
</html>

            <!-- END footer -->
