from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
import json

# These two lines make sure a faster SAT solver is used.
from nnf import config

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
    "Dmaj",
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
    "Cbmin",
    "Gbmin",
    "Abmin",
    "Dbmin",
    "Ebmin",
    "Dbmin",
    "Bbmin",
    "Fbmin",
]


class Song:
    def __init__(self, Name, Artist, BPM, Key, Genre):
        self.name = Name
        self.artist = Artist
        self.bpm = BPM
        self.key = Key
        self.genre = Genre

    def __str__(self):
        return (
            f"Name: {self.name}, "
            f"Artist: {self.artist}, "
            f"BPM: {self.bpm}, "
            f"Key: {self.key}, "
            f"Genre: {self.genre}"
        )


def make_implication(left, right):
    return left.negate() | right


def exclude_genres(genre_dict, allowed):
    exclusion = False
    for gkey in genre_dict:
        if gkey not in allowed:
            exclusion |= genre_dict[gkey]
    return exclusion

def exclude_keys(key_dict, allowed):
    exclusion = False
    for kkey in key_dict:
        if kkey not in allowed:
            exclusion |= key_dict[kkey]
    return exclusion
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()


# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"


lt10 = BasicPropositions("lt10")
key_compat = BasicPropositions("key_compat")
genre_compat = BasicPropositions("genre_compat")

s1_genre = ""
s2_genre = ""
s1_key = ""
s2_key = ""


# Call your variables whatever you want
def init_props():

    s1_key_dict = {
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
        "s1Dbmaj": BasicPropositions("s1Dbmaj"),
        "s1Bbmaj": BasicPropositions("s1Bbmaj"),
        "s1Cmin": BasicPropositions("s1Cmin"),
        "s1Gmin": BasicPropositions("s1Gmin"),
        "s1Amin": BasicPropositions("s1Amin"),
        "s1Dmin": BasicPropositions("s1Dmin"),
        "s1Emin": BasicPropositions("s1Emin"),
        "s1Dmin": BasicPropositions("s1Dmin"),
        "s1Bmin": BasicPropositions("s1Bmin"),
        "s1Fmin": BasicPropositions("s1Fmin"),
        "s1Cbmin": BasicPropositions("s1Cbmin"),
        "s1Gbmin": BasicPropositions("s1Gbmin"),
        "s1Abmin": BasicPropositions("s1Abmin"),
        "s1Dbmin": BasicPropositions("s1Dbmin"),
        "s1Ebmin": BasicPropositions("s1Ebmin"),
        "s1Dbmin": BasicPropositions("s1Dbmin"),
        "s1Bbmin": BasicPropositions("s1Bbmin"),
        "s1Fbmin": BasicPropositions("s1Fbmin"),
    }
    s2_key_dict = {
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
        "s2Cbmin": BasicPropositions("s2Cbmin"),
        "s2Gbmin": BasicPropositions("s2Gbmin"),
        "s2Abmin": BasicPropositions("s2Abmin"),
        "s2Dbmin": BasicPropositions("s2Dbmin"),
        "s2Ebmin": BasicPropositions("s2Ebmin"),
        "s2Dbmin": BasicPropositions("s2Dbmin"),
        "s2Bbmin": BasicPropositions("s2Bbmin"),
        "s2Fbmin": BasicPropositions("s2Fbmin"),
    }
    s1_genre_dict = {
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
    s2_genre_dict = {
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

    return s1_key_dict, s2_key_dict, s1_genre_dict, s2_genre_dict


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    s1_keys, s2_keys, s1_genres, s2_genres = init_props()
    # Ensure exactly one key for s1
    s1_key_vars = list(s1_keys.values())
    constraint.add_exactly_one(E, *s1_key_vars)

    # Ensure exactly one key for s2
    s2_key_vars = list(s2_keys.values())
    constraint.add_exactly_one(E, *s2_key_vars)

    # Ensure exactly one genre for s1
    s1_genre_vars = list(s1_genres.values())
    constraint.add_exactly_one(E, *s1_genre_vars)

    # Ensure exactly one genre for s2
    s2_genre_vars = list(s2_genres.values())
    constraint.add_exactly_one(E, *s2_genre_vars)
    (s >> 2)
    
    # E.add_constraint(s1_genres[s1_genre]-->)

    E.add_constraint(
        make_implication(
            s1_genres["s1house"],
            (
                (
                    s2_genres["s2hip_hop"]
                    | s2_genres["s2techno"]
                    | s2_genres["s2dance_pop"]
                )
                & exclude_genres(
                    s2_genres, ["s2hip_hop", "s2techno", "s2dance_pop"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1trap"],
            (
                (s2_genres["s2hip_hop"] | s2_genres["s2dubstep"] | s2_genres["s2alt_rock"])
                & exclude_genres(s2_genres, ["s2hip_hop", "s2dubstep", "s2alt_rock"]).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1classical"],
            (
                (
                    s2_genres["s2hip_hop"]
                    | s2_genres["s2jungle_dnb"]
                    | s2_genres["s2classic_rock"]
                )
                & exclude_genres(
                    s2_genres, ["s2hip_hop", "s2jungle_dnb", "s2classic_rock"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1jungle_dnb"],
            (
                (s2_genres["s2dancehall"] | s2_genres["s2house"] | s2_genres["s2hip_hop"])
                & exclude_genres(s2_genres, ["s2dancehall", "s2house", "s2hip_hop"]).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1hip_hop"],
            (
                (s2_genres["s2house"] | s2_genres["s2trap"] | s2_genres["s2jungle_dnb"])
                & exclude_genres(s2_genres, ["s2house", "s2trap", "s2jungle_dnb"]).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1dubstep"],
            (
                (s2_genres["s2techno"] | s2_genres["s2dance_pop"] | s2_genres["s2trap"])
                & exclude_genres(s2_genres, ["s2techno", "s2dance_pop", "s2trap"]).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1classic_rock"],
            (
                (
                    s2_genres["s2alt_rock"]
                    | s2_genres["s2pop_rock"]
                    | s2_genres["s2classical"]
                    | s2_genres["s2folk"]
                )
                & exclude_genres(
                    s2_genres, ["s2alt_rock", "s2pop_rock", "s2classical", "s2folk"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1folk"],
            (
                (
                    s2_genres["s2country"]
                    | s2_genres["s2alt_rock"]
                    | s2_genres["s2classic_rock"]
                )
                & exclude_genres(
                    s2_genres["s2country", "s2alt_rock", "s2classic_rock"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1alt_rock"],
            (
                (s2_genres["s2country"] | s2_genres["s2classic_rock"] | s2_genres["s2trap"])
                & exclude_genres(
                    s2_genres, ["s2country", "s2classic_rock", "s2trap"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1dancehall"],
            (
                (
                    s2_genres["s2afrobeats"]
                    | s2_genres["s2jungle_dnb"]
                    | s2_genres["s2dance_pop"]
                    | s2_genres["s2alt_rock"]
                )
                & exclude_genres(
                    s2_genres, ["s2afrobeats", "s2jungle_dnb", "s2dance_pop", "s2alt_rock"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1afrobeats"],
            (
                (
                    s2_genres["s2dancehall"]
                    | s2_genres["s2house"]
                    | s2_genres["s2pop_rock"]
                    | s2_genres["s2dance_pop"]
                )
                & exclude_genres(
                    s2_genres, ["s2dancehall", "s2house", "s2pop_rock", "s2dance_pop"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1country"],
            (
                (s2_genres["s2folk"] | s2_genres["s2alt_rock"] | s2_genres["s2pop_rock"])
                & exclude_genres(s2_genres, ["s2folk", "s2alt_rock", "s2pop_rock"]).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1techno"],
            (
                (
                    s2_genres["s2house"]
                    | s2_genres["s2dance_pop"]
                    | s2_genres["s2trap"]
                    | s2_genres["s2hip_hop"]
                )
                & exclude_genres(
                    s2_genres, ["s2house", "s2dance_pop", "s2trap", "s2hip_hop"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1dance_pop"],
            (
                (
                    s2_genres["s2house"]
                    | s2_genres["s2techno"]
                    | s2_genres["s2dubstep"]
                    | s2_genres["s2dancehall"]
                )
                & exclude_genres(
                    s2_genres, ["s2house", "s2techno", "s2dubstep", "s2dancehall"]
                ).negate()
            ),
        )
    )

    E.add_constraint(
        make_implication(
            s1_genres["s1pop_rock"],
            (
                (s2_genres["s2country"] | s2_genres["s2folk"] | s2_genres["s2alt_rock"])
                & exclude_genres(s2_genres, ["s2country", "s2folk", "s2alt_rock"]).negate()
            ),
        )
    )

    E.add_constraint(make_implication(
    s1_keys["s1Cmaj"],
    (
        (s2_keys["s2Gmaj"] | s2_keys["s2Fmaj"] | s2_keys["s2Amin"]) 
        & exclude_keys(s2_keys, ["s2Gmaj", "s2Fmaj", "s2Amin"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Gmaj"],
    (
        (s2_keys["s2Cmaj"] | s2_keys["s2Dmaj"] | s2_keys["s2Emin"]) 
        & exclude_keys(s2_keys, ["sCmaj", "s2Dmaj", "s2Emin"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Dmaj"],
    (
        (s2_keys["s2Gmaj"] | s2_keys["s2Amaj"] | s2_keys["s2Bmin"]) 
        & exclude_keys(s2_keys, ["s2Gmaj", "s2Amaj", "s2Bmin"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Amaj"],
    (
        (s2_keys["s2Dmaj"] | s2_keys["s2Emaj"] | s2_keys["s2Gbmin"]) 
        & exclude_keys(s2_keys, ["s2Dmaj", "s2Emaj", "s2Gbmin"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Emaj"],
    (
        (s2_keys["s2Amaj"] | s2_keys["s2Bmaj"] | s2_keys["s2Dbmin"]) 
        & exclude_keys(s2_keys, ["s2Amaj", "s2Bmaj", "s2Dbmin"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Bmaj"],
    (
        (s2_keys["s2Emaj"] | s2_keys["s2Gbmaj"] | s2_keys["s2Abmin"]) 
        & exclude_keys(s2_keys, ["s2Emaj", "s2Gmaj", "s2Abmin"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Gbmaj"],
    (
        (s2_keys["s2Bmaj"] | s2_keys["s2Dbmaj"] | s2_keys["s2Ebmin"]) 
        & exclude_keys(s2_keys, ["s2Bmaj", "s2Dbmaj", "s2Ebmin"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Dbmaj"],
    (
        (s2_keys["s2Gbmaj"] | s2_keys["s2Abmaj"] | s2_keys["s2Bbmin"]) 
        & exclude_keys(s2_keys, ["s2Gbmaj", "s2Abmaj", "s2Bbmin"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Abmaj"],
    (
        (s2_keys["s2Dbmaj"] | s2_keys["s2Ebmaj"] | s2_keys["s2Fmin"]) 
        & exclude_keys(s2_keys, ["s2Dbmaj", "s2Ebmaj", "s2Fmin"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Ebmaj"],
    (
        (s2_keys["s2Abmaj"] | s2_keys["s2Bbmaj"] | s2_keys["s2Cmin"]) 
        & exclude_keys(s2_keys, ["s2Abmaj", "s2Bbmaj", "s2Cmin"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Bbmaj"],
    (
        (s2_keys["s2Ebmaj"] | s2_keys["s2Fmaj"] | s2_keys["s2Gmin"]) 
        & exclude_keys(s2_keys, ["s2Ebmaj", "s2Fmaj", "s2Gmin"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Fmaj"],
    (
        (s2_keys["s2Bbmaj"] | s2_keys["s2Cmaj"] | s2_keys["s2Dmin"]) 
        & exclude_keys(s2_keys, ["s2Bbmaj", "s2Cmaj", "s2Dmin"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Amin"],
    (
        (s2_keys["s2Dmin"] | s2_keys["s2Emin"] | s2_keys["s2Cmaj"]) 
        & exclude_keys(s2_keys, ["s2Dmin", "s2Emin", "s2Cmaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Emin"],
    (
        (s2_keys["s2Amin"] | s2_keys["s2Bmin"] | s2_keys["s2Gmaj"]) 
        & exclude_keys(s2_keys, ["s2Amin", "s2Bmin", "s2Gmaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Bmin"],
    (
        (s2_keys["s2Emin"] | s2_keys["s2Gbmin"] | s2_keys["s2Dmaj"]) 
        & exclude_keys(s2_keys, ["s2Emin", "s2Gbmin", "s2Dmaj"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Gbmin"],
    (
        (s2_keys["s2Bmin"] | s2_keys["s2Dbmin"] | s2_keys["s2Amaj"]) 
        & exclude_keys(s2_keys, ["s2Bmin", "s2Dbmin", "s2Amaj"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Dbmin"],
    (
        (s2_keys["s2Gbmin"] | s2_keys["s2Abmin"] | s2_keys["s2Emaj"]) 
        & exclude_keys(s2_keys, ["s2Gbmin", "s2Abmin", "s2Emaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Abmin"],
    (
        (s2_keys["s2Dbmin"] | s2_keys["s2Ebmin"] | s2_keys["s2Bmaj"]) 
        & exclude_keys(s2_keys, ["s2Dbmin", "s2Ebmin", "s2Bmaj"]).negate()
    )
))

    E.add_constraint(make_implication(
    s1_keys["s1Ebmin"],
    (
        (s2_keys["s2Abmin"] | s2_keys["s2Bbmin"] | s2_keys["s2Gbmaj"]) 
        & exclude_keys(s2_keys, ["s2Abmin", "s2Bbmin", "s2Gbmaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Bbmin"],
    (
        (s2_keys["s2Ebmin"] | s2_keys["s2Fmin"] | s2_keys["s2Dbmaj"]) 
        & exclude_keys(s2_keys, ["s2Ebmin", "s2Fmin", "s2Dbmaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Fmin"],
    (
        (s2_keys["s2Bbmin"] | s2_keys["s2Cmin"] | s2_keys["s2Abmaj"]) 
        & exclude_keys(s2_keys, ["s2Bbmin", "s2Cmin", "s2Abmaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Cmin"],
    (
        (s2_keys["s2Fmin"] | s2_keys["s2Gmin"] | s2_keys["s2Ebmaj"]) 
        & exclude_keys(s2_keys, ["s2Fmin", "s2Gmin", "s2Ebmaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Gmin"],
    (
        (s2_keys["s2Cmin"] | s2_keys["s2Dmin"] | s2_keys["s2Bbmaj"]) 
        & exclude_keys(s2_keys, ["s2Cmin", "s2Dmin", "s2Bbmaj"]).negate()
    )
))
    
    E.add_constraint(make_implication(
    s1_keys["s1Dmin"],
    (
        (s2_keys["s2Gmin"] | s2_keys["s2Amin"] | s2_keys["s2Fmaj"]) 
        & exclude_keys(s2_keys, ["s2Gmin", "s2Amin", "s2Fmaj"]).negate()
    )
))
    return E


def solve(song1, song2):
    T = example_theory()
    if abs(song1.BPM - song2.BPM) <= 10:
        T.add_constraint(lt10)
    T.add_constraint(s1_genre)
    T.add_constraint(s2_genre)
    T.add_constraint(s1_key)
    T.add_constraint(s2_key)
    return T.satisfiable()


def loadGenre(genre1, genre2):
    s1_genre = "s1" + genre1
    s2_genre = "s2" + genre2


def load_key(key1, key2):
    s1_key = key1
    s2_key = key2


def load_songs():
    with open("songlib.json", "r") as file:
        jsongs = json.load(file)

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


def print_2songs(song1, song2):
    print(song1.na)


def mixingAssist(song1):
    count = 0
    compat_count = 0
    for song2 in songs:
        loadGenre(song1.genre, song2.genre)
        load_key(song1.key, song2.key)
        if solve(song1, song2):
            print(song1, song2, "are compatible!")
            compat_count += 1
        if count == len(songs) - 1 & compat_count == 0:
            print("no songs compat")

    print("Type in the name of the song you would like to play next:")


if __name__ == "__main__":

    # T = example_theory()
    ## Don't compile until you're finished adding all your constraints!
    # T = T.compile()
    ## After compilation (and only after), you can check some of the properties
    ## of your model:
    # print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))
    # print("   Solution: %s" % T.solve())
    # print("\nVariable likelihoods:")
    # for v, vn in zip([a, b, c, x, y, z], "abcxyz"):
    #    # Ensure that you only send these functions NNF formulas
    #    # Literals are compiled to NNF here
    #    print(" %s: %.2f" % (vn, likelihood(T, v)))

    print("Welcome to Disc Jockey")

    songs = loadSongs()
    while True:
        choice = input(" Enter the name of the song you want to play first:")
        for song in songs:
            if song.name == choice:
                mixingAssist(song)
                break
            else:
                print("Song not in list of songs! Enter again...")
