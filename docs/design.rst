Design
=======

		**ec** is a module launcher. It's a simpler and better implementation of commander. It is designed to shed some feature creep and to provide a better UX.
		
Design Goals
------------
* A minimalistic design.

* Improved usability.

* Zero feature creep.

* Using simpler structures on the code level.

Ideas
-----
* Using simple functions,lambdas and callable classes as types, bot for conversion and validation.

* Nested args, by using tasks as types.

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

* Supplying args are more interactive.

Notes
------
* The args follow a **argName=value** pattern for enhancing readability, especially on the dispatch mode.

* The config decorators return the underlyings, instead of their decorated versions, so to allow a hassle free use of the underlyings within the script.


Thoughts
--------
* **scriptlets** - plugin like mini-programs that could accomplish specific tasks.

* Example script to serve as the documentation, as well as the targets for the tests. To keep it DRY.

Learned
-------
* With experience errors get reduced.

* Simpler structures are often robust.

* Writing tests is a lot simpler than imagined.

* Configurable code (code tht could be manipulated through data) is more structured.

* Visualizing the data flow helps with creating better structures.

* Programming is not software engineering.

* Reading good code could help writting good code.

* Data inputs should be preserved, they might have additions, but not editions or deletions.

* Complex and humongus classes makes the implementation inflexible and complex to understand. In a flexible design classes should be simple, with most processing happens in flow *(the path of functions, through which the objects of the classes pass through)*. In other words: A program with a more functions that handle simple objects is more flexible than a programm that combines classes to achieve the same.


Decisions
---------
* The methods to be used by the loaded scripts are added to __builtins__, in order to avoid an explicit import of ec from the script; which will load a separate instance of ec and complicate the passing of data between the two instances.

* 150630_1500	Decided to add an attribute __ec_member__ the underlyings, to identify them for ec. An alternate implementation was thought of; in which the underlyings and the members would be buffered (as a list / dict) and processed before starting the core. Though the later method doesn't alter the underlying, the former is chosen for it's simplicity. It took ~30 mins for the rewiring.

* 150714_0400	Decided to use an explicit method **modules.config.member** to facilitate the addition of imported members; instead of automatically scanning the scripts for importables. This is because "Explicit is better than implicit".
