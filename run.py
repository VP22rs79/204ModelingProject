from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
import json
from nnf import Var, true, false

# These two lines make sure a faster SAT solver is used.
from nnf import config

# list of all the genres and keys.
genres = [
    "house",
    "hip_hop",
    "trap",
    "jungle_dnb",
    "classical",
    "dubstep",
    "folk",
    "classic_rock",
    "alt_rock",
    "dancehall",
    "afrobeats",
    "country",
    "techno",
    "dance_pop",
    "pop_rock",
]

keys = [
    "Cmaj",
    "Gmaj",
    "Amaj",
    "Dmaj",
    "Emaj",
    "Bmaj",
    "Fmaj",
    "Cbmaj",
    "Gbmaj",
    "Abmaj",
    "Dbmaj",
    "Ebmaj",
    "Dbmaj",
    "Bbmaj",
    "Cmin",
    "Gmin",
    "Amin",
    "Dmin",
    "Emin",
    "Dmin",
    "Bmin",
    "Fmin",
    "Gbmin",
    "Abmin",
    "Dbmin",
    "Ebmin",
    "Dbmin",
    "Bbmin",
]


# the class song which encapsulates all the data tied to a song.
class Song:
    def __init__(self, Name, Artist, BPM, Key, Genre):
        self.name = Name
        self.artist = Artist
        self.bpm = BPM
        self.key = Key
        self.genre = Genre

    def __str__(self):
        return (
            f"Name: {self.name}, \n"
            f"Artist: {self.artist}, \n"
            f"BPM: {self.bpm}, \n"
            f"Key: {self.key}, \n"
            f"Genre: {self.genre}"
        )


config.sat_backend = "kissat"
E = Encoding()


@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"


# class variables to store the genres and keys of the two songs and all the genres and keys
s1_genre = ""
s2_genre = ""
s1_key = ""
s2_key = ""
s1_keys = {}
s2_keys = {}
s1_genres = {}
s2_genres = {}


# function to declutter code and instantiate all the propositions
def init_props():
    global s1_keys, s2_keys, s1_genres, s2_genres
    # all the keys and genres are stored in dictionaries for easy access later on.
    s1_keys = {
        "s1Cmaj": BasicPropositions("s1Cmaj"),
        "s1Gmaj": BasicPropositions("s1Gmaj"),
        "s1Amaj": BasicPropositions("s1Amaj"),
        "s1Dmaj": BasicPropositions("s1Dmaj"),
        "s1Emaj": BasicPropositions("s1Emaj"),
        "s1Dmaj": BasicPropositions("s1Dmaj"),
        "s1Bmaj": BasicPropositions("s1Bmaj"),
        "s1Fmaj": BasicPropositions("s1Fmaj"),
        "s1Cbmaj": BasicPropositions("s1Cbmaj"),
        "s1Gbmaj": BasicPropositions("s1Gbmaj"),
        "s1Abmaj": BasicPropositions("s1Abmaj"),
        "s1Dbmaj": BasicPropositions("s1Dbmaj"),
        "s1Ebmaj": BasicPropositions("s1Ebmaj"),
        "s1Bbmaj": BasicPropositions("s1Bbmaj"),
        "s1Cmin": BasicPropositions("s1Cmin"),
        "s1Gmin": BasicPropositions("s1Gmin"),
        "s1Amin": BasicPropositions("s1Amin"),
        "s1Dmin": BasicPropositions("s1Dmin"),
        "s1Emin": BasicPropositions("s1Emin"),
        "s1Dmin": BasicPropositions("s1Dmin"),
        "s1Bmin": BasicPropositions("s1Bmin"),
        "s1Fmin": BasicPropositions("s1Fmin"),
        "s1Gbmin": BasicPropositions("s1Gbmin"),
        "s1Abmin": BasicPropositions("s1Abmin"),
        "s1Dbmin": BasicPropositions("s1Dbmin"),
        "s1Ebmin": BasicPropositions("s1Ebmin"),
        "s1Dbmin": BasicPropositions("s1Dbmin"),
        "s1Bbmin": BasicPropositions("s1Bbmin"),
    }
    s2_keys = {
        "s2Cmaj": BasicPropositions("s2Cmaj"),
        "s2Gmaj": BasicPropositions("s2Gmaj"),
        "s2Amaj": BasicPropositions("s2Amaj"),
        "s2Dmaj": BasicPropositions("s2Dmaj"),
        "s2Emaj": BasicPropositions("s2Emaj"),
        "s2Dmaj": BasicPropositions("s2Dmaj"),
        "s2Bmaj": BasicPropositions("s2Bmaj"),
        "s2Fmaj": BasicPropositions("s2Fmaj"),
        "s2Cbmaj": BasicPropositions("s2Cbmaj"),
        "s2Gbmaj": BasicPropositions("s2Gbmaj"),
        "s2Abmaj": BasicPropositions("s2Abmaj"),
        "s2Dbmaj": BasicPropositions("s2Dbmaj"),
        "s2Ebmaj": BasicPropositions("s2Ebmaj"),
        "s2Dbmaj": BasicPropositions("s2Dbmaj"),
        "s2Bbmaj": BasicPropositions("s2Bbmaj"),
        "s2Cmin": BasicPropositions("s2Cmin"),
        "s2Gmin": BasicPropositions("s2Gmin"),
        "s2Amin": BasicPropositions("s2Amin"),
        "s2Dmin": BasicPropositions("s2Dmin"),
        "s2Emin": BasicPropositions("s2Emin"),
        "s2Dmin": BasicPropositions("s2Dmin"),
        "s2Bmin": BasicPropositions("s2Bmin"),
        "s2Fmin": BasicPropositions("s2Fmin"),
        "s2Gbmin": BasicPropositions("s2Gbmin"),
        "s2Abmin": BasicPropositions("s2Abmin"),
        "s2Dbmin": BasicPropositions("s2Dbmin"),
        "s2Ebmin": BasicPropositions("s2Ebmin"),
        "s2Dbmin": BasicPropositions("s2Dbmin"),
        "s2Bbmin": BasicPropositions("s2Bbmin"),
    }
    s1_genres = {
        "s1house": BasicPropositions("s1house"),
        "s1hip_hop": BasicPropositions("s1hip_hop"),
        "s1trap": BasicPropositions("s1trap"),
        "s1jungle_dnb": BasicPropositions("s1jungle_dnb"),
        "s1classical": BasicPropositions("s1classical"),
        "s1dubstep": BasicPropositions("s1dubstep"),
        "s1folk": BasicPropositions("s1folk"),
        "s1classic_rock": BasicPropositions("s1classic_rock"),
        "s1alt_rock": BasicPropositions("s1alt_rock"),
        "s1dancehall": BasicPropositions("s1dancehall"),
        "s1country": BasicPropositions("s1country"),
        "s1afrobeats": BasicPropositions("s1afrobeats"),
        "s1techno": BasicPropositions("s1techno"),
        "s1dance_pop": BasicPropositions("s1dance_pop"),
        "s1pop_rock": BasicPropositions("s1pop_rock"),
    }
    s2_genres = {
        "s2house": BasicPropositions("s2house"),
        "s2hip_hop": BasicPropositions("s2hip_hop"),
        "s2trap": BasicPropositions("s2trap"),
        "s2jungle_dnb": BasicPropositions("s2jungle_dnb"),
        "s2classical": BasicPropositions("s2classical"),
        "s2dubstep": BasicPropositions("s2dubstep"),
        "s2folk": BasicPropositions("s2folk"),
        "s2classic_rock": BasicPropositions("s2classic_rock"),
        "s2alt_rock": BasicPropositions("s2alt_rock"),
        "s2dancehall": BasicPropositions("s2dancehall"),
        "s2country": BasicPropositions("s2country"),
        "s2afrobeats": BasicPropositions("s2afrobeats"),
        "s2techno": BasicPropositions("s2techno"),
        "s2dance_pop": BasicPropositions("s2dance_pop"),
        "s2pop_rock": BasicPropositions("s2pop_rock"),
    }
    return s1_keys, s2_keys, s1_genres, s2_genres


# all the constraints that decide the compability between genre and key.
def example_theory():
    s1_keys, s2_keys, s1_genres, s2_genres = init_props()
    E.add_constraint(
        s1_genres["s1trap"]
        >> (
            (
                s2_genres["s2hip_hop"]
                | s2_genres["s2dubstep"]
                | s2_genres["s2alt_rock"]
                | s2_genres["s2classic_rock"]
                | s2_genres["s2techno"]
                | s2_genres["s2dance_pop"]
                | s2_genres["s2trap"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2jungle_dnb"]
                | ~s2_genres["s2classical"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2dancehall"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2pop_rock"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1classical"])
        >> (
            (
                s2_genres["s2hip_hop"]
                | s2_genres["s2jungle_dnb"]
                | s2_genres["s2classic_rock"]
                | s2_genres["s2classical"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2trap"]
                | ~s2_genres["s2dubstep"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2dancehall"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2techno"]
                | ~s2_genres["s2dance_pop"]
                | ~s2_genres["s2pop_rock"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1jungle_dnb"])
        >> (
            (
                s2_genres["s2dancehall"]
                | s2_genres["s2house"]
                | s2_genres["s2hip_hop"]
                | s2_genres["s2techno"]
                | s2_genres["s2classical"]
                | s2_genres["s2jungle_dnb"]
            )
            & (
                ~s2_genres["s2trap"]
                | ~s2_genres["s2dubstep"]
                | ~s2_genres["s2classic_rock"]
                | ~s2_genres["s2alt_rock"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2dance_pop"]
                | ~s2_genres["s2pop_rock"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1hip_hop"])
        >> (
            (
                s2_genres["s2house"]
                | s2_genres["s2trap"]
                | s2_genres["s2jungle_dnb"]
                | s2_genres["s2classical"]
                | s2_genres["s2techno"]
                | s2_genres["s2dancehall"]
                | s2_genres["s2afrobeats"]
                | s2_genres["s2hip_hop"]
            )
            & (
                ~s2_genres["s2dubstep"]
                | ~s2_genres["s2classic_rock"]
                | ~s2_genres["s2alt_rock"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2dance_pop"]
                | ~s2_genres["s2pop_rock"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1dubstep"])
        >> (
            (
                s2_genres["s2techno"]
                | s2_genres["s2dance_pop"]
                | s2_genres["s2trap"]
                | s2_genres["s2classic_rock"]
                | s2_genres["s2jungle_dnb"]
                | s2_genres["s2dubstep"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2hip_hop"]
                | ~s2_genres["s2alt_rock"]
                | ~s2_genres["s2classical"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2dancehall"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2pop_rock"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1classic_rock"])
        >> (
            (
                s2_genres["s2alt_rock"]
                | s2_genres["s2pop_rock"]
                | s2_genres["s2classical"]
                | s2_genres["s2folk"]
                | s2_genres["s2country"]
                | s2_genres["s2trap"]
                | s2_genres["s2dubstep"]
                | s2_genres["s2classic_rock"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2jungle_dnb"]
                | ~s2_genres["s2hip_hop"]
                | ~s2_genres["s2dancehall"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2techno"]
                | ~s2_genres["s2dance_pop"]
                | ~s2_genres["s2pop_rock"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1folk"])
        >> (
            (
                s2_genres["s2country"]
                | s2_genres["s2alt_rock"]
                | s2_genres["s2classic_rock"]
                | s2_genres["s2pop_rock"]
                | s2_genres["s2folk"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2trap"]
                | ~s2_genres["s2jungle_dnb"]
                | ~s2_genres["s2hip_hop"]
                | ~s2_genres["s2dubstep"]
                | ~s2_genres["s2dancehall"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2techno"]
                | ~s2_genres["s2dance_pop"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1alt_rock"])
        >> (
            (
                s2_genres["s2country"]
                | s2_genres["s2classic_rock"]
                | s2_genres["s2trap"]
                | s2_genres["s2folk"]
                | s2_genres["s2pop_rock"]
                | s2_genres["s2dancehall"]
                | s2_genres["s2alt_rock"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2jungle_dnb"]
                | ~s2_genres["s2hip_hop"]
                | ~s2_genres["s2dubstep"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2techno"]
                | ~s2_genres["s2dance_pop"]
                | ~s2_genres["s2classical"]
            )
        )
    )

    E.add_constraint(
        s1_genres["s1dancehall"]
        >> (
            (
                s2_genres["s2afrobeats"]
                | s2_genres["s2jungle_dnb"]
                | s2_genres["s2dance_pop"]
                | s2_genres["s2alt_rock"]
                | s2_genres["s2hip_hop"]
                | s2_genres["s2dancehall"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2trap"]
                | ~s2_genres["s2dubstep"]
                | ~s2_genres["s2classic_rock"]
                | ~s2_genres["s2pop_rock"]
                | ~s2_genres["s2classical"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2techno"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1afrobeats"])
        >> (
            (
                s2_genres["s2dancehall"]
                | s2_genres["s2house"]
                | s2_genres["s2pop_rock"]
                | s2_genres["s2dance_pop"]
                | s2_genres["s2alt_rock"]
                | s2_genres["s2hip_hop"]
                | s2_genres["s2afrobeats"]
            )
            & (
                ~s2_genres["s2techno"]
                | ~s2_genres["s2trap"]
                | ~s2_genres["s2jungle_dnb"]
                | ~s2_genres["s2classic_rock"]
                | ~s2_genres["s2classical"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2dubstep"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1country"])
        >> (
            (
                s2_genres["s2folk"]
                | s2_genres["s2alt_rock"]
                | s2_genres["s2pop_rock"]
                | s2_genres["s2classic_rock"]
                | s2_genres["s2country"]
            )
        )
        & (
            ~s2_genres["s2house"]
            | ~s2_genres["s2jungle_dnb"]
            | ~s2_genres["s2trap"]
            | ~s2_genres["s2hip_hop"]
            | ~s2_genres["s2dubstep"]
            | ~s2_genres["s2dancehall"]
            | ~s2_genres["s2afrobeats"]
            | ~s2_genres["s2techno"]
            | ~s2_genres["s2dance_pop"]
            | ~s2_genres["s2classical"]
        )
    )

    E.add_constraint(
        (s1_genres["s1techno"])
        >> (
            (
                s2_genres["s2house"]
                | s2_genres["s2dance_pop"]
                | s2_genres["s2trap"]
                | s2_genres["s2hip_hop"]
                | s2_genres["s2jungle_dnb"]
                | s2_genres["s2dubstep"]
                | s2_genres["s2techno"]
            )
            & (
                ~s2_genres["s2classic_rock"]
                | ~s2_genres["s2alt_rock"]
                | ~s2_genres["s2classical"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2dancehall"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2pop_rock"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1dance_pop"])
        >> (
            (
                s2_genres["s2house"]
                | s2_genres["s2techno"]
                | s2_genres["s2dubstep"]
                | s2_genres["s2dancehall"]
                | s2_genres["s2pop_rock"]
                | s2_genres["s2dance_pop"]
            )
            & (
                ~s2_genres["s2trap"]
                | ~s2_genres["s2hip_hop"]
                | ~s2_genres["s2jungle_dnb"]
                | ~s2_genres["s2classic_rock"]
                | ~s2_genres["s2alt_rock"]
                | ~s2_genres["s2classical"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2country"]
            )
        )
    )
    E.add_constraint(
        (s1_genres["s1house"])
        >> (
            s2_genres["s2afrobeats"]
            | s2_genres["s2hip_hop"]
            | s2_genres["s2trap"]
            | s2_genres["s2jungle_dnb"]
            | s2_genres["s2techno"]
            | s2_genres["s2dance_pop"]
            | s2_genres["s2house"]
            & (
                ~s2_genres["s2classic_rock"]
                | ~s2_genres["s2pop_rock"]
                | ~s2_genres["s2classical"]
                | ~s2_genres["s2folk"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2dubstep"]
                | ~s2_genres["s2alt_rock"]
                | ~s2_genres["s2dancehall"]
            )
        )
    )

    E.add_constraint(
        (s1_genres["s1pop_rock"])
        >> (
            (
                s2_genres["s2country"]
                | s2_genres["s2folk"]
                | s2_genres["s2alt_rock"]
                | s2_genres["s2dance_pop"]
                | s2_genres["s2classic_rock"]
                | s2_genres["s2pop_rock"]
            )
            & (
                ~s2_genres["s2house"]
                | ~s2_genres["s2trap"]
                | ~s2_genres["s2jungle_dnb"]
                | ~s2_genres["s2hip_hop"]
                | ~s2_genres["s2dubstep"]
                | ~s2_genres["s2dancehall"]
                | ~s2_genres["s2afrobeats"]
                | ~s2_genres["s2country"]
                | ~s2_genres["s2techno"]
            )
        )
    )
    E.add_constraint(
        (s1_keys["s1Ebmaj"])
        >> (
            s2_keys["s2Abmaj"]
            | s2_keys["s2Bbmaj"]
            | s2_keys["s2Cmin"]
            | s2_keys["s2Ebmaj"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
            )
        )
    )
    E.add_constraint(
        (s1_keys["s1Bmaj"])
        >> (
            s2_keys["s2Emaj"]
            | s2_keys["s2Gbmaj"]
            | s2_keys["s2Abmin"]
            | s2_keys["s2Bmaj"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
            )
        )
    )
    E.add_constraint(
        (s1_keys["s1Gbmaj"])
        >> (
            s2_keys["s2Ebmin"]
            | s2_keys["s2Dbmaj"]
            | s2_keys["s2Bmaj"]
            | s2_keys["s2Gbmaj"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Cmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Bbmaj"])
        >> (
            s2_keys["s2Ebmaj"]
            | s2_keys["s2Fmaj"]
            | s2_keys["s2Gmin"]
            | s2_keys["s2Bbmaj"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Fmaj"])
        >> (
            s2_keys["s2Bbmaj"]
            | s2_keys["s2Cmaj"]
            | s2_keys["s2Dmin"]
            | s2_keys["s2Fmaj"]
            & (
                ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Emaj"])
        >> (
            s2_keys["s2Emaj"]
            | s2_keys["s2Dbmin"]
            | s2_keys["s2Amaj"]
            | s2_keys["s2Bmaj"]
            & (
                ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Dmaj"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Amaj"])
        >> (
            s2_keys["s2Amaj"]
            | s2_keys["s2Emaj"]
            | s2_keys["s2Dmaj"]
            | s2_keys["s2Gbmin"]
            & (
                s2_keys["s2Gmaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Abmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Amin"])
        >> (
            s2_keys["s2Dmin"]
            | s2_keys["s2Emin"]
            | s2_keys["s2Cmaj"]
            | s2_keys["s2Amin"]
            & (
                ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Abmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Emin"])
        >> (
            s2_keys["s2Amin"]
            | s2_keys["s2Bmin"]
            | s2_keys["s2Gmaj"]
            | s2_keys["s2Emin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Bmin"])
        >> (
            s2_keys["s2Emin"]
            | s2_keys["s2Gbmin"]
            | s2_keys["s2Dmaj"]
            | s2_keys["s2Bmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Gbmin"])
        >> (
            s2_keys["s2Bmin"]
            | s2_keys["s2Dbmin"]
            | s2_keys["s2Amaj"]
            | s2_keys["s2Gbmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Dbmin"])
        >> (
            s2_keys["s2Gbmin"]
            | s2_keys["s2Abmin"]
            | s2_keys["s2Emaj"]
            | s2_keys["s2Dbmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Fmaj"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Abmin"])
        >> (
            s2_keys["s2Dbmin"]
            | s2_keys["s2Ebmin"]
            | s2_keys["s2Bmaj"]
            | s2_keys["s2Abmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Fmaj"]
            )
        )
    )
    E.add_constraint(
        (s1_keys["s1Ebmin"])
        >> (
            s2_keys["s2Abmaj"]
            | s2_keys["s2Bbmin"]
            | s2_keys["s2Gbmaj"]
            | s2_keys["s2Ebmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Bbmin"])
        >> (
            s2_keys["s2Ebmin"]
            | s2_keys["s2Fmin"]
            | s2_keys["s2Dbmaj"]
            | s2_keys["s2Bbmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Bmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Fmin"])
        >> (
            s2_keys["s2Bbmin"]
            | s2_keys["s2Cmin"]
            | s2_keys["s2Abmaj"]
            | s2_keys["s2Fmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Cmin"])
        >> (
            s2_keys["s2Fmin"]
            | s2_keys["s2Gmin"]
            | s2_keys["s2Ebmaj"]
            | s2_keys["s2Cmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Bbmaj"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Amin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Gmin"])
        >> (
            s2_keys["s2Cmin"]
            | s2_keys["s2Dmin"]
            | s2_keys["s2Bbmaj"]
            | s2_keys["s2Gmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Amin"]
            )
        )
    )

    E.add_constraint(
        (s1_keys["s1Dmin"])
        >> (
            s2_keys["s2Gmin"]
            | s2_keys["s2Amin"]
            | s2_keys["s2Fmaj"]
            | s2_keys["s2Dmin"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Bbmaj"]
            )
        )
    )

    E.add_constraint(
        s1_keys["s1Dbmaj"]
        >> (
            s2_keys["s2Gbmaj"]
            | s2_keys["s2Abmaj"]
            | s2_keys["s2Bbmin"]
            | s2_keys["s2Dbmaj"]
            & (
                ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Bbmaj"]
            )
        )
    )

    E.add_constraint(
        s1_keys["s1Cmaj"]
        >> (
            s2_keys["s2Fmaj"]
            | s2_keys["s2Gmaj"]
            | s2_keys["s2Amin"]
            | s2_keys["s2Cmaj"]
            & (
                ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Bbmaj"]
            )
        )
    )

    E.add_constraint(
        s1_keys["s1Gmaj"]
        >> (
            s2_keys["s2Cmaj"]
            | s2_keys["s2Dmaj"]
            | s2_keys["s2Emin"]
            | s2_keys["s2Gmaj"]
            & (
                ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Bbmaj"]
            )
        )
    )

    E.add_constraint(
        s1_keys["s1Dmaj"]
        >> (
            s2_keys["s2Gmaj"]
            | s2_keys["s2Amaj"]
            | s2_keys["s2Bmin"]
            | s2_keys["s2Dmaj"]
            & (
                ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Abmaj"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Dbmaj"]
                | ~s2_keys["s2Ebmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Fmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmaj"]
            )
        )
    )

    E.add_constraint(
        s1_keys["s1Abmaj"]
        >> (
            s2_keys["s2Dbmaj"]
            | s2_keys["s2Ebmaj"]
            | s2_keys["s2Fmin"]
            | s2_keys["s2Abmaj"]
            & (
                ~s2_keys["s2Gbmaj"]
                | ~s2_keys["s2Gmaj"]
                | ~s2_keys["s2Amaj"]
                | ~s2_keys["s2Bmin"]
                | ~s2_keys["s2Dmaj"]
                | ~s2_keys["s2Cmaj"]
                | ~s2_keys["s2Emin"]
                | ~s2_keys["s2Fmaj"]
                | ~s2_keys["s2Amin"]
                | ~s2_keys["s2Bbmin"]
                | ~s2_keys["s2Gmin"]
                | ~s2_keys["s2Emaj"]
                | ~s2_keys["s2Bmaj"]
                | ~s2_keys["s2Cmin"]
                | ~s2_keys["s2Dmin"]
                | ~s2_keys["s2Gbmin"]
                | ~s2_keys["s2Abmin"]
                | ~s2_keys["s2Dbmin"]
                | ~s2_keys["s2Ebmin"]
                | ~s2_keys["s2Bbmaj"]
            )
        )
    )

    return E


# function to derive the key and genre compatibility of two songs
def solve(song1, song2):
    T = example_theory()
    # injecting the genres and keys of the two songs into the theory.
    T.add_constraint(s1_genres[s1_genre])
    T.add_constraint(s2_genres[s2_genre])
    T.add_constraint(s1_keys[s1_key])
    T.add_constraint(s2_keys[s2_key])

    T = T.compile()
    return T.satisfiable()


# function which assigns the genres to the global variables
def load_genre(genre1, genre2):
    global s1_genre, s2_genre
    s1_genre = "s1" + genre1
    s2_genre = "s2" + genre2


# final comparison to derive the two songs compatiblity relative to its key, genre, and bpm compatibility.
def determine_compat(song1, song2):
    gkCompat = solve(song1, song2)
    bpm1 = int(song1.bpm)
    bpm2 = int(song2.bpm)
    # finds ouot whether or not the two songs are within a range of 10 accounting for double and half time
    BPM_compat = abs(bpm1 - bpm2) <= 10
    BPM_2times_compat = abs(bpm1 - 2 * bpm2) <= 10 or abs(2 * bpm1 - bpm2) <= 10
    BPM_half_compat = abs(bpm1 - bpm2 / 2) <= 10 or abs(bpm2 - bpm1 / 2) <= 10
    # final comparison to ensure all three genre, key, and bpm are compatible.
    if gkCompat and (BPM_compat or BPM_2times_compat or BPM_half_compat):
        return True
    return False


# method which loads the keys into the global key variables
def load_key(key1, key2):
    global s1_key, s2_key
    s1_key = "s1" + key1
    s2_key = "s2" + key2


# loads the songs from the json into a list
def load_songs():
    # reading the file
    with open("songlib.json", "r") as file:
        jsongs = json.load(file)

    # parsing the info and storing it in a list of objects of type Song
    songs = []
    for i in range(len(jsongs) - 1):
        songs.append(
            Song(
                jsongs[i]["Name"],
                jsongs[i]["Artist"],
                jsongs[i]["BPM"],
                jsongs[i]["Key"],
                jsongs[i]["Genre"],
            )
        )
    return songs


# main function to determine compatibility
def mixingAssist(song1):
    global E
    count = 0
    compat_count = 0
    name1 = str(song1.name)
    # iterating through the songs
    for song2 in songs:

        if name1 != song2.name:
            # loads the keys and genres into global variables
            load_genre(song1.genre, song2.genre)
            load_key(song1.key, song2.key)
            # checks for compatiblity between two songs and prints them accordingly
            if determine_compat(song1, song2):
                print(song1, "\n", song2, "\n", "These two songs are compatible!\n")
                compat_count += 1
        # statement to check that it is done iterating through the list and there were no compatible songs
        temp1 = count == len(songs) - 1
        temp2 = compat_count == 0
        if temp1 and temp2:
            print("No songs are compatible")


if __name__ == "__main__":
    print("Welcome to Disc Jockey")
    # declares the songs and initializes a list which takes note of every song that was played by index.
    songs = load_songs()
    used_songs = []
    # while there are more unplayed songs than available
    while len(used_songs) < len(songs):
        choice = str(input(" Enter the name of the song you want to play:"))

        for i in range(len(songs)):
            # checks to make sure that the song that they selected exists and hasnt been played.
            if (str(songs[i].name) == choice) and (i not in used_songs):
                used_songs.append(i)
                mixingAssist(songs[i])
            elif i in used_songs:
                print("This song has already been played!")
