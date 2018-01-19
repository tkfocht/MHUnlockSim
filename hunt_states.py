import json
from scipy.stats import gamma, triang

class Team:
	def __init__(self, percentile_mode, percentile_lower, percentile_upper):
		self.percentile_mode = percentile_mode
		self.percentile_lower = percentile_lower
		self.percentile_upper = percentile_upper

	def generate_regular_solve_percentile(self):
		scale = self.percentile_upper - self.percentile_lower
		shape = ((self.percentile_mode - self.percentile_lower) / float(self.percentile_upper - self.percentile_lower))
		return triang.rvs(shape, scale=scale, loc=self.percentile_lower, size=1)[0]

class SolvePattern:
	def __init__(self):
		pass

	def generate_solve_time(self):
		pass

class IndependentGammaSolvePattern(SolvePattern):
	def __init__(self, solve_pattern_dict):
		self.avg_seed = solve_pattern_dict['avg_seed']
		self.sd_seed = solve_pattern_dict['sd_seed']
		self.scale = self.sd_seed * self.sd_seed / float(self.avg_seed)
		self.shape = self.avg_seed / float(self.scale)

	def generate_solve_time(self, percentile):
		return gamma.ppf(percentile, self.shape, scale=self.scale)

def generate_solve_pattern(solve_pattern_dict):
	if solve_pattern_dict['rule'] == 'independent_gamma':
		return IndependentGammaSolvePattern(solve_pattern_dict)
	else:
		raise ValueError

def Unlock:
	def __init__(self):
		pass
	

class PuzzleDefinition:
	def __init__(self, puzzle_definition_dict):
		self.id = puzzle_definition_dict['id']
		self.solve_pattern = generate_solve_pattern(puzzle_definition_dict['solve_pattern'])

	def __repr__(self):
		return 'PuzzleDefinition: {{ id: {0}, p50: {1} }}'.format(self.id, self.solve_pattern.generate_solve_time(0.5))

class HuntDefinition:
	def __init__(self, filename):
		hunt_definition_data = json.load(open(filename))
		if 'puzzles' in hunt_definition_data:
			self.puzzle_definitions = [PuzzleDefinition(p_dict) for p_dict in hunt_definition_data['puzzles']]

class TeamHuntProjection:
	def __init__(self, hunt_definition, team):
		def project(puzzle_definition):
			team_pctile = team.generate_regular_solve_percentile()
			solve_time = puzzle_definition.solve_pattern.generate_solve_time(team_pctile)
			return int(solve_time)
		self.puzzle_projections = { p_def.id: project(p_def) for p_def in hunt_definition.puzzle_definitions }