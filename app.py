from flask import Flask, abort
from flask import jsonify
from flask import request
from flask_cors import CORS
import json

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import pyodbc
from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


cnxn = None
engine = None
session = None
try:
    connection_string = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=0.0.0.0;DATABASE=PRUEBA;UID=SA;PWD=Pass.word12$;TrustServerCertificate=yes;PORT=1401;MARS_Connection=yes'
    cnxn = pyodbc.connect(connection_string)
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    print("conectado a base de datos")
    session = sessionmaker(engine)

except:
    print("no se pudo conectar a la base de datos")

app = Flask(__name__)
CORS(app)

orders = [{'fecha': '12/03/2024', 'estatus': 'elaborada', 'departamento': 'dep1', 'ramo': 1, 'motivo': 'moivo1', 'grupoProd': 'grupo1', 'consecutivo': '1', 'direccion': 'Direc1', 'proyecto': 'proyecto1',
           'fechaEntrega': '', 'oficinaEntrega': 'oficina1 ', 'tipoProd': 'tipo1', 'productos': [{'label': 'The Shawshank Redemption', 'year': 1994}], 'comentario': 'comentario1', 'solicitante': 'usuario', 'archivo': {}}]

cotizaciones = []
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


def castFecha(fecha):
    [d, m, y] = fecha.split("/")
    return f"{y}-{m}-{d}"


@app.route("/ramo", methods=["GET"])
# @jwt_required()
def getCatalogoRamo():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("select ramoid, nombre, FuenteFinanciamientoCONACId, RamoDetalleId, TipoRecurso from TblRamo"):
        data.append(dict(
            ramoid=x[0], nombre=x[1], FuenteFinanciamientoCONACId=x[2], RamoDetalleId=x[3], TipoRecurso=x[4], value=x[0], label=x[1]))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'RamoId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 1, 'NO', 39)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'Nombre', -9, 'nvarchar', 250, 500, None, None, 0, None, None, -9, None, 500, 2, 'NO', 39)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'Editable', -7, 'bit', 1, 1, None, None, 0, None, None, -7, None, None, 3, 'NO', 50)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'FuenteFinanciamientoCONACId', 12, 'varchar', 2, 2, None, None, 0, None, None, 12, None, 2, 4, 'NO', 39)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'TipoGastoDestinoId', 12, 'varchar', 2, 2, None, None, 1, None, None, 12, None, 2, 5, 'YES', 39)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'Anio', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 6, 'YES', 38)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'RamoDetalleId', 12, 'varchar', 12, 12, None, None, 1, None, None, 12, None, 12, 7, 'YES', 39)
# viendo x ('WideWorldImporters', 'dbo', 'tblRamo', 'TipoRecurso', 12, 'varchar', 2, 2, None, None, 1, None, None, 12, None, 2, 8, 'YES', 39)


@app.route("/departamento", methods=["GET"])
# @jwt_required()
def getCatogoDepartamento():
    data = []
    cu = cnxn.cursor()
    # tblFuenteFinanciamientoCONAC=ramo
    for x in cu.execute("select DependenciaId, Nombre, CuentaDeRegistro from TblDependencia where CuentaDeRegistro=1"):
        data.append(dict(DependenciaId=x[0],
                    Nombre=x[1], CuentaDeRegistro=x[2], value=x[0], label=x[1]))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)

# viendo x ('WideWorldImporters', 'dbo', 'tblDependencia', 'DependenciaId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 1, 'NO', 39)
# viendo x ('WideWorldImporters', 'dbo', 'tblDependencia', 'Nombre', -9, 'nvarchar', 250, 500, None, None, 0, None, None, -9, None, 500, 2, 'NO', 39)
# viendo x ('WideWorldImporters', 'dbo', 'tblDependencia', 'CuentaDeRegistro', -7, 'bit', 1, 1, None, None, 0, None, None, -7, None, None, 3, 'NO', 50)


@app.route("/grupoproducto", methods=["GET"])
# @jwt_required()
def getCatogoGrupoProducto():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("select GrupoProductoId,  Nombre from tblGrupoProducto"):
        data.append(
            dict(GrupoProductoId=x[0], Nombre=x[1], value=x[0], label=f"{x[0]}-{x[1]}"))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)

# tablas  ('WideWorldImporters', 'dbo', 'tblGrupoProducto', 'GrupoProductoId', 12, 'varchar', 3, 3, None, None, 0, None, None, 12, None, 3, 1, 'NO', 39)
# tablas  ('WideWorldImporters', 'dbo', 'tblGrupoProducto', 'Nombre', 12, 'varchar', 100, 100, None, None, 0, None, None, 12, None, 100, 2, 'NO', 39)


@app.route("/dependencia", methods=["GET"])
# @jwt_required()
def dependencia():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("select * from  tblDependencia where CuentaDeRegistro=0"):
        data.append(dict(
            tblDependencia=x[0], Nombre=x[1], CuentaDeRegistro=x[2], value=x[0], label=x[1]))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)

# columna  ('WideWorldImporters', 'dbo', 'tblDependencia', 'DependenciaId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 1, 'NO', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblDependencia', 'Nombre', -9, 'nvarchar', 250, 500, None, None, 0, None, None, -9, None, 500, 2, 'NO', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblDependencia', 'CuentaDeRegistro', -7, 'bit', 1, 1, None, None, 0, None, None, -7, None, None, 3, 'NO', 50)

# tblAlmacen = entregar en
# unidad administrativa =dependencia = direccion = tblDependencia
# proyecto prosceso =  = proyecto = tblProyecto
# fuente de financimiento = ramo= tblRamo
# tipo operacion = tblTipoOperacion
# tipo comprobante fiscal = tblTipoComprobanteFiscal
# tipo Prod


@app.route("/proyecto", methods=["GET"])
# @jwt_required()
def proyecto():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("select * from tblProyecto"):
        data.append(dict(
            ProyectoId=x[0], ClasificadorFuncionalId=x[1], SubProgramaGobiernoId=x[2],
            Nombre=x[3], Editable=x[4], ClasificacionGeograficaId=x[5], Capitulos=x[6],
            value=x[0], label=f'{x[3]}- {x[0]}'))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)


# columan  ('WideWorldImporters', 'dbo', 'tblProyecto', 'ProyectoId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 1, 'NO', 39)
# columan  ('WideWorldImporters', 'dbo', 'tblProyecto', 'ClasificadorFuncionalId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 2, 'NO', 39)
# columan  ('WideWorldImporters', 'dbo', 'tblProyecto', 'SubProgramaGobiernoId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 3, 'NO', 39)
# columan  ('WideWorldImporters', 'dbo', 'tblProyecto', 'Nombre', -9, 'nvarchar', 250, 500, None, None, 0, None, None, -9, None, 500, 4, 'NO', 39)
# columan  ('WideWorldImporters', 'dbo', 'tblProyecto', 'Editable', -7, 'bit', 1, 1, None, None, 0, None, None, -7, None, None, 5, 'NO', 50)
# columan  ('WideWorldImporters', 'dbo', 'tblProyecto', 'ClasificacionGeograficaId', 12, 'varchar', 6, 6, None, None, 1, None, None, 12, None, 6, 6, 'YES', 39)
# columan  ('WideWorldImporters', 'dbo', 'tblProyecto', 'Capitulos', 12, 'varchar', 10, 10, None, None, 1, None, None, 12, None, 10, 7, 'YES', 39)


@app.route("/almacen", methods=["GET"])
# @jwt_required()
def almacen():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("select * from tblAlmacen"):
        data.append(dict(
            AlmacenId=x[0], EstadoId=x[1], MunicipioId=x[2], Nombre=x[3],
            ControlDeProducto=x[4], Domicilio=x[5], Colonia=x[6], CodigoPostal=x[7],
            Telefono1=x[8], Telefono2=x[9], ConsecutivoAlmacen=x[10], value=x[0], label=x[3]))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)


# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'AlmacenId', 12, 'varchar', 4, 4, None, None, 0, None, None, 12, None, 4, 1, 'NO', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'EstadoId', -9, 'nvarchar', 2, 4, None, None, 0, None, None, -9, None, 4, 2, 'NO', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'MunicipioId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 3, 'NO', 56)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'Nombre', 12, 'varchar', 100, 100, None, None, 0, None, None, 12, None, 100, 4, 'NO', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'ControlDeProducto', -7, 'bit', 1, 1, None, None, 0, None, None, -7, None, None, 5, 'NO', 50)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'Domicilio', 12, 'varchar', 250, 250, None, None, 0, None, None, 12, None, 250, 6, 'NO', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'Colonia', 12, 'varchar', 250, 250, None, None, 0, None, None, 12, None, 250, 7, 'NO', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'CodigoPostal', 12, 'varchar', 5, 5, None, None, 1, None, None, 12, None, 5, 8, 'YES', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'Telefono1', 12, 'varchar', 25, 25, None, None, 1, None, None, 12, None, 25, 9, 'YES', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'Telefono2', 12, 'varchar', 25, 25, None, None, 1, None, None, 12, None, 25, 10, 'YES', 39)
# columna  ('WideWorldImporters', 'dbo', 'tblAlmacen', 'ConsecutivoAlmacen', 12, 'varchar', 6, 6, None, None, 1, None, None, 12, None, 6, 11, 'YES', 39)

@app.route("/producto", methods=["GET"])
# @jwt_required()
def producto():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("select * from tblProducto"):
        data.append(dict(ProductoId=x[0], TarifaImpuestoId=x[1], Clave=x[2], ObjetoGastoId=x[3], Descripcion=x[4],
                    UnidadDeMedidaId=x[5], Status=x[6], Existencia=x[7], CostoPromedio=x[8],
                    CostoUltimo=x[9], value=x[0], label=f"{x[0]}-{x[4]}"))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)

# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'ProductoId', 12, 'varchar', 10, 10, None, None, 0, None, None, 12, None, 10, 1, 'NO', 39)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'TarifaImpuestoId', 12, 'varchar', 10, 10, None, None, 0, None, None, 12, None, 10, 2, 'NO', 39)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'Clave', 12, 'varchar', 6, 6, None, None, 0, None, None, 12, None, 6, 3, 'NO', 39)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'ObjetoGastoId', 12, 'varchar', 8, 8, None, None, 0, None, None, 12, None, 8, 4, 'NO', 39)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'Descripcion', 12, 'varchar', 250, 250, None, None, 0, None, None, 12, None, 250, 5, 'NO', 39)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'UnidadDeMedidaId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 6, 'NO', 56)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 7, 'NO', 47)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'Existencia', 6, 'float', 15, 8, None, 10, 0, None, '((0))', 6, None, None, 8, 'NO', 62)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'CostoPromedio', 3, 'money', 19, 21, 4, 10, 0, None, '((0))', 3, None, None, 9, 'NO', 60)
# columna ('WideWorldImporters', 'dbo', 'tblProducto', 'CostoUltimo', 3, 'money', 19, 21, 4, 10, 0, None, '((0))', 3, None, None, 10, 'NO', 60)


@app.route("/cuentapresupuestal", methods=["GET"])
# @jwt_required()
def cuentaPresupuestal():
    data = []
    cu = cnxn.cursor()
    if args:
        print("si hubo args", args)
    else:
        for x in cu.execute("select * from tblCuentaPresupuestalEgr"):
            args = request.args
            print("viendo x ", x)
        # data.append(dict(ProductoId=x[0], TarifaImpuestoId=x[1], Clave=x[2], ObjetoGastoId=x[3], Descripcion=x[4],
        #           UnidadDeMedidaId=x[5], Status=x[6], Existencia=x[7], CostoPromedio=x[8], CostoUltimo=x[9], value=x[0], label=x[4]))
    cu.close()
    return jsonify(data)

# producto  ('WideWorldImporters', 'dbo', 'tblCuentaPresupuestalEgr', 'CuentaPresupuestalEgrId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# producto  ('WideWorldImporters', 'dbo', 'tblCuentaPresupuestalEgr', 'RamoId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 2, 'NO', 39)
# producto  ('WideWorldImporters', 'dbo', 'tblCuentaPresupuestalEgr', 'ProyectoId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 3, 'NO', 39)
# producto  ('WideWorldImporters', 'dbo', 'tblCuentaPresupuestalEgr', 'DependenciaId', -9, 'nvarchar', 6, 12, None, None, 0, None, None, -9, None, 12, 4, 'NO', 39)
# producto  ('WideWorldImporters', 'dbo', 'tblCuentaPresupuestalEgr', 'ObjetoGastoId', 12, 'varchar', 8, 8, None, None, 0, None, None, 12, None, 8, 5, 'NO', 39)
# producto  ('WideWorldImporters', 'dbo', 'tblCuentaPresupuestalEgr', 'TipoGastoId', -9, 'nvarchar', 1, 2, None, None, 0, None, None, -9, None, 2, 6, 'NO', 39)


@app.route("/unidaddemedida", methods=["GET"])
# @jwt_required()
def unidadDeMedida():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("sp_columns 'tblUnidadDeMedida'"):
        data.append(dict(
            UnidadDeMedidaId=x[0], Abreviatura=x[1], Descripcion=x[2],  value=x[0], label=x[2]))
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)

# producto  ('PRUEBA', 'dbo', 'tblUnidadDeMedida', 'UnidadDeMedidaId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# producto  ('PRUEBA', 'dbo', 'tblUnidadDeMedida', 'Abreviatura', 12, 'varchar', 50, 50, None, None, 0, None, None, 12, None, 50, 2, 'NO', 39)
# producto  ('PRUEBA', 'dbo', 'tblUnidadDeMedida', 'Descripcion', 12, 'varchar', 100, 100, None, None, 0, None, None, 12, None, 100, 3, 'NO', 39)


@app.route("/revisarpresupuestoegresos", methods=["GET"])
# @jwt_required()
def revisarPresupuestoEgresos():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("sp_columns  'vwPresupuestoDetE'"):
        print("producto ", x)
        # data.append(dict(ProductoId=x[0], TarifaImpuestoId=x[1], Clave=x[2], ObjetoGastoId=x[3], Descripcion=x[4],
        #           UnidadDeMedidaId=x[5], Status=x[6], Existencia=x[7], CostoPromedio=x[8], CostoUltimo=x[9], value=x[0], label=x[4]))
    cu.close()
    return jsonify(data)


@app.route("/tablas", methods=["GET"])
# @jwt_required()
def getTablasSQL():
    data = []
    cu = cnxn.cursor()
    for x in cu.execute("sp_tables"):
        print("viendo tabla ", x)
    cu.close()
    return jsonify(data)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


@app.route("/auth/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username not in ["usuario", "director", "jefecompras"] and password not in ["pass123"]:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    permisos = []
    if username == "usuario":
        permisos = []
    elif username == "director":
        permisos = ["vistoBuenoReq", "rechazarReq"]
    elif username == "jefecompras":
        permisos = ["autorizarReq", "rechazarReq"]
    else:
        permisos = []

    return jsonify(id=1, permisos=permisos, name=username, email=username, role=username, mobile="331834", routes=[{"path": "/orden/all"}, {"path": "/orden/crear"}, {"path": "/orden/editar"}, {"path": "/admin/users"}], token=access_token)


@app.route("/prueba", methods=["GET"])
def prueba():
    cu = cnxn.cursor()
    cu.execute(
        "select CuentaPresupuestalEgrId from tblCuentaPresupuestalEgr where CuentaPresupuestalEgrId=123796")
    result = cu.fetchone()
    print("viendo result ", result)
    return jsonify({})


def crearReqDetalle(productos, orderId, cuentasPresupuestales):
    # campos que no estoy seguro
    # Costo hasta TotalPresupuesto
    cu = cnxn.cursor()
    print("antes de grabar productos ", productos)
    for i, producto in enumerate(productos):
        print("pasi ", i)
        query = f""" insert into tblRequisicionDet (RequisicionId, TarifaImpuestoId, ProductoId,
        CuentaPresupuestalEgrId, descripcion, Status, cantidad,
        Costo, Importe,
        IVA,
        ISH, RetencionISR, RetencionCedular, RetencionIVA,
        TotalPresupuesto, 
        Total) 
        values ({orderId}, '{producto['TarifaImpuestoId']}', '{producto['ProductoId']}',
        {cuentasPresupuestales[i]}, '{producto['Descripcion']}', '{producto['Status']}', {float(producto['cantidad'])},
        {float(producto['precio'])}, {(float(producto['cantidad'])* float(producto['precio']))}, 
        {((float(producto['cantidad'])* float(producto['precio']))*.16)},
        0, 0, 0, 0,
        {((float(producto['cantidad'])* float(producto['precio']))*1.16)}, 
        {((float(producto['cantidad'])* float(producto['precio']))*1.16)})
        """
        print("el query ", query)
        cu.execute(query)
        cu.commit()
    cu.close()
    return "bien"


# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'OrdenCompraDetId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'OrdenCompraId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'TarifaImpuestoId', 12, 'varchar', 10, 10, None, None, 0, None, None, 12, None, 10, 3, 'NO', 39)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'ProductoId', 12, 'varchar', 10, 10, None, None, 0, None, None, 12, None, 10, 4, 'NO', 39)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'CuentaPresupuestalEgrId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 5, 'NO', 56)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'Descripcion', 12, 'varchar', 250, 250, None, None, 0, None, None, 12, None, 250, 6, 'NO', 39)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 7, 'NO', 47)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'Cantidad', 6, 'float', 15, 8, None, 10, 0, None, '((0))', 6, None, None, 8, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'Costo', 3, 'money', 19, 21, 4, 10, 0, None, '((0))', 3, None, None, 9, 'NO', 60)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'Importe', 3, 'money', 19, 21, 4, 10, 0, None, '((0.00))', 3, None, None, 10, 'NO', 60)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'IEPS', 6, 'float', 15, 8, None, 10, 0, None, '((0))', 6, None, None, 11, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'Ajuste', 6, 'float', 15, 8, None, 10, 0, None, '((0))', 6, None, None, 12, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'IVA', 6, 'float', 15, 8, None, 10, 0, None, None, 6, None, None, 13, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'ISH', 6, 'float', 15, 8, None, 10, 0, None, None, 6, None, None, 14, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'RetencionISR', 6, 'float', 15, 8, None, 10, 0, None, None, 6, None, None, 15, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'RetencionCedular', 6, 'float', 15, 8, None, 10, 0, None, None, 6, None, None, 16, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'RetencionIVA', 6, 'float', 15, 8, None, 10, 0, None, None, 6, None, None, 17, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'TotalPresupuesto', 6, 'float', 15, 8, None, 10, 0, None, None, 6, None, None, 18, 'NO', 62)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompraDet', 'Total', 6, 'float', 15, 8, None, 10, 0, None, None, 6, None, None, 19, 'NO', 62)


def obtenerCuentasPresupuestales(order):
    bien = True
    error = ""
    cuentasPresupuestales = []
    cu = cnxn.cursor()
    for producto in order['productos']:
        query = f"""select CuentaPresupuestalEgrId from tblCuentaPresupuestalEgr where 
        ramoid={order['ramo']} and ProyectoId='{order['proyecto']}' 
        and DependenciaId='{order['departamento']}' and ObjetoGastoId={producto['ObjetoGastoId']} 
        and TipoGastoId={order['tipoGasto']};"""
        cu.execute(query)
        result = cu.fetchone()
        if result == None:
            bien = False
            error += f"{producto['Clave']} - {producto['Descripcion']}\n"
        else:
            cuentasPresupuestales.append(result[0])
    cu.close()
    return (bien, cuentasPresupuestales, error)


@app.route("/requisicion", methods=["POST"])
def createRequisicion():
    id = None
    print("viendo el request", request.json)
    order = request.json
    order['estatus'] = 'elaborada'
    cu = cnxn.cursor()
    cu.execute("select max(RequisicionId) from tblRequisicion ")
    row = cu.fetchone()
    id = row[0]
    productos = order.get('productos', [])
    if not productos:
        return jsonify(message=f'la requisición debe contener al menos 1 producto'), 404
    (cuentasBien, cuentasPresupuestales, error) = obtenerCuentasPresupuestales(order)
    if not cuentasBien:
        return jsonify(message=f'Alguna cuenta prespuestal no fue encontrada: \n {error}, llamar a gerente de base de datos'), 404
    if id == None:
        query = f"""insert into tblRequisicion (Fecha, Estatus, Departamento, Ramo,
        Motivo,GrupoProd, Direccion, Proyecto, 
        FechaEntrega, OficinaEntrega, Comentario, 
        Solicitante,Archivo, ArchivoBinary, TipoGasto) values
        ('{castFecha(order['fecha'])}', '{order['estatus']}', '{order['departamento']}', '{order['ramo']}',
        '{order['motivo']}', {order['grupoProd']}, '{order['direccion']}', '{order['proyecto']}',
        '{castFecha(order['fechaEntrega'])}', '{order['oficinaEntrega']}', '{order['comentario']}',
        '{order['solicitante']}', '', null, {order['tipoGasto']})"""
        cu.execute(query)
        cu.commit()
        cu.close()
        # crearOrdenCompra(order, id)
        crearReqDetalle(order['productos'], 1, cuentasPresupuestales)
        return jsonify(order)
    else:
        id = int(id)
        print("entro aqui ")
        id += 1
        order['consecutivo'] = id
        query = f"""insert into tblRequisicion (Fecha, Estatus, Departamento, Ramo,
        Motivo,GrupoProd, Direccion, Proyecto, 
        FechaEntrega, OficinaEntrega, Comentario, 
        Solicitante,Archivo, ArchivoBinary, TipoGasto) values
        ('{castFecha(order['fecha'])}', '{order['estatus']}', '{order['departamento']}', '{order['ramo']}',
        '{order['motivo']}', {order['grupoProd']}, '{order['direccion']}', '{order['proyecto']}',
        '{castFecha(order['fechaEntrega'])}', '{order['oficinaEntrega']}', '{order['comentario']}',
        '{order['solicitante']}', '', null, {order['tipoGasto']})"""
        cu.execute(query)
        cu.commit()
        cu.close()
        crearReqDetalle(order['productos'], id, cuentasPresupuestales)
        return jsonify(order)


def setEstateRequisicion(reqId, status):
    cu = cnxn.cursor()
    query = f"""update tblRequisicion set estatus='{status}' where RequisicionId={reqId} """
    cu.execute(query)
    cu.commit()
    cu.close()


@app.route("/updatestaterequisicion", methods=["POST"])
def updateStateRequisicion():
    jval = request.json
    print("viendo jval ", jval)
    setEstateRequisicion(jval["id"], jval["estatus"])
    orderval = retrieveRequsicion(jval["id"])
    return jsonify(orderval)


def retrieveRequsicion(id):
    cu = cnxn.cursor()
    productos = []
    cu.execute(f"select * from tblRequisicionDet where RequisicionId={id}")
    results = cu.fetchall()
    for x in results:
        print("producto ", x)
        importe = '{0:.2f}'.format((float(x[7]) * float(x[8])))
        iva = '{0:.2f}'.format(((float(x[7]) * float(x[8]))*.16))
        total = '{0:.2f}'.format(((float(x[7]) * float(x[8]))*1.16))
        productos.append(
            {"cuentaPresupuestalEgrId": f'{x[4]}', "productId": f'{x[3]}', "label": f'{x[3]} - {x[5]}', "um": "este falta", "precio": f'{x[8]}', "cantidad": x[7], "costo": x[8], "importe": importe, "iva": iva, "total": total})

    query = f"""select RequisicionId, convert(varchar, fecha, 103), estatus, departamento, ramo,
               motivo, grupoProd, direccion, proyecto, convert(varchar, fechaEntrega, 103), oficinaEntrega, 
               tipoGasto, comentario, solicitante, OrdenCompraId, CompraId  from tblRequisicion where RequisicionId={id}"""
    cu.execute(query)
    order = cu.fetchone()
    print("viendo order ", order)
    if not order:
        return jsonify(message=f'la orden {id} no se encuentra en el sistema'), 404
    orderval = {'consecutivo': order[0], 'fecha': order[1], 'estatus': order[2], 'departamento': order[3], 'ramo': order[4], 'motivo': order[5], 'grupoProd': order[6], 'direccion': order[7], 'proyecto': order[8],
                'fechaEntrega': order[9], 'oficinaEntrega': order[10], 'tipoGasto': order[11], 'productos': productos, 'comentario': order[12], 'solicitante': order[13], 'archivo': {}, "ordenCompraId": order[14], "CompraId": order[15]}
    cu.close()
    return orderval

# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'RequisicionDetId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'RequisicionId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 2, 'YES', 38)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'TarifaImpuestoId', 12, 'varchar', 10, 10, None, None, 1, None, None, 12, None, 10, 3, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'ProductoId', 12, 'varchar', 10, 10, None, None, 1, None, None, 12, None, 10, 4, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'CuentaPresupuestalEgrId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 5, 'YES', 38)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'Descripcion', 12, 'varchar', 250, 250, None, None, 1, None, None, 12, None, 250, 6, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'Status', 1, 'char', 1, 1, None, None, 1, None, None, 1, None, 1, 7, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'Cantidad', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 8, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'Costo', 3, 'money', 19, 21, 4, 10, 1, None, None, 3, None, None, 9, 'YES', 110)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'Importe', 3, 'money', 19, 21, 4, 10, 1, None, None, 3, None, None, 10, 'YES', 110)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'IEPS', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 11, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'Ajuste', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 12, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'IVA', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 13, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'ISH', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 14, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'RetencionISR', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 15, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'RetencionCedular', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 16, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'RetencionIVA', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 17, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'TotalPresupuesto', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 18, 'YES', 109)
# x tabla  ('PRUEBA', 'dbo', 'tblRequisicionDet', 'Total', 6, 'float', 15, 8, None, 10, 1, None, None, 6, None, None, 19, 'YES', 109)


@app.route("/requisicion/<id>", methods=["GET"])
# @jwt_required()
def getOrder(id):
    orderval = retrieveRequsicion(id)
    return jsonify(orderval)


@app.route("/requisiciones", methods=["GET"])
def getReqAll():
    cu = cnxn.cursor()
    data = []
    for x in cu.execute("select * from tblRequisicion"):
        data.append(dict(consecutivo=x[0], fecha=x[1], estatus=x[2], departamento=x[3],
                         ramo=x[4], motivo=x[5], grupoProd=x[6], direccion=x[7], proyecto=x[8], fechaEntrega=x[9],
                         oficinaEntrega=x[10], comentario=x[11], solicitante=x[12], archivo=x[13], archivoBinary=x[14],
                         tipoGasto=x[15]))
    cu.close()
    return jsonify(data)


@app.route("/compras", methods=["GET"])
def getComprasAll():
    cu = cnxn.cursor()
    data = []
    cu.execute(
        """select c.CompraId, c.ProveedorId, c.AlmacenId, c.TipoOperacionId, c.TipoComprobanteFiscalId,
        c.FolioFactura, c.Ejercicio, c.Fecha, c.FechaVencimiento, c.FechaContrarecibo, c.FechaPagoProgramado,
        c.Status, c.Observaciones, c.PagoProveedorId, pp.PagoProgramadoId
        from tblCompra c left join tblPagoProgramado pp on pp.CompraId=c.CompraId""")
    results = cu.fetchall()
    print("viendo results ", results)
    for x in results:
        cu.execute(
            f"select RazonSocial, RFC from tblProveedor where ProveedorId={x[1]}")
        result = cu.fetchone()
        cu.execute(
            f"select RequisicionId from tblRequisicion where CompraId={x[0]}")
        reqresult = cu.fetchone()
        reqid = 0
        if reqresult:
            reqid = reqresult[0]
        data.append(
            dict(consecutivo=x[0], Proveedor=result[0], RFC=result[1], Status=x[11], Fecha=x[7], PagoId=x[14], requisicionId=reqid))
    cu.close()
    return jsonify(data)


@app.route("/compra/<id>", methods=["GET"])
def getCompraId(id):
    cu = cnxn.cursor()
    data = []
    cu.execute(
        f"""select c.CompraId, c.ProveedorId, c.AlmacenId, c.TipoOperacionId, c.TipoComprobanteFiscalId,
        c.FolioFactura, c.Ejercicio, c.Fecha, c.FechaVencimiento, c.FechaContrarecibo, c.FechaPagoProgramado,
        c.Status, c.Observaciones, c.PagoProveedorId, pp.PagoProgramadoId
        from tblCompra c left join tblPagoProgramado pp on pp.CompraId=c.CompraId where c.CompraId={id}""")
    results = cu.fetchall()
    print("viendo results ", results)
    for x in results:
        cu.execute(
            f"select RazonSocial, RFC from tblProveedor where ProveedorId={x[1]}")
        result = cu.fetchone()
        cu.execute(
            f"select RequisicionId from tblRequisicion where CompraId={x[0]}")
        reqresult = cu.fetchone()
        reqid = 0
        if reqresult:
            reqid = reqresult[0]
        data.append(
            dict(consecutivo=x[0], Proveedor=result[0], RFC=result[1], Status=x[11], Fecha=x[7], PagoId=x[14], requisicionId=reqid, FolioFactura=x[5]))
    cu.close()

    return jsonify(data[0])


# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'CompraId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'ProveedorId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'AlmacenId', 12, 'varchar', 4, 4, None, None, 0, None, None, 12, None, 4, 3, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'TipoOperacionId', 1, 'char', 2, 2, None, None, 0, None, None, 1, None, 2, 4, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'TipoComprobanteFiscalId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 5, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FolioFactura', 12, 'varchar', 40, 40, None, None, 1, None, None, 12, None, 40, 6, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Ejercicio', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 7, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Fecha', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 8, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FechaVencimiento', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 9, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FechaContrarecibo', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 10, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FechaPagoProgramado', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 11, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 12, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Observaciones', 12, 'varchar', 1000, 1000, None, None, 1, None, None, 12, None, 1000, 13, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'PagoProveedorId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 14, 'YES', 38)


@app.route("/profile", methods=["GET"])
def profile():
    return jsonify(routes=[{"path": "/orden/all"}, {"path": "/orden/crear"}, {"path": "/orden/editar"}, {"path": "/admin/users"}], menu=[], image="https://www.google.com/aclk?sa=l&ai=DChcSEwjz6vKv1r-EAxWzD60GHeKCDdsYABABGgJwdg&ase=2&gclid=CjwKCAiA_tuuBhAUEiwAvxkgTrmm7scpFGLPdSynPbzNhJ8J2qTaPqWUw4aTezSM0wwjO1gCI7xj0xoCTA0QAvD_BwE&sig=AOD64_0lOClhjyT_EpSPCWafCWfKgYbcOw&ctype=5&nis=6&adurl&ved=2ahUKEwjumuav1r-EAxVt6MkDHafSBMQQvhd6BAgBEH4", token="asss")


# @app.route("/catalogodepartamento", methods=["GET"])
# # @jwt_required()
# def catalogo():
#     return jsonify(data=[{"id": 1, "nombre": "departamento 1"}, {"id": 2, "nombre": "departamento 2"}, {"id": 1, "nombre": "departamento 3"}])

def insertCompraDet(compraId, productos):
    cu = cnxn.cursor()
    for producto in productos:
        print("viendo x ", producto)
        query = f"select * from tblProducto where productoId='{producto['productId']}'"
        cu.execute(query)
        result = cu.fetchone()
        print("viendo el producto ", result)
        query = f"""insert into  tblCompraDet (compraId, total, TarifaImpuestoId, IVA, ProductoId,
        CuentaPresupuestalEgrId, Descripcion, ISH, RetencionISR, RetencionCedular, RetencionIVA,
        TotalPresupuesto, Cantidad, Costo,
        Importe, IEPS, Ajuste) values
        ({compraId}, {float(producto['total'])}, '{result[1]}', {float(producto['iva'])}, '{producto['productId']}',
        {int(producto['cuentaPresupuestalEgrId'])}, '{result[4]}', 0, 0, 0, 0,
        {float(producto['total'])},  {float(producto['cantidad'])}, {float(producto['costo'])},
        {float(producto['importe'])}, 0, 0)"""
        print("viendo query ", query)
        cu.execute(query)
        cu.commit()
    cu.close()


@app.route("/compra", methods=["POST"])
def crearCompra():
    compra = request.json
    print("viendo compra ", compra)
    cu = cnxn.cursor()
    query = f"""insert into tblCompra (ProveedorId, AlmacenId, TipoOperacionId, TipoComprobanteFiscalId,
    Ejercicio, Fecha, FechaVencimiento, FechaContrarecibo, FechaPagoProgramado,
    Status) 
    values 
    ({compra['proveedorId']}, '{compra['almacenId']}', '{compra['tipoOperacionId']}', {compra['tipoComprobanteFiscal']},
    {compra['ejercicio']}, '{castFecha(compra['fecha'])}', '{castFecha(compra['fechaPagoProgramado'])}', '{castFecha(compra['fechaPagoProgramado'])}', '{castFecha(compra['fechaPagoProgramado'])}',
    '{compra['status']}')"""
    print("query ", query)
    cu.execute(query)
    cu.commit()
    print("ya paso esto")
    query = "select max(CompraId) from tblCompra"
    cu.execute(query)
    result = cu.fetchone()
    compraId = result[0]
    insertCompraDet(compraId, compra['productos'])
    query = f"update tblOrdenCompra set status='R' where OrdenCompraId={compra['ordenCompraId']}"
    cu.execute(query)
    cu.commit()
    query = f"""update tblRequisicion set estatus='Compra', CompraId={compraId}  where RequisicionId={compra['reqId']} """
    cu.execute(query)
    cu.commit()
    cu.close()

    return jsonify({})

# {'proveedorId': 1119, 'almacenId': '0', 'tipoOperacionId': '85', 'tipoComprobanteFiscal': 1,
#  'folioFactura': '13334', 'ejercicio': 2024, 'fecha': '24/03/2024',
#  'fechaPagoProgramado': '30/03/2024', 'status': 'A', 'observacion': 'a', 'pagoProveedorId': ''}


# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'CompraId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'ProveedorId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'AlmacenId', 12, 'varchar', 4, 4, None, None, 0, None, None, 12, None, 4, 3, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'TipoOperacionId', 1, 'char', 2, 2, None, None, 0, None, None, 1, None, 2, 4, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'TipoComprobanteFiscalId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 5, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FolioFactura', 12, 'varchar', 40, 40, None, None, 1, None, None, 12, None, 40, 6, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Ejercicio', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 7, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Fecha', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 8, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FechaVencimiento', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 9, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FechaContrarecibo', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 10, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'FechaPagoProgramado', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 11, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 12, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'Observaciones', 12, 'varchar', 1000, 1000, None, None, 1, None, None, 12, None, 1000, 13, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCompra', 'PagoProveedorId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 14, 'YES', 38)

@app.route("/pagos", methods=["GET"])
def getPagos():
    data = []
    cu = cnxn.cursor()
    cu.execute(f"select CompraId, ProveedorId, FolioFactura  from tblCompra")
    compras = cu.fetchall()
    for compra in compras:
        cu.execute(
            f"select RazonSocial, RFC from tblProveedor where ProveedorId={compra[1]}")
        provResult = cu.fetchone()
        proveedor = provResult[0]
        rfc = provResult[1]
        total = 0
        cu.execute(f"select * from tblCompradet where CompraId={compra[0]}")
        results2 = cu.fetchall()
        for y in results2:
            total += y[-1]
        totalf = '{0:.2f}'.format(total)
        data.append(
            dict(CompraId=compra[0], ProveedorId=compra[1], FolioFactura=compra[2], Proveedor=proveedor, RFC=rfc, Total=totalf))
    # cu.execute(
    #     f"select CompraId, ProveedorId, FolioFactura  from tblCompra")
    # results = cu.fetchall()
    # for x in results:
    #     print("el tbl compra ", x)
    #     cu.execute(
    #         f"select RazonSocial, RFC from tblProveedor where ProveedorId={x[1]}")
    #     provResult = cu.fetchone()
    #     provedor = provResult[0]
    #     rfc = provResult[1]
    #     cu.execute(f"select * from tblCompradet where CompraId={x[0]}")
    #     results2 = cu.fetchall()
    #     for y in results2:
    #         print("viendo det ", y)
    #         total += y[-1]
    #     totalf = '{0:.2f}'.format(total)
    #     data.append(dict(CompraId=x[0], RFC=rfc, Proveedor=provedor,
    #                 ProveedorId=x[1], FolioFactura=x[2], Total=totalf))
    return jsonify(data)


@app.route("/pago/<id>", methods=["GET"])
def pagoId(id):
    cu = cnxn.cursor()
    total = 0
    cu.execute(
        f"select tc.ProveedorId, tc.FolioFactura, ppd.PagoProveedorId from tblCompra tc join tblPagoProveedorDet ppd on tc.CompraId=ppd.CompraId where tc.CompraId={id}")
    result = cu.fetchone()
    cu.execute(
        f"select RazonSocial, RFC from tblProveedor where ProveedorId={result[0]}")
    provResult = cu.fetchone()
    provedor = provResult[0]
    rfc = provResult[1]
    cu.execute(
        f"select Folio, FormaDePagoId, RefCuentaBancoId, Concepto from tblPagoProveedor where PagoProveedorId={result[2]}")
    pagoProveedorResult = cu.fetchone()
    cu.execute(f"select * from tblCompradet where CompraId={id}")
    results = cu.fetchall()
    for x in results:
        print("viendo det ", x)
        total += x[-1]
    totalf = '{0:.2f}'.format(total)
    return jsonify(dict(Folio=pagoProveedorResult[0], FormaDePagoId=pagoProveedorResult[1],
                        RefCuentaBancoId=pagoProveedorResult[2], Concepto=pagoProveedorResult[3],
                        RFC=rfc, Provedor=provedor, ProveedorId=result[0], FolioFactura=result[1], Total=totalf, PagoProveedorId=result[2]))

# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'PagoProveedorId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'ProveedorId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'TipoPagoId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 3, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'FormaDePagoId', 12, 'varchar', 1, 1, None, None, 0, None, None, 12, None, 1, 4, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Ejercicio', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 5, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Fecha', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 6, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 7, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'RefCuentaBancoId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 8, 'YES', 38)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Folio', 12, 'varchar', 20, 20, None, None, 1, None, None, 12, None, 20, 9, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Concepto', 12, 'varchar', 1000, 1000, None, None, 0, None, None, 12, None, 1000, 10, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Total', 3, 'money', 19, 21, 4, 10, 0, None, None, 3, None, None, 11, 'NO', 60)


@app.route("/autorizarpago", methods=["POST"])
def autorizarPago():
    cu = cnxn.cursor()
    pago = request.json
    print("fiend pago ", pago)
    query = f"""insert into  tblPagoProgramado (CompraId, Fecha, 
    FechaPagoProgramado, Importe, Status, Observaciones) 
    values ({pago['CompraId']}, '{castFecha(pago['Fecha'])}',
    '{castFecha(pago['Fecha'])}', {float(pago['Importe'])}, '{pago['Status']}', '{pago['Observaciones']}')"""
    print("query ", query)
    cu.execute(query)
    cu.commit()
    cu.close()
    return jsonify({})

# x tabla  ('PRUEBA', 'dbo', 'tblPagoProgramado', 'PagoProgramadoId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProgramado', 'CompraId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProgramado', 'Fecha', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 3, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProgramado', 'FechaPagoProgramado', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 4, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProgramado', 'Importe', 3, 'money', 19, 21, 4, 10, 0, None, None, 3, None, None, 5, 'NO', 60)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProgramado', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 6, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProgramado', 'Observaciones', 12, 'varchar', 1000, 1000, None, None, 1, None, None, 12, None, 1000, 7, 'YES', 39)


@app.route("/aplicarpago", methods=["POST"])
def aplicarPago():
    cu = cnxn.cursor()
    pago = request.json
    compraId = pago['compraId']
    print("fiend pago ", pago)
    query = f"""insert into tblPagoProveedor (ProveedorId, TipoPagoId, FormaDePagoId, Ejercicio, Fecha,
    Status, RefCuentaBancoId, Folio, Concepto, Total) 
    values 
    ({pago['pagoProveedorId']}, 1, '{pago['formaDePagoId']}', {pago['ejercicio']}, '{castFecha(pago['fecha'])}',
    'A', {pago['refCuentaBancoId']}, '{pago['folio']}', '{pago['concepto']}', {pago['total']})"""
    print("query ", query)
    cu.execute(query)
    cu.commit()
    cu.execute("select max(PagoProveedorId) from tblPagoProveedor")
    maxPagoProveedorId = cu.fetchone()
    cu.execute(
        f"select PagoProgramadoId from tblPagoProgramado where CompraId={int(compraId)}")
    result = cu.fetchone()
    query = f"""insert into tblPagoProveedorDet (PagoProveedorId, RefPagoProgramadoId, CompraId, Importe) 
    values 
    ({maxPagoProveedorId[0]}, {result[0]}, {compraId}, {pago['total']})"""
    print("viendo query ", query)
    cu.execute(query)
    cu.commit()
    cu.close()
    return jsonify({})


# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedorDet', 'PagoProveedorDetId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedorDet', 'PagoProveedorId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedorDet', 'RefPagoProgramadoId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 3, 'YES', 38)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedorDet', 'CompraId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 4, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedorDet', 'Importe', 3, 'money', 19, 21, 4, 10, 0, None, None, 3, None, None, 5, 'NO', 60)


# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'PagoProveedorId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'ProveedorId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'TipoPagoId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 3, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'FormaDePagoId', 12, 'varchar', 1, 1, None, None, 0, None, None, 12, None, 1, 4, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Ejercicio', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 5, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Fecha', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 6, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 7, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'RefCuentaBancoId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 8, 'YES', 38)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Folio', 12, 'varchar', 20, 20, None, None, 1, None, None, 12, None, 20, 9, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Concepto', 12, 'varchar', 1000, 1000, None, None, 0, None, None, 12, None, 1000, 10, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Total', 3, 'money', 19, 21, 4, 10, 0, None, None, 3, None, None, 11, 'NO', 60)

# {'CompraId': '1660', 'Fecha': '24/03/2024', 'FechaPagoProgramado': '24/03/2024', 'Importe': '696.00', 'Status': 'A', 'Observaciones': 'aasdd'}


@app.route("/pagoprovedor", methods=["GET"])
def getPagoProveedorll():
    cu = cnxn.cursor()
    data = []
    cu.execute("select * from tblPagoProveedor")
    results = cu.fetchall()
    print("viendo results ", results)
    for x in results:
        data.append(dict(FormaDePagoId=x[0], Nombre=x[1], Tipo=x[2]))
    cu.close()
    return jsonify(data)

# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'PagoProveedorId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'ProveedorId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'TipoPagoId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 3, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'FormaDePagoId', 12, 'varchar', 1, 1, None, None, 0, None, None, 12, None, 1, 4, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Ejercicio', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 5, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Fecha', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 6, 'NO', 61)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 7, 'NO', 47)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'RefCuentaBancoId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 8, 'YES', 38)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Folio', 12, 'varchar', 20, 20, None, None, 1, None, None, 12, None, 20, 9, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Concepto', 12, 'varchar', 1000, 1000, None, None, 0, None, None, 12, None, 1000, 10, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblPagoProveedor', 'Total', 3, 'money', 19, 21, 4, 10, 0, None, None, 3, None, None, 11, 'NO', 60)


@app.route("/jaja", methods=["GET"])
def jaja():
    cu = cnxn.cursor()
    for x in cu.execute("sp_columns 'tblPagoProveedor'"):
        print("x tabla ", x)
    return jsonify({})


@app.route("/proveedor", methods=["GET"])
def proveedor():
    data = []
    cu = cnxn.cursor()

    # falta join con tabla tblTipoOperacion para sacar texto de TipoOperacionId valor de TipoComprobanteFiscalId otra tabla tblTipoComprobanteFiscal
    for x in cu.execute("select * from  tblProveedor "):
        data.append(dict(ProveedorId=x[0],  TipoProveedorId=x[1], PaisId=x[3], EstadoId=x[4], MunicipioId=x[5],
                         RazonSocial=x[6], Status=[7], RFC=x[8], CURP=x[9], TipoOperacionId=x[10], TipoComprobanteFiscalId=x[11], value=x[0], label=x[5]))

    # tblProveedor
    cu.close()
    sortData = sorted(data, key=lambda x: x['label'])
    return jsonify(sortData)


# ('PRUEBA', 'dbo', 'tblProveedor', 'ProveedorId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# ('PRUEBA', 'dbo', 'tblProveedor', 'TipoProveedorId', 1, 'char', 2, 2, None, None, 0, None, None, 1, None, 2, 2, 'NO', 47)
# ('PRUEBA', 'dbo', 'tblProveedor', 'PaisId', 1, 'char', 2, 2, None, None, 1, None, None, 1, None, 2, 3, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'EstadoId', -9, 'nvarchar', 2, 4, None, None, 1, None, None, -9, None, 4, 4, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'MunicipioId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 5, 'YES', 38)
# ('PRUEBA', 'dbo', 'tblProveedor', 'RazonSocial', -9, 'nvarchar', 250, 500, None, None, 0, None, None, -9, None, 500, 6, 'NO', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Status', 1, 'char', 1, 1, None, None, 0, None, None, 1, None, 1, 7, 'NO', 47)
# ('PRUEBA', 'dbo', 'tblProveedor', 'RFC', -9, 'nvarchar', 15, 30, None, None, 1, None, None, -9, None, 30, 8, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'CURP', -9, 'nvarchar', 18, 36, None, None, 1, None, None, -9, None, 36, 9, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'TipoOperacionId', 1, 'char', 2, 2, None, None, 0, None, None, 1, None, 2, 10, 'NO', 47)
# ('PRUEBA', 'dbo', 'tblProveedor', 'TipoComprobanteFiscalId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 11, 'NO', 56)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Domicilio', -9, 'nvarchar', 250, 500, None, None, 1, None, None, -9, None, 500, 12, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Colonia', -9, 'nvarchar', 250, 500, None, None, 1, None, None, -9, None, 500, 13, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'CodigoPostal', -9, 'nvarchar', 5, 10, None, None, 1, None, None, -9, None, 10, 14, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Telefono1', -9, 'nvarchar', 25, 50, None, None, 1, None, None, -9, None, 50, 15, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Telefono2', -9, 'nvarchar', 25, 50, None, None, 1, None, None, -9, None, 50, 16, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Telefono3', -9, 'nvarchar', 25, 50, None, None, 1, None, None, -9, None, 50, 17, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Fax', -9, 'nvarchar', 25, 50, None, None, 1, None, None, -9, None, 50, 18, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Email', -9, 'nvarchar', 100, 200, None, None, 1, None, None, -9, None, 200, 19, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Contacto1', -9, 'nvarchar', 250, 500, None, None, 1, None, None, -9, None, 500, 20, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Contacto2', -9, 'nvarchar', 250, 500, None, None, 1, None, None, -9, None, 500, 21, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Observaciones', -9, 'nvarchar', 1000, 2000, None, None, 1, None, None, -9, None, 2000, 22, 'YES', 39)
# ('PRUEBA', 'dbo', 'tblProveedor', 'CatalogoCuentaId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 23, 'YES', 38)
# ('PRUEBA', 'dbo', 'tblProveedor', 'Origen', 1, 'char', 1, 1, None, None, 1, None, None, 1, None, 1, 24, 'YES', 39)


@app.route("/users", methods=["GET"])
def users():
    return jsonify(data=[{"id": "1", "name": "jorge", "email": "jorge@test.com", "roleId": 1, "value": 1}, {"id": "2", "name": "carlos", "email": "carlos@test.com", "roleId": 2, "value": 2}])


@app.route("/roles", methods=["GET"])
def roles():
    return jsonify(data=[{"label": "uno", "value": "uno"}])


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return 'You want path: %s' % path


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/ordencompra", methods=["GET"])
def ordenCompra():
    cu = cnxn.cursor()
    # falta join con tabla tblTipoOperacion para sacar texto de TipoOperacionId valor de TipoComprobanteFiscalId otra tabla tblTipoComprobanteFiscal
    for x in cu.execute("sp_columns 'tblOrdenCompra'"):
        print(x)

    # tblProveedor
    cu.close()
    return jsonify(data=[{"label": "uno", "value": "1"}])


def insertOrdenCompraDet(ordenId, productos):
    cu = cnxn.cursor()
    for producto in productos:
        print("viendo x ", producto)
        query = f"select * from tblProducto where productoId='{producto['productId']}'"
        cu.execute(query)
        result = cu.fetchone()
        print("viendo el producto ", result)
        query = f"""insert into  tblOrdenCompraDet (OrdenCompraId, total, TarifaImpuestoId, IVA, ProductoId,
        CuentaPresupuestalEgrId, Descripcion, ISH, RetencionISR, RetencionCedular, RetencionIVA,
        TotalPresupuesto, Status, Cantidad, Costo,
        Importe, IEPS, Ajuste) values
        ({ordenId}, {float(producto['total'])}, '{result[1]}', {float(producto['iva'])}, '{producto['productId']}',
        {int(producto['cuentaPresupuestalEgrId'])}, '{result[4]}', 0, 0, 0, 0,
        {float(producto['total'])}, '{result[6]}', {float(producto['cantidad'])}, {float(producto['costo'])},
        {float(producto['importe'])}, 0, 0)"""
        print("viendo query ", query)
        cu.execute(query)
        cu.commit()
    cu.close()


@app.route("/ordencompra", methods=["POST"])
def createOrdeCompra():
    orden = request.json
    print("viendo orden,", orden)
    proveedorId = orden['ProveedorId']
    cu = cnxn.cursor()
    query = f"select * from tblProveedor where ProveedorId={proveedorId}"
    cu.execute(query)
    result = cu.fetchone()
    print("viendo resulto ", result)
    tipoOperacion = result[9]
    TipoComprobanteFiscalId = result[10]
    query = f"""insert into tblOrdenCompra (ProveedorId, AlmacenId,
    TipoOperacionId, TipoComprobanteFiscalId, Ejercicio, Fecha,
    FechaRecepcion, Referencia, Status, Observacion) values (
        {orden['ProveedorId']}, '{orden['AlmacenId']}',
        '{tipoOperacion}', '{TipoComprobanteFiscalId}', {orden['Ejercicio']}, '{castFecha(orden['Fecha'])}',
        '{castFecha(orden['FechaRecepcion'])}', '{orden['Referencia']}', 'A', '{orden['Observacion']}')"""
    print("esta e sla orden ", orden)
    print("viendo query  --- ", query)
    cu.execute(query)
    cu.commit()
    query = "select max(OrdenCompraId) from tblOrdenCompra"
    cu.execute(query)
    result = cu.fetchone()
    Ordenid = result[0]
    insertOrdenCompraDet(Ordenid, orden['productos'])
    query = f"""update tblRequisicion set estatus='OrdenCompra', OrdenCompraId={Ordenid}  where RequisicionId={orden['reqId']} """
    cu.execute(query)
    cu.commit()
    # setEstateRequisicion(orden['reqId'], 'OrdenCompra')
    cu.close()
    return jsonify()


# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'OrdenCompraId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'ProveedorId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 2, 'NO', 56)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'AlmacenId', 12, 'varchar', 4, 4, None, None, 0, None, None, 12, None, 4, 3, 'NO', 39)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'TipoOperacionId', 1, 'char', 2, 2, None, None, 0, None, None, 1, None, 2, 4, 'NO', 47)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'TipoComprobanteFiscalId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 5, 'NO', 56)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'Ejercicio', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 6, 'NO', 56)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'Fecha', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 7, 'NO', 61)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'FechaRecepcion', 11, 'datetime', 23, 16, 3, None, 0, None, None, 9, 3, None, 8, 'NO', 61)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'Referencia', 12, 'varchar', 25, 25, None, None, 1, None, None, 12, None, 25, 9, 'YES', 39)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'Status', 1, 'char', 1, 1, None, None, 0, None, "('A')", 1, None, 1, 10, 'NO', 47)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'Observacion', 12, 'varchar', 1000, 1000, None, None, 1, None, None, 12, None, 1000, 11, 'YES', 39)
# ('WideWorldImporters', 'dbo', 'tblOrdenCompra', 'GastoPorComprobarId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 12, 'YES', 38)


@app.route("/ordercompra", methods=["GET"])
def getOrdersAll():
    cu = cnxn.cursor()
    data = []
    cu.execute("select * from tblOrdenCompra")
    results = cu.fetchall()
    print("viendo results ", results)
    for x in results:
        cu.execute(
            f"select RazonSocial, RFC from tblProveedor where ProveedorId={x[1]}")
        result = cu.fetchone()
        cu.execute(
            f"select RequisicionId from tblRequisicion where OrdenCompraId={x[0]}")
        reqresult = cu.fetchone()
        reqid = 0
        if reqresult:
            reqid = reqresult[0]
        data.append(
            dict(consecutivo=x[0], Proveedor=result[0], RFC=result[1], Status=x[9], Fecha=x[6], requisicionId=reqid))
    cu.close()
    return jsonify(data)


def retrieveOrdenCompraId(id):
    cu = cnxn.cursor()
    query = f"""select ProveedorId, status, AlmacenId, 
    TipoOperacionId, TipoComprobanteFiscalId, Ejercicio
    from tblOrdenCompra where OrdenCompraId={id}"""
    cu.execute(query)
    result = cu.fetchone()
    proveedorId = result[0]
    query2 = f"select RequisicionId from tblRequisicion where OrdenCompraId={id}"
    cu.execute(query2)
    dato = cu.fetchone()
    print("viendo dato ", dato)
    reqId = dato[0]

    return dict(ProveedorId=proveedorId, Status=result[1], AlmacenId=result[2],
                TipoOperacionId=result[3], TipoComprobanteFiscalId=result[4], Ejercicio=result[5],
                ReqId=reqId)


@app.route("/ordencompra/<id>", methods=["GET"])
def ordencompraId(id):
    ordenCompra = retrieveOrdenCompraId(id)
    return jsonify(ordenCompra)


@app.route("/tipopagos", methods=["GET"])
def getTipoPagosAll():
    cu = cnxn.cursor()
    data = []
    cu.execute("select * from tblFormaDePago")
    results = cu.fetchall()
    for x in results:
        data.append(
            dict(FormaDePagoId=x[0], Nombre=x[1], Tipo=x[2], value=x[0], label=x[1]))
    sortData = sorted(data, key=lambda x: x['label'])
    cu.close()
    return jsonify(sortData)

# x tabla  ('PRUEBA', 'dbo', 'tblFormaDePago', 'FormaDePagoId', 12, 'varchar', 1, 1, None, None, 0, None, None, 12, None, 1, 1, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblFormaDePago', 'Nombre', 12, 'varchar', 100, 100, None, None, 0, None, None, 12, None, 100, 2, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblFormaDePago', 'Tipo', 1, 'char', 1, 1, None, None, 1, None, None, 1, None, 1, 3, 'YES', 39)


@app.route("/cuentabancos", methods=["GET"])
def getCuentaBancosAll():
    cu = cnxn.cursor()
    data = []
    cu.execute("select * from tblCuentaBanco")
    results = cu.fetchall()
    for x in results:
        data.append(
            dict(CuentaBancoId=x[0], BancoId=x[1], CatalogoCuentaId=x[2], Cuenta=x[3],
                 FolioCheque=x[4], Descripcion=x[5], ReportePolizaCheque=x[6], RamoId=x[7],
                 value=x[0], label=x[5]))
    sortData = sorted(data, key=lambda x: x['label'])
    cu.close()
    return jsonify(sortData)

# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'CuentaBancoId', 4, 'int identity', 10, 4, 0, 10, 0, None, None, 4, None, None, 1, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'BancoId', 4, 'int', 10, 4, 0, 10, 1, None, None, 4, None, None, 2, 'YES', 38)
# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'CatalogoCuentaId', 4, 'int', 10, 4, 0, 10, 0, None, None, 4, None, None, 3, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'Cuenta', 12, 'varchar', 100, 100, None, None, 0, None, None, 12, None, 100, 4, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'FolioCheque', 4, 'int', 10, 4, 0, 10, 0, None, '((0))', 4, None, None, 5, 'NO', 56)
# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'Descripcion', 12, 'varchar', 250, 250, None, None, 0, None, None, 12, None, 250, 6, 'NO', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'ReportePolizaCheque', 12, 'varchar', 250, 250, None, None, 1, None, None, 12, None, 250, 7, 'YES', 39)
# x tabla  ('PRUEBA', 'dbo', 'tblCuentaBanco', 'RamoId', -9, 'nvarchar', 6, 12, None, None, 1, None, None, -9, None, 12, 8, 'YES', 39)


if __name__ == "__main__":
    app.run()
