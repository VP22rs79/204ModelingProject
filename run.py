from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
import json

# These two lines make sure a faster SAT solver is used.
from nnf import config

genres = [
    "House",
    "Hip-Hop",
    "Trap",
    "Jungle",
    "Classical",
    "Dubstep",
    "Folk",
    "Classic Rock",
    "Alternative Rock",
    "Dancehall",
    "Afrobeats",
    "Country",
    "Techno",
    "Dance Pop",
    "Pop Rock",
]

keys = [
    "Cmaj",
    "Gmaj",
    "Dmaj",
    "Amaj",
    "Emaj",
    "Bmaj",
    "Gbmaj",
    "Dbmaj",
    "Abmaj",
    "Ebmaj",
    "Bbmaj",
    "Fmaj",
    "Amin",
    "Emin",
    "Bmin",
    "Gbmin",
    "Dbmin",
    "Abmin",
    "Ebmin",
    "Bbmin",
    "Fmin",
    "Cmin",
    "Gmin",
    "Dmin",
]


class Song:
    def __init__(self, Name, Artist, BPM, Key, Genre):
        self.name = Name
        self.artist = Artist
        self.bpm = BPM
        self.key = Key
        self.genre = Genre

    def setKey():
        x = 2

    def setGenre():
        x = 1

    def setBpm():
        x = 0

    # TODO add a method that maps a key proposition to the song instance.
    # TODO add a method that maps a
    # for genre in genres:
    # if g


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
# Call your variables whatever you want
G = BasicPropositions("G")  # represents the genre
K = BasicPropositions("K")  # represents the key
B = BasicPropositions("B")  # represents the BPM
song = BasicPropositions("song")
Cmaj = BasicPropositions("Cmaj")
Gmaj = BasicPropositions("Gmaj")
Amaj = BasicPropositions("Amaj")
Dmaj = BasicPropositions("Dmaj")
Emaj = BasicPropositions("Emaj")
Dmaj = BasicPropositions("Dmaj")
Bmaj = BasicPropositions("Bmaj")
Fmaj = BasicPropositions("Fmaj")
Cbmaj = BasicPropositions("Cbmaj")
Gbmaj = BasicPropositions("Gbmaj")
Abmaj = BasicPropositions("Abmaj")
Dbmaj = BasicPropositions("Dbmaj")
Ebmaj = BasicPropositions("Ebmaj")
Dbmaj = BasicPropositions("Dbmaj")
Bbmaj = BasicPropositions("Bbmaj")
Cmin = BasicPropositions("Cmin")
Gmin = BasicPropositions("Gmin")
Amin = BasicPropositions("Amin")
Dmin = BasicPropositions("Dmin")
Emin = BasicPropositions("Emin")
Dmin = BasicPropositions("Dmin")
Bmin = BasicPropositions("Bmin")
Fmin = BasicPropositions("Fmin")
Cbmin = BasicPropositions("Cbmin")
Gbmin = BasicPropositions("Gbmin")
Abmin = BasicPropositions("Abmin")
Dbmin = BasicPropositions("Dbmin")
Ebmin = BasicPropositions("Ebmin")
Dbmin = BasicPropositions("Dbmin")
Bbmin = BasicPropositions("Bbmin")
Fbmin = BasicPropositions("Fbmin")
house = BasicPropositions("house")
hipHop = BasicPropositions("hipHop")
trap = BasicPropositions("trap")
jungle = BasicPropositions("jungle")
classical = BasicPropositions("classical")
dubstep = BasicPropositions("dubstep")
folk = BasicPropositions("folk")
classicRock = BasicPropositions("classicRock")
altRock = BasicPropositions("altRock")
dancehall = BasicPropositions("dancehall")
country = BasicPropositions("country")
afrobeats = BasicPropositions("afrobeats")
techno = BasicPropositions("techno")
dancePop = BasicPropositions("dancePop")
popRock = BasicPropositions("popRock")


# hi remy
# hello! -remy

# At least one of these will be true
Q = FancyPropositions(
    "Q"
)  # true if a song y can come after song x according to key, BPM, genre
oneGenre = FancyPropositions("oneGenre")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # if a song's genre is x and it only has one genre, then it cannot be any other genre
    # TODO comapre two songs bpm and make a proposition

    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E


def solve(song1, song2):
    T = example_theory()
    if abs(song1.BPM - song2.BPM) <= 10:
        T.add_constraint(lt10)
    # if(song1.genre in genres):


def loadSongs():
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


def autoGeneratePlaylist():
    songs = loadSongs()
    songA = ""
    songB = ""
    while True:
        songA = input("Enter the name of the first song you want to play:")
        for i in range(len(songs)):
            if songA == songs[i]["Name"]:
                break
        if songA == songs[i]["Name"]:
            break
        else:
            print("Song not found, retry with another song.")
    while True:
        songB = input("Enter the name of the last song you want to be played:")
        for j in range(len(songs)):
            if songB == songs[j]["Name"]:
                break
        if songB == songs[j]["Name"]:
            break
        else:
            print("Song not found, retry with another song.")


def mixingAssist():
    songs = loadSongs()


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v, vn in zip([a, b, c, x, y, z], "abcxyz"):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))

    loadSongs()
    print("Welcome to Disc Jockey, make a selection below.")
    choice = input("1 for autogenerated playlist, 2 for mixing app.")
    if choice == 1:
        autoGeneratePlaylist()
    elif choice == 2:
        mixingAssist
