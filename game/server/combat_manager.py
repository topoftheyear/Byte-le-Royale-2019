import math

from game.common.enums import *
from game.common.unit import *

special_abilities = {}

def get_special_ability(unit_class, verbose):
    global special_abilities

    # melee units

    if unit_class == UnitClass.knight:
        if UnitClass.knight not in special_abilities:
            special_abilities[UnitClass.knight] = Taunt(verbose)
        return special_abilities[UnitClass.knight]

    elif unit_class == UnitClass.brawler:
        if UnitClass.brawler not in special_abilities:
            special_abilities[UnitClass.brawler] = FitOfRage(verbose)
        return special_abilities[UnitClass.brawler]

    elif unit_class == UnitClass.pikeman:
        if UnitClass.pikeman not in special_abilities:
            special_abilities[UnitClass.pikeman] = TargetWeakness(verbose)
        return special_abilities[UnitClass.pikeman]

    # magic units

    elif unit_class == UnitClass.magus:
        if UnitClass.magus not in special_abilities:
            special_abilities[UnitClass.magus] = ElementalBurst(verbose)
        return special_abilities[UnitClass.magus]

    elif unit_class == UnitClass.wizard:
        if UnitClass.wizard not in special_abilities:
            special_abilities[UnitClass.wizard] = Invigorate(verbose)
        return special_abilities[UnitClass.wizard]

    elif unit_class == UnitClass.sorcerer:
        if UnitClass.sorcerer not in special_abilities:
            special_abilities[UnitClass.sorcerer] = Illusion(verbose)
        return special_abilities[UnitClass.sorcerer]

    elif unit_class == UnitClass.alchemist:
        if UnitClass.alchemist not in special_abilities:
            special_abilities[UnitClass.alchemist] = Resupply(verbose)
        return special_abilities[UnitClass.alchemist]

def reset_special_abilities():
    global special_abilities
    for _, sa in special_abilities.items():
        sa.reset()

def cooldown_abilities():
    global special_abilities
    for _, sa in special_abilities.items():
        sa.cooldown()


class SpecialAbility:

    def __init__(self, verbose):
        self.charged = False
        self.charging = False

        self.cooldown_timer = 0
        self.charge_timer = 0

        self.target = None

        self.verbose = verbose


    def cooldown(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def charge(self):
        if self.charge_timer > 0:
            self.charge_timer -= 1

    def set_target(self, target):
        self.target = target

    def reset(self):
        pass

    def print(self, msg):
        if self.verbose:
            print(msg)

class Taunt(SpecialAbility):

    def use(self, damage, targets, unit, monster):
        pass


class FitOfRage(SpecialAbility):

    def __init__(self, verbose):
        SpecialAbility.__init__(self, verbose)

        self.damage_taken = 0

    def use(self, turn_log, unit, monster, damage):

        if not self.charged:
            self.print("{0} is becoming enraged".format(unit.name))

            turn_log["events"].append({
                "type": Event.special_ability_charging,
                "unit": unit.id,
            })
            self.damage_taken += damage

            if not self.charging:
                self.charge_timer = 1
                self.charging = True
            else:
                self.charge_timer -= 1
                if self.charge_timer <= 0:
                    self.charging = False
                    self.charged = True
        else:
            n = 1.0
            if math.floor(unit.health * 0.25) < self.damage_taken <= math.floor(unit.health * 0.5):
                n = 2.0
            elif math.floor(unit.health * 0.5) < self.damage_taken <= math.floor(unit.health * 75):
                n = 3.0
            elif damage > math.floor(unit.health * 0.75):
                n = 3.5

            damage = math.floor(
                self.damage_taken * ( 3 + (0.25 *
                                               (
                                                   min(self.damage_taken, unit.health*0.1)/
                                                   unit.health * 0.01
                                               )
                                           )
                                     )
            )

            monster.current_health -= damage
            if monster.current_health < 0: monster.current_health = 0

            # heal unit for 10% of damage dealt
            health_to_restore = math.floor(damage * .25)
            unit.current_health += health_to_restore
            unit.current_health = min(unit.current_health, unit.health)

            turn_log["events"].append({
                "type": Event.special_ability_attack,
                "unit": unit.id,
                "damage": damage
            })

            self.print("In a Fit of Rage, {0} deals {1} damage to {2}".format(unit.name, damage, monster.name))

            self.reset()

    def reset(self):
        self.charged = False
        self.charging = False
        self.charge_timer = 0
        self.damage_taken = 0


class TargetWeakness(SpecialAbility):

    def use(self, turn_log, unit, monster):
        if not self.charged:
            self.charged = True
            self.print("{} searches {} for weaknesses.".format(unit.name, monster.name))

            turn_log["events"].append({
                "type": Event.special_ability_charging,
                "unit": unit.id,
            })

        else:
            self.charged = False

            damage = math.floor( unit.primary_weapon.damage * 2.5 )
            monster.current_health -= damage
            if monster.current_health < 0: monster.current_health = 0

            turn_log["events"].append({
                "type": Event.special_ability_attack,
                "unit": unit.id,
                "damage": damage
            })

            self.print("Seeing a weakness, {} strikes at {} for {} damage.".format(unit.name, monster.name, damage))

    def reset(self):
        self.charged = False


class ElementalBurst(SpecialAbility):

    def use(self, turn_log, unit, monster):

        if not self.charged:
            self.print("{0} charges up magical energy.".format(unit.name))

            turn_log["events"].append({
                "type": Event.special_ability_charging,
                "unit": unit.id,
            })

            if not self.charging:
                self.charge_timer = 2
                self.charging = True
            else:
                self.charge_timer -= 1
                if self.charge_timer <= 0:
                    self.charged = True
                    self.charging = False

        else:
            dmg_multiplier = 2.0
            for damage_type in [ DamageType.cold, DamageType.fire, DamageType.electricity ]:
                if damage_type in monster.weaknesses:
                    dmg_multiplier += 0.25

            damage = math.floor( unit.primary_weapon.damage * dmg_multiplier )
            monster.current_health -= damage
            if monster.current_health < 0: monster.current_health = 0

            turn_log["events"].append({
                "type": Event.special_ability_attack,
                "unit": unit.id,
                "damage": damage
            })

            self.print("With a burst of elemental energy, {0} deals {1} damage to {2}".format(unit.name, damage, monster.name))

            self.reset()

    def reset(self):
        self.charged = False
        self.charging = False
        self.charge_timer = 0

class Invigorate(SpecialAbility):

    def use(self):
        if self.cooldown_timer <= 0:
            self.cooldown_timer = 3
        else:
            self.cooldown_timer -= 1

class Illusion(SpecialAbility):

    def __init__(self, verbose):
        SpecialAbility.__init__(self, verbose)

    def use(self):
        if self.cooldown_timer <= 0:
            self.cooldown_timer = 5

    def reset(self):
        pass

class Resupply(SpecialAbility):

    def use(self, unit, bomb_type):
        pass


class CombatManager:

    def __init__(self, monster, units, verbose):
        self.round = 1

        self.monster = monster
        self.units = units

        self.done = False
        self.done_reason = ""
        self.success = None

        self.verbose = verbose

        # reset special abilities
        reset_special_abilities()


    def serialize_combat_state(self, first=False, last=False):
        data = {}

        if first:
            data["message_type"] = MessageType.combat_begin
        elif last:
            data["message_type"] = MessageType.combat_end
        else:
            data["message_type"] = MessageType.combat_round

        data["monster"] = self.monster.to_dict()

        data["units"] = []
        for u in self.units:
            d = u.to_dict()
            data["units"].append(d)

        return data



    def play_round(self, turn_log):
        living_units = [ u for u in self.units if u.is_alive() ]

        taunt_unit = None
        brawler_damage = 0
        invigorated_unit = None
        disguised_unit = None
        disguised_as_unit = None

        # handle early special abilities
        for unit in living_units:
            if unit.combat_action == CombatAction.special_ability:
                sa = get_special_ability(unit.unit_class, self.verbose)

                if unit.unit_class is UnitClass.knight:
                    taunt_unit = unit
                    turn_log["events"].append({
                        "type": Event.special_ability,
                        "unit": unit.id,
                        "target_1": None,
                        "target_2": None
                    })

                elif unit.unit_class == UnitClass.wizard:
                    if sa.cooldown_timer <= 0:
                        sa.use()
                        for u in self.units:
                            if u.id == unit.combat_action_target_1:
                                invigorated_unit = u
                                break
                        if invigorated_unit is not None:
                            self.print("{0} casts invigorate on {1}".format(unit.name, invigorated_unit.name))
                            turn_log["events"].append({
                                "type": Event.special_ability,
                                "unit": unit.id,
                                "target_1": invigorated_unit.id,
                                "target_2": None
                            })

                elif unit.unit_class == UnitClass.sorcerer:
                    if sa.cooldown_timer <= 0:
                        sa.use()
                        idx_1 = None
                        idx_2 = None
                        for idx, u in enumerate(living_units):
                            if unit.combat_action_target_1 == u.id:
                                idx_1 = idx
                            elif unit.combat_action_target_2 == u.id:
                                idx_2 = idx

                        if idx_1 is not None and idx_2 is not None:
                            self.print("{0} casts illusion on {1} disguising them as {2}".format(
                                unit.name,
                                living_units[idx_1].name,
                                living_units[idx_2].name))
                            disguised_unit = living_units[idx_1]
                            disguised_as_unit = living_units[idx_2]

                            living_units[idx_1] = living_units[idx_2]
                            living_units.remove(living_units[idx_2])

                            turn_log["events"].append({
                                "type": Event.special_ability,
                                "unit": unit.id,
                                "target_1": unit.combat_action_target_1,
                                "target_2": unit.combat_action_target_2
                            })


        # verify that invigorated_unit is not taunt_unit
        if invigorated_unit is not None:
            if taunt_unit is not None  and taunt_unit == invigorated_unit:
                # cancel taunt if unit is invigorated
                taunt_unit = None

        # pick targets / moves
        monster_target = self.monster.attack(living_units)
        monster_damage = self.monster.damage

        if ((disguised_as_unit is not None and disguised_unit is not None) and
             monster_target is disguised_as_unit):
            monster_target = disguised_unit


        # Apply monster damage
        if taunt_unit is not None:
            # Knight Taunt ability implementation
            blocked_damage = 0

            if type(monster_target) is list or type(monster_target) is tuple:
                # Deal Damage to other units
                damage = math.floor(monster_damage * 0.5)
                for target in monster_target:
                    blocked_damage += monster_damage - damage

                    if target.unit_class is UnitClass.brawler:
                        # record brawler damage
                        brawler_damage += damage

                    if target is not self:
                        target.current_health -= damage
                        if target.current_health < 0: target.current_health = 0

                        turn_log["events"].append({
                            "type": Event.monster_attack,
                            "unit": target.id,
                            "damage": damage
                        })

                        self.print("{0} deals {1} damage to {2}".format(
                            self.monster.name,
                            damage,
                            target.name))
            else:
                # Calculate Damage
                damage = math.floor(monster_damage * 0.85)

            blocked_damage += monster_damage - damage

            # Apply Damage to self
            taunt_unit.current_health -= damage
            if taunt_unit.current_health < 0: taunt_unit.current_health = 0

            turn_log["events"].append({
                "type": Event.monster_attack,
                "unit": taunt_unit.id,
                "damage": damage
            })

            self.print("{0} deals {1} damage to {2}".format(
                self.monster.name,
                damage,
                taunt_unit.name))
            self.print("{0} blocked {1} damage due to taunt.".format(taunt_unit.name, blocked_damage))

        else:
            # Normal Damage ( without taunt) implementation
            if type(monster_target) is not list:
                monster_target = [ monster_target ]

            for u in monster_target:
                u.current_health -= monster_damage

                turn_log["events"].append({
                    "type": Event.monster_attack,
                    "unit": u.id,
                    "damage": monster_damage
                })

                if u.unit_class is UnitClass.brawler:
                    # record brawler damage
                    brawler_damage += monster_damage

                if u.current_health < 0:
                    u.current_health = 0

                self.print("{0} deals {1} damage to {2}".format(
                    self.monster.name,
                    monster_damage,
                    u.name))


        # apply unit damage to monster
        for unit in living_units:
            dmg = 0
            weapon = None


            # get appropriate weapon
            if unit.combat_action == CombatAction.primary_weapon:
                self.print("{} uses primary weapon".format(unit.name))
                weapon = unit.primary_weapon
                item_slot = ItemSlot.primary

            elif unit.combat_action == CombatAction.special_ability:
                sa = get_special_ability(unit.unit_class, self.verbose)

                if unit.unit_class is UnitClass.brawler:
                    sa.use(turn_log, unit, self.monster, brawler_damage)

                elif unit.unit_class is UnitClass.pikeman:
                    sa.use(turn_log, unit, self.monster)

                elif unit.unit_class is UnitClass.alchemist:
                    if unit.combat_action_target_1 is 1:
                        if unit.bomb_1 is not None and unit.bomb_1_quantity < 3:
                            unit.bomb_1_quantity = 3

                            turn_log["events"].append({
                                "type": Event.special_ability,
                                "unit": unit.id
                            })

                    if unit.combat_action_target_1 is 2:
                        if unit.bomb_2 is not None and unit.bomb_2_quantity < 3:
                            unit.bomb_2_quantity = 3

                            turn_log["events"].append({
                                "type": Event.special_ability,
                                "unit": unit.id
                            })

                elif unit.unit_class is UnitClass.magus:
                    sa.use(turn_log, unit, self.monster)

            else:
                if unit.unit_class is UnitClass.rogue: # Hanble Rogue Items
                    if unit.combat_action == CombatAction.secondary_1 and unit.bomb_1 is not None and unit.bomb_1_quantity > 0:
                        self.print("{} uses {}".format(unit.name, unit.bomb_1.name))
                        weapon = unit.bomb_1
                        item_slot = ItemSlot.bomb_1
                        unit.bomb_1_quantity -= 1

                    elif unit.combat_action == CombatAction.secondary_2 and unit.bomb_2 is not None and unit.bomb_2_quantity > 0:
                        self.print("{} uses {}".format(unit.name, unit.bomb_2.name))
                        weapon = unit.bomb_2
                        item_slot = ItemSlot.bomb_2
                        unit.bomb_2_quantity -= 1

                    elif unit.combat_action == CombatAction.secondary_3 and unit.bomb_3 is not None and unit.bomb_3_quantity > 0:
                        self.print("{} uses {}".format(unit.name, unit.bomb_3.name))
                        weapon = unit.bomb_3
                        item_slot = ItemSlot.bomb_3
                        unit.bomb_3_quantity -= 1

                elif unit.unit_class is UnitClass.alchemist: # Handle Alchemist Items
                    if unit.combat_action == CombatAction.secondary_1 and unit.bomb_1 is not None and unit.bomb_1_quantity > 0:
                        self.print("{} uses {}".format(unit.name, unit.bomb_1.name))
                        weapon = unit.bomb_1
                        item_slot = ItemSlot.bomb_1
                        unit.bomb_1_quantity -= 1

                    elif unit.combat_action == CombatAction.secondary_2 and unit.bomb_2 is not None and unit.bomb_2_quantity > 0:
                        self.print("{} uses {}".format(unit.name, unit.bomb_2.name))
                        weapon = unit.bomb_2
                        item_slot = ItemSlot.bomb_2
                        unit.bomb_2_quantity -= 1

                elif unit.unit_class in [ UnitClass.magus, UnitClass.wizard, UnitClass.sorcerer]:
                    if unit.combat_action == CombatAction.secondary_1 and unit.spell_1 is not None:
                        self.print("{} uses {}".format(unit.name, unit.spell_1.name))
                        weapon = unit.spell_1
                        item_slot = ItemSlot.spell_1

                    elif unit.combat_action == CombatAction.secondary_2 and unit.spell_2 is not None:
                        self.print("{} uses {}".format(unit.name, unit.spell_2.name))
                        weapon = unit.spell_2
                        item_slot = ItemSlot.spell_2


                    elif unit.combat_action == CombatAction.secondary_3 and unit.spell_3 is not None:
                        self.print("{} uses {}".format(unit.name, unit.spell_3.name))
                        weapon = unit.spell_3
                        item_slot = ItemSlot.spell_3



            # calculate normal combat damage
            if weapon is not None:
                dmg_multiplier = 1.0

                if unit is invigorated_unit: # deal more damage if target was invigorated
                    dmg_multiplier += 2.5

                if unit.unit_class is UnitClass.alchemist:
                    dmg_multiplier += ((weapon.level * 5.0)/100) + 1.0

                for damage_type in weapon.damage_types:
                    if damage_type in self.monster.weaknesses:
                        dmg_multiplier += 0.25

                # apply damage * damage multiplier
                dmg += math.floor(weapon.damage * dmg_multiplier)

                self.print("{0} deals {1} damage to {2}".format(
                    unit.name,
                    dmg,
                    self.monster.name))

                self.monster.current_health -= dmg

                if self.monster.current_health < 0:
                    self.monster.current_health = 0
                    break

                turn_log["events"].append({
                    "type": Event.unit_attack,
                    "unit": unit.id,
                    "damage":dmg,
                    "item_used": item_slot
                })

            unit.combat_action = CombatAction.none


        self.round += 1
        cooldown_abilities()

        if self.monster.current_health <= 0:
            self.done = True
            self.done_reason = "Monster Defeated!"
            self.success = True

        if sum( int(u.is_alive()) for u in self.units ) == 0:
            self.done = True
            self.done_reason = "Party Defeated!\n Game Over!"
            self.success = False



    def print_summary(self):

        print()
        print("Combat Round {}".format(self.round-1))
        print(self.monster.summary())

        print()
        for u in self.units:
            print(u.summary())

    def print(self, msg):
        if self.verbose:
            print(msg)


