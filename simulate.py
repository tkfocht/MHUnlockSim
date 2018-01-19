from hunt_states import *

if __name__ == '__main__':
	hunt_definition = HuntDefinition('linear_hunt.json')
	print(hunt_definition)
	print(hunt_definition.puzzle_definitions)

	team = Team(0.25, 0.1, 0.75)
	
	teamHuntProj = TeamHuntProjection(hunt_definition, team)
	print(teamHuntProj.puzzle_projections)