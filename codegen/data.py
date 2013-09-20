# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Mars"

constants = [
  ]

playerData = [
  Variable('waterStored', int, 'The amount of water a player has.'),
  Variable('spawnRate', int, 'The speed at which a player can spawn units.'),
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

globals = [
  Variable('maxHealth', int, 'The maximum amount of health a unit will have.'),
  Variable('trenchDamage', int, 'The amount of damage walking over a trench.'),
  Variable('waterDamage', int, 'The amount of damage walking over water.'),
  Variable('turnNumber', int, 'The current turn number.'),
  Variable('attackDamage', int, 'The amount of damage a unit will deal.'),
  Variable('offenseCount', int, 'The count of offense.'),
  Variable('defenseCount', int, 'The count of defense.'),
  Variable('maxUnits', int, 'The maximum number of units allowed per player.'),
]
#UNIT
Unit = Model('Unit',
  parent = Mappable,
  data = [
    Variable('owner', int, 'The owner of this unit.'),
    Variable('type', int, 'The maximum number of moves this unit can move.'),
    Variable('curHealth', int, 'The current amount health this unit has remaining.'),
    Variable('curMovement', int, 'The number of moves this unit has remaining.'),
    Variable('maxMovement', int, 'The maximum number of moves this unit can move.'),

    ],
  doc='Represents a single unit on the map.',
    functions=[
    Function('move',[Variable('x', int), Variable('y', int)],
    doc='Make the unit move to the respective x and y location.'),
    Function('attack',[Variable('unit', int)],
    doc='Attack another unit!.'),
    Function('fill',[Variable('tile', int)],
    doc='Put dirt in a hole!'),
    Function('build',[Variable('tile', int)],
    doc='Build something!'),
    ],
  )
#TILE
Tile = Model('Tile',
  parent = Mappable,
  data = [
    Variable('owner', int, 'The owner of the tile.'),
    Variable('type', int, 'The type of tile this tile represents.'),
    Variable('resId', int, 'The owner of a reservoir.'),
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

PumpStation = Model('PumpStation',
  data = [
    Variable('owner', int, 'The owner of the PumpStation.'),
    Variable('waterAmount', int, 'The amount of water the PumpStation pumps.'),
    Variable('seigeCount', int, 'The length of time it takes to capture the PumpStation.'),
    ],
  functions=[],
  doc='',
  plural='SpeciesList',
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


