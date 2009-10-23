-module(rpsclient).
-export([start/1, attack/2]).

-vsn("1.0.0.1").

start(Attack) ->
	spawn(fun() -> looping_attack(Attack) end).

looping_attack(Attack) ->
	attack(Attack),
	timer:sleep(1000),
	looping_attack(Attack).

attack(Attack) ->
	Result = attack(Attack, server@yourmachinename),
	io:format("~p~n", [Result]).
attack(Attack, Host) ->
	{server, Host} ! {Attack, self()},
	receive
		{result, Result, ComputerAttack} ->
			{Result, ComputerAttack, checkOutThisCoolUpdate5};
		{error, Error} ->
			{Error}
	end.
