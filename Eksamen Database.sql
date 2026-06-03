-- Opprett ny database
CREATE DATABASE EksamenDB;
GO

USE EksamenDB;
GO

-- Brukertabell
CREATE TABLE Bruker (
    Id        INT PRIMARY KEY IDENTITY,
    Brukernavn NVARCHAR(50) NOT NULL UNIQUE,
    Passord   NVARCHAR(255) NOT NULL,
    Epost     NVARCHAR(100) NOT NULL,
    Rolle     NVARCHAR(10) NOT NULL CHECK(Rolle IN ('elev','laerer','admin')),
    Opprettet DATETIME DEFAULT GETDATE()
);

-- Saktabell
CREATE TABLE Sak (
    Id          INT PRIMARY KEY IDENTITY,
    ElevId      INT NOT NULL REFERENCES Bruker(Id),
    Tittel      NVARCHAR(100) NOT NULL,
    Beskrivelse NVARCHAR(MAX) NOT NULL,
    Kategori    NVARCHAR(10) NOT NULL CHECK(Kategori IN ('kritisk','viktig','lav')),
    Status      NVARCHAR(15) NOT NULL DEFAULT 'aapen' CHECK(Status IN ('aapen','paagaar','loest')),
    Opprettet   DATETIME DEFAULT GETDATE()
);

-- Svartabell
CREATE TABLE Svar (
    Id        INT PRIMARY KEY IDENTITY,
    SakId     INT NOT NULL REFERENCES Sak(Id),
    LaererId  INT NOT NULL REFERENCES Bruker(Id),
    Innhold   NVARCHAR(MAX) NOT NULL,
    Opprettet DATETIME DEFAULT GETDATE()
);

-- Loggtabell (autentiseringslogg - krav i oppgaven)
CREATE TABLE Logg (
    Id        INT PRIMARY KEY IDENTITY,
    BrukerId  INT REFERENCES Bruker(Id),
    Handling  NVARCHAR(100) NOT NULL,
    Tidspunkt DATETIME DEFAULT GETDATE()
);
GO

