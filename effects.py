import random

class Effect:
    def __init__(self, duration, description):
        self.duration = duration
        self.description = description

    def activate(self, character):
        raise NotImplementedError()

    def tick(self, character):
        self.duration -= 1

    def deactivate(self, character):
        raise NotImplementedError()

    def __str__(self):
        return f'Эффект: {self.description}; На протяжении {self.duration} раунда/ов.'


class HealthRegeneration(Effect):
    def __init__(self, amount, duration):
        super().__init__(duration, f'Восстановление здоровья на {amount}')
        self.amount = amount

    def activate(self, character):
        character._health += self.amount
        if character._health > character._max_health:
            character._health = character._max_health
        print(f"{character.name} восстановил {self.amount} здоровья.")

    def deactivate(self, character):
        pass


class DamageIncrease(Effect):
    def __init__(self, bonus_damage, duration):
        super().__init__(duration, f'Усиление урона на {bonus_damage}')
        self.bonus_damage = bonus_damage

    def activate(self, character):
        if not hasattr(character, 'original_damage'):
            character.original_damage = character.damage
        character.damage += self.bonus_damage
        print(f'{character.name} получил бонус к урону (+{self.bonus_damage}).')

    def deactivate(self, character):
        if hasattr(character, 'original_damage'):
            character.damage = character.original_damage
            del character.original_damage
            print(f'Закончился бонус к урону у {character.name}.')


class ArmorBoost(Effect):
    def __init__(self, amount, duration):
        super().__init__(duration, f'Повышение брони на {amount}')
        self.amount = amount

    def activate(self, character):
        if hasattr(character, 'armor'):
            character.base_armor = character.armor
            character.armor += self.amount
            print(f'{character.name} повысил свою броню на {self.amount}.')
        else:
            print(f'{character.name} не может использовать эффект повышения брони.')

    def deactivate(self, character):
        if hasattr(character, 'base_armor'):
            character.armor = character.base_armor
            del character.base_armor
            print(f'Эффект повышения брони у {character.name} прекратился.')


class SelfHealOnLowHealth(Effect):
    def __init__(self, threshold, chance, full_health_amount):
        super().__init__(None, f'Восстановление здоровья при здоровье ниже {threshold}%')
        self.threshold = threshold
        self.chance = chance
        self.full_health_amount = full_health_amount

    def check_and_apply(self, character):
        if character._health / character._max_health * 100 < self.threshold and random.random() < self.chance:
            character._health = self.full_health_amount
            print(f'{character.name} восстановил свое здоровье до {self.full_health_amount}.')

    def activate(self, character):
        pass

    def deactivate(self, character):
        pass

class Strategy:
    def __init__(self, condition_percentage, increase_percentage):
        self.condition_percentage = condition_percentage
        self.increase_percentage = increase_percentage
        self.applied = False

    def check_condition(self, boss):
        return boss._health / boss._max_health * 100 < self.condition_percentage

    def apply(self, boss):
        if not self.applied:
            boss.original_health = boss._health
            boss.original_damage = boss.damage
            boss._health *= int(1 + self.increase_percentage / 100)
            boss.damage *= int(1 + self.increase_percentage / 100)
            self.applied = True
            print(f'Эффект сработал: босс {'раздражён' if self.increase_percentage == 10 else 'в бешенстве'}!')

    def remove(self, boss):

        if self.applied:
            boss._health = boss.original_health
            boss.damage = boss.original_damage
            del boss.original_health
            del boss.original_damage
            self.applied = False
            print(f'Эффект снят: босс вернулся в нормальное состояние.')
