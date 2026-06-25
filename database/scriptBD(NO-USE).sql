//Este script lo puse aca como guia de la bd
/*use gimnasio;

show columns from USUARIO;
select * from USUARIO;
INSERT INTO USUARIO VALUES
(9638661, 'DANIEL RODRIGUEZ ROCA', '69161451', 'dr520878@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','M'), -- C
(1052486, 'LEANDRO ALVAREZ RODRIGUEZ', '68806043', 'leandro.ar2003@gmail.com', TRUE, 1, FALSE, FALSE, '2004-10-09','M'), -- C
(8967988, 'GABRIELA TOMICHA PEREZ', '69139278', 'gabriela.3849@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','F'), -- C
(5489761, 'PABLO CAMACHO VÁSQUEZ', '78956321', 'pablocamacho.54@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','M'), -- C
(9845620, 'VERONICA LANZA CABRERA', '69124781', 'vero_lanza_c9845@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','F'), -- C
(6587412, 'ALVARO DIEGO RODRIGUEZ CASTEDO', '78952103', 'alvaro.diego87_rodriguez@gmail.com',TRUE, FALSE, FALSE, FALSE, '2004-10-09','M'), -- C
(8945126, 'YERLIN SAMEJA YABETA', '78951235', 'Sameja_yabeta987456@gmail.com',0, 1, FALSE, FALSE, '2004-10-09','F'), -- I
(9456231, 'RODRIGO ROCHA ORTIZ', '65214878', 'rodrigorocha_rod@gmail.com',0, 1, FALSE, FALSE, '2004-10-09','M'), -- I  
(7896259, 'JUNIOR HURTADO FLORES', '78549565', 'junior_hurtado874569212@gmail.com',0, 1, FALSE, FALSE, '2004-10-09','M'), -- I
(9862513, 'RAUL RODRIGUEZ RIVERO', '73265410', 'rodriguezrivero.ar5498@gmail.com',0, 1, FALSE, FALSE, '2004-10-09','M'), -- I
(6845120, 'LUIS FERNANDO GUASICO DOLEA', '65498787', 'lfgd.luis6549@gmail.com',0, 1, FALSE, FALSE, '2004-10-09','M'), -- I
(5789456, 'ELENA MENACHO PEREZ', '78456256', 'elena_menacho.em782@gmail.com',0, FALSE, FALSE, 1, '2004-10-09','F'), -- A
(8956321, 'JOSE CORRALES HINOJOSA', '75632524', 'luisito_corraleshinojosa@gmail.com',0, FALSE, FALSE, 1, '2004-10-09','M'), -- A
(9895412, 'MARIA RENE CESPEDES CANDIA', '65987413', 'maria_rene_cespedes875@gmail.com',0, FALSE, FALSE, 1, '2004-10-09','F'), -- A
(1234567, 'CARLA SUÁREZ GÓMEZ', '70123456', 'carlasuarez@gmail.com',0, FALSE, 1, FALSE, '2004-10-09','F'); -- N
delete from USUARIO where ID!=1234;

INSERT INTO CLIENTE VALUES
(9638661,'PREMIUM-ANUAL',null,null),
(1052486,'PREMIUM-ANUAL',null,null),
(8967988,'PREMIUM-ANUAL',null,null),
(5489761,'PREMIUM-ANUAL',null,null),
(9845620,'NA',null,null),
(6587412,'NA',null,null);

INSERT INTO ADMINISTRATIVO VALUES
(5789456, 'RECEPCIONISTA','MAÑANA'),
(8956321, 'RECEPCIONISTA','TARDE'),
(9895412, 'RECEPCIONISTA','NOCHE');

INSERT INTO SUSCRIPCION (membresia, plan, descripcion, precio) VALUES
-- Membresía Premium
('Premium', 'Diario', 'Acceso a 5 disciplinas', 15.00),
('Premium', 'Mensual', 'Acceso a 5 disciplinas', 120.00),
('Premium', 'Semestral', 'Acceso a 5 disciplinas', 650.00),
('Premium', 'Anual', 'Acceso a 5 disciplinas', 1200.00),

-- Membresía Estándar
('Estándar', 'Diario', 'Acceso a 2 disciplinas', 10.00),
('Estándar', 'Mensual', 'Acceso a 2 disciplinas', 80.00),
('Estándar', 'Semestral', 'Acceso a 2 disciplinas', 450.00),
('Estándar', 'Anual', 'Acceso a 2 disciplinas', 850.00),

-- Membresía Básica
('Básica', 'Diario', 'Acceso solo a aparatos', 5.00),
('Básica', 'Mensual', 'Acceso solo a aparatos', 50.00),
('Básica', 'Semestral', 'Acceso solo a aparatos', 250.00),
('Básica', 'Anual', 'Acceso solo a aparatos', 450.00);

INSERT INTO PROMOCIONES (ID, Nombre, Tipo, Valor, Estado, Fecha_ini, Fecha_fin, Descripcion) VALUES
(1001, 'Promoción Verano', 'Descuento', 15.00, 'A', '2024-06-01', '2024-08-31', 'Descuento del 15% en todos los planes de membresías por la temporada de verano'),
(1002, 'Black Friday', 'Descuento', 50.00, 'A', '2024-11-25', '2024-12-01', 'Descuento del 50% en la compra de membresías mensuales durante Black Friday');

select * from PROMOCIONES;

show columns from PAGO;
select * from PAGO;
INSERT INTO PAGO VALUES
(2,'T', '2024-07-01', 102.00, 9638661, 5789456, 7, 1001),
(3,'E', '2024-08-10', 850.00, 9638661, 8956321, 9, NULL),
(4,'T', '2024-11-28', 25.00, 8967988, 9895412, 5, 1002),
(5,'T', '2024-10-15', 1200.00, 5489761, 5789456, 3, NULL),
(6,'E', '2024-06-15', 382.50, 9845620, 8956321, 1, 1001),
(7,'E', '2024-09-05', 5.00, 6587412, 9895412, 2, NULL);

INSERT INTO PERFIL (Estado, Tipo, Contrasena, UsuarioID, AdminID) VALUES 
('A', 'C', '15645959', 9638661,5789456),-- C
('A', 'C', '13700836', 1052486,8956321),-- C
('A', 'C', '14191910', 8967988,8956321),-- C
('A', 'C', '18647324', 5489761,8956321),-- C
('A', 'C', '45982167', 9845620,9895412),-- C
('A', 'C', '23458726', 6587412,9895412),-- C
('A', 'I', '21482347', 8945126,8956321),
('A', 'I', '98742614', 9456231,9895412),
('A', 'I', '24875135', 7896259,5789456),
('A', 'I', '75846921', 9862513,5789456),
('A', 'I', '24568725', 6845120,8956321),
('A', 'A', '31025492', 5789456,8956321),
('A', 'A', '35045065', 8956321,5789456),
('A', 'A', '60058460', 9895412,5789456),
('A', 'N', '18746942', 1234567,8956321);*/

INSERT INTO USUARIO (CI,Nombre,Telefono,Correo,RolC,RolI,RolN,RolA,Fecha_Nacimiento,Sexo) VALUES 
(9638661, 'DANIEL RODRIGUEZ ROCA', '69161451', 'dr520878@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','M'), -- C
(1052486, 'LEANDRO ALVAREZ RODRIGUEZ', '68806043', 'leandro.ar2003@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','M'), -- C
(8967988, 'GABRIELA TOMICHA PEREZ', '69139278', 'gabriela.3849@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','F'), -- C
(5489761, 'PABLO CAMACHO VÁSQUEZ', '78956321', 'pablocamacho.54@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','M'), -- C
(9845620, 'VERONICA LANZA CABRERA', '69124781', 'vero_lanza_c9845@gmail.com', TRUE, FALSE, FALSE, FALSE, '2004-10-09','F'), -- C
(6587412, 'ALVARO DIEGO RODRIGUEZ CASTEDO', '78952103', 'alvaro.diego87_rodriguez@gmail.com',TRUE, FALSE, FALSE, FALSE, '2004-10-09','M'), -- C
(8945126, 'YERLIN SAMEJA YABETA', '78951235', 'Sameja_yabeta987456@gmail.com',FALSE, TRUE, FALSE, FALSE, '2004-10-09','F'), -- I
(9456231, 'RODRIGO ROCHA ORTIZ', '65214878', 'rodrigorocha_rod@gmail.com',FALSE, TRUE, FALSE, FALSE, '2004-10-09','M'), -- I  
(7896259, 'JUNIOR HURTADO FLORES', '78549565', 'junior_hurtado874569212@gmail.com',FALSE, TRUE, FALSE, FALSE, '2004-10-09','M'), -- I
(9862513, 'RAUL RODRIGUEZ RIVERO', '73265410', 'rodriguezrivero.ar5498@gmail.com',FALSE, TRUE, FALSE, FALSE, '2004-10-09','M'), -- I
(6845120, 'LUIS FERNANDO GUASICO DOLEA', '65498787', 'lfgd.luis6549@gmail.com',FALSE, TRUE, FALSE, FALSE, '2004-10-09','M'), -- I
(5789456, 'ELENA MENACHO PEREZ', '78456256', 'elena_menacho.em782@gmail.com',FALSE, FALSE, FALSE, TRUE, '2004-10-09','F'), -- A
(8956321, 'JOSE CORRALES HINOJOSA', '75632524', 'luisito_corraleshinojosa@gmail.com',FALSE, FALSE, FALSE, TRUE, '2004-10-09','M'), -- A
(9895412, 'MARIA RENE CESPEDES CANDIA', '65987413', 'maria_rene_cespedes875@gmail.com',FALSE, FALSE, FALSE, TRUE, '2004-10-09','F'), -- A
(1234567, 'CARLA SUÁREZ GÓMEZ', '70123456', 'carlasuarez@gmail.com',FALSE, FALSE, TRUE, FALSE, '2004-10-09','F'); -- N


INSERT INTO ADMINISTRATIVO VALUES
(20012, 'RECEPCIONISTA','MANANA'),
(20013, 'RECEPCIONISTA','TARDE'),
(20014, 'RECEPCIONISTA','NOCHE');

INSERT INTO CLIENTE VALUES
(20001,null,null,null),
(20002,null,null,null),
(20003,null,null,null),
(20004,null,null,null),
(20005,null,null,null),
(20006,null,null,null);

INSERT INTO NUTRICIONISTA VALUES 
(20015, 'Lunes a Viernes 08:00 - 16:00');

INSERT INTO antecedentes(ID,ClienteID, NutricionistaID, Fecha, Fecha_Prox_Consulta, Diagnostico, Recomendaciones,Objetivo,Peso,Altura,IMC,GC,MM)
VALUES
(10,20001, 20015, '2024-09-20', '2024-10-20', 'Historial médico: Ninguna enfermedad crónica.', 'Recomendación: Continuar con una dieta balanceada.','Adelgasar', 70.5, 1.75, 23.0, 15.0, 55.0),
(11,20002, 20015, '2024-09-20', '2024-11-20', 'Historial médico: Antecedentes de hipertensión.', 'Recomendación: Reducir el consumo de sal y grasas saturadas.', 'Subir de peso',82.3, 1.80, 25.4, 18.0, 65.0),
(12,20003, 20015, '2024-09-20', '2024-12-20', 'Historial médico: Alergia a mariscos.', 'Recomendación: Incluir más fuentes de proteína vegetal.', 'Tonificar',120.0, 1.78, 37.9, 30.0, 80.0),
(13,20004, 20015, '2024-09-20', '2024-10-20', 'Historial médico: Ninguna enfermedad crónica.', 'Recomendación: Continuar con entrenamiento de fuerza.', 'Aumentar masa mmuscular',120.0, 1.78, 37.9, 30.0, 80.0),
(14,20005, 20015, '2024-09-20', '2024-11-20', 'Historial médico: Diabetes tipo 2.', 'Recomendación: Seguir una dieta baja en carbohidratos.', 'Adelgasar',82.3, 1.80, 25.4, 18.0, 65.0),
(15,20006, 20015, '2024-09-20', '2024-12-20', 'Historial médico: Ninguna enfermedad relevante.', 'Recomendación: Aumentar ejercicios aeróbicos en su rutina.', 'Adelgasar',70.5, 1.75, 23.0, 15.0, 55.0);

INSERT INTO INSTRUCTOR VALUES
(20007, 'BALLET FIT'),
(20008, 'CROSSFIT'),
(20009, 'CROSS TRAINING'),
(20010, 'CALISTENIA/BOXEO'),
(20011, 'FUNCIONAL');

INSERT INTO PERFIL (Estado, Tipo, Contrasena, UsuarioID, AdminID) VALUES 
('A', 'C', '15645959', 20001,20012),
('A', 'C', '13700836', 20002,20013),
('A', 'C', '14191910', 20003,20013),
('A', 'C', '18647324', 20004,20013),
('A', 'C', '45982167', 20005,20014),
('A', 'C', '23458726', 20006,20014),
('A', 'I', '21482347', 20007,20013),
('A', 'I', '98742614', 20008,20014),
('A', 'I', '24875135', 20009,20012),
('A', 'I', '75846921', 20010,20012),
('A', 'I', '24568725', 20011,20013),
('A', 'A', '31025492', 20012,20013),
('A', 'A', '35045065', 20013,20012),
('A', 'A', '60058460', 20014,20012),
('A', 'N', '18746942', 20015,20013);

INSERT INTO RUTINA (Nombre,Descripcion)VALUES -- desde el 100
('Rutina Fuerza', 'Entrenamiento enfocado en ejercicios compuestos con barra para mejorar la fuerza'),
('Rutina Volumen', 'Rutina para aumento de masa muscular con foco en la hipertrofia'),
('Rutina Definición', 'Entrenamiento para mejorar la definición muscular y perder grasa'),
('Rutina Funcional', 'Ejercicios basados en movimientos funcionales para mejorar la movilidad y estabilidad');

-- Insertar ejercicios en la tabla EJERCICIOS
INSERT INTO EJERCICIOS (Nombre, Descripcion) VALUES -- desde el 500
('Press Banca', 'Ejercicio para el pecho realizado en banco plano con barra.'),
('Sentadilla', 'Ejercicio para las piernas realizado en una posición de cuclillas.'),
('Peso Muerto', 'Ejercicio de levantamiento de pesas desde el suelo.'),
('Dominadas', 'Ejercicio de tracción en barra para fortalecer la espalda y los bíceps.'),
('Fondos', 'Ejercicio de empuje en paralelas para trabajar pecho y tríceps.'),
('Press Militar', 'Ejercicio de empuje vertical con barra para trabajar hombros.'),
('Peso Muerto Rumano', 'Variación del peso muerto enfocada en los isquiotibiales y glúteos.'),
('Remo con Barra', 'Ejercicio de tracción para la espalda con barra.'),
('Curl Bíceps con Barra', 'Ejercicio de aislamiento para bíceps con barra.'),
('Tríceps en Polea', 'Ejercicio para tríceps realizado en una máquina de poleas.'),
('Curl Bíceps con Mancuernas', 'Ejercicio de aislamiento para bíceps realizado con mancuernas.');  

-- Lunes - Fuerza
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES -- desde el 6000
('Lunes', '5', '5', '100', 100, 500),  -- Press Banca
('Lunes', '5', '5', '120', 100, 501),  -- Sentadilla
('Lunes', '5', '5', '150', 100, 502),  -- Peso Muerto
('Lunes', '5', '4', '70', 100, 503),   -- Dominadas
('Lunes', '8', '3', '40', 100, 504);   -- Fondos

-- Martes - Fuerza
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Martes', '5', '5', '110', 100, 505),  -- Press Militar
('Martes', '5', '5', '120', 100, 506),  -- Peso Muerto Rumano
('Martes', '5', '5', '100', 100, 507),  -- Remo con Barra
('Martes', '6', '4', '60', 100, 508),  -- Curl Bíceps con Barra
('Martes', '6', '3', '50', 100, 509);  -- Tríceps en Polea

-- Miércoles - Fuerza
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Miércoles', '5', '5', '105', 100, 500),  -- Press Banca
('Miércoles', '5', '5', '125', 100, 501),  -- Sentadilla
('Miércoles', '5', '5', '155', 100, 502),  -- Peso Muerto
('Miércoles', '5', '4', '75', 100, 503),   -- Dominadas
('Miércoles', '8', '3', '45', 100, 504);   -- Fondos

-- Jueves - Fuerza
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Jueves', '5', '5', '110', 100, 505),  -- Press Militar
('Jueves', '5', '5', '130', 100, 506),  -- Peso Muerto Rumano
('Jueves', '5', '5', '110', 100, 507),  -- Remo con Barra
('Jueves', '6', '4', '65', 100, 508),  -- Curl Bíceps con Barra
('Jueves', '6', '3', '55', 100, 509);  -- Tríceps en Polea

-- Viernes - Fuerza
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Viernes', '5', '5', '110', 100, 500),  -- Press Banca
('Viernes', '5', '5', '130', 100, 501),  -- Sentadilla
('Viernes', '5', '5', '160', 100, 502),  -- Peso Muerto
('Viernes', '5', '4', '80', 100, 503),   -- Dominadas
('Viernes', '8', '3', '50', 100, 504);   -- Fondos

-- Lunes - Volumen
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Lunes', '10', '4', '80', 101, 500),  -- Press Banca
('Lunes', '10', '4', '90', 101, 501),  -- Sentadilla
('Lunes', '10', '4', '120', 101, 502), -- Peso Muerto
('Lunes', '12', '4', '50', 101, 503),  -- Dominadas
('Lunes', '12', '4', '30', 101, 504);  -- Fondos

-- Martes - Volumen
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Martes', '10', '4', '60', 101, 505),  -- Press Militar
('Martes', '10', '4', '80', 101, 506),  -- Peso Muerto Rumano
('Martes', '10', '4', '70', 101, 507),  -- Remo con Barra
('Martes', '12', '4', '35', 101, 508), -- Curl Bíceps con Barra
('Martes', '12', '4', '25', 101, 509); -- Tríceps en Polea

-- Miércoles - Volumen
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Miércoles', '10', '4', '85', 101, 500),  -- Press Banca
('Miércoles', '10', '4', '95', 101, 501),  -- Sentadilla
('Miércoles', '10', '4', '125', 101, 502), -- Peso Muerto
('Miércoles', '12', '4', '55', 101, 503),  -- Dominadas
('Miércoles', '12', '4', '35', 101, 504);  -- Fondos

-- Jueves - Volumen
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Jueves', '10', '4', '65', 101, 505),  -- Press Militar
('Jueves', '10', '4', '85', 101, 506),  -- Peso Muerto Rumano
('Jueves', '10', '4', '75', 101, 507),  -- Remo con Barra
('Jueves', '12', '4', '40', 101, 508), -- Curl Bíceps con Barra
('Jueves', '12', '4', '30', 101, 509); -- Tríceps en Polea

-- Viernes - Volumen
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Viernes', '10', '4', '90', 101, 500),  -- Press Banca
('Viernes', '10', '4', '100', 101, 501), -- Sentadilla
('Viernes', '10', '4', '130', 101, 502), -- Peso Muerto
('Viernes', '12', '4', '60', 101, 503),  -- Dominadas
('Viernes', '12', '4', '40', 101, 504);  -- Fondos

-- Lunes - Definición
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Lunes', '15', '4', '60', 102, 500),  -- Press Banca
('Lunes', '15', '4', '70', 102, 501),  -- Sentadilla
('Lunes', '15', '4', '90', 102, 502),  -- Peso Muerto
('Lunes', '15', '3', '40', 102, 503),  -- Dominadas
('Lunes', '20', '3', '20', 102, 504);  -- Fondos

-- Martes - Definición
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Martes', '15', '4', '40', 102, 505),  -- Press Militar
('Martes', '15', '4', '60', 102, 506),  -- Peso Muerto Rumano
('Martes', '15', '4', '50', 102, 507),  -- Remo con Barra
('Martes', '20', '3', '25', 102, 508), -- Curl Bíceps con Barra
('Martes', '20', '3', '15', 102, 509); -- Tríceps en Polea

-- Miércoles - Definición
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Miércoles', '15', '4', '65', 102, 500),  -- Press Banca
('Miércoles', '15', '4', '75', 102, 501),  -- Sentadilla
('Miércoles', '15', '4', '95', 102, 502),  -- Peso Muerto
('Miércoles', '15', '3', '45', 102, 503),  -- Dominadas
('Miércoles', '20', '3', '25', 102, 504);  -- Fondos

-- Jueves - Definición
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Jueves', '15', '4', '45', 102, 505),  -- Press Militar
('Jueves', '15', '4', '65', 102, 506),  -- Peso Muerto Rumano
('Jueves', '15', '4', '55', 102, 507),  -- Remo con Barra
('Jueves', '20', '3', '30', 102, 508), -- Curl Bíceps con Barra
('Jueves', '20', '3', '20', 102, 509); -- Tríceps en Polea

-- Viernes - Definición
INSERT INTO DETALLE_RUTINA (Dia, Repeticiones, Serie, Peso, RutinaID, EjerciciosID) VALUES
('Viernes', '15', '4', '70', 102, 500),  -- Press Banca
('Viernes', '15', '4', '80', 102, 501),  -- Sentadilla
('Viernes', '15', '4', '100', 102, 502), -- Peso Muerto
('Viernes', '15', '3', '50', 102, 503),  -- Dominadas
('Viernes', '20', '3', '30', 102, 504);  -- Fondos

INSERT INTO SEGUIMIENTO (Fecha, Observaciones, Objetivo,Fecha_Prox_Consulta, ClienteID, InstructorID, RutinaID) -- desde el 1500
VALUES
('2024-09-01', 'Va por buen camino','Adelgasar', '2024-10-01',20001, 20007, 100),
('2024-09-05', 'Sin dificultad alguna','Aumentar masa muscular', '2024-10-05',20002, 20008, 101),
('2024-09-12', 'No le tiene miedo a nada','Mejorar resistencia', '2024-10-12',20004, 20008, 102);

INSERT INTO PROMOCIONES (Nombre, Tipo, Valor, Estado, Fecha_ini, Fecha_fin, Descripcion) VALUES -- desde el 10000
('Promoción Verano', 'Descuento', 15.00, 'A', '2024-06-01', '2024-08-31', 'Descuento del 15% en todos los planes de membresías por la temporada de verano'),
('Black Friday', 'Descuento', 50.00, 'A', '2024-11-25', '2024-12-01', 'Descuento del 50% en la compra de membresías mensuales durante Black Friday');

INSERT INTO SUSCRIPCION (membresia, plan, descripcion, precio) VALUES -- desde 1
-- Membresía Premium
('Premium', 'Diario', 'Acceso a 5 disciplinas', 15.00),
('Premium', 'Mensual', 'Acceso a 5 disciplinas', 120.00),
('Premium', 'Semestral', 'Acceso a 5 disciplinas', 650.00),
('Premium', 'Anual', 'Acceso a 5 disciplinas', 1200.00),

-- Membresía Estándar
('Estándar', 'Diario', 'Acceso a 2 disciplinas', 10.00),
('Estándar', 'Mensual', 'Acceso a 2 disciplinas', 80.00),
('Estándar', 'Semestral', 'Acceso a 2 disciplinas', 450.00),
('Estándar', 'Anual', 'Acceso a 2 disciplinas', 850.00),

-- Membresía Básica
('Básica', 'Diario', 'Acceso solo a aparatos', 5.00),
('Básica', 'Mensual', 'Acceso solo a aparatos', 50.00),
('Básica', 'Semestral', 'Acceso solo a aparatos', 250.00),
('Básica', 'Anual', 'Acceso solo a aparatos', 450.00);

INSERT INTO PAGO (Metodo_de_pago, Fecha, Monto_total, ClienteID, AdministradorID, SuscripcionID, PromocionesID) VALUES -- desde 50000
-- Pago con membresía Premium Mensual y Promoción de Verano
('T', '2024-07-01', 102.00, 20001, 20012, 2, 10000),

-- Pago con membresía Estándar Anual sin promoción
('E', '2024-08-10', 850.00, 20002, 20013, 8, NULL),

-- Pago con membresía Básica Mensual con Promoción de Black Friday
('T', '2024-11-28', 25.00, 20003, 20014, 10, 10001),

-- Pago con membresía Premium Anual sin promoción
('D', '2024-10-15', 1200.00, 20004, 20012, 4, NULL),

-- Pago con membresía Estándar Semestral y Promoción de Verano
('E', '2024-06-15', 382.50, 20005, 20013, 7, 10000),

-- Pago con membresía Básica Diario sin promoción
('D', '2024-09-05', 5.00, 20006, 20014, 9, NULL);

INSERT INTO COMPROBANTE (Monto, Fecha_ini_mem, fecha_fin_mem, PagoID, ClienteID) VALUES -- desde 7000
-- Comprobante para pago de membresía Premium Mensual con promoción de verano
(102.00, '2024-07-01', '2024-08-01', 50000, 20001),

-- Comprobante para pago de membresía Estándar Anual sin promoción
(850.00, '2024-08-10', '2025-08-10', 50001, 20002),

-- Comprobante para pago de membresía Básica Mensual con promoción de Black Friday
(25.00, '2024-11-28', '2024-12-28', 50002, 20003),

-- Comprobante para pago de membresía Premium Anual sin promoción
(1200.00, '2024-10-15', '2025-10-15', 50003, 20004),

-- Comprobante para pago de membresía Estándar Semestral con promoción de verano
(382.50, '2024-06-15', '2024-12-15', 50004, 20005),

-- Comprobante para pago de membresía Básica Diario sin promoción
(5.00, '2024-09-05', '2024-09-05', 50005, 20006);

INSERT INTO SALA (Descripcion, Capacidad) VALUES -- desde el 1 
('Sala 1', 30),
('Sala 2', 20),
('Sala 3', 40);

INSERT INTO DISCIPLINA (Nombre, Grupo, Cupo, SalaID) VALUES
('Yoga', 1, 30, 1),
('Zumba', 3, 40, 3),
('Crossfit', 4, 20, 2),
('Kickboxing', 5, 30, 1),
('Spinning', 6, 20, 2),
('Boxeo', 8, 40, 3);

INSERT INTO HORARIO (Dia, Hora_Inicial, Hora_Final, DisciplinaID) VALUES
('Lunes', '08:00:00', '09:00:00', 2001),
('Lunes', '09:00:00', '10:00:00', 2002),
('Lunes', '10:00:00', '11:00:00', 2003),
('Martes', '08:00:00', '09:00:00', 2001),
('Martes', '09:00:00', '10:00:00', 2002),
('Martes', '10:00:00', '11:00:00', 2003),
('Miércoles', '08:00:00', '09:00:00', 2001),
('Miércoles', '09:00:00', '10:00:00', 2002),
('Miércoles', '10:00:00', '11:00:00', 2003),
('Jueves', '08:00:00', '09:00:00', 2001),
('Jueves', '09:00:00', '10:00:00', 2002),
('Jueves', '10:00:00', '11:00:00', 2003),
('Viernes', '08:00:00', '09:00:00', 2001),
('Viernes', '09:00:00', '10:00:00', 2002),
('Viernes', '10:00:00', '11:00:00', 2003);

INSERT INTO HORARIO (Dia, Hora_Inicial, Hora_Final, DisciplinaID) VALUES -- desde 15000
('Lunes', '11:00:00', '12:00:00', 2004),
('Lunes', '12:00:00', '13:00:00', 2005),
('Lunes', '13:00:00', '14:00:00', 2006),
('Martes', '11:00:00', '12:00:00', 2004),
('Martes', '12:00:00', '13:00:00', 2005),
('Martes', '13:00:00', '14:00:00', 2006),
('Miércoles', '11:00:00', '12:00:00', 2004),
('Miércoles', '12:00:00', '13:00:00', 2005),
('Miércoles', '13:00:00', '14:00:00', 2006),
('Jueves', '11:00:00', '12:00:00', 2004),
('Jueves', '12:00:00', '13:00:00', 2005),
('Jueves', '13:00:00', '14:00:00', 2006),
('Viernes', '11:00:00', '12:00:00', 2004),
('Viernes', '12:00:00', '13:00:00', 2005),
('Viernes', '13:00:00', '14:00:00', 2006);

INSERT INTO RESERVA (Fecha, Estado, ClienteID, DisciplinaID, ComprobanteID)VALUES -- desde 800
('2024-09-05', 'A', 20003, 2006, 7002);



