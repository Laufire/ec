Design
=======

    **private** is a module launcher. It's a simpler and better implementatoin of commander. It is designed to shed some feature creep and to provide a better UX.
    
Design Goals
------------
* A minimalistic design.

* Improved usability.

* Zero feature creep.

* Using simpler structures on the code level.

Features
--------
Planned
#######

* Launching individual modules.

* Shell and Dispatch modes.

* Typed params.

* Every param is to be input, separately; with every query having a description, default value etc.

Later
#####

* Treating modules of a dir / package as sibblings.

* Externally adding params to modules that weren't designed for private.

* Helper commands like, help, list, etc, for shell mode.

Ideas
-----
* Using simple functions,lambdas and callable classes as types, bot for conversion and validation.

* Nested params, by using tasks as types.

Differences from Commander
--------------------------
Design
######
* Has only the essential features.

* Reduced dependencies (almost none).

Shed
####
* docstring and external configs, thus eliminates the need for validation and generation.

* Batch, TUI, Web and Proxy modes.

* Hooks.

* Standard helpers.

* Development utils, like debugging etc.

Changes
#######
* Config API-s are to be implemented as routes (inspired by bottle), hence docstrings are freed up for other purposes (especially for documentation).

Additions
#########

* Custom types.

* Supplying args are more interative.

Notes
------
* The args follow a **argName=value** pattern for enhancing redability, especially on the dispatch mode.

* The config decorators return the underlyings, instead of their decorated versions, so to allow a hasssle free use of the underlyings within the script.


Thoughts
--------
* **Commandlets** - plugin like mini-programmes that could acomplish specific tasks.

Learned
-------
* With experience errors get reduced.

* Simpler structures are often robust.

Decisions
---------
* The methods to be used by the loade scripts are added to __builtins__, in order to avoid an explicit import of private from the script; which will load a separate instance of private and complicate the passing of data between the two instances.

* 150630_1500 Decided to add an attribute __pr_member__ the underlyings, to identify them for private. An alternate impementation was thought of; in which the underlynings and the members would be buffered (as a list / dict) and processed before starting the core. Though the later method doesn't alter the underlying, the former is chosen for it's simplicity. It took ~30 mins for the rewiring.
