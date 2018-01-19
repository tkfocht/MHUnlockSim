from hunt_states import *

class Simulation:
    def __init__(self, hunt_definition, team):
        self.hunt_definition = hunt_definition
        self.puzzle_definitions = { p.id: p for p in self.hunt_definition.puzzle_definitions }
        self.team_hunt_projection = TeamHuntProjection(hunt_definition, team)
        self.current_time = 0
        self.puzzle_states = { p.id: 'LOCKED' for p in hunt_definition.puzzle_definitions }
        self.puzzle_history = {}
        self.team_state = hunt_definition.initial_team_state if hunt_definition.initial_team_state else {}
        self.complete = False

    def update_unlocks(self):
        updates_made = False
        for pid in [pk for pk in self.puzzle_states.keys() if self.puzzle_states[pk] == 'LOCKED']:
            p = self.puzzle_definitions[pid]
            if p.unlock.should_unlock(self):
                self.puzzle_states[p.id] = 'UNLOCKED'
                if p.id not in self.puzzle_history:
                    self.puzzle_history[p.id] = {}
                self.puzzle_history[p.id]['UNLOCKED'] = self.current_time
                updates_made = True
        if updates_made:
            self.update_unlocks()

    def update_solves(self):
        for pid in [pk for pk in self.puzzle_states.keys() if self.puzzle_states[pk] == 'UNLOCKED']:
            p = self.puzzle_definitions[pid]
            if self.team_hunt_projection.puzzle_projections[pid] + self.puzzle_history[pid]['UNLOCKED'] <= self.current_time:
                self.puzzle_states[p.id] = 'SOLVED'
                self.puzzle_history[p.id]['SOLVED'] = self.current_time
                if p.reward:
                    for k in p.reward.keys():
                        self.team_state[k] += p.reward[k]


    def advance(self):
        self.current_time += 1
        self.update_solves()
        self.update_unlocks()
        if (self.hunt_definition.end_state_unlock.should_unlock(self)):
            self.complete = True


    def __repr__(self):
        return '{{ current_time: {0}, puzzle_states: {{ {1} }}, team_state: {2} }}' \
            .format(self.current_time, ', '.join([k + ': ' + v for k,v in self.puzzle_states.iteritems()]), self.team_state)


if __name__ == '__main__':
    hunt_definition = HuntDefinition('loose_prereq_hunt.json')
    print(hunt_definition)
    print(hunt_definition.puzzle_definitions)

    team = Team(0.5, 0.05, 0.95)
    
    team_hunt_projection = TeamHuntProjection(hunt_definition, team)
    print(team_hunt_projection.puzzle_projections)

    sim = Simulation(hunt_definition, team)
    print(sim)

    while not sim.complete:
        sim.advance()
        print(sim)