$(document).ready(function(){
	console.log('%%%%%%%%%%%%%');
    $('.megaheart').click(function(){
      var back = ["#darkred","deepskyblue","pink","green","lightslategrey","mediumpurple","yellow","greenyellow","palevioletred"];
      var rand = back[Math.floor(Math.random() * back.length)];
      var rand2 = back[Math.floor(Math.random() * back.length)];
      $(this).css('color', rand);
      $('body').css('background-color', rand2);
      });
	});