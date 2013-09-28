# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Mars"

constants = [
  ]

globals = [
  Variable('maxHealth', int, 'The maximum amount of health a unit will have.'),
  Variable('trenchDamage', int, 'The amount of damage walking over a trench.'),
  Variable('waterDamage', int, 'The amount of damage walking over water.'),
  Variable('turnNumber', int, 'The current turn number.'),
  Variable('attackDamage', int, 'The amount of damage a unit will deal.'),
  Variable('offenseCount', int, 'How quickly a unit will siege a base.'),
  Variable('defenseCount', int, 'The much a unit will slow a  siege.'),
  Variable('maxUnits', int, 'The maximum number of units allowed per player.'),
  Variable('unitCost', int, 'The cost of spawning in a new unit'),
  Variable('playerID', int, 'The id of the current player.'),
  Variable('gameNumber', int, 'What number game this is for the server'),
]

playerData = [
  Variable('waterStored', int, 'The amount of water a player has.'),
  Variable('spawnResources', int, 'Resource used to spawn in units'),
  ]

playerFunctions = [
  Function('talk', [Variable('message', str)], doc='Allows a player to display messages on the screen'),
]
#MAPPABLE
Mappable = Model('Mappable',
  data=[
    Variable('x', int, 'X position of the object'),
    Variable('y', int, 'Y position of the object'),
  ],
  doc='A mappable object!',
)

#TILE
Tile = Model('Tile',
  parent = Mappable,
  data = [
    Variable('owner', int, 'The owner of the tile.'),
    Variable('type', int, 'The type of tile this tile represents.'),
    Variable('pumpID', int, 'Determines if this tile is a part of a Pump Station.'),
    Variable('waterAmount', int, 'The amount of water contained on the tile.'),
    Variable('isTrench', int, 'Whether the tile is a trench or not.'),
    ],
  functions=[
    Function('spawn',[Variable('type',int)],
    doc='Attempt to spawn a unit of a type on this tile.'),
    ],
  doc='Represents a single tile on the map, can contain some amount of water.',
  permanent = True,
  )

#UNIT
Unit = Model('Unit',
  parent = Mappable,
  data = [
    Variable('owner', int, 'The owner of this unit.'),
    Variable('type', int, 'The type of this unit (digger/filler).'),
    Variable('hasAttacked', int, 'Whether current unit has attacked or not.'),
    Variable('hasDigged', int, 'Whether the current unit has digged or not.'),
    Variable('hasBuilt', int, 'Whether the current unit has built or not.'),
    Variable('healthLeft', int, 'The current amount health this unit has remaining.'),
    Variable('maxHealth', int, 'The maximum amount of this health this unit can have'),
    Variable('movementLeft', int, 'The number of moves this unit has remaining.'),
    Variable('maxMovement', int, 'The maximum number of moves this unit can move.'),

    ],
  doc='Represents a single unit on the map.',
    functions=[
    Function('move',[Variable('x', int), Variable('y', int)],
    doc='Make the unit move to the respective x and y location.'),
    Function('fill',[Variable('tile', Tile)],
    doc='Put dirt in a hole!'),
    Function('dig',[Variable('tile', Tile)],
    doc='Dig out a tile'),
    ],
  )

Unit.addFunctions([Function("attack", [ Variable("target", Unit)],
    doc='Command to attack another Unit.')])


PumpStation = Model('PumpStation',
  data = [
    Variable('owner', int, 'The owner of the PumpStation.'),
    Variable('waterAmount', int, 'The amount of water the PumpStation pumps.'),
    Variable('siegeCount', int, 'The length of time it takes to capture the PumpStation.'),
    ],
  functions=[
  ],
  doc='Represents a base to which you want to lead water, and a spawn location for new units.',
  permanent = True,
  )

move = Animation('move',
  data=[
    Variable('actingID', int),
    Variable('fromX', int),
    Variable('fromY', int),
    Variable('toX', int),
    Variable('toY', int),
  ],
  )

dig = Animation('dig',
  data=[
    Variable('actingID', int),
    Variable('tileID', int),
  ],
  )

fill = Animation('fill',
  data=[
    Variable('actingID', int),
    Variable('tileID', int),
  ],
  )

attack = Animation('attack',
  data=[
    Variable('actingID', int),
    Variable('targetID', int)
  ],
  )

flow = Animation('flow',
  data=[
    Variable('sourceID', int),
    Variable('destID', int),
    Variable('waterAmount', int),
  ],
  )

spawn = Animation('spawn',
  data=[
    Variable('sourceID', int),
    Variable('unitID', int),
  ],
  )