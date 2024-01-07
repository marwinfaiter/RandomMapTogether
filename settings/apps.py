"""
This file contains the apps & apps settings and overrides the default ones that are defined in the core.
Documentation: http://pypla.net/

If you want to use other configuration methods like YAML or JSON files, take a look at http://pypla.net/ and head to the
configuration pages.
"""

# In the apps dictionary and array you configure the apps (or plugins) are loaded for specific pools (controllers).
# Be aware that the list will *ALWAYS* be prepended after the mandatory defaults are loaded in place.
# The mandatory defaults are specific per version, refer to the documentation:
# DOCUMENTATION: http://pypla.net/
APPS = {
    'default': [
        "pyplanet.apps.contrib.admin",
        "pyplanet.apps.contrib.players",
        "it.thexivn.random_maps_together",
    ]
}
