# Actions
Actions are mini python scripts that allow for scripting things in-game. Triggers and Actors both have the ability
to define action lists for themselves. These allow for level files to easily hook short scripts to a defined
object, and for custom code on objects to be done very simply.

Not all action methods are supported by all classes. For example currently Triggers will only respond to collision actions.

Actions are defined as methods to be called on specific events. Every actionlib must import whatever python/pygame libraries it needs.

Beyond that it merely needs a function for the event it wishes to respond to. Currently there are two events defined:

##Collision events:
On any collision event the function will receive:
- The sprite calling the event
- The sprite that collided with it
- The calling sprite's settings object
- A reference to the current game
- Any parameter values defined in the level file. 
The first three parameters must be supported by any collision function, all other parameters are optional 
as long as the action and the level agree.
These parameters do not have to be used by all functions, just received.
Example:

```def collision(me, collider, settings, game,  spellname):
    if collider.name == 'Player':
        collider.addspell(spellname.upper())
        me.kill()```

## Update events:
Update events are currently only supported by actors (player actor is not currently supported)
Update events, like collision events, have mandatory and optional parameters. All update events
will receive an instance of the sprite calling it, as well as that sprite's settings object. 
Update events can be used to code custom movements, ai's etc for enemies and allies. Because they 
are simple, single scripts - any compatible actor can reuse the actions created for another.


Any action must declare what type of event is responds to. It also has a method field which indicates
the name of the function to call from the script. This allows significant flexibility in calling 
actions from level files. Parameters are given as a dictionary and passed on using the kwargs approach. 
Thus you should name your function parameters according to what you will specify in the level file.