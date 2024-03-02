"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame (son las tablas).
    #
    filenames = glob.glob(f"{input_directory}/*.txt")

    #dataframes = []
    #for filename in filenames:
    #    dataframe.append(pd.read_csv(filenames[0], sep="\t", header=None, names=["text"]))  #Tomo un nombre de archivo filename, lee el archivo y me lo devuelve en DatFrame
    #lo hago con List comprehensions:
    dataframes = [
        pd.read_csv(filename, sep="\t", header=None, names=["text"])
        for filename in filenames
    ]
    concatenated_df = pd.concat(dataframes, ignore_index=True)
    return concatenated_df

# Elimine la puntuación y convierta el texto a minúsculas.
def clean_text(dataframe):
    """Text cleaning"""
    dataframe = dataframe.copy()    #se crea copia por seguridad
    dataframe["text"] = dataframe["text"].str.lower()
    dataframe["text"] = dataframe["text"].str.replace(".", "")
    dataframe["text"] = dataframe["text"].str.replace(",", "")
    return dataframe

def count_words(dataframe):
    """Word count"""
    dataframe = dataframe.copy() 
    dataframe["text"] = dataframe["text"].str.split()   #para crear una lista en cada fila separando las palabras
    dataframe = dataframe.explode("text")               #para sacar c/palabra de las listas
    dataframe["count"] = 1
    
    dataframe = dataframe.groupby("text").agg({"count": "sum"})  #agrupeme por texto y sumeme la columna count
                                                      
    
    return dataframe

def count_words_(dataframe):
    """Word count"""
    dataframe = dataframe.copy() 
    dataframe["text"] = dataframe["text"].str.split()   #para crear una lista en cada fila separando las palabras
    dataframe = dataframe.explode("text")               #para sacar c/palabra de las listas
    dataframe = dataframe["text"].value_counts()      
    return dataframe


def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, sep="\t", index=True, header=False) #csv es un archivo de texto separado por comas (comma-separated value)


def run(input_directory, output_filename):
    """Call all functions."""
    df = load_input(input_directory)
    df = clean_text(df)
    df = count_words_(df)
    save_output(df, output_filename)


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
