var modal = require('jquery-modal')

module.exports = (function (window, document, $, undefined, modal){

  (function (){

    return menu = {

      $collapse: $('#collapse'),
      $navparent: $('.nav'),
      $modal_alert: $("#modal-alert"),
      $more: $("#more"),
      id: "0",

      Init: function (){
        this.iniciarModal()
        this.closeModal()
        this.activarCollapse()
      },

      iniciarModal: function () {
        this.$modal_alert.css('display', 'none')

      },

      closeModal: function () {
        var self = this
        self.$more.on('click', function (evt) {
          evt.preventDefault()
          self.$modal_alert.css('display', 'none')
        })
      },

      activarCollapse: function (){
        var self = this
        self.$navparent.on('click', 'li.nav-parent', function (ev) {
          var $this = $(this)
          if (self.id == $this.data('id')){
            $("li[data-id='" + self.id + "']").find('.children').css('display', 'none')
          }else{
            $("li[data-id='" + self.id + "']").find('.children').css('display', 'none')
            self.id = $this.data('id')

            var $article = $("li[data-id='" + self.id + "']").find('.children')
            $article.css('display', 'block').fadeIn(3000);
          }
          return false
        })
      }
    }
  }) ()

  menu.Init()
}) (window, document, $, undefined, modal)
