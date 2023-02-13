from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = "Weenat Test Backend"
    contact: dict = {"contact": "dev@weenat.com"}
    version: str = "1.0"
    description: str = """
    
        ## Ennoncé
    
    Cet exercice vise à mettre en place:
    
    - un script de récupération de donnée depuis une tierce partie puis stockage dans une base de donnée;
    
    - une interface pour afficher les données récupérées;
    
    Le service devra être écrit en python. L'analyse des données devra utiliser les librairies numpy ou pandas.
    
    """


settings = Settings()
