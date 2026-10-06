import json
import statistics as _st
from jinja2 import Template
from datetime import datetime

# ── External institutions data (CEAC Mayo 2026, TMS Diciembre 2025) ──────────
_CEAC_RAW = [
    ("Aedo Rivas Rodrigo Eduardo","Generalista de Personas",1_600_000),
    ("Álvarez Gómez Carlos Andrés","Utilero Tramoya",1_166_257),
    ("Angel Tejos Sebastián Andrés","Técnico Iluminación",1_113_360),
    ("Antican Quiroz Fanny Denisse","Estafeta",1_056_639),
    ("Arenas Arce Lía Gabriela","Coordinación y Prod. Artística",1_664_988),
    ("Arévalo Pascual Waldo Ilich","Encargado de Sonido y Video",1_627_323),
    ("Barría Gutiérrez Margarita Rosa","Asistente de Dirección",2_181_822),
    ("Berríos Pérez Miguel Angel","Coordinador Orquesta",2_356_911),
    ("Bustos Estrada Rodrigo Iván","Productor General",1_900_000),
    ("Callejas Bustos Ana Carolina","Encargada de Comunicaciones Estratégicas",2_400_000),
    ("Canobra Gatica Francisco Eduardo","Analista de Personal",1_250_000),
    ("Cartes Alvarado Ítalo Alejandro","Utilero Archivo Musical",1_484_004),
    ("Castro Moncada Carlos Benjamín","Utilero Orquesta",1_282_564),
    ("Cifuentes Umaña Ricardo","Masoterapeuta",982_442),
    ("Contreras Ovando Cristian Fredy","Coordinador BANCH",2_611_151),
    ("Díaz Oyarce Sergio Alejandro","Utilero Tramoya",927_240),
    ("Figueroa Cantillana Nicolás","Encargado Comercial y Fundraising",2_585_000),
    ("Figueroa Lizana Loreto Andrea","Analista de Proyectos",1_500_000),
    ("Folch Almarza Antonia Isabella","Community Manager – Com. y Marketing",1_185_000),
    ("Fuentes Pinto Regina","Boletería",1_189_688),
    ("Gallardo Bustamante Natalia A.","Diseñador Gráfico",1_233_132),
    ("Gallardo Valdes Rodrigo Alejandro","Portero",851_488),
    ("Herrera Caniato Patricia Valeria","Coordinadora Coro",1_995_101),
    ("Hoffmann Muñoz Felipe","Prevencionista de Riesgo",1_508_896),
    ("Huaiquimil Retamal Noemí Betsabé","Encargada de Presupuesto",2_784_743),
    ("Ibáñez Gomien María Amelia","Encargada Área Educación Mediación",1_900_000),
    ("Jiménez Cayumán Aníbal Gabriel","Sonidista",1_464_986),
    ("Liberczuk Cinthia","Encargada Técnico",2_520_084),
    ("Madrid Guzmán Paola Francisca","Boletería",653_074),
    ("Medina Cañete Luis Alejandro","Auxiliar de Servicios Estafeta",874_898),
    ("Melo Araya Jessica Susana","Encargada de Compras",1_842_375),
    ("Moraga Espinoza Roberto O.","Portero",931_670),
    ("Morán Valenzuela Antonio Alberto","Utilero Tramoya",1_005_426),
    ("Obregón Gutiérrez Fronda Perla","Auxiliar de Servicios",905_880),
    ("Pacheco Sandoval Daniela Jesús","Técnico Sonido y Video",551_658),
    ("Pardo Oliva Claudio Rolando","Auxiliar de Servicios",1_072_581),
    ("Pérez Ramos Felipe Eugenio","Encargado Iluminación",1_609_706),
    ("Plaza Olivos Jaime Andrés","Utilero Orquesta",993_555),
    ("Ramos Lopez Marcelo Alejandro","Utilero Orquesta",936_556),
    ("Reyes González Ramón Ignacio","Analista Comercial",1_500_000),
    ("Reyes Madriaza Cecilia Trinidad","Coordinación General y Artística",3_166_241),
    ("Rojas Lizama Lucía Emperatriz","Encargada de Personal y RRHH",1_931_488),
    ("Rojas Ramírez Valentina Alejandra","Asistente de Personas",1_060_534),
    ("Segura Espinoza Nelson Octavio","Técnico Iluminación",1_056_571),
    ("Sepúlveda Vilches César Antonio","Coordinador de Plataformas Digitales",1_903_917),
    ("Springinsfeld Rodríguez Priscilla","Encargada de Comunicaciones",2_268_424),
    ("Torrealba Concha Johana M.","Analista Contable",728_430),
    ("Triviño Hernández Sergio Iván","Nochero",825_132),
    ("Trujillo Varas Héctor Iván","Afinador de Piano",770_313),
    ("Uribe Villa Jacqueline","Audiovisual – Com. y Marketing",1_352_804),
    ("Valdés Mateu Gerardo Andrés","Utilero Tramoya",1_045_690),
    ("Vergara Llagostera Carolina Andrea","Vestuarista",1_219_199),
    ("Vergara Manubens Alejandra Alicia","Administrador",2_261_917),
    ("Vergara Manubens Marcial Enrique","Diseñador Gráfico",2_071_601),
    ("Villarroel Machuca Cecilia Elvira","Auxiliar de Servicios",783_325),
    ("Villarroel Pérez Marcelo Andrés","Asistente de Compras",121_405),
    ("Vizcaíno Arismendi Constanza","Kinesiólogo",832_493),
]

_TMS_RAW = [
    ("Abukhowsk Aleksandr","Concertino","Orquesta",1_684_534),
    ("Acuña Zapata Vania","Inspectora Escuela de Ballet","Escuela Ballet",893_000),
    ("Adebhanslung Bering Kamilia","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Aguayo Correa Macarena","Copista Digital – Archivo Musical","Administración Orquesta",1_863_440),
    ("Aguilar Guila Constanza","Coordinadora Escuela de Ballet","Escuela Ballet",1_853_631),
    ("Aguilera Muñoz Miriam","Jefa de Servicios Generales","Servicios Generales",2_742_000),
    ("Agüero García Ramiro","Oficial Bienestar y Desarrollo Org.","Personal y Remuneraciones",2_415_402),
    ("Ahumada Navarri Pablo","Concertmaster","Orquesta",1_963_232),
    ("Alarcón Lucas","Primera Bailarina","Ballet",2_521_001),
    ("Aldunate Jerez Luis","Portería e Informaciones","Portería e Informaciones",744_028),
    ("Aliaga Herrera Jonathan","Tramoyero","Tramoya",1_759_670),
    ("Almeida de Castro Luiza","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Alvarado Carlos René","Cuerpo de Baile 3","Ballet",1_087_101),
    ("Alvarado Jacob Jovanni","Cuerpo de Baile 3","Ballet",1_087_101),
    ("Alvarado Madrid Susana","Encargada Comercial","Ventas Boletería",1_863_440),
    ("Alvarado Jiménez Benjamin","Pianista Escuela de Ballet","Escuela Ballet",1_823_608),
    ("Alvarez Sepúlveda Patricio","Cantante Coro","Coro",1_844_291),
    ("Ansaur Flores Claudio","Asistente Contable","Contabilidad y Control de Gestión",1_913_113),
    ("Angulo Macías Viviana","Tutti Dir. Viento","Orquesta",2_063_945),
    ("Apablaza Sepulveda Ana","Apoyo","Librería",319_100),
    ("Apolaza Acevedo Verónica","Asistente de Producción","Difusión",2_427_331),
    ("Arce Muñoz Natalia","Archivo Musical Ballet","Administración Ballet",862_855),
    ("Aracena Morette Carlos","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Araneda Filippi","Primera Bailarina","Ballet",2_521_001),
    ("Araniva Aytica Evelyn","Sub-Directora de Comunicaciones","Prensa",3_343_378),
    ("Araya Ithanwalee France","Tramoyero","Tramoya",1_201_305),
    ("Anaya Pereira Gonzalo","Cantante Coro","Coro",1_375_969),
    ("Arcig Herrera Christian","Portería e Informaciones","Portería e Informaciones",744_028),
    ("Arellano Macpaca Mauricio","Portería Boletería","Boletería",2_489_377),
    ("Armengol Barboza Rodrigo","Asistente Dir. Tramoya II","Tramoya",1_931_100),
    ("Artiuello Sánchez Rodrigo","Gerente General","Gerencia General",6_087_300),
    ("Augustilloloi Marri Anne","Tutti Dir. Violín","Orquesta",2_063_945),
    ("Baeza Rico Sebastian","Oboe Orquesta","Orquesta",2_063_945),
    ("Barrios González Luis","Ayudante Boletería Obrero","Boletería",1_111_403),
    ("Becerra Sánchez Marina","Enlace Técnico Taller de Vestuario","Dirección Técnica",2_177_632),
    ("Benitez Soto Camila","Contrafagot","Orquesta",2_661_401),
    ("Berríos Rodríguez Roberto","Cantante Coro","Coro",370_000),
    ("Blaque Barrios Richard","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Bolas Castilla Lorena","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Bolar Álvarez Bastián","Tutti Contrabajo","Orquesta",2_063_945),
    ("Briones Ortiz Pablo","Tutti Boletería","Boletería",3_859_677),
    ("Brito Leama Carlos","Tutti Vello","Orquesta",2_063_945),
    ("Browni Garrido Carolina","Maestra de Escuela de Ballet","Escuela Ballet",1_843_978),
    ("Brown Parshlay Edward","Director Técnico","Dirección Técnica",2_163_291),
    ("Browing Lopez Andrés","Asistente Director Técnico","Dirección Técnica",2_163_291),
    ("Burgos Sepúlveda Juan","Tutti Dir. Viento","Orquesta",2_063_945),
    ("Bustos Inztroza Patricio","Tramoyero","Tramoya",1_863_202),
    ("Bustos Rivas Marco Antonio","Tramoyero","Tramoya",1_863_202),
    ("Caballero Mendoza Junior","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Caceres Parasol Eusebio","Cerro Volante","Orquesta",2_061_409),
    ("Caceres Vargas Natalia","Tramoyero","Tramoya",1_553_500),
    ("Calvo Morales Vania","Encargada Comunicaciones","Orquesta",1_111_409),
    ("Canales Vargas Juan José","Tramoyero","Tramoya",1_803_945),
    ("Cantillana Sánchez Daniel","Tramoyero","Tramoya",1_461_305),
    ("Capacitta García Miriam","Cantante Coro","Coro",1_871_600),
    ("Cárdenas Jiménez Camilo","Tramoyero","Tramoya",1_869_779),
    ("Cárdenas Lankari Sebastian","Tramoyero","Tramoya",1_863_202),
    ("Carrasco Sanchez Nicolás","Asistente Clarinete","Orquesta",2_987_466),
    ("Carvajal Pargas Giovanni","Aux. Servicios Guardiagas","Servicios Generales",1_763_098),
    ("Castillo Jara Osvaldo","Pianista Escuela de Ballet","Escuela Ballet",1_813_008),
    ("Castro Espinoza José","Cantante Coro","Coro",1_971_969),
    ("Castro González Ricardo","Gerente Nutrición","Gerencia",2_394_356),
    ("Cayugueo Croche Luis","Jefe de Portería","Portería e Informaciones",3_025_520),
    ("Cerda Martínez Claudio","Cantante Coro","Coro",1_371_969),
    ("Chamberk Karen Ella","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Conejo Alixia Nadina","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Concha del Río Carolina","Cuerpo de Baile 3","Ballet",1_087_101),
    ("Contreras Arias Javier","Trompeta","Orquesta",2_714_637),
    ("Cordero Marín Javier","Tutti Contrabajo","Orquesta",2_063_945),
    ("Córdova Campos Fernando","Auxiliar","Bodega y Compras",791_000),
    ("Córdova González Marlene","Encargada de Compras","Bodega y Compras",3_227_339),
    ("Correa Schaffrine Daniela","Mda de Producción/Coordinación Artística","Coordinación Artística",1_920_655),
    ("Crespo Faras Luciano","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Curto Ortiz Luis","Kenis OT Técnica","Dirección Técnica",1_861_295),
    ("Cuevas Rosalba Juan","Operador de Caldera","Mantención",1_884_990),
    ("Díaz Espinoza Carolina","Cuerpo de Baile 3","Ballet",1_087_101),
    ("Díaz Guzmán Jorge","Tramoyero","Tramoya",1_463_639),
    ("Díaz Martínez Eduardo","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Díaz Soto Pablo","Tramoyero","Tramoya",642_836),
    ("Díaz Yiannico Carmen","Tramoyero Dir. Orquesta","Administración Orquesta",2_869_403),
    ("Dobriva Smulieva Albena","Pianista","Ballet",2_473_660),
    ("Dosek John Tyler","Cantante Coro","Coro",1_963_221),
    ("Durán Calquín Carmen","Asistente de Recursos Humanos","Personal y Remuneraciones",1_843_978),
    ("Durán Espinosa Daniel","Tramoyero","Tramoya",1_861_305),
    ("Durán Pino Patricia","Supervisora Almacén","Ventas Boletería",2_561_842),
    ("Durán Suárez Juan","Pabellón Blando Mayor","Dirección Técnica",1_865_716),
    ("Echeverría Torres Gustavo","Primera Bailarina","Ballet",2_521_001),
    ("Elgueta Díaz Jaime","Cantante Coro","Coro",1_964_990),
    ("Enguer Peñaipa Carlos","Cantante Coro","Coro",3_153_417),
    ("Escalona Mario Ethana","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Escondido Arumada Lina","Cantante Coro","Coro",1_971_669),
    ("Espinosa Jagur Alejandra","Asistente Admin. Dirección del Ballet","Administración Ballet",2_753_645),
    ("Espinoza Espinoza Francisco","Cantante Coro","Coro",1_971_669),
    ("Espinoza Marchant Mauricio","Auxiliar Teatro Escultura","Escultura",1_863_232),
    ("Espinoza Marchant Patricio","Auxiliar Teatro Escultura","Escultura",1_863_232),
    ("Farías González Pamela","Apoyo","Taller De Vestuario",963_000),
    ("Farías Morales Cristobal","Tramoyero","Tramoya",1_263_869),
    ("Fernández Casado Karnal","Cantante Coro","Coro",870_000),
    ("Ferrán Minoya Mónica","Cantante Coro","Coro",1_971_669),
    ("Ferrer Valenzuela Macarena","Violín 2 Ayudante","Orquesta",2_062_797),
    ("Figueroa Rodett Moisés","Tramoyero","Tramoya",2_201_963),
    ("Figueroa Sáez Víctor","Tramoyero","Tramoya",1_761_533),
    ("Flores Frey Javiera","Asistente Área de Contenidos","Marketing",911_607),
    ("Flores Guisosenviro Simón","Cantante Coro","Coro",4_172_846),
    ("Flores Libornio Lorenzo","Violinchelo","Orquesta",1_319_637),
    ("Flores Wheppla Rodrigo","Tramoyero","Tramoya",2_221_509),
    ("Fonbeca Cytrus Claudia","Gran Ayudante","Orquesta",2_714_637),
    ("Fontecilla Moupin Nicolas","Cantante Coro","Coro",1_949_221),
    ("Fonzalez Carlos","Asistente de Relaciones Corporativas","Ventas Empresas",798_646),
    ("Franco Romero Eduardo","Mamonzón Tutti","Orquesta",2_063_945),
    ("Fredes Yaber Gustavo","Tramoyero","Tramoya",1_863_232),
    ("Freís Fredero Juan Luis","Portería e Informaciones","Portería e Informaciones",779_306),
    ("Fuenzalida Hunca Pablo","Tutti Contrabajo","Orquesta",2_063_947),
    ("Fuentes Torres Enzo","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Fuguien Herrera Andrea","Cuerpo de Baile 3","Ballet",1_087_101),
    ("Gablin Guerra Christian","Asistente Contable","Contabilidad y Control de Gestión",1_962_845),
    ("Garay Ruiz Yaule Isabel","Cantante Coro","Coro",1_971_969),
    ("García Navarro Constanza","Apoyo","Taller De Vestuario",763_420),
    ("García Nuñez López Gonzalo","Tutti","Orquesta",2_714_637),
    ("Garrido Pérez Juan Ramón","Auxiliar de Ases","Servicios Generales",2_363_520),
    ("Godoy Paredes Joel","Portería e Informaciones","Portería e Informaciones",744_028),
    ("Godoy Sotelo Josí","Tramoyero","Tramoya",1_863_760),
    ("Gocochiea Marcela Inés","Maestra Compañía de Ballet","Administración Ballet",2_303_008),
    ("Gómez Puentes Marisol","Oboe Orquesta","Orquesta",2_714_637),
    ("González Bustamante Carmen","Pianista Escuela de Ballet","Escuela Ballet",985_202),
    ("González Gutiérrez Tomás","Tramoyero","Tramoya",1_703_280),
    ("González Manriney Ricardo","Cantante Coro","Coro",1_971_969),
    ("González Muñoz Alfonso","Personal de Sala","Personal De Sala",829_911),
    ("González Ojeda Juan Gabriel","Tutti Viento","Orquesta",2_063_945),
    ("Guerroa Orellana Arrasini","Tutti Vello","Orquesta",2_063_945),
    ("Guevara Guzmán Oswald","Tutti Vello","Orquesta",2_063_945),
    ("Guissiana Stupanich Camila","Cantante Coro","Coro",1_971_669),
    ("Gutiérrez Dyllan Roxana","Auxiliar Teatro Escultura","Escultura",1_963_232),
    ("Gutiérrez Tayfo Cristobal","Cantante Coro","Coro",1_844_221),
    ("Gutiérrez Ángela Ana María","Ayudante","Taller De Vestuario",863_860),
    ("Guzmán García Gastón","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Guzmán Yacecin Rodrigo","Maestro de Escuela de Ballet","Escuela Ballet",1_713_001),
    ("Hernández Majilme Jorge","Auxiliar Contable","Contabilidad y Control de Gestión",1_282_846),
    ("Hernández Villar Rodrigas","Bailarina Solista","Orquesta",2_429_425),
    ("Hirmica Barraza Carlos","Mamonzón Tutti","Orquesta",2_063_947),
    ("Hermana Donoso Sandra","Secretaria","Dirección General",3_533_232),
    ("Hiva Angulo José","Pianista","Orquesta",2_063_223),
    ("Hidalgo Hernández Simón","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Hidalgo Victoria","Tramoyero Dir. Orquesta","Administración Orquesta",1_750_860),
    ("Hormanzabal Garrido José","Tramoyero","Tramoya",1_861_305),
    ("Huerto Pancosa Marco","Tramoyero","Tramoya",1_963_221),
    ("Inostroza Mona Juan","Tramoyero","Tramoya",1_362_613),
    ("Iastray Yanaklau","Percusión","Orquesta",3_859_677),
    ("Jashiona Evodinina","Baila Solista","Orquesta",3_859_677),
    ("Jara Cabernas Zara","Asistente de Tramoya","Tramoya",1_285_137),
    ("Jaquira Urra Fabiola","Asistente Comercial","Ventas Boletería",2_815_950),
    ("Jara Anabalón Enrique","Portería e Informaciones","Portería e Informaciones",862_135),
    ("Johnson Mugumel Alexis","Tramoyero","Tramoya",2_227_565),
    ("Juan Vásquez Vargas Margarita","Maestra de Escuela de Ballet","Escuela Ballet",1_823_643),
    ("Kootiminova Olia","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Korotoktko Margarita","Baila","Ballet",1_973_660),
    ("Labrador Moncaga Roderick","Balleto","Orquesta",2_063_945),
    ("Larrañas de la Fuente Carmen","Directora General","Dirección General",6_087_300),
    ("Larrau Toro Pedro","Tramoyero","Tramoya",1_375_677),
    ("Latorre Barros Fernando","Cantante Coro","Coro",1_371_969),
    ("Latorre Homero Fernando","Obrero Orquesta","Administración Orquesta",1_760_055),
    ("Latruz Bustamante Esperanza","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Leiva Cortez Manuel","Tutti Vello","Orquesta",2_063_945),
    ("Leiva Vega Pablo","Oboe 1","Orquesta",2_063_945),
    ("Lercominas Morales Magdalena","Dirección de Coordinación Artística","Coordinación Artística",3_820_937),
    ("León González Jorge","Cantante Coro","Coro",1_813_677),
    ("Lora Domínguez Alejandra","Administración Ballet","Administración Ballet",891_905),
    ("Lizama Muñoz Marcelo","Control de Entradas","Personal De Sala",823_914),
    ("Lizama Vrado Sebastián","Coros","Coro",2_061_487),
    ("López Fuentes Byron","Flute 1","Orquesta",2_063_945),
    ("López Gatiuz Maximiliano","Tutti Solistas","Ballet",2_218_439),
    ("López González Montserrat","Bailarina Solista","Ballet",2_219_649),
    ("Maulén Antilao Rodrigo","Operador de Caldera","Mantención",981_062),
    ("Maureira Pauvre Jeannette","Auxiliar de Ases","Servicios Generales",730_176),
    ("Medina Amroso Clara","Auxiliar de Ases","Servicios Generales",730_176),
    ("Medina Acevedo Oscar","Jefe Taller de Audiovisual","Gerencia",3_305_309),
    ("Medina Díaz Blah","Auxiliar de Ases","Servicios Generales",730_176),
    ("Medina Holguín Félix","Tramoyero","Tramoya",1_451_810),
    ("Meza Cerreceda Pablo","Tramoyero","Tramoya",1_861_365),
    ("Meza Gutiérrez Marcelo","Realizador Multimedia","Audiovisual",1_170_000),
    ("Meza Zuñiga Eduardo","Tramoyero","Tramoya",1_843_760),
    ("Meza Zúñiga Sofia","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Milanka Castro Javier","Coros","Coro",2_714_637),
    ("Miranka Robles Constanza","Administración Orquesta","Administración Orquesta",2_063_945),
    ("Miranda Molina María Teresa","Coordinación Ballet Solistas","Administración Ballet",2_714_637),
    ("Molina Xantandori María","Cantante Coro","Coro",1_971_969),
    ("Molinalve Espinoza Celin","Cantante Ballet","Administración Ballet",1_573_520),
    ("Montesinos Marro Macarena","Resumen de Baile y Contabilidad","Administración Ballet",1_864_316),
    ("Montenegro Fernández Fabricio","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Montenegro Montenegro Francisca","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Montero Riveros Sylva","Cantante Coro","Coro",1_975_400),
    ("Mona Balazar Carlos","Jefe Taller de Vestuario","Dirección Técnica",3_276_685),
    ("Morales Anderson César","Director Artístico Compañía de Ballet","Administración Ballet",3_760_000),
    ("Morales Becanilla Wilfredo","Portería e Informaciones","Portería e Informaciones",770_308),
    ("Morales Fernández Gustavo","Cantante Coro","Coro",1_971_669),
    ("Morales González Sergio","Tramoyero","Tramoya",1_354_610),
    ("Muñoz González María","Auxiliar Contable","Contabilidad y Control de Gestión",1_864_766),
    ("Muñoz Lares Miguel","Tramoyero","Tramoya",1_861_760),
    ("Muñoz Roto María Francisca","Cantante Coro","Coro",1_813_032),
    ("Navaira Pizueda Fernando","Asistente Admin. Orquesta","Administración Orquesta",1_803_443),
    ("Nivarros Guijares Bryam","Asistente Comercial","Ventas Boletería",2_219_649),
    ("Nicolás Misochan Debora","Coordinadora de Marca y Diseño","Marketing",1_287_295),
    ("Novalco Pérez José","Cantante Coro","Coro",1_913_832),
    ("Núñez Hidalgo María","Asistente de Bienestar","Personal y Remuneraciones",1_877_205),
    ("Nuñez Mansiones Pablo","Jefe de Vestuario y Caracterización","Dirección Técnica",3_239_306),
    ("Ochoa Yanez María","Tramoyero","Tramoya",1_823_934),
    ("Olivos Alfaro Constanza","Cantante Coro","Coro",1_813_221),
    ("Olivares Martínez Soyfe","Cantante Coro","Coro",1_971_969),
    ("Ono Jara Usemi Tomás","Gerente Audiovisual","Marketing",782_762),
    ("Orellana Alaharín Rodrigo","Tramoyero","Tramoya",1_763_654),
    ("Orellana Bravo Ángel","Portería e Informaciones","Portería e Informaciones",770_000),
    ("Orellana López Carmen","Inspectora de la Escuela de Ballet","Escuela Ballet",839_833),
    ("Ortiz Cortés Fernanda","Ayudante","Taller De Vestuario",863_000),
    ("Ortiz Espinoza Carolina","Cantante Coro","Coro",1_971_669),
    ("Ortiz Flores Sergio","Segundo Director Escenario","Escenario",2_750_000),
    ("Ortiz Romero Pablo","Cantante Coro","Coro",1_971_969),
    ("Osa Prades Joselyn","Auditor de Tesorería","Tesorería",1_864_758),
    ("Ovalle Ortigia Beatrice","Razón Drasino","Orquesta",2_587_409),
    ("Ovalle Ortigia Maria Manuel","Cantante Coro","Coro",1_971_969),
    ("Panisinoc Acueved Alexer","Apoyo","Taller De Vestuario",1_881_671),
    ("Pavez Villar Bárbara","Pianista","Administración Coro",2_369_967),
    ("Peccionla Martina","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Piluc Peña Miroslav","Maestro de Escuela de Ballet","Escuela Ballet",1_823_633),
    ("Peñaloza Hidalgo Osvaldo","Portería e Informaciones","Portería e Informaciones",862_855),
    ("Piralta Tobar Cristian","Tutti Contrabajo","Orquesta",2_063_945),
    ("Dayelin Pineda Karl","Supervisor de Producción","Dirección Técnica",2_347_305),
    ("Pérez Méndez Juan Manuel","Tramoyero","Tramoya",1_184_814),
    ("Pérez Méndez Roberto","Tramoyero Boletería","Tramoya",2_201_365),
    ("Pérez Mona Bastian","Tramoyero","Tramoya",1_087_361),
    ("Pernilla Melgardes María","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Pinto Muñoz Josip","Ayudante","Taller De Vestuario",870_300),
    ("Pinas Correda Enrique","Tramoyero","Tramoya",1_861_365),
    ("Piraro Correda Jesús","Tramoyero","Tramoya",3_237_015),
    ("Piras Piraro David","Tramoyero Orquesta","Tramoya",1_861_365),
    ("Prudencio Plano Pedro","Director de Orquesta Residente","Orquesta",4_263_439),
    ("Quezada Zorquiera Patricia","Sub Jefa de Vestuario","Taller De Vestuario",2_282_424),
    ("Ramírez Díaz Pablo","Pianista","Administración Ballet",1_861_305),
    ("Ramírez Vásquez Jennifer","Cantante Coro","Coro",1_971_969),
    ("Ramos Mata Robert","Tutti Vello","Orquesta",2_063_945),
    ("Ravanas Sauveron Álvaro","Jefe de Sistemas","Sistemas",3_213_678),
    ("Rioshuiron Bustos Martín","Tramoyero","Tramoya",1_843_780),
    ("Reyes Rodrigo Marcelo","Tramoyero","Tramoya",867_873),
    ("Royer Via Aneya Alejandro","Sub-Director de Coro","Administración Coro",2_280_600),
    ("Rodriguez Bertona Paola","Cantante Coro","Coro",1_971_969),
    ("Rodriguez Delgado Katherine","Primera Bailarina","Ballet",2_521_001),
    ("Rojas Arizmada Francisco","Jefe Articulador de Coro","Administración Coro",2_463_877),
    ("Rojas Flores David","Cantante Coro","Coro",1_913_032),
    ("Rojas Rojas Glorias Loreto","Cantante Coro","Coro",1_971_669),
    ("Roluc Fernandez Lux","Jefe de Sala","Personal De Sala",1_711_835),
    ("Romero Ledesma Tatiana","Cantante Coro","Coro",2_061_480),
    ("Romero Morales Matías","Bailarina Solista","Ballet",2_218_439),
    ("Romero González Damián","Tutti Contrabajo","Orquesta",2_063_945),
    ("Rosales Pinto Roberto","Tramoyero","Tramoya",1_861_305),
    ("Rosales Selvi Mauricio","Tramoyero","Tramoya",1_375_677),
    ("Ruiz Jofre Valentina","Coordinadora Área Comunitaria","Coordinación Artística",1_963_009),
    ("Saavedra Gerosa David","Cuerpo de Baile 3","Ballet",1_087_101),
    ("Samarth Gurola Belén","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Samata Tovar Jorge","Portería e Informaciones","Portería e Informaciones",844_028),
    ("Salazar Ramos María","Bailarina Solista","Ballet",2_219_439),
    ("Salgado Bustamante Francisco","Cantante Coro","Coro",1_843_632),
    ("Salgado Castillo José","Cantante Coro","Coro",1_971_969),
    ("Salinas Fernández Jaime","Cantante Coro","Coro",1_971_969),
    ("San Martín Palma Lady","Kinesiólogo","Contabilidad y Control de Gestión",1_864_866),
    ("San Martín Peñailillo Sebastián","Coordinador Rel. Corporativas","Ventas Empresas",1_423_500),
    ("Sandoval Yanes Maria Sol","Cantante Coro","Coro",2_063_945),
    ("Sánchez Cornejo Juan Carlos","Tesorero","Tesorería",2_769_060),
    ("Sánchez Molina María Teresa","Auxiliar de Ases","Servicios Generales",730_176),
    ("Sánchez Díaz Alexis","Cantante Coro","Coro",1_843_237),
    ("Sánchez Vidal Esteban","Dirección Técnica","Dirección Técnica",3_342_207),
    ("Sánchez Beoquin Nilén","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Sánchez Martínez Alberto","Tramoyero","Tramoya",1_987_101),
    ("Santovena Hemonques Carlos","Cantante Coro","Coro",770_176),
    ("Scanlon Sarah Rosalinda","Tutti Vello","Orquesta",2_063_945),
    ("Schindormir Oriana","Cuerpo de Baile 2","Ballet",1_087_101),
    ("Segura Valenzuela Oscar","Tramoyero","Tramoya",1_861_305),
    ("Seona Morales Galeara","Primera Bailarina","Ballet",2_507_837),
    ("Sepúlveda Gallardo Rodrigo","Prevencionista de Riesgo","Prevención De Riesgos",2_242_400),
    ("Sepúlveda Pillao Andrés","Jefe de Taller de Utilería","Utilería",3_271_803),
    ("Sermenkov Salgardo Rodrigo","Cuerpo de Baile 1","Ballet",1_963_965),
    ("Silva García Marcela","Bailarina Solista","Ballet",3_279_428),
    ("Silva Morales Ricardo","Tramoyero","Tramoya",2_063_945),
    ("Simalt Zeluvins","Fagot","Orquesta",3_869_677),
    ("Soto Fuentes Miguel","Escenógrafo Ballet","Librería",642_540),
    ("Soto Mutia Berta","Cantante Coro","Coro",1_971_969),
    ("Soto González Vintlawa","Pianista","Ballet",1_875_640),
    ("Tapia Puebla Matías","Trombone","Orquesta",3_111_401),
    ("Tolber Muila Marcu","Control de Entradas","Personal De Sala",929_911),
    ("Tomar Muñoz Miguel","Jefe Taller de Construcciones","Construcción",3_270_409),
    ("Toledo Godot Jonathan","Tramoyero","Tramoya",1_863_760),
    ("Toro Continumar José","Tramoyero","Tramoya",1_865_232),
    ("Toro Loyola Matías","Tutti Tutti","Orquesta",2_063_032),
    ("Torres Martín Alonso","Tramoyero","Tramoya",1_963_221),
    ("Torres Martin Coordinador","Coordinador Del Pequeño Municipal","Coordinación Artística",1_863_396),
    ("Ulloa Gamonal Felipe","Cantante Coro","Coro",1_843_221),
    ("Urbano Jiménez Mariajo","Cantante Coro","Coro",1_843_221),
    ("Urrutia Benavides María","Sindiculada Comercial","Ventas Boletería",863_373),
    ("Urrutia Roblando Alejandra","Directora Municipal Orquesta Cámara","Orquesta",1_903_909),
    ("Urrutia Herrera Cecilia","Coordinadora Serv. Mediación Cultural","Audiencia",2_012_800),
    ("Urrutia Escalada Diego","Tramoyero","Tramoya",3_134_764),
    ("Valladares Mona Pía","Contrafagot","Orquesta",3_863_760),
    ("Vargas Arriagos Manuel","Tramoyero","Tramoya",1_843_760),
    ("Vargas Sirkin Dina","Cantante Coro","Coro",842_000),
    ("Vargas González Matías","Apoyo","Tramoya",870_300),
    ("Vargas Silva Marcos","Solicitero","Administración Orquesta",814_034),
    ("Vásquez Sepúlveda Karen","Archivera Musical","Administración Orquesta",1_863_000),
    ("Vásquez Calvo Francisca","Subgerenta Comercial y Marketing","Ventas Empresas",3_473_811),
    ("Vásquez González Juan Carlos","Auxiliar Contable","Contabilidad y Control de Gestión",1_146_112),
    ("Vásquez Villarpoble Madeleine","Primera Bailarina","Ballet",2_521_001),
    ("Vega Cabriora Hugo","Tramoyero","Tramoya",1_863_760),
    ("Vega Huamra Walter","Auxiliar de Ases","Servicios Generales",842_856),
    ("Vega Martínez Páez Abraham","Tramoyero","Tramoya",1_863_760),
    ("Venegas Amamorosa Guillermo","Tramoyero","Taller De Vestuario",1_863_760),
    ("Vera Molina Alejandro","Asistente Judicial Legal","Gerencia",5_111_428),
    ("Vera Rontchini Alejandra","Tramoyero","Librería",1_823_634),
    ("Vidal Low Pablo","Balleto","Orquesta",2_063_945),
    ("Videla Londrio Belén","Ayudante","Ballet",870_300),
    ("Videla Londrio Florencia","Ayudante","Ballet",870_300),
    ("Vinitul Espinoza Ángel","Apoyo","Tramoya",870_300),
    ("Yáñez Noji Bárbara","Coordinadora Serv. Mediación Cultural","Audiencia",2_063_034),
    ("Yavar Párachi María","Dirección Comercial y Diseño","Dirección Comercial",3_773_000),
    ("Zahen Wilkie","Baila Solista","Orquesta",2_063_945),
    ("Zapata Arévalo Julio","Cantante Coro","Coro",2_063_945),
    ("Zapata Basuaño Julio","Portería e Informaciones","Portería e Informaciones",744_028),
    ("Zapata Ramírez Rodolfo","Ayudante Solista Dir. Vista","Orquesta",2_063_761),
    ("Zuñiga Valdermente Giraldo","Maestro Mantención y Servicios Generales","Servicios Generales",1_263_343),
    ("Zurita Mauiuira Héctor","Tramoyero","Tramoya",1_823_634),
]

def _cat_ceac(cargo):
    c = cargo.lower()
    if any(k in c for k in ['coordinación general','coordinacion general','producción general','productor general']):
        return 'Dirección y Gestión'
    if any(k in c for k in ['afinador','sonidista','pianista','coordinador orquesta','coordinadora coro','coordinador banch']):
        return 'Artístico / Músicos'
    if any(k in c for k in ['técnico','tecnico','iluminación','iluminacion','sonido','video','tramoya','utilero','vestuarista','encargado tecnico','encargada tecnico']):
        return 'Técnico / Escénico'
    return 'Administrativo / Apoyo'

def _cat_tms(cargo, area):
    c = cargo.lower(); a = area.lower()
    if any(k in c for k in ['director general','directora general','gerente general','director artístico','director de orquesta','directora municipal','director técnico']):
        return 'Dirección y Gestión'
    if any(k in a for k in ['orquesta','ballet','coro','escuela ballet']) or \
       any(k in c for k in ['cantante','pianista','bailarina','cuerpo de baile','primera bailarina','solista','concertino','tutti','contrabajo','violin','oboe','fagot','contrafagot','trombone','flute','trompeta','percusión','maestro de escuela','maestra de escuela','balleto','baila ']):
        return 'Artístico / Músicos'
    if any(k in c for k in ['tramoyero','tramoya','técnico','tecnico','iluminación','iluminacion','vestuario','caracterización','utilería','caldera','construcción','audiovisual','escenógrafo','realizador multimedia']):
        return 'Técnico / Escénico'
    return 'Administrativo / Apoyo'

def _cat_corcudec(nivel):
    if nivel in ('Director', 'Jefatura'):
        return 'Dirección y Gestión'
    if nivel in ('Concertino','Asistente Concertino','Jefe de Fila','Asistente de Fila','Tutti'):
        return 'Artístico / Músicos'
    return 'Administrativo / Apoyo'

_HOMOLOG = {
    # ── CEAC ──────────────────────────────────────────────────────────────────
    "Generalista de Personas":                          "RECURSOS HUMANOS",
    "Utilero Tramoya":                                  "AUXILIAR ORQUESTA",
    "Técnico Iluminación":                              "TECNICO EN ILUMINACION",
    "Estafeta":                                         "ASISTENTE LOGISTICO",
    "Coordinación y Prod. Artística":                   "PRODUCTOR",
    "Encargado de Sonido y Video":                      "TECNICO EN ILUMINACION",
    "Asistente de Dirección":                           "SECRETARIA EJECUTIVA",
    "Coordinador Orquesta":                             "COORDINADOR ORQUESTA",
    "Productor General":                                "PRODUCTOR",
    "Encargada de Comunicaciones Estratégicas":         "DIRECTORA  COMUNICACIONES",
    "Analista de Personal":                             "RECURSOS HUMANOS",
    "Utilero Archivo Musical":                          "ARCHIVOS MUSICALES Y COPISTERIA",
    "Utilero Orquesta":                                 "AUXILIAR ORQUESTA",
    "Masoterapeuta":                                    "Sin equivalente CORCUDEC",
    "Coordinador BANCH":                                "COORDINADOR ORQUESTA",
    "Encargado Comercial y Fundraising":                "PRODUCTOR",
    "Analista de Proyectos":                            "Sin equivalente CORCUDEC",
    "Community Manager – Com. y Marketing":             "PERIODISTA",
    "Boletería":                                        "ENCARGADA DE BOLETERIA",
    "Diseñador Gráfico":                                "AUDIOVISUALISTA",
    "Portero":                                          "PORTERO",
    "Coordinadora Coro":                                "AUXILIAR CORO ORQUESTA Y TEATRO",
    "Encargada de Presupuesto":                         "ENCARGADA DE CONTABILIDAD CONTROL Y SOPORTE",
    "Encargada Área Educación Mediación":               "Sin equivalente CORCUDEC",
    "Sonidista":                                        "TECNICO EN ILUMINACION",
    "Encargada Técnico":                                "ENCARGADO TECNICOS",
    "Auxiliar de Servicios Estafeta":                   "ASISTENTE LOGISTICO",
    "Auxiliar de Servicios":                            "AUXILIAR ORQUESTA",
    "Técnico Sonido y Video":                           "TECNICO EN ILUMINACION",
    "Encargado Iluminación":                            "TECNICO EN ILUMINACION",
    "Analista Comercial":                               "Sin equivalente CORCUDEC",
    "Coordinación General y Artística":                 "DIRECTOR EJECUTIVO",
    "Encargada de Personal y RRHH":                     "RECURSOS HUMANOS",
    "Asistente de Personas":                            "RECURSOS HUMANOS",
    "Coordinador de Plataformas Digitales":             "AUDIOVISUALISTA",
    "Encargada de Comunicaciones":                      "DIRECTORA  COMUNICACIONES",
    "Analista Contable":                                "ASISTENTE LOGISTICA Y CONTABILIDAD",
    "Nochero":                                          "PORTERO",
    "Afinador de Piano":                                "Sin equivalente CORCUDEC",
    "Audiovisual – Com. y Marketing":                   "AUDIOVISUALISTA",
    "Vestuarista":                                      "ENCARGADA DE CAMARINES",
    "Administrador":                                    "DIRECTOR EJECUTIVO",
    "Asistente de Compras":                             "ASISTENTE LOGISTICO",
    # ── TMS ───────────────────────────────────────────────────────────────────
    "Concertino":                                       "CONCERTINO",
    "Inspectora Escuela de Ballet":                     "SECRETARIA EJECUTIVA",
    "Cuerpo de Baile 1":                                "Sin equivalente CORCUDEC",
    "Copista Digital – Archivo Musical":                "ARCHIVOS MUSICALES Y COPISTERIA",
    "Coordinadora Escuela de Ballet":                   "COORDINADOR ORQUESTA",
    "Jefa de Servicios Generales":                      "ENCARGADO TECNICOS",
    "Oficial Bienestar y Desarrollo Org.":              "RECURSOS HUMANOS",
    "Concertmaster":                                    "CONCERTINO",
    "Primera Bailarina":                                "Sin equivalente CORCUDEC",
    "Portería e Informaciones":                         "PORTERO",
    "Tramoyero":                                        "AUXILIAR ORQUESTA",
    "Cuerpo de Baile 2":                                "Sin equivalente CORCUDEC",
    "Cuerpo de Baile 3":                                "Sin equivalente CORCUDEC",
    "Encargada Comercial":                              "PRODUCTOR",
    "Pianista Escuela de Ballet":                       "Sin equivalente CORCUDEC",
    "Cantante Coro":                                    "Sin equivalente CORCUDEC",
    "Asistente Contable":                               "ASISTENTE LOGISTICA Y CONTABILIDAD",
    "Tutti Dir. Viento":                                "MUSICO TUTTI TROMBON",
    "Apoyo":                                            "AUXILIAR ORQUESTA",
    "Asistente de Producción":                          "ASISTENTE LOGISTICO",
    "Archivo Musical Ballet":                           "ARCHIVOS MUSICALES Y COPISTERIA",
    "Sub-Directora de Comunicaciones":                  "DIRECTORA  COMUNICACIONES",
    "Portería Boletería":                               "ENCARGADA DE BOLETERIA",
    "Asistente Dir. Tramoya II":                        "AUXILIAR ORQUESTA",
    "Gerente General":                                  "DIRECTOR EJECUTIVO",
    "Tutti Dir. Violín":                                "MUSICO TUTTI VIOLINES",
    "Oboe Orquesta":                                    "MUSICO JEFE DE FILA OBOE",
    "Ayudante Boletería Obrero":                        "ENCARGADA DE BOLETERIA",
    "Enlace Técnico Taller de Vestuario":               "TECNICO EN ILUMINACION",
    "Contrafagot":                                      "Sin equivalente CORCUDEC",
    "Tutti Contrabajo":                                 "MUSICO  VIOLINISTA TUTTI",
    "Tutti Boletería":                                  "MUSICO  VIOLINISTA TUTTI",
    "Tutti Vello":                                      "MUSICO  VIOLINISTA TUTTI",
    "Maestra de Escuela de Ballet":                     "Sin equivalente CORCUDEC",
    "Director Técnico":                                 "ENCARGADO TECNICOS",
    "Asistente Director Técnico":                       "DIRECTOR EJECUTIVO",
    "Cerro Volante":                                    "Sin equivalente CORCUDEC",
    "Encargada Comunicaciones":                         "DIRECTORA  COMUNICACIONES",
    "Asistente Clarinete":                              "ASISTENTE LOGISTICO",
    "Aux. Servicios Guardiagas":                        "Sin equivalente CORCUDEC",
    "Gerente Nutrición":                                "DIRECTOR EJECUTIVO",
    "Jefe de Portería":                                 "PORTERO",
    "Trompeta":                                         "MUSICO TUTTI TROMPETA",
    "Auxiliar":                                         "AUXILIAR ORQUESTA",
    "Encargada de Compras":                             "ASISTENTE LOGISTICO",
    "Mda de Producción/Coordinación Artística":         "PRODUCTOR",
    "Kenis OT Técnica":                                 "Sin equivalente CORCUDEC",
    "Operador de Caldera":                              "Sin equivalente CORCUDEC",
    "Tramoyero Dir. Orquesta":                          "AUXILIAR ORQUESTA",
    "Pianista":                                         "Sin equivalente CORCUDEC",
    "Asistente de Recursos Humanos":                    "RECURSOS HUMANOS",
    "Supervisora Almacén":                              "Sin equivalente CORCUDEC",
    "Pabellón Blando Mayor":                            "Sin equivalente CORCUDEC",
    "Asistente Admin. Dirección del Ballet":            "Sin equivalente CORCUDEC",
    "Auxiliar Teatro Escultura":                        "AUXILIAR ORQUESTA",
    "Violín 2 Ayudante":                                "MUSICO ASISTENTE DE VIOLINES",
    "Asistente Área de Contenidos":                     "ASISTENTE LOGISTICO",
    "Violinchelo":                                      "Sin equivalente CORCUDEC",
    "Gran Ayudante":                                    "Sin equivalente CORCUDEC",
    "Asistente de Relaciones Corporativas":             "ASISTENTE LOGISTICO",
    "Mamonzón Tutti":                                   "MUSICO  VIOLINISTA TUTTI",
    "Tutti":                                            "MUSICO  VIOLINISTA TUTTI",
    "Auxiliar de Ases":                                 "AUXILIAR ORQUESTA",
    "Maestra Compañía de Ballet":                       "Sin equivalente CORCUDEC",
    "Personal de Sala":                                 "RECURSOS HUMANOS",
    "Tutti Viento":                                     "MUSICO  VIOLINISTA TUTTI",
    "Ayudante":                                         "Sin equivalente CORCUDEC",
    "Maestro de Escuela de Ballet":                     "Sin equivalente CORCUDEC",
    "Auxiliar Contable":                                "AUXILIAR ORQUESTA",
    "Bailarina Solista":                                "Sin equivalente CORCUDEC",
    "Secretaria":                                       "SECRETARIA EJECUTIVA",
    "Percusión":                                        "ASISTENTE DE FILA PERCUSION",
    "Baila Solista":                                    "Sin equivalente CORCUDEC",
    "Asistente de Tramoya":                             "AUXILIAR ORQUESTA",
    "Asistente Comercial":                              "ASISTENTE LOGISTICO",
    "Baila":                                            "Sin equivalente CORCUDEC",
    "Balleto":                                          "Sin equivalente CORCUDEC",
    "Directora General":                                "DIRECTOR EJECUTIVO",
    "Obrero Orquesta":                                  "Sin equivalente CORCUDEC",
    "Oboe 1":                                           "MUSICO JEFE DE FILA OBOE",
    "Dirección de Coordinación Artística":              "DIRECTOR TITULAR DE LA ORQUESTA",
    "Administración Ballet":                            "Sin equivalente CORCUDEC",
    "Control de Entradas":                              "Sin equivalente CORCUDEC",
    "Coros":                                            "Sin equivalente CORCUDEC",
    "Flute 1":                                          "MUSICO ASISTENTE  DE FILA DE FLAUTA",
    "Tutti Solistas":                                   "MUSICO  VIOLINISTA TUTTI",
    "Jefe Taller de Audiovisual":                       "AUDIOVISUALISTA",
    "Realizador Multimedia":                            "Sin equivalente CORCUDEC",
    "Administración Orquesta":                          "Sin equivalente CORCUDEC",
    "Coordinación Ballet Solistas":                     "Sin equivalente CORCUDEC",
    "Cantante Ballet":                                  "Sin equivalente CORCUDEC",
    "Resumen de Baile y Contabilidad":                  "ASISTENTE LOGISTICA Y CONTABILIDAD",
    "Jefe Taller de Vestuario":                         "ENCARGADA DE CAMARINES",
    "Director Artístico Compañía de Ballet":            "DIRECTOR EJECUTIVO",
    "Asistente Admin. Orquesta":                        "ASISTENTE LOGISTICO",
    "Coordinadora de Marca y Diseño":                   "AUDIOVISUALISTA",
    "Asistente de Bienestar":                           "ASISTENTE LOGISTICO",
    "Jefe de Vestuario y Caracterización":              "ENCARGADA DE CAMARINES",
    "Gerente Audiovisual":                              "DIRECTOR EJECUTIVO",
    "Inspectora de la Escuela de Ballet":               "Sin equivalente CORCUDEC",
    "Segundo Director Escenario":                       "DIRECTOR EJECUTIVO",
    "Auditor de Tesorería":                             "ASISTENTE LOGISTICA Y CONTABILIDAD",
    "Razón Drasino":                                    "Sin equivalente CORCUDEC",
    "Supervisor de Producción":                         "PRODUCTOR",
    "Tramoyero Boletería":                              "AUXILIAR ORQUESTA",
    "Tramoyero Orquesta":                               "AUXILIAR ORQUESTA",
    "Director de Orquesta Residente":                   "DIRECTOR TITULAR DE LA ORQUESTA",
    "Sub Jefa de Vestuario":                            "ENCARGADA DE CAMARINES",
    "Jefe de Sistemas":                                 "Sin equivalente CORCUDEC",
    "Sub-Director de Coro":                             "DIRECTOR EJECUTIVO",
    "Jefe Articulador de Coro":                         "Sin equivalente CORCUDEC",
    "Jefe de Sala":                                     "Sin equivalente CORCUDEC",
    "Coordinadora Área Comunitaria":                    "Sin equivalente CORCUDEC",
    "Kinesiólogo":                                      "Sin equivalente CORCUDEC",
    "Coordinador Rel. Corporativas":                    "Sin equivalente CORCUDEC",
    "Tesorero":                                         "Sin equivalente CORCUDEC",
    "Dirección Técnica":                                "Sin equivalente CORCUDEC",
    "Prevencionista de Riesgo":                         "Sin equivalente CORCUDEC",
    "Jefe de Taller de Utilería":                       "Sin equivalente CORCUDEC",
    "Fagot":                                            "MUSICO JEFE DE FILA  FAGOT",
    "Escenógrafo Ballet":                               "Sin equivalente CORCUDEC",
    "Trombone":                                         "MUSICO TROMBON",
    "Jefe Taller de Construcciones":                    "Sin equivalente CORCUDEC",
    "Tutti Tutti":                                      "MUSICO  VIOLINISTA TUTTI",
    "Coordinador Del Pequeño Municipal":                "Sin equivalente CORCUDEC",
    "Sindiculada Comercial":                            "Sin equivalente CORCUDEC",
    "Directora Municipal Orquesta Cámara":              "DIRECTOR TITULAR DE LA ORQUESTA",
    "Coordinadora Serv. Mediación Cultural":            "Sin equivalente CORCUDEC",
    "Solicitero":                                       "Sin equivalente CORCUDEC",
    "Archivera Musical":                                "Sin equivalente CORCUDEC",
    "Subgerenta Comercial y Marketing":                 "Sin equivalente CORCUDEC",
    "Asistente Judicial Legal":                         "ASISTENTE LOGISTICO",
    "Dirección Comercial y Diseño":                     "AUDIOVISUALISTA",
    "Ayudante Solista Dir. Vista":                      "Sin equivalente CORCUDEC",
    "Maestro Mantención y Servicios Generales":         "Sin equivalente CORCUDEC",
}

def _simplify_hom(corcudec_cargo):
    if corcudec_cargo == 'Sin equivalente CORCUDEC':
        return 'Sin equivalente'
    c = corcudec_cargo.upper()
    if 'DIRECTOR' in c:               return 'Director'
    if 'ASISTENTE CONCERTINO' in c:   return 'Asistente Concertino'
    if 'CONCERTINO' in c:             return 'Concertino'
    if 'JEFE DE FILA' in c:           return 'Jefe de Fila'
    if 'ASISTENTE DE FILA' in c or 'ASISTENTE  DE FILA' in c: return 'Asistente de Fila'
    if 'TUTTI' in c:                  return 'Músico Tutti'
    if 'MUSICO' in c and 'TROMBON' in c: return 'Músico Tutti'
    if 'MUSICO' in c and 'VIOLINISTA' in c: return 'Músico Tutti'
    if 'MUSICO' in c and 'TROMPETA' in c: return 'Músico Tutti'
    if 'MUSICO' in c and 'ASISTENTE' in c: return 'Asistente de Fila'
    if 'MUSICO' in c:                 return 'Músico'
    if 'COORDINADOR ORQUESTA' in c:   return 'Coordinador Orquesta'
    if 'AUXILIAR CORO' in c:          return 'Auxiliar Coro'
    if 'AUXILIAR ORQUESTA' in c or 'AUXILIAR  ORQUESTA' in c: return 'Auxiliar'
    if 'ARCHIVOS MUSICALES' in c or 'COPISTERIA' in c: return 'Archivos Musicales'
    if 'TECNICO EN ILUMINACION' in c: return 'Técnico'
    if 'ENCARGADO TECNICOS' in c:     return 'Jefe Técnico'
    if 'RECURSOS HUMANOS' in c:       return 'RRHH'
    if 'COMUNICACIONES' in c:         return 'Comunicaciones'
    if 'PERIODISTA' in c:             return 'Comunicaciones'
    if 'AUDIOVISUAL' in c:            return 'Comunicaciones'
    if 'ASISTENTE LOGISTIC' in c:     return 'Asistente'
    if 'PORTERO' in c:                return 'Portero'
    if 'BOLETERIA' in c:              return 'Boletería'
    if 'PRODUCTOR' in c:              return 'Producción'
    if 'SECRETARIA' in c:             return 'Secretaría'
    if 'CAMARINES' in c:              return 'Camarines'
    if 'CONTABILIDAD' in c:           return 'Contabilidad'
    if 'JEFATURA' in c:               return 'Jefatura'
    return corcudec_cargo.title()

def _build_comp_json(df_corcudec):
    CATS = ['Dirección y Gestión','Artístico / Músicos','Técnico / Escénico','Administrativo / Apoyo']
    INSTS = ['CORCUDEC','TMS','CEAC']

    all_emp = {}
    # CEAC
    all_emp['CEAC'] = [{'nombre': n, 'cargo': c, 'area': '—', 'remuneracion': int(r),
                         'categoria': _cat_ceac(c),
                         'cargo_hom': _simplify_hom(_HOMOLOG.get(c, 'Sin equivalente CORCUDEC'))}
                        for n, c, r in _CEAC_RAW]
    # TMS
    all_emp['TMS'] = [{'nombre': n, 'cargo': c, 'area': a, 'remuneracion': int(r),
                        'categoria': _cat_tms(c, a),
                        'cargo_hom': _simplify_hom(_HOMOLOG.get(c, 'Sin equivalente CORCUDEC'))}
                       for n, c, a, r in _TMS_RAW]
    # CORCUDEC (no names — privacy)
    all_emp['CORCUDEC'] = [{'nombre': f"Trabajador {i+1}", 'cargo': row['cargo'],
                             'area': row['departamento'], 'remuneracion': int(row['total_haberes']),
                             'categoria': _cat_corcudec(row['nivel']),
                             'cargo_hom': _simplify_hom(row['cargo'])}
                            for i, row in df_corcudec.reset_index().iterrows()]

    def pct(vals, p):
        s = sorted(vals)
        idx = int(len(s) * p)
        return s[min(idx, len(s)-1)]

    stats_out = {}
    for cat in CATS:
        stats_out[cat] = {}
        for inst in INSTS:
            vals = [e['remuneracion'] for e in all_emp[inst] if e['categoria'] == cat]
            if not vals:
                stats_out[cat][inst] = None
            else:
                stats_out[cat][inst] = {
                    'n': len(vals), 'min': min(vals), 'max': max(vals),
                    'median': int(_st.median(vals)), 'mean': int(_st.mean(vals)),
                    'p25': pct(vals, 0.25), 'p75': pct(vals, 0.75),
                }

    return json.dumps({'stats': stats_out, 'empleados': all_emp}, ensure_ascii=False)

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análisis Salarial CORCUDEC — Julio 2026</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');
  :root {
    --navy: #1C3557; --gold: #B8892A; --cream: #F7F4EF;
    --text: #1a1a2e; --muted: #6b7280; --white: #ffffff;
    --green: #2E7D52; --red: #8B1A1A;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Source Sans 3', sans-serif; background: var(--cream); color: var(--text); line-height: 1.6; }
  header {
    background: var(--navy);
    border-top: 5px solid var(--gold);
    border-bottom: 5px solid var(--gold);
    display: flex;
    align-items: stretch;
    min-height: 155px;
  }
  .hdr-left {
    flex: 1;
    padding: 1.8rem 2rem 1.8rem 2.2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .hdr-left h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--white);
    line-height: 1.25;
    letter-spacing: 0.01em;
  }
  .hdr-divider {
    width: 1px;
    background: rgba(255,255,255,0.12);
    margin: 0;
  }
  .hdr-sub {
    color: rgba(255,255,255,0.55);
    font-size: 0.88rem;
    margin-top: 0.25rem;
  }
  .hdr-sub2 {
    color: rgba(255,255,255,0.55);
    font-size: 0.88rem;
    margin-top: 0.12rem;
  }
  .hdr-rule {
    width: 100%;
    max-width: 380px;
    height: 1px;
    background: var(--gold);
    opacity: 0.5;
    margin: 0.55rem 0;
  }
  .badge {
    display: inline-block;
    background: var(--gold);
    color: var(--white);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.22rem 0.9rem;
    border-radius: 2rem;
    letter-spacing: 0.06em;
    margin-top: 0.3rem;
    align-self: flex-start;
  }
  .hdr-right {
    width: 300px;
    flex-shrink: 0;
    padding: 1rem 1.3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  .lidera-card {
    background: #F7F4EF;
    border-radius: 10px;
    box-shadow: 2px 3px 14px rgba(0,0,0,0.22);
    width: 100%;
    padding: 1.1rem 1rem 0.9rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
  }
  .lidera-by {
    font-size: 0.65rem;
    color: rgba(0,0,0,0.28);
    font-style: italic;
    margin-bottom: 0.45rem;
    letter-spacing: 0.02em;
  }
  .lidera-wordmark {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #4a4a4a;
    letter-spacing: 0.06em;
    line-height: 1;
    margin-top: 0.3rem;
  }
  .lidera-gold-rule {
    width: 110px;
    height: 1.5px;
    background: var(--gold);
    opacity: 0.65;
    margin: 0.55rem 0 0.4rem;
  }
  .lidera-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #3a3a3a;
    letter-spacing: 0.01em;
  }
  .lidera-tagline {
    font-size: 0.62rem;
    color: #999;
    font-style: italic;
    margin-top: 0.18rem;
    text-align: center;
  }
  @media (max-width: 700px) {
    header { flex-direction: column; }
    .hdr-right { width: 100%; border-top: 1px solid rgba(255,255,255,0.12); }
    .hdr-divider { display: none; }
  }
  main { max-width: 1100px; margin: 0 auto; padding: 2rem 1.5rem 3rem; }
  section { margin-bottom: 2.5rem; }
  h2 { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; color: var(--navy); border-bottom: 2px solid var(--gold); padding-bottom: 0.4rem; margin-bottom: 1.2rem; }
  .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; }
  .kpi { background: var(--white); border-left: 4px solid var(--navy); padding: 1rem 1.2rem; border-radius: 0 6px 6px 0; }
  .kpi.gold { border-left-color: var(--gold); }
  .kpi.green { border-left-color: var(--green); }
  .kpi label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); display: block; }
  .kpi .value { font-family: 'Cormorant Garamond', serif; font-size: 1.7rem; font-weight: 600; color: var(--navy); font-variant-numeric: tabular-nums; }
  .kpi .sub { font-size: 0.8rem; color: var(--muted); margin-top: 0.1rem; }
  .chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  .chart-row.single { grid-template-columns: 1fr; }
  .chart-box { background: var(--white); border-radius: 8px; padding: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
  .chart-box img { width: 100%; height: auto; display: block; }
  .chart-box canvas { width: 100% !important; }
  .chart-hint { font-size: 0.72rem; color: var(--muted); text-align: center; margin-top: 0.5rem; }
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; background: var(--white); border-radius: 8px; overflow: hidden; }
  thead tr { background: var(--navy); color: var(--white); }
  th { padding: 0.65rem 0.9rem; text-align: left; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.04em; }
  td { padding: 0.55rem 0.9rem; border-bottom: 1px solid #f0ede8; }
  tr:last-child td { border-bottom: none; }
  tr:nth-child(even) { background: #fbf9f6; }
  .num { text-align: right; font-variant-numeric: tabular-nums; }
  .tag { display: inline-block; font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 1rem; font-weight: 600; }
  .tag-orch { background: #e8eef5; color: var(--navy); }
  .tag-admin { background: #e8f5ee; color: var(--green); }
  .tag-dir { background: #f5e8e8; color: var(--red); }
  .info-box { background: #fff8e8; border-left: 4px solid var(--gold); padding: 0.9rem 1.2rem; border-radius: 0 6px 6px 0; font-size: 0.9rem; }
  footer { text-align: center; padding: 1.5rem; font-size: 0.8rem; color: var(--muted); border-top: 1px solid #e5e1d8; margin-top: 1rem; }
  tr.drillable { cursor: pointer; transition: background 0.15s; }
  tr.drillable:hover td { background: #eef3f8 !important; }
  tr.drillable td:first-child::after { content: ' ↗'; font-size: 0.68rem; color: var(--muted); }
  /* Login */
  #loginOverlay { position: fixed; inset: 0; background: var(--navy); z-index: 200; display: flex; align-items: center; justify-content: center; }
  #loginOverlay.hidden { display: none; }
  .login-box { background: var(--white); border-radius: 12px; padding: 2.5rem 2.8rem; width: 100%; max-width: 380px; box-shadow: 0 12px 50px rgba(0,0,0,0.35); text-align: center; }
  .login-box .logo { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 600; color: var(--navy); margin-bottom: 0.2rem; }
  .login-box .sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 1.8rem; }
  .login-box .gold-bar { width: 2.5rem; height: 3px; background: var(--gold); margin: 0.5rem auto 1.6rem; border-radius: 2px; }
  .login-field { width: 100%; border: 1.5px solid #e0dcd6; border-radius: 6px; padding: 0.65rem 0.9rem; font-size: 0.95rem; font-family: inherit; color: var(--text); background: #fafaf8; margin-bottom: 0.8rem; outline: none; transition: border-color 0.15s; }
  .login-field:focus { border-color: var(--navy); }
  .login-btn { width: 100%; background: var(--navy); color: var(--white); border: none; border-radius: 6px; padding: 0.7rem; font-size: 0.95rem; font-weight: 600; cursor: pointer; letter-spacing: 0.04em; transition: background 0.15s; margin-top: 0.4rem; }
  .login-btn:hover { background: #243f63; }
  .login-error { color: var(--red); font-size: 0.82rem; margin-top: 0.6rem; min-height: 1.2em; }
  .login-lidera { border-top: 1px solid #e8e4de; margin-top: 1.4rem; padding-top: 1rem; display: flex; flex-direction: column; align-items: center; gap: 0.2rem; }
  .login-lidera-by { font-size: 0.62rem; color: #aaa; font-style: italic; }
  .login-lidera-inner { display: flex; align-items: center; gap: 0.45rem; margin-top: 0.3rem; }
  .login-lidera-word { font-family: 'Source Sans 3', sans-serif; font-size: 1.25rem; font-weight: 700; color: #4a4a4a; letter-spacing: 0.07em; }
  .login-lidera-name { font-size: 0.72rem; color: #888; margin-top: 0.15rem; }
  #reportContent { display: none; }
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); z-index: 100; display: none; align-items: flex-start; justify-content: center; padding: 2rem 1rem; overflow-y: auto; }
  .modal-overlay.open { display: flex; }
  .modal { background: var(--white); border-radius: 10px; width: 100%; max-width: 900px; box-shadow: 0 8px 40px rgba(0,0,0,0.18); animation: fadeUp 0.2s ease; }
  @keyframes fadeUp { from { opacity:0; transform: translateY(12px); } to { opacity:1; transform: translateY(0); } }
  .modal-header { background: var(--navy); color: var(--white); padding: 1.1rem 1.4rem; border-radius: 10px 10px 0 0; display: flex; align-items: center; justify-content: space-between; }
  .modal-header h3 { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; font-weight: 600; }
  .modal-header .badge-count { background: var(--gold); font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 1rem; letter-spacing: 0.04em; }
  .modal-close { background: none; border: none; color: rgba(255,255,255,0.8); font-size: 1.4rem; cursor: pointer; line-height: 1; padding: 0 0.2rem; }
  .modal-close:hover { color: var(--white); }
  .modal-body { padding: 1.2rem 1.4rem 1.4rem; overflow-x: auto; }
  .modal-body table { font-size: 0.84rem; }
  .modal-stats { display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; }
  .modal-stat { flex: 1; min-width: 130px; background: var(--cream); border-radius: 6px; padding: 0.6rem 0.9rem; }
  .modal-stat label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.07em; color: var(--muted); display: block; }
  .modal-stat .val { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; font-weight: 600; color: var(--navy); }
  @media (max-width: 700px) {
    .chart-row { grid-template-columns: 1fr; }
    .kpi-grid { grid-template-columns: 1fr 1fr; }
    .modal-overlay { padding: 0; align-items: flex-end; }
    .modal { border-radius: 12px 12px 0 0; }
  }
  /* ── Comparative section ─────────────────────────────── */
  .inst-legend { display: flex; gap: 1.6rem; flex-wrap: wrap; margin-bottom: 1rem; align-items: center; }
  .inst-pill { display: flex; align-items: center; gap: 7px; }
  .inst-swatch { width: 13px; height: 13px; border-radius: 3px; flex-shrink: 0; }
  .inst-name { font-size: 0.82rem; font-weight: 700; letter-spacing: 0.04em; color: var(--navy); }
  .comp-wrap { background: #fff; border-radius: 10px; padding: 1.4rem 1.4rem 1rem; box-shadow: 0 1px 6px rgba(0,0,0,.07); }
  .chart-hint { font-size: 0.75rem; color: var(--muted); margin: 0.45rem 0 0; text-align: center; }
  .comp-breadcrumb { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 0.8rem; flex-wrap: wrap; }
  .comp-back-btn { background: var(--navy); color: #fff; border: none; border-radius: 6px; padding: 0.35rem 0.9rem; font-size: 0.8rem; font-weight: 600; cursor: pointer; letter-spacing: 0.03em; }
  .comp-back-btn:hover { background: #2a4f7c; }
  .comp-breadcrumb-path { font-size: 0.82rem; color: var(--muted); }
  .comp-breadcrumb-path strong { color: var(--navy); }
</style>
</head>
<body>

<!-- Login overlay -->
<div id="loginOverlay">
  <div class="login-box">
    <div class="logo">CORCUDEC</div>
    <div class="gold-bar"></div>
    <div class="sub">Análisis Salarial Interno · Julio 2026</div>
    <input id="loginUser" class="login-field" type="text" placeholder="Usuario" autocomplete="username">
    <input id="loginPass" class="login-field" type="password" placeholder="Contraseña" autocomplete="current-password">
    <button class="login-btn" id="loginBtn">Acceder</button>
    <div class="login-error" id="loginError"></div>
    <div class="login-lidera">
      <div class="login-lidera-by">Análisis desarrollado por</div>
      <div class="login-lidera-inner">
        <svg width="36" height="42" viewBox="0 0 68 72" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="14" cy="8"  rx="7" ry="8"  fill="#D4623B"/>
          <ellipse cx="14" cy="19" rx="3.5" ry="3" fill="#D4623B"/>
          <ellipse cx="14" cy="28" rx="7" ry="8"  fill="#D4623B"/>
          <ellipse cx="14" cy="39" rx="3.5" ry="3" fill="#D4623B"/>
          <ellipse cx="14" cy="48" rx="7" ry="8"  fill="#D4623B"/>
          <ellipse cx="14" cy="59" rx="3.5" ry="3" fill="#D4623B"/>
          <ellipse cx="14" cy="68" rx="7" ry="4"  fill="#D4623B"/>
          <ellipse cx="34" cy="8"  rx="7" ry="8"  fill="#7B3A8E"/>
          <ellipse cx="34" cy="19" rx="3.5" ry="3" fill="#7B3A8E"/>
          <ellipse cx="34" cy="28" rx="7" ry="8"  fill="#7B3A8E"/>
          <ellipse cx="34" cy="39" rx="3.5" ry="3" fill="#7B3A8E"/>
          <ellipse cx="34" cy="48" rx="7" ry="8"  fill="#7B3A8E"/>
          <ellipse cx="34" cy="59" rx="3.5" ry="3" fill="#7B3A8E"/>
          <ellipse cx="34" cy="68" rx="7" ry="4"  fill="#7B3A8E"/>
          <ellipse cx="54" cy="8"  rx="7" ry="8"  fill="#259990"/>
          <ellipse cx="54" cy="19" rx="3.5" ry="3" fill="#259990"/>
          <ellipse cx="54" cy="28" rx="7" ry="8"  fill="#259990"/>
          <ellipse cx="54" cy="39" rx="3.5" ry="3" fill="#259990"/>
          <ellipse cx="54" cy="48" rx="7" ry="8"  fill="#259990"/>
          <ellipse cx="54" cy="59" rx="3.5" ry="3" fill="#259990"/>
          <ellipse cx="54" cy="68" rx="7" ry="4"  fill="#259990"/>
        </svg>
        <span class="login-lidera-word">LIDERA</span>
      </div>
      <div class="login-lidera-name">Consultora Lidera</div>
    </div>
  </div>
</div>

<div id="reportContent">
<header>
  <div class="hdr-left">
    <h1>Corporación Cultural<br>Universidad de Concepción</h1>
    <div class="hdr-rule"></div>
    <div class="hdr-sub">Orquesta Sinfónica Universidad de Concepción</div>
    <div class="hdr-sub2">Análisis de Dotación y Bandas Salariales · Julio 2026</div>
    <span class="badge">JULIO 2026 · {{ stats.total_empleados }} TRABAJADORES ACTIVOS</span>
  </div>
  <div class="hdr-divider"></div>
  <div class="hdr-right">
    <div class="lidera-card">
      <div class="lidera-by">Análisis desarrollado por</div>
      <!-- Bead columns SVG (centered) -->
      <svg width="68" height="72" viewBox="0 0 68 72" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Orange column (left) -->
        <ellipse cx="14" cy="8"  rx="7" ry="8"  fill="#D4623B"/>
        <ellipse cx="14" cy="19" rx="3.5" ry="3" fill="#D4623B"/>
        <ellipse cx="14" cy="28" rx="7" ry="8"  fill="#D4623B"/>
        <ellipse cx="14" cy="39" rx="3.5" ry="3" fill="#D4623B"/>
        <ellipse cx="14" cy="48" rx="7" ry="8"  fill="#D4623B"/>
        <ellipse cx="14" cy="59" rx="3.5" ry="3" fill="#D4623B"/>
        <ellipse cx="14" cy="68" rx="7" ry="4"  fill="#D4623B"/>
        <!-- Purple column (center) -->
        <ellipse cx="34" cy="8"  rx="7" ry="8"  fill="#7B3A8E"/>
        <ellipse cx="34" cy="19" rx="3.5" ry="3" fill="#7B3A8E"/>
        <ellipse cx="34" cy="28" rx="7" ry="8"  fill="#7B3A8E"/>
        <ellipse cx="34" cy="39" rx="3.5" ry="3" fill="#7B3A8E"/>
        <ellipse cx="34" cy="48" rx="7" ry="8"  fill="#7B3A8E"/>
        <ellipse cx="34" cy="59" rx="3.5" ry="3" fill="#7B3A8E"/>
        <ellipse cx="34" cy="68" rx="7" ry="4"  fill="#7B3A8E"/>
        <!-- Teal column (right) -->
        <ellipse cx="54" cy="8"  rx="7" ry="8"  fill="#259990"/>
        <ellipse cx="54" cy="19" rx="3.5" ry="3" fill="#259990"/>
        <ellipse cx="54" cy="28" rx="7" ry="8"  fill="#259990"/>
        <ellipse cx="54" cy="39" rx="3.5" ry="3" fill="#259990"/>
        <ellipse cx="54" cy="48" rx="7" ry="8"  fill="#259990"/>
        <ellipse cx="54" cy="59" rx="3.5" ry="3" fill="#259990"/>
        <ellipse cx="54" cy="68" rx="7" ry="4"  fill="#259990"/>
      </svg>
      <div class="lidera-wordmark">LIDERA</div>
      <div class="lidera-gold-rule"></div>
      <div class="lidera-name">Consultora Lidera</div>
      <div class="lidera-tagline">Consultoría en Gestión de Personas y Organizaciones</div>
    </div>
  </div>
</header>
<main>

<section>
  <h2>Indicadores Generales</h2>
  <div class="kpi-grid">
    <div class="kpi"><label>Trabajadores activos</label><div class="value">{{ stats.total_empleados }}</div><div class="sub">Dotación julio 2026</div></div>
    <div class="kpi gold"><label>Sueldo base promedio</label><div class="value">{{ format_clp(stats.sueldo_base_promedio) }}</div><div class="sub">Mediana: {{ format_clp(stats.sueldo_base_mediana) }}</div></div>
    <div class="kpi gold"><label>Haberes promedio</label><div class="value">{{ format_clp(stats.haberes_promedio) }}</div><div class="sub">Incl. asignaciones e imponibles</div></div>
    <div class="kpi green"><label>Masa salarial SB</label><div class="value">{{ format_mclp(stats.masa_salarial_sb) }}</div><div class="sub">Sueldo base total mensual</div></div>
    <div class="kpi green"><label>Masa salarial haberes</label><div class="value">{{ format_mclp(stats.masa_salarial_haberes) }}</div><div class="sub">Total haberes mensual</div></div>
    <div class="kpi"><label>Dispersión salarial</label><div class="value">{{ format_clp(stats.sueldo_base_min) }}–{{ format_clp(stats.sueldo_base_max) }}</div><div class="sub">Mín.–Máx. sueldo base</div></div>
    <div class="kpi"><label>P25 – P75</label><div class="value">{{ format_clp(stats.p25) }}</div><div class="sub">P75: {{ format_clp(stats.p75) }}</div></div>
    <div class="kpi"><label>Mujeres / Hombres</label><div class="value">{{ genero.mujeres }} / {{ genero.hombres }}</div><div class="sub">{{ "%.0f"|format(genero.mujeres / stats.total_empleados * 100) }}% / {{ "%.0f"|format(genero.hombres / stats.total_empleados * 100) }}%</div></div>
  </div>
</section>

<section>
  <h2>Distribución Salarial</h2>
  <div class="chart-row">
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.distribucion }}" alt="Distribución salarios"></div>
    <div class="chart-box">
      <canvas id="chartDept" height="140"></canvas>
      <p class="chart-hint">↑ Haz clic en una barra para ver los trabajadores del área</p>
    </div>
  </div>
</section>

<section>
  <h2>Escalafón por Nivel de Cargo</h2>
  <div class="chart-row single">
    <div class="chart-box">
      <canvas id="chartNivel" height="90"></canvas>
      <p class="chart-hint">↑ Haz clic en una barra para ver los trabajadores del nivel</p>
    </div>
  </div>
  <br>
  <table>
    <thead><tr>
      <th>Nivel</th><th class="num">N°</th><th class="num">SB Promedio</th>
      <th class="num">SB Mínimo</th><th class="num">SB Máximo</th><th class="num">Haberes Prom.</th>
    </tr></thead>
    <tbody>
    {% for _, row in nivel_df.iterrows() %}
    <tr class="drillable" data-drill="nivel" data-value="{{ row.nivel }}">
      <td>{{ row.nivel }}</td>
      <td class="num">{{ row.empleados }}</td>
      <td class="num">{{ format_clp(row.sb_promedio) }}</td>
      <td class="num">{{ format_clp(row.sb_min) }}</td>
      <td class="num">{{ format_clp(row.sb_max) }}</td>
      <td class="num">{{ format_clp(row.haberes_promedio) }}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</section>

<section>
  <h2>Bandas Salariales</h2>
  <div class="chart-row">
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.bandas }}" alt="Bandas salariales"></div>
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.componentes }}" alt="Componentes haberes"></div>
  </div>
</section>

<section>
  <h2>Análisis Comparativo Interinstitucional</h2>
  <div class="inst-legend">
    <div class="inst-pill"><div class="inst-swatch" style="background:#1C3557"></div><span class="inst-name">CORCUDEC</span></div>
    <div class="inst-pill"><div class="inst-swatch" style="background:#C0392B"></div><span class="inst-name">TMS – Teatro Municipal de Santiago</span></div>
    <div class="inst-pill"><div class="inst-swatch" style="background:#259990"></div><span class="inst-name">CEAC – Universidad de Chile</span></div>
    <div class="inst-pill"><div class="inst-swatch" style="background:#2E7D52;border-radius:50%"></div><span class="inst-name" style="color:#2E7D52">Mediana del sector (referencia)</span></div>
  </div>
  <!-- Nivel 1: mega-categorías -->
  <div id="compLevel1">
    <div class="comp-wrap">
      <canvas id="chartComp" height="85"></canvas>
    </div>
    <p class="chart-hint">↑ Haz clic en una categoría para ver el desglose por cargo</p>
  </div>

  <!-- Nivel 2: cargos homologados dentro de una categoría -->
  <div id="compLevel2" style="display:none">
    <div class="comp-breadcrumb">
      <button class="comp-back-btn" onclick="showCompLevel1()">← Todas las categorías</button>
      <span class="comp-breadcrumb-path">Categoría: <strong id="compL2Cat"></strong></span>
    </div>
    <div class="comp-wrap">
      <canvas id="chartComp2" height="95"></canvas>
    </div>
    <p class="chart-hint">↑ Haz clic en una banda para ver los trabajadores de ese cargo e institución</p>
  </div>

  <div class="info-box" style="margin-top:1rem;font-size:0.78rem">
    <strong>Fuentes:</strong> CORCUDEC Julio 2026 (74 trabajadores activos) · TMS Diciembre 2025 · CEAC Mayo 2026.
    Las bandas muestran el rango P25–P75; el trazo central la mediana.
    Remuneraciones en pesos chilenos (CLP) corrientes.
    Los nombres de trabajadores CORCUDEC están anonimizados en esta vista comparativa.
  </div>
</section>

<section>
  <h2>Comparativo Salarial Orquestal · CORCUDEC vs TMS</h2>
  <div class="inst-legend">
    <div class="inst-pill"><div class="inst-swatch" style="background:#1C3557"></div><span class="inst-name">CORCUDEC</span></div>
    <div class="inst-pill"><div class="inst-swatch" style="background:#C0392B"></div><span class="inst-name">TMS – Teatro Municipal de Santiago</span></div>
  </div>
  <div class="comp-wrap">
    <canvas id="chartOrch" height="90"></canvas>
  </div>
  <p class="chart-hint">↑ Haz clic en una banda para ver el detalle de los músicos</p>
  <div class="info-box" style="margin-top:1rem;font-size:0.78rem">
    <strong>Nota:</strong> Incluye exclusivamente músicos de orquesta. CEAC no cuenta con músicos en planta.
    TMS muestra sólo personal del área Orquesta con cargo homologado. CORCUDEC incluye todos los músicos titulares.
    Los nombres de trabajadores CORCUDEC están anonimizados.
  </div>
</section>

<section>
  <h2>Equidad de Género</h2>
  <div class="chart-row">
    <div class="chart-box" style="grid-column: span 1"><img src="data:image/png;base64,{{ graficas.genero }}" alt="Equidad género"></div>
    <div style="display: flex; flex-direction: column; gap: 1rem; justify-content: center;">
      <div class="kpi"><label>SB promedio hombres</label><div class="value">{{ format_clp(genero.sb_promedio_hombres) }}</div></div>
      <div class="kpi"><label>SB promedio mujeres</label><div class="value">{{ format_clp(genero.sb_promedio_mujeres) }}</div></div>
      <div class="kpi {% if genero.brecha_porcentual|abs < 5 %}green{% else %}gold{% endif %}">
        <label>Brecha salarial (H–M)</label>
        <div class="value">{{ "%.1f"|format(genero.brecha_porcentual) }}%</div>
        <div class="sub">{% if not genero.diferencia_significativa %}No significativa estadísticamente{% else %}Diferencia significativa (p={{ "%.3f"|format(genero.p_value) }}){% endif %}</div>
      </div>
    </div>
  </div>
</section>

<section>
  <h2>Top 10 Remuneraciones (Total Haberes)</h2>
  <table>
    <thead><tr>
      <th>#</th><th>Cargo</th><th>Área</th><th>Nivel</th>
      <th class="num">Sueldo Base</th><th class="num">Total Haberes</th><th class="num">Líquido</th>
    </tr></thead>
    <tbody>
    {% for _, row in top_df.iterrows() %}
    <tr>
      <td>{{ loop.index }}</td>
      <td>{{ row.cargo }}</td>
      <td><span class="tag {% if row.departamento == 'Orquesta' %}tag-orch{% elif row.departamento == 'Administración' %}tag-admin{% else %}tag-dir{% endif %}">{{ row.departamento }}</span></td>
      <td>{{ row.nivel }}</td>
      <td class="num">{{ format_clp(row.sueldo_base) }}</td>
      <td class="num">{{ format_clp(row.total_haberes) }}</td>
      <td class="num">{{ format_clp(row.liquido) }}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</section>

<section>
  <h2>Por Área</h2>
  <table>
    <thead><tr>
      <th>Área</th><th class="num">N°</th><th class="num">SB Promedio</th>
      <th class="num">SB Mediana</th><th class="num">Haberes Prom.</th><th class="num">Masa SB</th>
    </tr></thead>
    <tbody>
    {% for _, row in dept_df.iterrows() %}
    <tr class="drillable" data-drill="departamento" data-value="{{ row.departamento }}">
      <td><span class="tag {% if row.departamento == 'Orquesta' %}tag-orch{% elif row.departamento == 'Administración' %}tag-admin{% else %}tag-dir{% endif %}">{{ row.departamento }}</span></td>
      <td class="num">{{ row.empleados }}</td>
      <td class="num">{{ format_clp(row.sb_promedio) }}</td>
      <td class="num">{{ format_clp(row.sb_mediana) }}</td>
      <td class="num">{{ format_clp(row.haberes_promedio) }}</td>
      <td class="num">{{ format_mclp(row.masa_sb) }}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</section>

<div class="info-box">
  <strong>Fuente:</strong> Imagen de Remuneraciones Julio 2026 · CORCUDEC.<br>
  Incluye 74 trabajadores activos (1 funcionario con licencia excluido). Datos en pesos chilenos (CLP) corrientes.
  Generado: {{ fecha_generacion }}.
</div>

</main>
<footer>Corporación Cultural Universidad de Concepción &nbsp;|&nbsp; Análisis Salarial Interno &nbsp;|&nbsp; {{ fecha_generacion }}</footer>
</div><!-- /reportContent -->

<!-- Modal drill-down -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <div class="modal-header">
      <h3 id="modalTitle">Detalle</h3>
      <div style="display:flex;align-items:center;gap:0.8rem">
        <span class="badge-count" id="modalCount"></span>
        <button class="modal-close" id="modalClose" aria-label="Cerrar">×</button>
      </div>
    </div>
    <div class="modal-body">
      <div class="modal-stats" id="modalStats"></div>
      <div style="overflow-x:auto">
        <table id="modalTable">
          <thead id="modalThead"></thead>
          <tbody id="modalTbody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
// ── Auth ─────────────────────────────────────────────────
const AUTH_USER_HASH = "{{ auth_user_hash }}";
const AUTH_PASS_HASH = "{{ auth_pass_hash }}";

async function sha256(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function showReport() {
  document.getElementById('loginOverlay').classList.add('hidden');
  document.getElementById('reportContent').style.display = 'block';
}

(async () => {
  if (sessionStorage.getItem('corcudec_auth') === '1') { showReport(); return; }
})();

document.getElementById('loginBtn').addEventListener('click', async () => {
  const user = document.getElementById('loginUser').value.trim();
  const pass = document.getElementById('loginPass').value;
  const err  = document.getElementById('loginError');
  err.textContent = '';
  if (!user || !pass) { err.textContent = 'Ingresa usuario y contraseña.'; return; }
  const [uh, ph] = await Promise.all([sha256(user), sha256(pass)]);
  if (uh === AUTH_USER_HASH && ph === AUTH_PASS_HASH) {
    sessionStorage.setItem('corcudec_auth', '1');
    showReport();
  } else {
    err.textContent = 'Credenciales incorrectas.';
    document.getElementById('loginPass').value = '';
  }
});

['loginUser','loginPass'].forEach(id => {
  document.getElementById(id).addEventListener('keydown', e => {
    if (e.key === 'Enter') document.getElementById('loginBtn').click();
  });
});

// ── Data ──────────────────────────────────────────────────
const EMPLEADOS = {{ empleados_json }};

function fmtClp(v) {
  return '$' + Math.round(v).toLocaleString('es-CL');
}
function avg(arr) {
  return arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
}

// ── Dept chart ────────────────────────────────────────────
const DEPT_COLORS = {
  'Orquesta': '#1C3557',
  'Administración': '#2E7D52',
  'Dirección Musical': '#8B1A1A',
};
const deptGroups = {};
EMPLEADOS.forEach(e => {
  (deptGroups[e.departamento] = deptGroups[e.departamento] || []).push(e);
});
const deptLabels = Object.keys(deptGroups).sort(
  (a, b) => avg(deptGroups[a].map(e => e.sueldo_base)) - avg(deptGroups[b].map(e => e.sueldo_base))
);
new Chart(document.getElementById('chartDept'), {
  type: 'bar',
  data: {
    labels: deptLabels,
    datasets: [{
      data: deptLabels.map(d => avg(deptGroups[d].map(e => e.sueldo_base)) / 1e6),
      backgroundColor: deptLabels.map(d => (DEPT_COLORS[d] || '#1C3557') + 'cc'),
      borderColor: deptLabels.map(d => DEPT_COLORS[d] || '#1C3557'),
      borderWidth: 1.5,
      borderRadius: 4,
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    onClick(e, els) { if (els.length) openDrill('departamento', deptLabels[els[0].index]); },
    onHover(e, els) { e.native.target.style.cursor = els.length ? 'pointer' : 'default'; },
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Sueldo Base Promedio por Área', font: { size: 13, weight: 'bold' }, color: '#1a1a2e' },
      tooltip: { callbacks: { label: ctx => ' ' + fmtClp(ctx.raw * 1e6) + ' — clic para detalle' } }
    },
    scales: {
      x: { ticks: { callback: v => '$' + Number(v).toFixed(1) + 'M' }, grid: { color: '#f0ede8' } },
      y: { grid: { display: false } }
    }
  }
});

// ── Nivel chart ───────────────────────────────────────────
const NIVEL_ORDER = ['Director','Concertino','Asistente Concertino','Jefatura',
                     'Jefe de Fila','Asistente de Fila','Tutti','Administrativo'];
function nivelColor(n) {
  if (n === 'Director') return '#8B1A1A';
  if (n === 'Concertino' || n === 'Asistente Concertino') return '#B8892A';
  if (['Jefe de Fila','Asistente de Fila','Tutti'].includes(n)) return '#1C3557';
  return '#2E7D52';
}
const nivelGroups = {};
EMPLEADOS.forEach(e => {
  (nivelGroups[e.nivel] = nivelGroups[e.nivel] || []).push(e);
});
const nivelLabels = NIVEL_ORDER.filter(n => nivelGroups[n]);
new Chart(document.getElementById('chartNivel'), {
  type: 'bar',
  data: {
    labels: nivelLabels,
    datasets: [{
      data: nivelLabels.map(n => avg(nivelGroups[n].map(e => e.sueldo_base)) / 1e6),
      backgroundColor: nivelLabels.map(n => nivelColor(n) + 'cc'),
      borderColor: nivelLabels.map(n => nivelColor(n)),
      borderWidth: 1.5,
      borderRadius: 4,
    }]
  },
  options: {
    responsive: true,
    onClick(e, els) { if (els.length) openDrill('nivel', nivelLabels[els[0].index]); },
    onHover(e, els) { e.native.target.style.cursor = els.length ? 'pointer' : 'default'; },
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Escalafón Salarial por Nivel', font: { size: 13, weight: 'bold' }, color: '#1a1a2e' },
      tooltip: { callbacks: { label: ctx => ' ' + fmtClp(ctx.raw * 1e6) + ' — clic para detalle' } }
    },
    scales: {
      y: { ticks: { callback: v => '$' + Number(v).toFixed(1) + 'M' }, grid: { color: '#f0ede8' } },
      x: { grid: { display: false } }
    }
  }
});

// ── Modal ─────────────────────────────────────────────────
const overlay = document.getElementById('modalOverlay');

function openDrill(campo, valor) {
  const rows = EMPLEADOS.filter(e => e[campo] === valor);
  const sbs = rows.map(e => e.sueldo_base);
  const habs = rows.map(e => e.total_haberes);

  document.getElementById('modalTitle').textContent = valor;
  document.getElementById('modalCount').textContent = rows.length + ' trabajadores';

  document.getElementById('modalStats').innerHTML = `
    <div class="modal-stat"><label>SB Promedio</label><div class="val">${fmtClp(avg(sbs))}</div></div>
    <div class="modal-stat"><label>SB Mínimo</label><div class="val">${fmtClp(Math.min(...sbs))}</div></div>
    <div class="modal-stat"><label>SB Máximo</label><div class="val">${fmtClp(Math.max(...sbs))}</div></div>
    <div class="modal-stat"><label>Haberes Prom.</label><div class="val">${fmtClp(avg(habs))}</div></div>
  `;

  const extraHeader = campo === 'departamento' ? 'Nivel' : 'Área';
  document.getElementById('modalThead').innerHTML = `<tr>
    <th>#</th><th>Cargo</th><th>${extraHeader}</th><th>Sexo</th>
    <th class="num">Sueldo Base</th><th class="num">Total Haberes</th><th class="num">Líquido</th>
  </tr>`;

  const sorted = [...rows].sort((a, b) => b.sueldo_base - a.sueldo_base);
  document.getElementById('modalTbody').innerHTML = sorted.map((e, i) => {
    const extra = campo === 'departamento' ? e.nivel : e.departamento;
    return `<tr>
      <td>${i + 1}</td>
      <td>${e.cargo}</td>
      <td>${extra}</td>
      <td>${e.sexo === 'M' ? 'H' : 'M'}</td>
      <td class="num">${fmtClp(e.sueldo_base)}</td>
      <td class="num">${fmtClp(e.total_haberes)}</td>
      <td class="num">${fmtClp(e.liquido)}</td>
    </tr>`;
  }).join('');

  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeDrill() {
  overlay.classList.remove('open');
  document.body.style.overflow = '';
}

document.getElementById('modalClose').addEventListener('click', closeDrill);
overlay.addEventListener('click', e => { if (e.target === overlay) closeDrill(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrill(); });

document.querySelectorAll('tr.drillable').forEach(tr => {
  tr.addEventListener('click', () => openDrill(tr.dataset.drill, tr.dataset.value));
});

// ── Comparative chart ─────────────────────────────────────
const COMP_DATA = {{ comp_json }};

(function buildCompChart() {
  const CATS  = ['Dirección y Gestión','Artístico / Músicos','Técnico / Escénico','Administrativo / Apoyo'];
  const INSTS = ['CORCUDEC','TMS','CEAC'];
  const COLORS = { CORCUDEC: '#1C3557', TMS: '#C0392B', CEAC: '#259990' };
  const CAT_LABELS = [
    ['Dirección','y Gestión'],
    ['Artístico','Músicos'],
    ['Técnico','Escénico'],
    ['Administrativo','Apoyo'],
  ];

  // Band datasets: floating bars [P25, P75]
  const bandDS = INSTS.map(inst => ({
    type: 'bar',
    label: inst,
    data: CATS.map(cat => {
      const s = COMP_DATA.stats[cat][inst];
      return s ? [s.p25 / 1e6, s.p75 / 1e6] : null;
    }),
    backgroundColor: COLORS[inst] + '55',
    borderColor: COLORS[inst],
    borderWidth: 1.5,
    borderRadius: 3,
    barPercentage: 0.72,
    categoryPercentage: 0.88,
  }));

  // Median stripe: thin floating bar overlaid on same stack
  const medDS = INSTS.map(inst => ({
    type: 'bar',
    label: '__med_' + inst,
    data: CATS.map(cat => {
      const s = COMP_DATA.stats[cat][inst];
      if (!s) return null;
      const half = s.median * 0.016 / 1e6;
      return [s.median / 1e6 - half, s.median / 1e6 + half];
    }),
    backgroundColor: COLORS[inst],
    borderColor: COLORS[inst],
    borderWidth: 0,
    borderRadius: 0,
    barPercentage: 0.72,
    categoryPercentage: 0.88,
  }));

  // Sector benchmark: combined median of all 3 institutions per category
  const benchDS = {
    type: 'line',
    label: 'Mediana del sector',
    data: CATS.map(cat => {
      const allVals = INSTS.flatMap(inst =>
        (COMP_DATA.empleados[inst] || [])
          .filter(e => e.categoria === cat)
          .map(e => e.remuneracion)
      ).sort((a, b) => a - b);
      if (!allVals.length) return null;
      const mid = Math.floor(allVals.length / 2);
      return (allVals.length % 2 === 0
        ? (allVals[mid - 1] + allVals[mid]) / 2
        : allVals[mid]) / 1e6;
    }),
    backgroundColor: '#2E7D52',
    borderColor: '#2E7D52',
    borderWidth: 0,
    pointRadius: 9,
    pointHoverRadius: 12,
    pointBackgroundColor: '#2E7D52',
    pointBorderColor: '#fff',
    pointBorderWidth: 2.5,
    showLine: false,
    order: 0,
  };

  const compChart = new Chart(document.getElementById('chartComp'), {
    data: { labels: CAT_LABELS, datasets: [...bandDS, ...medDS, benchDS] },
    options: {
      responsive: true,
      onClick(e, els) {
        if (!els.length) return;
        const ds = compChart.data.datasets[els[0].datasetIndex];
        if (ds.label.startsWith('__med_') || ds.label === 'Mediana del sector') return;
        showCompLevel2(CATS[els[0].index]);
      },
      onHover(e, els) {
        const skip = ['__med_', 'Mediana del sector'];
        const vis = els.some(el => !skip.some(s => compChart.data.datasets[el.datasetIndex].label.startsWith(s)));
        e.native.target.style.cursor = vis ? 'pointer' : 'default';
      },
      plugins: {
        legend: {
          labels: {
            filter: item => !item.text.startsWith('__med_'),
            boxWidth: 13, boxHeight: 13,
            color: '#1a1a2e', font: { size: 12, weight: '600' },
          },
        },
        title: {
          display: true,
          text: 'Bandas Salariales por Categoría Funcional  ·  P25 — Mediana — P75',
          font: { size: 13, weight: 'bold' }, color: '#1a1a2e',
        },
        tooltip: {
          filter: item => !item.dataset.label.startsWith('__med_'),
          callbacks: {
            label(ctx) {
              if (ctx.dataset.label === 'Mediana del sector') {
                const cat = CATS[ctx.dataIndex];
                const n = INSTS.reduce((acc, inst) =>
                  acc + (COMP_DATA.empleados[inst] || []).filter(e => e.categoria === cat).length, 0);
                return `Mediana del sector: ${fmtClp(ctx.raw * 1e6)}  (n total=${n})`;
              }
              const inst = ctx.dataset.label;
              const cat = CATS[ctx.dataIndex];
              const s = COMP_DATA.stats[cat] && COMP_DATA.stats[cat][inst];
              if (!s) return inst + ': sin datos';
              return [
                inst + '  (n=' + s.n + ')',
                '  P25: ' + fmtClp(s.p25) + '   Mediana: ' + fmtClp(s.median) + '   P75: ' + fmtClp(s.p75),
              ];
            },
          },
        },
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 11 } } },
        y: {
          ticks: { callback: v => '$' + Number(v).toFixed(1) + 'M' },
          grid: { color: '#f0ede8' },
          title: { display: true, text: 'Millones CLP', color: '#888', font: { size: 11 } },
        },
      },
    },
  });

  // ── Level 2: desglose por cargo homologado ────────────────
  let compChart2 = null;

  window.showCompLevel1 = function() {
    document.getElementById('compLevel1').style.display = '';
    document.getElementById('compLevel2').style.display = 'none';
  };

  window.showCompLevel2 = function(cat) {
    document.getElementById('compL2Cat').textContent = cat;
    document.getElementById('compLevel1').style.display = 'none';
    document.getElementById('compLevel2').style.display = '';

    // Collect all cargo_hom values for this category across all institutions
    const cargoSet = new Set();
    INSTS.forEach(inst => {
      (COMP_DATA.empleados[inst] || [])
        .filter(e => e.categoria === cat)
        .forEach(e => cargoSet.add(e.cargo_hom));
    });

    // Sort: put 'Sin equivalente' last, rest alphabetically
    const cargoLabels = [...cargoSet].sort((a, b) => {
      if (a === 'Sin equivalente') return 1;
      if (b === 'Sin equivalente') return -1;
      return a.localeCompare(b, 'es');
    });

    // Helper: stats for a set of values
    function calcStats(vals) {
      if (!vals.length) return null;
      const s = [...vals].sort((a, b) => a - b);
      const mid = i => s[Math.min(i, s.length - 1)];
      const p = frac => mid(Math.floor(s.length * frac));
      const med = s.length % 2 === 0
        ? (s[s.length / 2 - 1] + s[s.length / 2]) / 2
        : s[Math.floor(s.length / 2)];
      return { n: s.length, min: s[0], max: s[s.length-1],
               median: med, p25: p(0.25), p75: p(0.75) };
    }

    // Band + median datasets per institution
    const l2BandDS = INSTS.map(inst => ({
      type: 'bar',
      label: inst,
      data: cargoLabels.map(ch => {
        const vals = (COMP_DATA.empleados[inst] || [])
          .filter(e => e.categoria === cat && e.cargo_hom === ch)
          .map(e => e.remuneracion);
        const s = calcStats(vals);
        return s ? [s.p25 / 1e6, s.p75 / 1e6] : null;
      }),
      backgroundColor: COLORS[inst] + '55',
      borderColor: COLORS[inst],
      borderWidth: 1.5,
      borderRadius: 3,
      barPercentage: 0.72,
      categoryPercentage: 0.88,
    }));

    const l2MedDS = INSTS.map(inst => ({
      type: 'bar',
      label: '__med2_' + inst,
      data: cargoLabels.map(ch => {
        const vals = (COMP_DATA.empleados[inst] || [])
          .filter(e => e.categoria === cat && e.cargo_hom === ch)
          .map(e => e.remuneracion);
        const s = calcStats(vals);
        if (!s) return null;
        const half = s.median * 0.016 / 1e6;
        return [s.median / 1e6 - half, s.median / 1e6 + half];
      }),
      backgroundColor: COLORS[inst],
      borderColor: COLORS[inst],
      borderWidth: 0,
      borderRadius: 0,
      barPercentage: 0.72,
      categoryPercentage: 0.88,
    }));

    if (compChart2) compChart2.destroy();
    compChart2 = new Chart(document.getElementById('chartComp2'), {
      data: { labels: cargoLabels, datasets: [...l2BandDS, ...l2MedDS] },
      options: {
        responsive: true,
        onClick(e, els) {
          if (!els.length) return;
          const ds = compChart2.data.datasets[els[0].datasetIndex];
          if (ds.label.startsWith('__med2_')) return;
          openCompDrill(cargoLabels[els[0].index], ds.label, 'cargo_hom');
        },
        onHover(e, els) {
          const vis = els.some(el => !compChart2.data.datasets[el.datasetIndex].label.startsWith('__med2_'));
          e.native.target.style.cursor = vis ? 'pointer' : 'default';
        },
        plugins: {
          legend: {
            labels: {
              filter: item => !item.text.startsWith('__med2_'),
              boxWidth: 13, boxHeight: 13,
              color: '#1a1a2e', font: { size: 12, weight: '600' },
            },
          },
          title: {
            display: true,
            text: 'Desglose por Cargo Homologado  ·  ' + cat,
            font: { size: 13, weight: 'bold' }, color: '#1a1a2e',
          },
          tooltip: {
            filter: item => !item.dataset.label.startsWith('__med2_'),
            callbacks: {
              label(ctx) {
                const inst = ctx.dataset.label;
                const ch = cargoLabels[ctx.dataIndex];
                const vals = (COMP_DATA.empleados[inst] || [])
                  .filter(e => e.categoria === cat && e.cargo_hom === ch)
                  .map(e => e.remuneracion);
                const s = calcStats(vals);
                if (!s) return inst + ': sin datos';
                return [
                  inst + '  (n=' + s.n + ')',
                  '  P25: ' + fmtClp(s.p25) + '   Mediana: ' + fmtClp(Math.round(s.median)) + '   P75: ' + fmtClp(s.p75),
                ];
              },
            },
          },
        },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 11 }, maxRotation: 35 } },
          y: {
            ticks: { callback: v => '$' + Number(v).toFixed(1) + 'M' },
            grid: { color: '#f0ede8' },
            title: { display: true, text: 'Millones CLP', color: '#888', font: { size: 11 } },
          },
        },
      },
    });
  };

  // ── Comparativo Orquestal CORCUDEC vs TMS ────────────────────────────────
  (function() {
    const ORCH_ORDER = ['Concertino','Asistente Concertino','Jefe de Fila','Asistente de Fila','Músico Tutti','Músico'];
    const ORCH_INSTS = ['CORCUDEC','TMS'];
    const ORCH_COLOR  = { CORCUDEC:'#1C3557', TMS:'#C0392B' };
    const ORCH_ALPHA  = { CORCUDEC:'rgba(28,53,87,0.22)', TMS:'rgba(192,57,43,0.22)' };

    const orchEmps = {
      CORCUDEC: (COMP_DATA.empleados['CORCUDEC'] || []).filter(e => e.categoria === 'Artístico / Músicos'),
      TMS:      (COMP_DATA.empleados['TMS']       || []).filter(e => ORCH_ORDER.includes(e.cargo_hom)),
    };

    function calcSt(vals) {
      if (!vals.length) return null;
      const s = [...vals].sort((a,b) => a-b);
      const p = f => s[Math.min(Math.floor(s.length*f), s.length-1)];
      const med = s.length%2===0 ? (s[s.length/2-1]+s[s.length/2])/2 : s[Math.floor(s.length/2)];
      return { n:s.length, p25:p(0.25), median:med, p75:p(0.75), max:s[s.length-1] };
    }

    const bandDS = ORCH_INSTS.map(inst => ({
      label: inst, type:'bar',
      backgroundColor: ORCH_ALPHA[inst], borderColor: ORCH_COLOR[inst],
      borderWidth:1.5, borderSkipped:false,
      barPercentage:0.38, categoryPercentage:0.8,
      data: ORCH_ORDER.map(role => {
        const st = calcSt(orchEmps[inst].filter(e=>e.cargo_hom===role).map(e=>e.remuneracion));
        return st ? [st.p25, st.p75] : null;
      }),
    }));

    const medDS = ORCH_INSTS.map(inst => ({
      label:'__om_'+inst, type:'bar',
      backgroundColor: ORCH_COLOR[inst], borderWidth:0, borderSkipped:false,
      barPercentage:0.38, categoryPercentage:0.8,
      data: ORCH_ORDER.map(role => {
        const st = calcSt(orchEmps[inst].filter(e=>e.cargo_hom===role).map(e=>e.remuneracion));
        if (!st) return null;
        const h = Math.max((st.p75-st.p25)*0.04, 20000);
        return [st.median-h, st.median+h];
      }),
    }));

    const orchChart = new Chart(document.getElementById('chartOrch'), {
      type:'bar',
      data:{ labels: ORCH_ORDER, datasets:[...bandDS,...medDS] },
      options:{
        responsive:true, animation:false,
        plugins:{
          legend:{ labels:{ filter: i=>!i.text.startsWith('__'), color:'#444', font:{size:12} }},
          title:{
            display:true,
            text:'Bandas Salariales por Posición Orquestal  ·  P25 — Mediana — P75',
            color:'#1C3557', font:{size:13,weight:'600'}, padding:{bottom:16},
          },
          tooltip:{
            callbacks:{
              label(ctx) {
                if (ctx.dataset.label.startsWith('__')) return null;
                const inst = ctx.dataset.label;
                const role = ORCH_ORDER[ctx.dataIndex];
                const st = calcSt(orchEmps[inst].filter(e=>e.cargo_hom===role).map(e=>e.remuneracion));
                if (!st) return inst+': sin datos';
                return [inst+' (n='+st.n+')',
                  '  P25: '+fmtClp(st.p25),
                  '  Med: '+fmtClp(Math.round(st.median)),
                  '  P75: '+fmtClp(st.p75)];
              }
            }
          }
        },
        onClick(e, els) {
          if (!els.length) return;
          const ds = orchChart.data.datasets[els[0].datasetIndex];
          if (ds.label.startsWith('__')) return;
          openOrchDrill(ORCH_ORDER[els[0].index], ds.label);
        },
        scales:{
          x:{ stacked:false, ticks:{color:'#444',font:{size:11}}, grid:{display:false} },
          y:{
            ticks:{ color:'#888', callback: v=>'$'+(v/1e6).toFixed(1)+'M' },
            grid:{ color:'#f0ede8' },
            title:{ display:true, text:'Millones CLP', color:'#888', font:{size:11} },
          }
        }
      }
    });

    window.openOrchDrill = function(role, inst) {
      const emps = orchEmps[inst].filter(e=>e.cargo_hom===role);
      const rems = emps.map(e=>e.remuneracion).sort((a,b)=>a-b);
      function pct(a,f){ return a[Math.min(Math.floor(a.length*f),a.length-1)]; }
      const med = rems.length%2===0?(rems[rems.length/2-1]+rems[rems.length/2])/2:rems[Math.floor(rems.length/2)];
      const showName = inst!=='CORCUDEC';
      document.getElementById('modalTitle').textContent = role+'  ·  '+inst;
      document.getElementById('modalCount').textContent = emps.length+' músicos';
      document.getElementById('modalStats').innerHTML = !rems.length
        ? '<p style="color:var(--muted)">Sin datos.</p>'
        : `<div class="modal-stat"><label>Mediana</label><div class="val">${fmtClp(Math.round(med))}</div></div>
           <div class="modal-stat"><label>P25</label><div class="val">${fmtClp(pct(rems,0.25))}</div></div>
           <div class="modal-stat"><label>P75</label><div class="val">${fmtClp(pct(rems,0.75))}</div></div>
           <div class="modal-stat"><label>Máximo</label><div class="val">${fmtClp(rems[rems.length-1])}</div></div>`;
      document.getElementById('modalThead').innerHTML = `<tr>
        <th>#</th>${showName?'<th>Nombre</th>':''}
        <th>Cargo original</th><th>Cargo homologado</th><th class="num">Remuneración</th>
      </tr>`;
      const sorted = [...emps].sort((a,b)=>b.remuneracion-a.remuneracion);
      document.getElementById('modalTbody').innerHTML = sorted.map((e,i)=>`<tr>
        <td>${i+1}</td>${showName?'<td>'+e.nombre+'</td>':''}
        <td>${e.cargo}</td><td>${e.cargo_hom}</td>
        <td class="num">${fmtClp(e.remuneracion)}</td>
      </tr>`).join('');
      overlay.classList.add('open');
      document.body.style.overflow='hidden';
    };
  })();

  // ── Level 3: modal de empleados (desde nivel 1 o nivel 2) ─
  window.openCompDrill = function(filterVal, inst, filterField) {
    filterField = filterField || 'categoria';
    const emps = (COMP_DATA.empleados[inst] || []).filter(e => e[filterField] === filterVal);
    const rems = emps.map(e => e.remuneracion).sort((a, b) => a - b);

    // Inline stats
    function pct(arr, f) { return arr[Math.min(Math.floor(arr.length * f), arr.length - 1)]; }
    const med = rems.length % 2 === 0
      ? (rems[rems.length/2-1] + rems[rems.length/2]) / 2 : rems[Math.floor(rems.length/2)];
    const hasData = rems.length > 0;

    const showName = inst !== 'CORCUDEC';
    document.getElementById('modalTitle').textContent = filterVal + '  ·  ' + inst;
    document.getElementById('modalCount').textContent = emps.length + ' trabajadores';

    document.getElementById('modalStats').innerHTML = !hasData
      ? '<p style="color:var(--muted)">Sin datos para esta combinación.</p>'
      : `<div class="modal-stat"><label>Mediana</label><div class="val">${fmtClp(Math.round(med))}</div></div>
         <div class="modal-stat"><label>P25</label><div class="val">${fmtClp(pct(rems, 0.25))}</div></div>
         <div class="modal-stat"><label>P75</label><div class="val">${fmtClp(pct(rems, 0.75))}</div></div>
         <div class="modal-stat"><label>Máximo</label><div class="val">${fmtClp(rems[rems.length-1])}</div></div>`;

    document.getElementById('modalThead').innerHTML = `<tr>
      <th>#</th>${showName ? '<th>Nombre</th>' : ''}
      <th>Cargo</th><th>Cargo Homologado</th><th>Área</th><th class="num">Remuneración</th>
    </tr>`;

    const sorted = [...emps].sort((a, b) => b.remuneracion - a.remuneracion);
    document.getElementById('modalTbody').innerHTML = sorted.map((e, i) => `<tr>
      <td>${i + 1}</td>
      ${showName ? '<td>' + e.nombre + '</td>' : ''}
      <td>${e.cargo}</td><td>${e.cargo_hom}</td><td>${e.area}</td>
      <td class="num">${fmtClp(e.remuneracion)}</td>
    </tr>`).join('');

    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
})();
</script>
</body>
</html>
"""


def generar_reporte(stats, genero, nivel_df, dept_df, top_df, graficas, ruta_salida, df=None,
                    auth_user_hash='', auth_pass_hash=''):
    def format_clp(v):
        if v is None or (isinstance(v, float) and v != v):
            return '$0'
        return f'${int(v):,}'.replace(',', '.')

    def format_mclp(v):
        return f'${v/1_000_000:.1f}M'

    cols = ['cargo', 'departamento', 'nivel', 'sexo', 'sueldo_base', 'total_haberes', 'liquido']
    if df is not None:
        records = df[cols].to_dict('records')
        for r in records:
            for k in ('sueldo_base', 'total_haberes', 'liquido'):
                r[k] = int(r[k]) if r[k] == r[k] else 0
    else:
        records = []
    empleados_json = json.dumps(records, ensure_ascii=False)

    comp_json = _build_comp_json(df) if df is not None else json.dumps({'stats': {}, 'empleados': {}})

    tpl = Template(TEMPLATE_HTML)
    html = tpl.render(
        stats=stats,
        genero=genero,
        nivel_df=nivel_df,
        dept_df=dept_df,
        top_df=top_df,
        graficas=graficas,
        format_clp=format_clp,
        format_mclp=format_mclp,
        empleados_json=empleados_json,
        comp_json=comp_json,
        auth_user_hash=auth_user_hash,
        auth_pass_hash=auth_pass_hash,
        fecha_generacion=__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M'),
    )
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    return ruta_salida
