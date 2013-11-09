# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Mars"

constants = [
  ]

modelOrder = ['Player', 'Mappable', 'PumpStation', 'Unit', 'Tile', 'UnitType']

globals = [
  Variable('mapWidth', int, 'The width of the total map.'),
  Variable('mapHeight', int, 'The height of the total map.'),
  Variable('waterDamage', int, 'The amount of damage walking over water.'),
  Variable('turnNumber', int, 'The current turn number.'),
  Variable('maxUnits', int, 'The maximum number of units allowed per player.'),
  Variable('playerID', int, 'The id of the current player.'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('maxSiege', int, 'The maximum siege value before the PumpStation is sieged.'),
  Variable('oxygenRate', float, 'The rate at which missing oxygen is regained.'),
  Variable('depositionRate', int, 'The number of turns until sediment is deposited on the trenches.'),
]

playerData = [
  Variable('waterStored', int, 'The amount of water a player has.'),
  Variable('oxygen', int, 'Resource used to spawn in units.'),
  Variable('maxOxygen', int, "The player's oxygen cap."),
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
    Variable('pumpID', int, 'Determines if this tile is a part of a Pump Station.'),
    Variable('waterAmount', int, 'The amount of water contained on the tile.'),
    Variable('depth', int, 'The depth of the tile. Tile is a trench if depth is greater than zero.'),
    Variable('turnsUntilDeposit', int, 'The number of turns until sediment is deposited on this tile.'),
    Variable('isSpawning', int, 'Determines if this tile is attempting to spawn something or not.')
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
    Variable('type', int, 'The type of this unit. This type refers to list of UnitTypes.'),
    Variable('hasAttacked', int, 'Whether current unit has attacked or not.'),
    Variable('hasDug', int, 'Whether the current unit has dug or not.'),
    Variable('hasFilled', int, 'Whether the current unit has filled or not.'),
    Variable('healthLeft', int, 'The current amount health this unit has remaining.'),
    Variable('maxHealth', int, 'The maximum amount of this health this unit can have'),
    Variable('movementLeft', int, 'The number of moves this unit has remaining.'),
    Variable('maxMovement', int, 'The maximum number of moves this unit can move.'),
    Variable('range', int, 'The range of this unit\'s attack.'),
    Variable('offensePower', int, 'The power of the unit\'s offensive siege ability.'),
    Variable('defensePower', int, 'The power of the unit\'s defensive siege ability.'),
    Variable('digPower', int, 'The power of this unit types\'s digging ability.'),
    Variable('fillPower', int, 'The power of this unit type\'s filling ability.'),
    Variable('attackPower', int, 'The power of this unit type\'s attack.'),

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
    Variable('siegeAmount', int, 'The amount the PumpStation has been sieged.'),
    ],
  functions=[
  ],
  doc='Represents a base to which you want to lead water.',
  permanent = True,
  )

#UNITTYPE
UnitType = Model('UnitType',
  data = [
    Variable('name', str, 'The name of this type of unit.'),
    Variable('type', int, 'The UnitType specific id representing this type of unit.'),
    Variable('cost', int, 'The oxygen cost to spawn this unit type into the game.'),
    Variable('attackPower', int, 'The power of the attack of this type of unit.'),
    Variable('digPower', int, 'The power of this unit types\'s digging ability.'),
    Variable('fillPower', int, 'The power of this unit type\'s filling ability.'),
    Variable('maxHealth', int, 'The maximum amount of this health this unit can have'),
    Variable('maxMovement', int, 'The maximum number of moves this unit can move.'),
    Variable('offensePower', int, 'The power of the unit type\'s offensive siege ability.'),
    Variable('defensePower', int, 'The power of the unit type\'s defensive siege ability.'),
    Variable('range', int, 'The range of the unit type\'s attack.')

    ],
  doc='Represents type of unit.',
  functions=[],
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

death = Animation('death',
  data=[
    Variable('sourceID', int),
  ],
  )
