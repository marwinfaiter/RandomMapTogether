# RandomMapTogether
Simple pyplanet application to add RandomMapsTogether gamemodes

## Installation
### docker
There are two ways I would recommend:
* Using docker and using the following image docker.buddaphest.se/marwinfaiter/pyplanet:rmt
  * Requires a database and also a trackmania server to hook into 
* Cloning this repo and running "docker compose up -d"
  * This is probably the easier one

## configurations
| ***setting***       | ***values***         | ***description***                                                                                                      |
|---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------|
| min_perm_start      | 0,1,2,3              | level required to start the game <br/>LEVEL_PLAYER = 0<br/>LEVEL_OPERATOR = 1<br/>LEVEL_ADMIN = 2<br/>LEVEL_MASTER = 3 |

