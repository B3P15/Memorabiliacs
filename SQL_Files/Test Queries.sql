-- Test if I can acces another DB while in a separate one

 use ARuppDB;
 
 select P.*
 from PokemonTCG.Cards as P, ARuppDB.Pokemon as A
 where A.CardID = P.CardID;