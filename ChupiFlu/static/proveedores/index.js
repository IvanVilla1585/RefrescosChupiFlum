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
