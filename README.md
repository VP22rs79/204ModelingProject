# CISC/CMPE 204 Modelling Project
Disk jockey is a program which helps transition through songs in a set list by helping the user to select the next song which is most compatible on the basis of key, BPM(beats per minute), and genre.

# Program functionality
By comparing the current song with the others in the library, the differences between the songs are calculated together to determine a compatibility score. 
A song's score is derived through the differences in BPM, genre and key. The score is then used to rank the unplayed songs in terms of compatibility. Every time a transition is made, the scores are recalculated. 
The user is presented with 2 approaches to derivng the set list.<br/>
    Option 1 (test compatibility): The user selects a song from the library and the program will return the songs that are nearest in compatibility for them to  choose from while mixing.<br/> 
    Option 2 (create a set list): The program intakes a beginning song and an ending song for their setlist. The user also denotes the total number of tracks they would want in the generated set list. The program then returns a list of songs that gradually progress through the most compatible tracks in order to smoothly transition from the first to final track. 