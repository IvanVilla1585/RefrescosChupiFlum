# -*- coding: utf-8 -*-

tittlesMenu = {
    '/admin/': u'Admin',
    '/MenuPrincipal/': u'Menú Principal',
    '/login/': u'Ingreso al Sistema',
    '/MenuPrincipal/Proveedor/': u'Compras - Proveedores',
    '/MenuPrincipal/Proveedor/Guardar/': u'Compras - Proveedores',
    '/MenuPrincipal/Proveedor/Listar/': u'Compras - Listado Proveedores',
    '/MenuPrincipal/Productos/': u'Inventarios - Productos Terminados',
    '/MenuPrincipal/Productos/Guardar/': u'Inventarios - Productos Terminados',
    '/MenuPrincipal/Productos/Listar': u'Inventarios - Listado Productos Terminados',
    '/MenuPrincipal/MateriaPrima/': u'Inventarios - Materia Prima',
    '/MenuPrincipal/MateriaPrima/Crear/': u'Inventarios - Materia Prima',
    '/MenuPrincipal/MateriaPrima/Listar/': u'Inventarios - Listar Materia Prima',
    '/MenuPrincipal/Maquina/': u'Producción - Máquinas',
    '/MenuPrincipal/Maquina/Guardar': u'Producción - Máquinas',
    '/MenuPrincipal/Maquina/Listar/': u'Producción - Listar Máquinas',
    '/MenuPrincipal/Usuarios/': u'Permisos - Usuarios',
    '/MenuPrincipal/Usuarios/Listar/': u'Permisos - Listar Usuarios',
    '/MenuPrincipal/Usuarios/Guardar/': u'Permisos - Usuarios',
    '/MenuPrincipal/UnidadMedida/': u'Producción - Unidades de Medida',
    '/MenuPrincipal/UnidadMedida/Listar/': u'Producción - Listado Unidades de Medida',
    '/MenuPrincipal/UnidadMedida/Guardar/': u'Producción - Unidades de Medida',
    '/MenuPrincipal/Grupos/': u'Permisos - Roles',
    '/MenuPrincipal/Grupos/Guardar/': u'Permisos - Roles',
    '/MenuPrincipal/Pedidos/': u'Compras - Pedidos',
    '/MenuPrincipal/Pedidos/Guardar': u'Compras - Pedidos',
    '/MenuPrincipal/Proveedor/Consultar/': u'Compras - Registrar Proveedor'
}
def tittles(request):
    tittle = ''
    try:
        tittle = tittlesMenu[request.path]
    except Exception as e:
        tittle = u'Menú Principal'
    return {'tittle': tittle}
