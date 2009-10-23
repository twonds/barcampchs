%% Author : http://twitter.com/lukevenediger

-module(rpsserver).
-export([start/0, play/2, loop/0]).
-deprecated({start,0}). 

%%spawn and register our service
start() ->	
	register( server, spawn( fun() -> loop() end)).

%%the message pump
loop() ->
	receive 
		{Action,Pid} -> 
			%%%%io:format("Got message from: ~p~n", [Pid]),
			Pid ! play( Action,Pid ),
			rpsserver:loop()
	end.
			
bob() ->
   start().
     
%%play against the computer
play(Action, Pid) -> 	
        %%validate the player attack
        case is_an_attack( Action ) of          
          false -> {error, stop_cheating};
          true  -> compete( Action, Pid )
        end.
        
compete( Action, Pid ) ->
	%% We need to pick a random Attack
        AttackList = attacks(),
        SelectedAttack = lists:nth( random:uniform(length(AttackList)), AttackList),
	
	%% Now we need to decide on the outcome
	Result = gameOutcome({computer, SelectedAttack}, {player, Action}),
	%%io:format( "Result: ~p~n", [Result] ),
	Result.
	

%%deterimne the result
%tie
gameOutcome({computer, Attack}, {player, Attack}) ->
	{result, tie, Attack};
%%computer wins with dynamite
gameOutcome({computer, dynamite}, {player, _}) ->
	{result, lose, dynamite};
%%player wins with dynamite
gameOutcome({computer, ComputerAttack}, {player, dynamite}) ->
	{result, win, ComputerAttack};
%%computer wins
gameOutcome({computer, paper}, {player, rock}) ->
	{result, lose, paper};
gameOutcome({computer, rock}, {player, scissors}) ->
	{result, lose, rock};
gameOutcome({computer, scissors}, {player, paper}) ->
	{result, lose, scissors};
%player wins 
gameOutcome({computer, Attack}, {player, _}) ->
	{result, win, Attack}.

%%defines all of out possible outcomes
attacks() ->
  	%~ [rock, paper, scissors].
        [rock, paper, scissors, dynamite].

%%used to validate if a valid attack has been made
is_an_attack(Attack) ->
	lists:member(Attack, attacks()).
