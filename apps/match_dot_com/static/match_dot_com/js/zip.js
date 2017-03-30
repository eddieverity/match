$(document).ready(function() {
    var zip = "https://www.zipcodeapi.com/rest/T0rL6kxrFEJyuza4H9jsHeQVheFFxDNrDfcKzJcfnVOSvYWd7gFPvvKMJqsg4gII/radius.json/"; 
    var counter = 2;

    function cap(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // This is a function that shows pokedex info when pokemon is clicked after being
    // dynamically generated. 

    function pokeclick(){
        $('#entries img').click(function(){
            // show pokedex entries
            $('#dexdata').css('display', 'inline-block');
            // hide any currently visible entries
            $('#dexdata img, p, ul').hide();
            var pokeid = $(this).attr('id');
            // show pokedex data in display
            $.get("http://pokeapi.co/api/v1/pokemon/" + pokeid + "/", function(res) {
                $('#dexdata').append("<img class='deximg' src='" + poke + pokeid + ".png'>")
                $('#pokename').after('<p>'+ res.name + '</p>');
                $('#pokeheight').after('<p>'+ res.height + '</p>');
                $('#pokewt').after('<p>'+ res.weight + '</p>');
                if(res.types.length == 1){
                    $('#poketype').after('<p>'+ cap(res.types[0].name) + '</p>');
                }
                else{
                    $('#poketype').after('<ul><li>'+ cap(res.types[0].name) + '</li><li>'+ cap(res.types[1].name) + '</li></ul>');
                }
            }, "json");         
            })
        }

    $('#dex').click(function(){
        $('p').hide();
        while(counter < 152){
            $('#'+ (counter - 1)).after("<img id='" + counter + "' src='" + poke + counter + ".png'>")
            counter++;
        };
        pokeclick();
    });
});