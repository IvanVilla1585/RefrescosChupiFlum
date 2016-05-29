(function (window, document, $, undefined){

  (function (){

    return menu = {

      $collapse: $('#collapse'),
      $navparent: $('.nav'),
      id: "0",

      Init: function (){
        this.activarCollapse()
      },

      activarCollapse: function (){
        var self = this
        self.$navparent.on('click', 'li.nav-parent', function (ev) {
          var $this = $(this)
          if (self.id == $this.data('id') && $this.css('display') == 'block'){
            $("li[data-id='" + self.id + "']").find('.children').css('display', 'none')
          }else{
            $("li[data-id='" + self.id + "']").find('.children').css('display', 'none')
            self.id = $this.data('id')

            var $article = $("li[data-id='" + self.id + "']").find('.children')
            $article.css('display', 'block').fadeIn(3000);
          }
        })
      }
    }
  }) ()

  menu.Init()
}) (window, document, $, undefined)
