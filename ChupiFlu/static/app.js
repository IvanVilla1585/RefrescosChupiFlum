(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
/*
    A simple jQuery modal (http://github.com/kylefox/jquery-modal)
    Version 0.7.0
*/
(function($) {

  var modals = [],
      getCurrent = function() {
        return modals.length ? modals[modals.length - 1] : null;
      },
      selectCurrent = function() {
        var i,
            selected = false;
        for (i=modals.length-1; i>=0; i--) {
          if (modals[i].$blocker) {
            modals[i].$blocker.toggleClass('current',!selected).toggleClass('behind',selected);
            selected = true;
          }
        }
      };

  $.modal = function(el, options) {
    var remove, target;
    this.$body = $('body');
    this.options = $.extend({}, $.modal.defaults, options);
    this.options.doFade = !isNaN(parseInt(this.options.fadeDuration, 10));
    this.$blocker = null;
    if (this.options.closeExisting)
      while ($.modal.isActive())
        $.modal.close(); // Close any open modals.
    modals.push(this);
    if (el.is('a')) {
      target = el.attr('href');
      //Select element by id from href
      if (/^#/.test(target)) {
        this.$elm = $(target);
        if (this.$elm.length !== 1) return null;
        this.$body.append(this.$elm);
        this.open();
      //AJAX
      } else {
        this.$elm = $('<div>');
        this.$body.append(this.$elm);
        remove = function(event, modal) { modal.elm.remove(); };
        this.showSpinner();
        el.trigger($.modal.AJAX_SEND);
        $.get(target).done(function(html) {
          if (!$.modal.isActive()) return;
          el.trigger($.modal.AJAX_SUCCESS);
          var current = getCurrent();
          current.$elm.empty().append(html).on($.modal.CLOSE, remove);
          current.hideSpinner();
          current.open();
          el.trigger($.modal.AJAX_COMPLETE);
        }).fail(function() {
          el.trigger($.modal.AJAX_FAIL);
          var current = getCurrent();
          current.hideSpinner();
          modals.pop(); // remove expected modal from the list
          el.trigger($.modal.AJAX_COMPLETE);
        });
      }
    } else {
      this.$elm = el;
      this.$body.append(this.$elm);
      this.open();
    }
  };

  $.modal.prototype = {
    constructor: $.modal,

    open: function() {
      var m = this;
      this.block();
      if(this.options.doFade) {
        setTimeout(function() {
          m.show();
        }, this.options.fadeDuration * this.options.fadeDelay);
      } else {
        this.show();
      }
      $(document).off('keydown.modal').on('keydown.modal', function(event) {
        var current = getCurrent();
        if (event.which == 27 && current.options.escapeClose) current.close();
      });
      if (this.options.clickClose)
        this.$blocker.click(function(e) {
          if (e.target==this)
            $.modal.close();
        });
    },

    close: function() {
      modals.pop();
      this.unblock();
      this.hide();
      if (!$.modal.isActive())
        $(document).off('keydown.modal');
    },

    block: function() {
      this.$elm.trigger($.modal.BEFORE_BLOCK, [this._ctx()]);
      this.$body.css('overflow','hidden');
      this.$blocker = $('<div class="jquery-modal blocker current"></div>').appendTo(this.$body);
      selectCurrent();
      if(this.options.doFade) {
        this.$blocker.css('opacity',0).animate({opacity: 1}, this.options.fadeDuration);
      }
      this.$elm.trigger($.modal.BLOCK, [this._ctx()]);
    },

    unblock: function(now) {
      if (!now && this.options.doFade)
        this.$blocker.fadeOut(this.options.fadeDuration, this.unblock.bind(this,true));
      else {
        this.$blocker.children().appendTo(this.$body);
        this.$blocker.remove();
        this.$blocker = null;
        selectCurrent();
        if (!$.modal.isActive())
          this.$body.css('overflow','');
      }
    },

    show: function() {
      this.$elm.trigger($.modal.BEFORE_OPEN, [this._ctx()]);
      if (this.options.showClose) {
        this.closeButton = $('<a href="#close-modal" rel="modal:close" class="close-modal ' + this.options.closeClass + '">' + this.options.closeText + '</a>');
        this.$elm.append(this.closeButton);
      }
      this.$elm.addClass(this.options.modalClass).appendTo(this.$blocker);
      if(this.options.doFade) {
        this.$elm.css('opacity',0).show().animate({opacity: 1}, this.options.fadeDuration);
      } else {
        this.$elm.show();
      }
      this.$elm.trigger($.modal.OPEN, [this._ctx()]);
    },

    hide: function() {
      this.$elm.trigger($.modal.BEFORE_CLOSE, [this._ctx()]);
      if (this.closeButton) this.closeButton.remove();
      var _this = this;
      if(this.options.doFade) {
        this.$elm.fadeOut(this.options.fadeDuration, function () {
          _this.$elm.trigger($.modal.AFTER_CLOSE, [_this._ctx()]);
        });
      } else {
        this.$elm.hide(0, function () {
          _this.$elm.trigger($.modal.AFTER_CLOSE, [_this._ctx()]);
        });
      }
      this.$elm.trigger($.modal.CLOSE, [this._ctx()]);
    },

    showSpinner: function() {
      if (!this.options.showSpinner) return;
      this.spinner = this.spinner || $('<div class="' + this.options.modalClass + '-spinner"></div>')
        .append(this.options.spinnerHtml);
      this.$body.append(this.spinner);
      this.spinner.show();
    },

    hideSpinner: function() {
      if (this.spinner) this.spinner.remove();
    },

    //Return context for custom events
    _ctx: function() {
      return { elm: this.$elm, $blocker: this.$blocker, options: this.options };
    }
  };

  $.modal.close = function(event) {
    if (!$.modal.isActive()) return;
    if (event) event.preventDefault();
    var current = getCurrent();
    current.close();
    return current.$elm;
  };

  // Returns if there currently is an active modal
  $.modal.isActive = function () {
    return modals.length > 0;
  }

  $.modal.defaults = {
    closeExisting: true,
    escapeClose: true,
    clickClose: true,
    closeText: 'Close',
    closeClass: '',
    modalClass: "modal",
    spinnerHtml: null,
    showSpinner: true,
    showClose: true,
    fadeDuration: null,   // Number of milliseconds the fade animation takes.
    fadeDelay: 1.0        // Point during the overlay's fade-in that the modal begins to fade in (.5 = 50%, 1.5 = 150%, etc.)
  };

  // Event constants
  $.modal.BEFORE_BLOCK = 'modal:before-block';
  $.modal.BLOCK = 'modal:block';
  $.modal.BEFORE_OPEN = 'modal:before-open';
  $.modal.OPEN = 'modal:open';
  $.modal.BEFORE_CLOSE = 'modal:before-close';
  $.modal.CLOSE = 'modal:close';
  $.modal.AFTER_CLOSE = 'modal:after-close';
  $.modal.AJAX_SEND = 'modal:ajax:send';
  $.modal.AJAX_SUCCESS = 'modal:ajax:success';
  $.modal.AJAX_FAIL = 'modal:ajax:fail';
  $.modal.AJAX_COMPLETE = 'modal:ajax:complete';

  $.fn.modal = function(options){
    if (this.length === 1) {
      new $.modal(this, options);
    }
    return this;
  };

  // Automatically bind links with rel="modal:close" to, well, close the modal.
  $(document).on('click.modal', 'a[rel="modal:close"]', $.modal.close);
  $(document).on('click.modal', 'a[rel="modal:open"]', function(event) {
    event.preventDefault();
    $(this).modal();
  });
})(jQuery);

},{}],2:[function(require,module,exports){
var modal = require('jquery-modal')
var proveedor = require('./proveedores/index.js')

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

},{"./proveedores/index.js":3,"jquery-modal":1}],3:[function(require,module,exports){
var modal = require('jquery-modal')
module.exports = (function (window, document, $, undefined, modal){

  (function (){

    return proveedor = {
      $modal_alert: $("#modal-alert"),
      $more: $("#more"),
      $buscar: $('#buscar'),
      $text_modal: $("#text-modal"),
      $title_modal: $('#title_modal'),
      $cancelar_prove: $('#cancelar_prove'),
      $consultar_prove: $('#consultar_prove'),
      $consulta_nit: $('#consulta_nit'),
      $cancelar_modal: $('#cancelar_modal'),
      $input_consulta: $('#input_consulta'),
      $modal_boton: $('#modal_boton'),
      $nit: $('#id_nit'),
      $nombre_empresa: $('#id_nombre_empresa'),
      $direccion: $('#id_direccion'),
      $telefono: $('#id_telefono'),
      $fax: $('#id_fax'),
      $correo_empresa: $('#id_correo_empresa'),
      $nombre_contacto: $('#id_nombre_contacto'),
      $telefono_contacto: $('#id_telefono_contacto'),
      $correo_contacto: $('#id_correo_contacto'),

      Init: function (){
        this.iniciarModal()
        this.closeModal(this.$more)
        this.closeModal(this.$cancelar_prove)
        this.closeModal(this.$cancelar_modal)
        this.escucharBuscar()
        this.escucharConsulta()
      },

      iniciarModal: function () {
        this.$modal_alert.css('display', 'none')
      },

      closeModal: function (elemento) {
        var self = this
        elemento.on('click', function (evt) {
          evt.preventDefault()
          self.$modal_alert.css('display', 'none')
        })
      },

      escucharBuscar: function () {
        var self = this
        self.$buscar.on('click', function (evt) {
          evt.preventDefault()
          self.activarInputConsulta()
          self.$title_modal.empty().text('Consultar')
          self.$text_modal.empty().text('Ingrese el nit del proveedor a consultar')
          self.$modal_alert.css('display', 'block')
        })
      },

      escucharConsulta: function () {
        var self = this
        self.$consultar_prove.on('click', function (evt) {
          evt.preventDefault()
          var nit = self.$consulta_nit.val()
          if (nit != null && nit != ""){
            var params = nit + '/?format=json'
            var url = 'MenuPrincipal/Proveedor/Consultar/' + params
            self.peticion(url)
          }else{
            self.desactivarInputConsulta()
            self.$title_modal.empty().text('Alerta')
            self.$text_modal.empty().text('Debe Ingresar el nit del proveedor a consultar')
            self.$modal_alert.css('display', 'block')
          }
        })
      },

      peticion: function (url) {
        var self = this
        $.ajax({
					url: url,
					data: {},
					type:'GET',
					dataType: 'json',
					succes: function ( data ){
						console.dir(data);
            self.llenarFormulario(data)
					},
					error: function ( xhr, status ){
						alert('Problema al realizar el ajax'+ xhr.error());
					}
        });
      },

      activarInputConsulta: function () {
        this.$input_consulta.css('display', 'block')
        this.$modal_boton.css('display', 'none')
      },

      desactivarInputConsulta: function () {
        this.$modal_boton.css('display', 'block')
        this.$input_consulta.css('display', 'none')
      },

      llenarFormulario: function (data) {
        var self = this
        self.$nit.val(data.proveedor.nit)
        self.$nombre_empresa.val(data.proveedor.nombre_empresa)
        self.$direccion.val(data.proveedor.direccion)
        self.$telefono.val(data.proveedor.telefono)
        self.$fax.val(data.proveedor.fax)
        self.$correo_empresa.val(data.proveedor.correo_empresa)
        self.$nombre_contacto.val(data.proveedor.nombre_contacto)
        self.$telefono_contacto.val(data.proveedor.telefono_contacto)
        self.$correo_contacto.val(data.proveedor.correo_contacto)
      },

      limpiarFormulario: function () {
        var self = this
        self.$nit.val("")
        self.$nombre_empresa.val("")
        self.$direccion.val("")
        self.$telefono.val("")
        self.$fax.val("")
        self.$correo_empresa.val("")
        self.$nombre_contacto.val("")
        self.$telefono_contacto.val("")
        self.$correo_contacto.val("")
      },

      desactivarFormulario: function () {
        var self = this
        self.$nit.attr('disabled', 'disabled')
        self.$nombre_empresa.attr('disabled', 'disabled')
        self.$direccion.attr('disabled', 'disabled')
        self.$telefono.attr('disabled', 'disabled')
        self.$fax.attr('disabled', 'disabled')
        self.$correo_empresa.attr('disabled', 'disabled')
        self.$nombre_contacto.attr('disabled', 'disabled')
        self.$telefono_contacto.attr('disabled', 'disabled')
        self.$correo_contacto.attr('disabled', 'disabled')
      },

      activarFormulario: function () {
        var self = this
        self.$nit.removeAttr("disabled")
        self.$nombre_empresa.removeAttr("disabled")
        self.$direccion.removeAttr("disabled")
        self.$telefono.removeAttr("disabled")
        self.$fax.removeAttr("disabled")
        self.$correo_empresa.removeAttr("disabled")
        self.$nombre_contacto.removeAttr("disabled")
        self.$telefono_contacto.removeAttr("disabled")
        self.$correo_contacto.removeAttr("disabled")
      }
    }
  }) ()

  proveedor.Init()
}) (window, document, $, undefined, modal)

},{"jquery-modal":1}]},{},[2]);
