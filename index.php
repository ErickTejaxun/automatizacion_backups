<title> Post Virtualización y escalabilidad de servidores </title>

<h1>Virtualización y escalabilidad de servidores </h1>
<?php
$enlace = mysqli_connect("192.168.122.128", "administrador", "capitantrueno", "database_virtualizacion");

if (!$enlace) {
    echo "Error: No se pudo conectar a MySQL." . PHP_EOL; 
    echo "errno de depuración: " . mysqli_connect_errno() . PHP_EOL;
    echo "error de depuración: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

$fecha= date_create();

if(!$enlace->real_query("insert into post(usuario,mensaje) values ('ericktejaxun','".date_timestamp_get($fecha)."')"))
{
    echo "Falló la creación de la tabla: (" . $enlace->errno . ") " . $enlace->error;
}


$enlace->real_query("SELECT * FROM post");
$resultado = $enlace->use_result();

#echo "Orden del conjunto de resultados...\n";
echo "<table style='border: solid 1px black;'>";
echo "<tr><th>Código</th><th>Nombre</th><th>Mensaje</th></tr>";
while ($fila = $resultado->fetch_assoc())
{
    echo "<tr><th align='left'>".$fila['codigo']."</th><th align='left'>".$fila['usuario']."</th><th align='left'>".$fila['mensaje']."</th></tr>\n";
}
echo "</table>";

?>
  



<?php
mysqli_close($enlace);
?>