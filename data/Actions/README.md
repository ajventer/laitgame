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
- Any parameter values defined in the level file. 
The fist three parameters must be supported by any collision function, all other parameters are optional 
as long as the action and the level agree.
Example:

```def collision(me, collider, settings,  spellname):
    if collider.name == 'Player':
        collider.addspell(spellname.upper())
        me.kill()```

## Update events:
Update events are currently only supported by actors (player actor is not currently supported)
Update events, like collision events, have mandatory and optional parameters. All update events
will receive an instance of the sprite calling it, as well as that sprite's settings object. 
Update events can be used to code custom movements, ai's etc for enemies and allies. Because they 
are simple, single scripts - any compatible actor can reuse the actions created for another.
