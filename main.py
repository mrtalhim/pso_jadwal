import random
import math

class Particle:
    def __init__(self, input_range):
        self.x = input_range['min'] + random.random() * (input_range['max'] - input_range['min'])
        self.v = self.x
        self.local_best = 0

    def update_velocity(self, W, c1, c2, global_best):
        self.v = W * self.v + c1 * random.random() * (self.local_best - self.x) + c2 * random.random() * (global_best - self.x)
        self.update_x()

    def update_x(self):
        self.x = self.x + self.v

    def set_local_best(self, local_best):
        self.local_best = local_best

    def get_x(self):
        return round(self.x)
    
    def get_local_best(self):
        return self.local_best

class Pelajaran:
    def __init__(self, range_hari, range_jam, id_guru='', id_pel='') -> None:
        self.hari = Particle(range_hari)
        self.jam = Particle(range_jam)
        self.id_guru = id_guru
        self.id_pel = id_pel
        self.local_best = 0

    def __str__(self) -> str:
        return f'(guru,pel): {self.id_guru},{self.id_pel} (hari,jam): {self.hari.get_x()},{self.jam.get_x()} local best: {self.local_best}'
    
    def compare(self, other):
        if isinstance(other, self.__class__):
            collisions = 0
            if self.hari.get_x() == other.hari.get_x():
                collisions += 1
            if self.jam.get_x() == other.jam.get_x():
                collisions += 1
            if self.get_id_guru() == other.get_id_guru():
                collisions += 1
            return collisions
        return 0

    def set_local_best(self, fitness):
        self.local_best = fitness if fitness > self.local_best else self.local_best
        self.hari.set_local_best(self.local_best)
        self.jam.set_local_best(self.local_best)

    def update_velocity(self, W, c1, c2, global_best):
        self.hari.update_velocity(W, c1, c2, global_best)
        self.jam.update_velocity(W, c1, c2, global_best)

    def get_id_guru(self):
        return self.id_guru

    def get_id_pel(self):
        return self.id_pel

def main():
    jumlah_jadwal = 10
    kelas = 12
    range_hari = {'min': 1, 'max': 5}
    range_jam = {'min': 1, 'max': 5}
    jadwal = [Pelajaran(range_hari, range_jam, id_guru=str(x), id_pel=str(x)) for x in range(jumlah_jadwal)]

    for x in jadwal:
        print(x)
    print()

    """calculate fitness"""
    W, c1, c2 = 0.5, 1.5, 1.5
    iteration = 2

    for z in range(iteration):
        global_best = 0
        collision = 0
        fitness = 0
        for x in range(jumlah_jadwal):
            for y in range(x + 1, jumlah_jadwal):
                collision = jadwal[x].compare(jadwal[y])
                fitness = 1 / (collision + 1)
                jadwal[x].set_local_best(fitness)
            # global_best = fitness if fitness > global_best else global_best
            # jadwal[x].update_velocity(W, c1, c2, global_best)

    for x in jadwal:
        print(x)

if __name__ == "__main__":
    main()