var modal = require('jquery-modal')

class Proveedor {

  constructor(){
    this.$modal_alert = $("#modal-alert")
    this.$more = $("#more")
    this.$buscar = $('#buscar')
    this.$text_modal = $("#text-modal")
    this.$title_modal = $('#title_modal')
    this.$cancelar_prove = $('#cancelar_prove')
    this.$consultar_prove = $('#consultar_prove')
    this.$consulta_nit = $('#consulta_nit')
    this.$cancelar_modal = $('#cancelar_modal')
    this.$input_consulta = $('#input_consulta')
    this.$modal_boton = $('#modal_boton')
    this.$nit = $('#id_nit')
    this.$nombre_empresa = $('#id_nombre_empresa')
    this.$direccion = $('#id_direccion')
    this.$telefono = $('#id_telefono')
    this.$fax = $('#id_fax')
    this.$correo_empresa = $('#id_correo_empresa')
    this.$nombre_contacto = $('#id_nombre_contacto')
    this.$telefono_contacto = $('#id_telefono_contacto')
    this.$correo_contacto = $('#id_correo_contacto')
    this.iniciarModal()
    this.closeModal(this.$more)
    this.closeModal(this.$cancelar_prove)
    this.closeModal(this.$cancelar_modal)
    this.escucharBuscar()
    this.escucharConsulta()
  }

  iniciarModal () {
    this.$modal_alert.css('display', 'none')
  }

  closeModal (elemento) {
    elemento.on('click', (evt) => {
      evt.preventDefault()
      this.$modal_alert.css('display', 'none')
    })
  }

  escucharBuscar () {
    this.$buscar.on('click', (evt) => {
      evt.preventDefault()
      this.activarInputConsulta()
      this.$title_modal.empty().text('Consultar')
      this.$text_modal.empty().text('Ingrese el nit del proveedor a consultar')
      this.$modal_alert.css('display', 'block')
    })
  }

  escucharConsulta () {
    this.$consultar_prove.on('click', (evt) => {
      evt.preventDefault()
      let nit = this.$consulta_nit.val()
      if (nit != null && nit != ""){
        let params = nit + '/?format=json'
        let url = 'MenuPrincipal/Proveedor/Consultar/' + params
        this.peticion(url)
      }else{
        this.desactivarInputConsulta()
        this.$title_modal.empty().text('Alerta')
        this.$text_modal.empty().text('Debe Ingresar el nit del proveedor a consultar')
        this.$modal_alert.css('display', 'block')
      }
    })
  }

  peticion (url) {
    $.ajax({
      url: url,
      data: {},
      type:'GET',
      dataType: 'json',
      succes: ( data ) => {
        console.dir(data);
        this.llenarFormulario(data)
      },
      error: ( xhr, status ) => {
        alert('Problema al realizar el ajax'+ xhr.error());
      }
    });
  }

  activarInputConsulta () {
    this.$input_consulta.css('display', 'block')
    this.$modal_boton.css('display', 'none')
  }

  desactivarInputConsulta () {
    this.$modal_boton.css('display', 'block')
    this.$input_consulta.css('display', 'none')
  }

  llenarFormulario (data) {
    this.$nit.val(data.proveedor.nit)
    this.$nombre_empresa.val(data.proveedor.nombre_empresa)
    this.$direccion.val(data.proveedor.direccion)
    this.$telefono.val(data.proveedor.telefono)
    this.$fax.val(data.proveedor.fax)
    this.$correo_empresa.val(data.proveedor.correo_empresa)
    this.$nombre_contacto.val(data.proveedor.nombre_contacto)
    this.$telefono_contacto.val(data.proveedor.telefono_contacto)
    this.$correo_contacto.val(data.proveedor.correo_contacto)
  }

  limpiarFormulario () {
    var self = this
    this.$nit.val("")
    this.$nombre_empresa.val("")
    this.$direccion.val("")
    this.$telefono.val("")
    this.$fax.val("")
    this.$correo_empresa.val("")
    this.$nombre_contacto.val("")
    this.$telefono_contacto.val("")
    this.$correo_contacto.val("")
  }

  desactivarFormulario () {
    this.$nit.attr('disabled', 'disabled')
    this.$nombre_empresa.attr('disabled', 'disabled')
    this.$direccion.attr('disabled', 'disabled')
    this.$telefono.attr('disabled', 'disabled')
    this.$fax.attr('disabled', 'disabled')
    this.$correo_empresa.attr('disabled', 'disabled')
    this.$nombre_contacto.attr('disabled', 'disabled')
    this.$telefono_contacto.attr('disabled', 'disabled')
    this.$correo_contacto.attr('disabled', 'disabled')
  }

  activarFormulario () {
    this.$nit.removeAttr("disabled")
    this.$nombre_empresa.removeAttr("disabled")
    this.$direccion.removeAttr("disabled")
    this.$telefono.removeAttr("disabled")
    this.$fax.removeAttr("disabled")
    this.$correo_empresa.removeAttr("disabled")
    this.$nombre_contacto.removeAttr("disabled")
    this.$telefono_contacto.removeAttr("disabled")
    this.$correo_contacto.removeAttr("disabled")
  }
}
const proveedor = new Proveedor
