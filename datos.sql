drop database if exists sorisound;

create database sorisound;

use sorisound;

create table embalaje(
    tipo varchar(25),
    stock int,
    costo float,
    fecha_ultima_actualizacion date,
    primary key(tipo)
);


create table producto(
    modelo varchar(50),
    descripcion varchar(100),
    color varchar(20),
    embalaje varchar(25),
    foreign key(embalaje) references(tipo),
    primary key(modelo)
);

create table tipo_item(
    tipo varchar(25),
    primary key(tipo)
);

create table proceso(
    tipo_proceso varchar(50),
    costo float,
    fecha date,
    primary key(tipo_proceso) 
);

create table item(
    codigo_item varchar(10),
    color varchar(20),
    descripcion varchar(100),
    peso float,
    tipo_item varchar(25),
    ancho float,
    largo float,
    diametro float,
    espesor float,
    largo_tira_tubo float,
    precio_materia_prima float,
    primary key(codigo_item),
    foreign key(tipo_item) references tipo_item(tipo) 

);

create table item_proceso(
    codigo_item varchar(10),
    tipo_proceso varchar(50),
    foreign key(codigo_item) references item(codigo_item),
    foreign key(tipo_proceso) references proceso(tipo_proceso),
    primary key(codigo_item,tipo_proceso)

);

create table producto_item(
    modelo varchar(50),
    codigo_item varchar(10),
    cantidad int,
    primary key(modelo, codigo_item),
    foreign key(modelo) references producto(nodelo),
    foreign key(codigo_item) references item(codigo_item)
);

