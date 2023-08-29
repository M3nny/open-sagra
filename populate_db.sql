create database sagra;
use sagra;

create table os_operatore ( 
    IDOperatore char(6) NOT NULL primary key,
    NomeOperatore varchar(64) NOT NULL,
    CognomeOperatore varchar(64) NOT NULL,
    Email varchar(256) NOT NULL,
    Password varchar(256) NOT NULL, 
    Ruolo text NOT NULL
);

create table os_alimento (
    IDAlimento char(4) NOT NULL primary key,
    NomeAlimento varchar(64) NOT NULL,
    PrezzoVendita float(100,2) NOT NULL,
    Categoria varchar(256) NOT NULL,
    Festivo boolean,
    Alcolico boolean
);


create table os_ingrediente (
    IDIngrediente char(4) NOT NULL primary key,
    NomeIngrediente varchar(64) NOT NULL,
    Qta int NOT NULL
);


create table os_composizione (
    IDAlimento char(4) NOT NULL,
    IDIngrediente char(4) NOT NULL,
    Qta int NOT NULL,
    PRIMARY KEY (IDAlimento, IDIngrediente),
    FOREIGN KEY (IDAlimento) REFERENCES os_alimento(IDAlimento) ON DELETE CASCADE,
    FOREIGN KEY (IDIngrediente) REFERENCES os_ingrediente(IDIngrediente) ON DELETE CASCADE
);

create table os_ordine (
    IDOperatore char(6) NOT NULL,
    IDAlimento char(4) NOT NULL,
    NOrdine int NOT NULL,
    Qta int NOT NULL,
    PRIMARY KEY (IDOperatore, IDAlimento, NOrdine),
    FOREIGN KEY (IDOperatore) REFERENCES os_operatore(IDOperatore) ON DELETE CASCADE,
    FOREIGN KEY (IDAlimento) REFERENCES os_alimento(IDAlimento) ON DELETE CASCADE
);


insert into os_alimento values
    ("p001", "Panino", 2.50, "piatto", null, null),
    ("p002", "Panin onto", 4.00, "piatto", null, null),
    ("p003", "Tagliata e Patatine", 10.00, "piatto", null, null),
    ("p004", "Piatto Costine e contorni", 9.00, "piatto", null, null),
    ("p005", "Piatto BOCIA", 5.00, "piatto", null, null),
    ("p006", "Patatine", 1.50, "piatto", null, null),
    ("p007", "Piatto misto con contorni e polenta", 8.00, "piatto", true, null),
    ("p008", "Braciola con contorni e polenta", 8.00, "piatto", true, null);

insert into os_alimento values 
    ("d001", "Fetta di dolce", 1.50, "dolce", null, null),
    ("d002", "Vin brule", 1.50, "dolce", null, null),
    ("d003", "Grappa prugna", 1.50, "dolce", null, null);

insert into os_alimento values
    ("b001", "Birra", 2.00, "bevanda", null, true),
    ("b002", "Birra speciale 0,5", 4.00, "bevanda", true, true),
    ("b003", "Acqua 0,5 litro naturale", 0.50, "bevanda", null, false),
    ("b004", "Acqua 0,5 litro frizzante", 0.50, "bevanda", null, false),
    ("b005", "Vino Rosso/Bianco spina", 0.80, "bevanda", null, true),
    ("b006", "Vino DOC bicchiere", 2.00, "bevanda", null, true),
    ("b007", "Caraffa Vino Spina 1/2 litro", 2.50, "bevanda", null, true),
    ("b008", "Caraffa Vino Spina 1 litro", 4.00, "bevanda", null, true),
    ("b009", "Bottiglia Vino DOC", 10.00, "bevanda", null, true),
    ("b010", "Bibita in lattina", 1.50, "bevanda", null, false),
    ("b011", "Caffe", 1.00, "bevanda", null, false),
    ("b012", "Caffe Corretto", 1.30, "bevanda", null, true),
    ("b013", "Spriz Aperol", 2.00, "bevanda", null, true);

insert into os_ingrediente values
    ("i000", "comprato", 500),
    ("i001", "patatine", 200),
    ("i002", "olio da friggere", 40),
    ("i003", "formaggio", 50),
    ("i004", "sopressa", 20),
    ("i005", "salsiccia", 300),
    ("i006", "peperoni", 300),
    ("i007", "cipolla", 300),
    ("i008", "manzo per tagliata", 200),
    ("i009", "costine di maiale", 300),
    ("i010", "polenta", 400),
    ("i011", "fagioli", 200),
    ("i012", "funghi", 200),
    ("i013", "pancetta", 30),
    ("i014", "wurstel", 400),
    ("i015", "pagnotta", 500),
    ("i016", "braciola", 150),
    ("i017", "bootiglia vino DOC", 150),
    ("i018", "prosecco", 150),
    ("i019", "aperol", 150),
    ("i020", "grappa", 150),
    ("i021", "caffe", 150),
    ("i022", "birra", 150),
    ("i023", "birra sp", 150),
    ("i024", "acqua n", 150),
    ("i025", "acqua f", 150),
    ("i026", "lattina", 150),
    ("i027", "fetta di dolce", 150);
    

insert into os_composizione values 
    ("p001", "i015", 1),
    ("p001", "i003", 2),
    ("p001", "i004", 4),
    ("p002", "i015", 1),
    ("p002", "i005", 1),
    ("p002", "i006", 1),
    ("p002", "i007", 1),
    ("p003", "i008", 1),
    ("p003", "i001", 1),
    ("p004", "i009", 4),
    ("p004", "i011", 1),
    ("p004", "i012", 1),
    ("p005", "i014", 2),
    ("p005", "i005", 1),
    ("p005", "i001", 1),
    ("p006", "i001", 1),
    ("p007", "i005", 1),
    ("p007", "i009", 4),
    ("p007", "i013", 1),
    ("p007", "i014", 3),
    ("p007", "i010", 1),
    ("p007", "i011", 1),
    ("p007", "i012", 1),
    ("p008", "i016", 1),
    ("p008", "i010", 1),
    ("p008", "i011", 1),
    ("p008", "i012", 1),
    ("b001", "i022", 1),
    ("b002", "i023", 1),
    ("b003", "i024", 1),
    ("b004", "i025", 1),
    ("b005", "i000", 1),
    ("b006", "i000", 1),
    ("b007", "i000", 1),
    ("b008", "i000", 1),
    ("b009", "i017", 1),
    ("b010", "i026", 1),
    ("b011", "i021", 1),
    ("b012", "i021", 1),
    ("b012", "i020", 1),
    ("b013", "i018", 1),
    ("b013", "i019", 1),
    ("d001", "i027", 1),
    ("d002", "i000", 1),
    ("d003", "i000", 1);

insert into os_operatore values ("a00001", 
    "Antonio", 
    "Rossi", 
    "placeholder@mail", 
    "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86", 
    "admin"
);