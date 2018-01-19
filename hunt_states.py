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



class Unlock:
    def __init__(self):
        pass

	def should_unlock(self, simulation):
		return False

class HuntStartUnlock(Unlock):
	def __init__(self, unlock_dict):
		pass

	def should_unlock(self, simulation):
		return True

class PuzzlesSolvedUnlock(Unlock):
	def __init__(self, unlock_dict):
		self.prereq_ids = unlock_dict['prereqs']
		self.minimum = unlock_dict['minimum'] if 'minimum' in unlock_dict else len(self.prereq_ids)

	def should_unlock(self, simulation):
		return len([s for s in [simulation.puzzle_states[k] for k in self.prereq_ids] if s == 'SOLVED']) >= self.minimum

class ScoreMinimumUnlock(Unlock):
	def __init__(self, unlock_dict):
		self.score = unlock_dict['score']

	def should_unlock(self, simulation):
		return simulation.team_state['score'] >= self.score

def generate_unlock(unlock_dict):
    if unlock_dict['rule'] == 'hunt_start':
        return HuntStartUnlock(unlock_dict)
    elif unlock_dict['rule'] == 'puzzles_solved':
    	return PuzzlesSolvedUnlock(unlock_dict)
    elif unlock_dict['rule'] == 'score_minimum':
    	return ScoreMinimumUnlock(unlock_dict)
    else:
        raise ValueError


class PuzzleDefinition:
    def __init__(self, puzzle_definition_dict):
        self.id = puzzle_definition_dict['id']
        self.solve_pattern = generate_solve_pattern(puzzle_definition_dict['solve_pattern'])
        self.unlock = generate_unlock(puzzle_definition_dict['unlock'])
        self.reward = puzzle_definition_dict['reward'] if 'reward' in puzzle_definition_dict else None

    def __repr__(self):
        return 'PuzzleDefinition: {{ id: {0}, p50: {1} }}'.format(self.id, self.solve_pattern.generate_solve_time(0.5))

class HuntDefinition:
    def __init__(self, filename):
        hunt_definition_data = json.load(open(filename))
        if 'puzzles' in hunt_definition_data:
            self.puzzle_definitions = [PuzzleDefinition(p_dict) for p_dict in hunt_definition_data['puzzles']]
        self.end_state_unlock = generate_unlock(hunt_definition_data['end_state'])
        self.initial_team_state = hunt_definition_data['initial_team_state'] if 'initial_team_state' in hunt_definition_data else None

class TeamHuntProjection:
    def __init__(self, hunt_definition, team):
        def project(puzzle_definition):
            team_pctile = team.generate_regular_solve_percentile()
            solve_time = puzzle_definition.solve_pattern.generate_solve_time(team_pctile)
            return int(solve_time)
        self.puzzle_projections = { p_def.id: project(p_def) for p_def in hunt_definition.puzzle_definitions }