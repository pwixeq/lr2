from effects import *
class Character:
    def __init__(self, name, health, damage):
        self.name = name
        self._health = health
        self._max_health = health
        self.damage = damage
        self.active_effects = []

    def __str__(self):
        return f'Имя:{self.name} Здоровье:{self._health} Урон:{self.damage}'

    def take_damage(self, damage):
        self._health -= damage
        if self._health < 0:
            self._health = 0
        print(f'{self.name} получил {damage} урона! HP: {self._health}')

    def heal(self):
        if self._health > self._max_health:
            self._health = self._max_health

    def attack(self, other):
        print(f'{self.name} атакует {other.name}')
        other.take_damage(self.damage)

    def is_alive(self):
        return self._health > 0


class Hero(Character):
    pass

class Enemy(Character):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.effects = [
            Strategy(condition_percentage=50, increase_percentage=10),
            Strategy(condition_percentage=20, increase_percentage=20)
        ]

    def update_effects(self):
        for effect in self.effects:
            if effect.check_condition(self):
                effect.apply(self)
            else:
                effect.remove(self)

    def attack(self, other):
        self.update_effects()
        super().attack(other)

    def take_damage(self, damage):
        super().take_damage(damage)
        self.update_effects()

class Warrior(Hero):
    def attack(self, other):
        if random.random() < 0.25:
            crit_damage = self.damage * 2
            print(f'{self.name} делает критический удар')
            other.take_damage(crit_damage)
        else:
            super().attack(other)

class Mage(Hero):
    def attack(self, other):
        print(f'{self.name} посылает ураган на {other.name}')
        other.take_damage(self.damage+10)

class Archer(Hero):
    def attack(self, other):
        if random.random() < 0.2:
            miss_damage = self.damage * 0
            print(f'{self.name} - Лучник криворучник!')
            other.take_damage(miss_damage)
        else:
            super().attack(other)

class Paladin(Hero):
    def __init__(self, name, health, damage, armor):
        super().__init__(name, health, damage)
        self.armor = armor
    def take_damage(self, damage):
        e_damage = max(damage - self.armor, 0)
        self.armor -= min(damage, self.armor)
        self._health -= e_damage
        if self._health <=0:
            self._health = 0
        print(f'{self.name} получил {e_damage} урона. Осталось {min(damage, self.armor)} брони. HP: {self._health}')
    def __str__(self):
        return f'Имя:{self.name} Здоровье:{self._health} Урон:{self.damage} Броня: {self.armor}'



party = [
    Warrior("Майк", 150, 25),
    Mage("Оди", 100,  30),
    Archer("Уилл", 120,  20),
    Paladin("Стив", 180, 30, 15)
]
boss = Enemy("Векна", 500, 40)

turn = 0
round_num = 1
alive_party = set(party[:])

while alive_party and boss.is_alive():
    print(f'\n~~~~~~~ Раунд {round_num} ~~~~~~~')


    current_attacker = None
    if turn % 2 == 0:
        current_attacker = boss
        victim = random.choice(list(alive_party))
        current_attacker.attack(victim)
        if not victim.is_alive():
            print(f"{victim.name} пал!")
            alive_party.discard(victim)
    else:
        current_attacker = next(iter(alive_party))
        current_attacker.attack(boss)
        alive_party.add(current_attacker)


    if current_attacker in party and random.random() < 0.4:
        possible_effects = [
            HealthRegeneration(random.randint(10, 50), 1),
            DamageIncrease(random.randint(5, 20), random.randint(1, 3)),
            ArmorBoost(random.randint(10, 20), random.randint(1, 3))
        ]
        new_effect = random.choice(possible_effects)
        current_attacker.active_effects.append(new_effect)
        new_effect.activate(current_attacker)
        print(f"{current_attacker.name} получил случайный положительный эффект: {new_effect}")


    for hero in party:
        for effect in hero.active_effects[:]:
            effect.tick(hero)
            if effect.duration <= 0:
                effect.deactivate(hero)
                hero.active_effects.remove(effect)


    print('\nИтоги раунда:')
    for hero in party:
        print(hero)
    print(boss)

    turn += 1
    round_num += 1


if boss.is_alive():
    print("\nВекна победил. Все герои в изнанке.")
else:

    print("\nПобеда! Дети сюжета.")
