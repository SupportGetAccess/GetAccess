from graphviz import Digraph

dot = Digraph(comment='GetAccess DER', format='jpg')
dot.attr(rankdir='TB', size='16,12', dpi='150')
dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')

# Tablas
dot.node('usuarios', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD bgcolor="#6366f1" colspan="2"><FONT color="white"><B>USUARIOS</B></FONT></TD></TR>
<TR><TD>id (PK)</TD><TD>INTEGER</TD></TR>
<TR><TD>email</TD><TD>VARCHAR</TD></TR>
<TR><TD>nombre</TD><TD>VARCHAR(100)</TD></TR>
<TR><TD>apellido</TD><TD>VARCHAR(100)</TD></TR>
<TR><TD>password</TD><TD>VARCHAR</TD></TR>
<TR><TD>verificado</TD><TD>INTEGER</TD></TR>
<TR><TD>rol</TD><TD>TEXT</TD></TR>
</TABLE>>''')

dot.node('eventos', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD bgcolor="#6366f1" colspan="2"><FONT color="white"><B>EVENTOS</B></FONT></TD></TR>
<TR><TD>id (PK)</TD><TD>INTEGER</TD></TR>
<TR><TD>nombre</TD><TD>VARCHAR(200)</TD></TR>
<TR><TD>descripcion</TD><TD>VARCHAR</TD></TR>
<TR><TD>fecha</TD><TD>DATETIME</TD></TR>
<TR><TD>lugar</TD><TD>VARCHAR(200)</TD></TR>
<TR><TD>precio</TD><TD>FLOAT</TD></TR>
<TR><TD>capacidad</TD><TD>INTEGER</TD></TR>
<TR><TD>vendidos</TD><TD>INTEGER</TD></TR>
<TR><TD>imagen</TD><TD>VARCHAR</TD></TR>
<TR><TD>categoria</TD><TD>TEXT</TD></TR>
</TABLE>>''')

dot.node('entradas', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD bgcolor="#10b981" colspan="2"><FONT color="white"><B>ENTRADAS</B></FONT></TD></TR>
<TR><TD>id (PK)</TD><TD>INTEGER</TD></TR>
<TR><TD>evento_id (FK)</TD><TD>INTEGER</TD></TR>
<TR><TD>usuario_id (FK)</TD><TD>INTEGER</TD></TR>
<TR><TD>cantidad</TD><TD>INTEGER</TD></TR>
<TR><TD>total</TD><TD>FLOAT</TD></TR>
<TR><TD>estado</TD><TD>VARCHAR(50)</TD></TR>
<TR><TD>preference_id</TD><TD>VARCHAR</TD></TR>
<TR><TD>usada</TD><TD>INTEGER</TD></TR>
</TABLE>>''')

dot.node('validaciones', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD bgcolor="#f59e0b" colspan="2"><FONT color="white"><B>VALIDACIONES</B></FONT></TD></TR>
<TR><TD>id (PK)</TD><TD>INTEGER</TD></TR>
<TR><TD>entrada_id (FK)</TD><TD>INTEGER</TD></TR>
<TR><TD>scanner_id (FK)</TD><TD>INTEGER</TD></TR>
<TR><TD>cantidad_original</TD><TD>INTEGER</TD></TR>
<TR><TD>timestamp</TD><TD>TEXT</TD></TR>
</TABLE>>''')

dot.node('transferencias', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD bgcolor="#ec4899" colspan="2"><FONT color="white"><B>TRANSFERENCIAS</B></FONT></TD></TR>
<TR><TD>id (PK)</TD><TD>INTEGER</TD></TR>
<TR><TD>entrada_id (FK)</TD><TD>INTEGER</TD></TR>
<TR><TD>usuario_origen (FK)</TD><TD>INTEGER</TD></TR>
<TR><TD>usuario_destino</TD><TD>TEXT</TD></TR>
<TR><TD>token</TD><TD>TEXT</TD></TR>
<TR><TD>estado</TD><TD>TEXT</TD></TR>
<TR><TD>created_at</TD><TD>TEXT</TD></TR>
<TR><TD>accepted_at</TD><TD>TEXT</TD></TR>
</TABLE>>''')

dot.node('evento_imagenes', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD bgcolor="#8b5cf6" colspan="2"><FONT color="white"><B>EVENTO_IMAGENES</B></FONT></TD></TR>
<TR><TD>id (PK)</TD><TD>INTEGER</TD></TR>
<TR><TD>evento_id (FK)</TD><TD>INTEGER</TD></TR>
<TR><TD>url</TD><TD>TEXT</TD></TR>
<TR><TD>orden</TD><TD>INTEGER</TD></TR>
</TABLE>>''')

dot.node('password_reset', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD bgcolor="#64748b" colspan="2"><FONT color="white"><B>PASSWORD_RESET</B></FONT></TD></TR>
<TR><TD>id (PK)</TD><TD>INTEGER</TD></TR>
<TR><TD>email</TD><TD>TEXT</TD></TR>
<TR><TD>token</TD><TD>TEXT</TD></TR>
<TR><TD>usado</TD><TD>INTEGER</TD></TR>
<TR><TD>expires_at</TD><TD>TEXT</TD></TR>
</TABLE>>''')

# Relaciones
dot.edge('eventos', 'entradas', label='1:N')
dot.edge('usuarios', 'entradas', label='1:N')
dot.edge('entradas', 'validaciones', label='1:N')
dot.edge('usuarios', 'validaciones', label='1:N')
dot.edge('eventos', 'evento_imagenes', label='1:N')
dot.edge('entradas', 'transferencias', label='1:N')
dot.edge('usuarios', 'transferencias', label='1:N')

dot.render('C:/Users/guill/eventos_tickets_full/DER_GetAccess', cleanup=True)
print("DER_GetAccess.jpg creado exitosamente")
