CREATE TABLE tblRequisicion (RequisicionId int IDENTITY(1, 1) NOT NULL primary key,
Fecha DATE, Estatus varchar(20), Departamento varchar(20), Ramo varchar(10), 
Motivo varchar(150), GrupoProd Int, Direccion varchar(20), Proyecto varchar(20), 
FechaEntrega DATE, OficinaEntrega varChar(10), Comentario varchar(150), 
Solicitante varchar(100), Archivo varchar(100), ArchivoBinary VARBINARY(MAX), TipoGasto int,
OrdenCompraId int, CompraId int)


CREATE TABLE tblRequisicionDet (RequisicionDetId int IDENTITY(1, 1) NOT NULL primary key,
RequisicionId int, TarifaImpuestoId varchar(10), ProductoId varchar(10), CuentaPresupuestalEgrId int, 
Descripcion varchar(250), Status char(1), Cantidad float, Costo money, 
Importe money, IEPS float, Ajuste float, 
IVA float, ISH float, RetencionISR float, RetencionCedular float,
RetencionIVA float, TotalPresupuesto float, Total float)



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

