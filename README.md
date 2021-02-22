# CMIMC-2020 
(My code/solutions in the CMIMC 2020 contest)

The contest is done in teams of 3. It has two parts: an optimization round and an AI round. Each round has 3 questions.

Our team split the work by having one person do one question per round.
Later, I helped out my friend as I finished mine.

# Optimization round
(Circle Covers & Unique Products)

Circle Covers: You are given a list of points and a list of radii (the length). You are to find where to put these circles of specified radii in order for the circles to cover the most amount of points.

Unique Products: You are given 2 integers *N* and *M*. You are to find *N* distinct sets of natural numbers of the same length composed of elemtents found within the set {1, 2, 3, ... *M*}. These *N* distinct sets must satisfy the following condition: the product of any two elemtents from different sets must be unique.

My main question is Circle Covers, which I got a score of ~95%, ranking ~top 10%, but my programs took like days to run.

For Unique Products, I got a simple strategy that worked and found results, but it was more math and not as much optimization. Didn't place very well either.

# AI round
(Trap the Scotty Dog)

2 players play against eachother on a 15x15 grid map. One player takes the role of Scotty the Dog and the other player takes the role of the Traper. Scotty starts in the middle of the grid and his goal is to get out of the grid (escape). The Trapper's goal is to stop Scotty from escaping by putting blocking tiles (Scotty can't go onto blocked tiles). The map starts with some blockades already placed to help out the Trapper. The game is played in turns, with the Trapper going first. Each turn, Scotty can choose to move into one of the eight tiles adjacent to his current tile. Each turn, the Trapper may place a blockade in one tile on the map. Scotty wins if he exits the map, the Trapper wins if Scotty has no possible moves left (encircled on all 8 sides), and the game is tied after 200 rounds are played.

I didn't get to finish coding the Trapper, but I did finish coding a first version of Scotty. Didn't place too well, but had a win rate of ~55%, while the best team's was ~65%.
