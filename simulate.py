from hunt_states import *

class Simulation:
	def __init__(self, hunt_definition, team):
		self.team_hunt_projection = TeamHuntProjection(hunt_definition, team)
		self.current_time = 0

if __name__ == '__main__':
	hunt_definition = HuntDefinition('linear_hunt.json')
	print(hunt_definition)
	print(hunt_definition.puzzle_definitions)

	team = Team(0.25, 0.1, 0.75)
	
	team_hunt_projection = TeamHuntProjection(hunt_definition, team)
	print(team_hunt_projection.puzzle_projections)