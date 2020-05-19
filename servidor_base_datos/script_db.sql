
/*
Agregar permisos para conexión remota a nuestro servidor frontal con el usuario administrador.
*/


CREATE USER 'root'@'localhost' IDENTIFIED BY 'capitantrueno';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost'
WITH GRANT OPTION;
CREATE USER 'administrador'@'%' IDENTIFIED BY 'capitantrueno';
GRANT ALL PRIVILEGES ON *.* TO 'administrador'@'192.168.122.181'
WITH GRANT OPTION;


/*
mysql -u root -p database_virtualizacion < script_db.sql
*/


create database if not exists database_virtualizacion;
use database_virtualizacion;

CREATE TABLE IF NOT EXISTS tipoUsuario
(
    codigo int (11) NOT NULL auto_increment,
    nombre varchar(40) NOT NULL,
    descripcion varchar(100) NOT NULL,
    PRIMARY KEY(codigo)
);

CREATE TABLE IF NOT EXISTS usuario
(
    identificador varchar(40) NOT NULL,
    nombre varchar(40) NOT NULL,
    apellido varchar(40) NOT NULL,
    direccion varchar(40) NOT NULL,
    tipoUsuario int(11) NOT NULL,
    PRIMARY KEY(identificador),
    FOREIGN KEY (tipoUsuario) REFERENCES tipoUsuario(codigo)
);

CREATE TABLE IF NOT EXISTS post 
(
    codigo int (11) NOT NULL auto_increment,
    mensaje varchar(200) NOT NULL, 
    usuario varchar(40) NOT NULL,
    PRIMARY KEY(codigo),
    FOREIGN KEY (usuario) REFERENCES usuario(identificador)
);

insert into tipoUsuario(nombre, descripcion) values ('administrador','Administradores del sistema.');
insert into tipoUsuario(nombre, descripcion) values ('desarrollador','Usuario normal del sistema');
insert into tipoUsuario(nombre, descripcion) values ('moderador','Moderador de temas en los foros.');


insert into usuario(identificador, nombre, apellido, direccion, tipoUsuario) values ('ericktejaxun','Erick','Tejaxun','Cáceres',1);
insert into usuario(identificador, nombre, apellido, direccion, tipoUsuario) values ('santiagoestrada','Santiago','Estrada','Badajoz',2);
insert into usuario(identificador, nombre, apellido, direccion, tipoUsuario) values ('miriamgonzales','Miriam','Gonzales','Cáceres',2);
insert into usuario(identificador, nombre, apellido, direccion, tipoUsuario) values ('pabloguzman','Pablo','Guzman','Cáceres',3);
insert into usuario(identificador, nombre, apellido, direccion, tipoUsuario) values ('eddyleon','Eddy','De León','Segovia',3);


insert into post(mensaje, usuario) values ('Se ha cambiado un log en el sistema.','ericktejaxun');
insert into post(mensaje, usuario) values ('Se ha hecho un merge en la rama principal','santiagoestrada');
insert into post(mensaje, usuario) values ('Se ha cambiado las rutas en el firewall','ericktejaxun');
insert into post(mensaje, usuario) values ('Se ha reinicio el servidor de jira','pabloguzman');
insert into post(mensaje, usuario) values ('Se ha creado una nueva rama para probar nuevas características','miriamgonzales');


