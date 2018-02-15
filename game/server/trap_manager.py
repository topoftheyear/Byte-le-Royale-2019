import math
import random

from game.common.enums import *

class TrapManager:

    def __init__(self, trap, units, verbose):
        self.trap = trap
        self.units = units
        self.verbose = verbose

        self.trap_damage_counter = 0

        self.done = False
        self.success = None


    def play_round(self, game_log):
        living_units = sorted([ u for u in self.units if u.is_alive() ], key=lambda e: e.name)

        # handle unit actions
        for idx, unit in enumerate(sorted(self.units, key=lambda e: e.name)):
            if unit.is_alive():

                trap_energy = unit.current_focus if self.trap.stat is TrapStat.focus else unit.current_will

                if unit.trap_action is TrapAction.large_effort and trap_energy >= 5:

                    if self.trap.pass_type is TrapPassType.group_pass:
                        self.trap.current_effort = min(self.trap.required_effort, self.trap.current_effort+4)

                        game_log["events"].append({
                            "type": Event.trap_effort,
                            "current_effort": self.trap.current_effort
                        })

                        if self.trap.stat is TrapStat.focus:
                            unit.current_focus = max(0, unit.current_focus-5)
                        else:
                            unit.current_will = max(0, unit.current_will-5)

                    elif (self.trap.pass_type is TrapPassType.individual_pass or
                          self.trap.pass_type is TrapPassType.group_pass_on_first_success):
                        self.trap.current_effort[idx] = min(self.trap.required_effort, self.trap.current_effort[idx]+4)

                        game_log["events"].append({
                            "type": Event.trap_effort,
                            "unit_idx": idx,
                            "current_effort": self.trap.current_effort[idx]
                        })

                        if self.trap.stat is TrapStat.focus:
                            unit.current_focus = max(0, unit.current_focus-5)
                        else:
                            unit.current_will = max(0, unit.current_will-5)

                elif unit.trap_action is TrapAction.little_effort and trap_energy >= 2:

                    if self.trap.pass_type is TrapPassType.group_pass:
                        self.trap.current_effort = min(self.trap.required_effort, self.trap.current_effort+2)

                        game_log["events"].append({
                            "type": Event.trap_effort,
                            "current_effort": self.trap.current_effort
                        })

                        if self.trap.stat is TrapStat.focus:
                            unit.current_focus = max(0, unit.current_focus-2)
                        else:
                            unit.current_will = max(0, unit.current_will-2)

                    elif (self.trap.pass_type is TrapPassType.individual_pass or
                          self.trap.pass_type is TrapPassType.group_pass_on_first_success):
                        self.trap.current_effort[idx] = min(self.trap.required_effort, self.trap.current_effort[idx]+2)

                        game_log["events"].append({
                            "type": Event.trap_effort,
                            "unit_idx": idx,
                            "current_effort": self.trap.current_effort[idx]
                        })

                        if self.trap.stat is TrapStat.focus:
                            unit.current_focus = max(0, unit.current_focus-2)
                        else:
                            unit.current_will = max(0, unit.current_will-2)


        # handle any trap damage
        self.trap_damage_counter += 1
        if self.trap_damage_counter >= self.trap.damage_interval:
            self.trap_damage_counter = 0

            trap_targets = []

            if self.trap.damage_type is TrapDamageType.random_one:
                copy = living_units[:]

                if len(copy) > 0:
                    target = random.choice(copy)
                    trap_targets.append(target)

            elif self.trap.damage_type is TrapDamageType.random_two:
                copy = living_units[:]

                if len(copy) > 0:
                    target = random.choice(copy)
                    trap_targets.append(target)
                    copy.remove(target)

                if len(copy) > 0:
                    target = random.choice(copy)
                    trap_targets.append(target)

            elif self.trap.damage_type is TrapDamageType.random_three:
                copy = living_units[:]

                if len(copy) > 0:
                    target = random.choice(copy)
                    trap_targets.append(target)
                    copy.remove(target)

                if len(copy) > 0:
                    target = random.choice(copy)
                    trap_targets.append(target)
                    copy.remove(target)

                if len(copy) > 0:
                    target = random.choice(copy)
                    trap_targets.append(target)

            elif self.trap.damage_type is TrapDamageType.all:
                trap_targets = living_units

            elif self.trap.damage_type is TrapDamageType.highest_health:
                trap_targets.append( max(living_units, key=lambda e: e.current_health) )

            elif self.trap.damage_type is TrapDamageType.lowest_health:
                trap_targets.append( min(living_units, key=lambda e: e.current_health) )

            # apply trap damage to targets
            for unit in trap_targets:
                if unit.trap_action == TrapAction.evade:
                    dmg = math.floor(self.trap.damage * 0.5)

                    # if individual pass and unit has completed the trap
                    # don't let it take damage from it
                    if self.trap.trap_type is TrapPassType.individual_pass:
                        unit_idx = self.units.index(unit)
                        if self.trap.current_effort[unit_idx] >= self.trap.required_effort:
                            continue

                    unit.current_health = max(0, unit.current_health-dmg)

                    game_log["events"].append({
                        "type": Event.trap_damage,
                        "unit": unit.id,
                        "damage": dmg,
                    })
                else:
                    unit.current_health = max(0, unit.current_health-self.trap.damage)

        # reset unit actions
        for unit in self.units:
            unit.trap_action = TrapAction.wait

        # regain one point of trap stats
        for unit in living_units:
            unit.current_focus = min(unit.focus, unit.current_focus+1)
            unit.current_will = min(unit.will, unit.current_will+1)

        # check if the trap has been cleared
        self.check_done()

    def check_done(self):

        living_units = [ u for u in self.units if u.is_alive() ]
        if len(living_units) == 0:
            self.done = True
            self.success = False
            return

        if self.trap.pass_type is TrapPassType.group_pass:
            if self.trap.current_effort >= self.trap.required_effort:
                self.done = True
                self.success = True

        elif self.trap.pass_type is TrapPassType.individual_pass:
            completed = []
            for unit_effort, unit in zip(self.trap.current_effort, sorted(self.units, key=lambda u: u.name)):
                if unit.is_alive():
                    completed.append( unit_effort >= self.trap.required_effort )
                else:
                    completed.append(True)

            if all(completed):
                self.done = True
                self.success = True


        elif self.trap.pass_type is TrapPassType.group_pass_on_first_success:

            completed = []
            for unit_effort, unit in zip(self.trap.current_effort, sorted(self.units, key=lambda u: u.name)):
                if unit.is_alive():
                    completed.append( unit_effort >= self.trap.required_effort )

            if any(completed):
                self.done = True
                self.success = True

    def serialize_state(self):
        data = {}

        data["message_type"] = MessageType.trap_round
        data["trap"] = self.trap.to_dict()

        data["units"] = []
        for u in self.units:
            d = u.to_dict()
            data["units"].append(d)

        return data

    def print(self, msg, force=False):
        if self.verbose or force:
            print(msg)


