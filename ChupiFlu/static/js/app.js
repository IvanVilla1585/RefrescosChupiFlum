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
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _jqueryModal = require('jquery-modal');

var _jqueryModal2 = _interopRequireDefault(_jqueryModal);

var _index = require('./proveedores/index.js');

var _index2 = _interopRequireDefault(_index);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Menu = function () {
  function Menu() {
    _classCallCheck(this, Menu);

    this.$collapse = $('#collapse');
    this.$navparent = $('.nav');
    this.$modal_alert = $("#modal-alert");
    this.$more = $("#more");
    this.id = "0";
    this.iniciarModal();
    this.closeModal();
    this.activarCollapse();
  }

  _createClass(Menu, [{
    key: 'iniciarModal',
    value: function iniciarModal() {
      this.$modal_alert.css('display', 'none');
    }
  }, {
    key: 'closeModal',
    value: function closeModal() {
      this.$more.on('click', function (evt) {
        evt.preventDefault();
        this.$modal_alert.css('display', 'none');
      });
    }
  }, {
    key: 'activarCollapse',
    value: function activarCollapse() {
      this.$navparent.on('click', 'li.nav-parent', function (ev) {
        var $this = $(this);
        if (this.id == $this.data('id')) {
          $("li[data-id='" + this.id + "']").find('.children').slideToggle("slow");
        } else {
          $("li[data-id='" + this.id + "']").find('.children').slideToggle("slow");
          this.id = $this.data('id');

          var $article = $("li[data-id='" + this.id + "']").find('.children');
          $article.slideToggle("slow");
        }
      });
    }
  }]);

  return Menu;
}();

var menu = new Menu();
var proveedor = new _index2.default();

},{"./proveedores/index.js":3,"jquery-modal":1}],3:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var modal = require('jquery-modal');

var Proveedor = function () {
  function Proveedor() {
    _classCallCheck(this, Proveedor);

    this.$modal_alert = $("#modal-alert");
    this.$more = $("#more");
    this.$buscar = $('#buscar');
    this.$text_modal = $("#text-modal");
    this.$title_modal = $('#title_modal');
    this.$cancelar_prove = $('#cancelar_prove');
    this.$consultar_prove = $('#consultar_prove');
    this.$consulta_nit = $('#consulta_nit');
    this.$cancelar_modal = $('#cancelar_modal');
    this.$input_consulta = $('#input_consulta');
    this.$modal_boton = $('#modal_boton');
    this.$nit = $('#id_nit');
    this.$nombre_empresa = $('#id_nombre_empresa');
    this.$direccion = $('#id_direccion');
    this.$telefono = $('#id_telefono');
    this.$fax = $('#id_fax');
    this.$correo_empresa = $('#id_correo_empresa');
    this.$nombre_contacto = $('#id_nombre_contacto');
    this.$telefono_contacto = $('#id_telefono_contacto');
    this.$correo_contacto = $('#id_correo_contacto');
    this.iniciarModal();
    this.closeModal(this.$more);
    this.closeModal(this.$cancelar_prove);
    this.closeModal(this.$cancelar_modal);
    this.escucharBuscar();
    this.escucharConsulta();
  }

  _createClass(Proveedor, [{
    key: "iniciarModal",
    value: function iniciarModal() {
      this.$modal_alert.css('display', 'none');
    }
  }, {
    key: "closeModal",
    value: function closeModal(elemento) {
      var _this = this;

      elemento.on('click', function (evt) {
        evt.preventDefault();
        _this.$modal_alert.css('display', 'none');
      });
    }
  }, {
    key: "escucharBuscar",
    value: function escucharBuscar() {
      var _this2 = this;

      this.$buscar.on('click', function (evt) {
        evt.preventDefault();
        _this2.activarInputConsulta();
        _this2.$title_modal.empty().text('Consultar');
        _this2.$text_modal.empty().text('Ingrese el nit del proveedor a consultar');
        _this2.$modal_alert.css('display', 'block');
      });
    }
  }, {
    key: "escucharConsulta",
    value: function escucharConsulta() {
      var _this3 = this;

      this.$consultar_prove.on('click', function (evt) {
        evt.preventDefault();
        var nit = _this3.$consulta_nit.val();
        if (nit != null && nit != "") {
          var params = nit + '/?format=json';
          var url = '/MenuPrincipal/Proveedor/Consultar/' + params;
          _this3.$modal_alert.css('display', 'none');
          $.ajax({
            url: url,
            type: 'GET',
            succes: function succes(data) {
              debugger;
              console.dir(data);
              _this3.llenarFormulario(data);
            },
            error: function error(xhr, status) {
              alert('Problema al realizar el ajax' + xhr.error());
            }
          });
        } else {
          _this3.desactivarInputConsulta();
          _this3.$title_modal.empty().text('Alerta');
          _this3.$text_modal.empty().text('Debe Ingresar el nit del proveedor a consultar');
          _this3.$modal_alert.css('display', 'block');
        }
      });
    }
  }, {
    key: "peticion",
    value: function peticion(url) {
      var _this4 = this;

      $.ajax({
        url: url,
        data: {},
        type: 'GET',
        dataType: 'json',
        succes: function succes(data) {
          console.dir(data);
          _this4.llenarFormulario(data);
        },
        error: function error(xhr, status) {
          alert('Problema al realizar el ajax' + xhr.error());
        }
      });
    }
  }, {
    key: "activarInputConsulta",
    value: function activarInputConsulta() {
      this.$input_consulta.css('display', 'block');
      this.$modal_boton.css('display', 'none');
    }
  }, {
    key: "desactivarInputConsulta",
    value: function desactivarInputConsulta() {
      this.$modal_boton.css('display', 'block');
      this.$input_consulta.css('display', 'none');
    }
  }, {
    key: "llenarFormulario",
    value: function llenarFormulario(data) {
      this.$nit.val(data.proveedor.nit);
      this.$nombre_empresa.val(data.proveedor.nombre_empresa);
      this.$direccion.val(data.proveedor.direccion);
      this.$telefono.val(data.proveedor.telefono);
      this.$fax.val(data.proveedor.fax);
      this.$correo_empresa.val(data.proveedor.correo_empresa);
      this.$nombre_contacto.val(data.proveedor.nombre_contacto);
      this.$telefono_contacto.val(data.proveedor.telefono_contacto);
      this.$correo_contacto.val(data.proveedor.correo_contacto);
    }
  }, {
    key: "limpiarFormulario",
    value: function limpiarFormulario() {
      var self = this;
      this.$nit.val("");
      this.$nombre_empresa.val("");
      this.$direccion.val("");
      this.$telefono.val("");
      this.$fax.val("");
      this.$correo_empresa.val("");
      this.$nombre_contacto.val("");
      this.$telefono_contacto.val("");
      this.$correo_contacto.val("");
    }
  }, {
    key: "desactivarFormulario",
    value: function desactivarFormulario() {
      this.$nit.attr('disabled', 'disabled');
      this.$nombre_empresa.attr('disabled', 'disabled');
      this.$direccion.attr('disabled', 'disabled');
      this.$telefono.attr('disabled', 'disabled');
      this.$fax.attr('disabled', 'disabled');
      this.$correo_empresa.attr('disabled', 'disabled');
      this.$nombre_contacto.attr('disabled', 'disabled');
      this.$telefono_contacto.attr('disabled', 'disabled');
      this.$correo_contacto.attr('disabled', 'disabled');
    }
  }, {
    key: "activarFormulario",
    value: function activarFormulario() {
      this.$nit.removeAttr("disabled");
      this.$nombre_empresa.removeAttr("disabled");
      this.$direccion.removeAttr("disabled");
      this.$telefono.removeAttr("disabled");
      this.$fax.removeAttr("disabled");
      this.$correo_empresa.removeAttr("disabled");
      this.$nombre_contacto.removeAttr("disabled");
      this.$telefono_contacto.removeAttr("disabled");
      this.$correo_contacto.removeAttr("disabled");
    }
  }]);

  return Proveedor;
}();

exports.default = Proveedor;

},{"jquery-modal":1}]},{},[2]);
