import random
import re
import pandas as pd
import numpy as np

class Particle:
    def __init__(self, input_range):
        self.input_range = input_range
        self.x = input_range['min'] + random.random() * (input_range['max'] - input_range['min'])
        self.v = self.x
        self.local_best = 0

    def update_velocity(self, W, c1, c2, global_best):
        self.v = W * self.v + c1 * random.random() * (self.local_best - self.x) + c2 * random.random() * (global_best - self.x)
        self.update_x()

    def update_x(self):
        self.x = round(self.x + self.v)
        self.x = self.x % self.input_range['max'] + 1

    def set_local_best(self, local_best):
        self.local_best = local_best

    def get_x(self) -> int:
        return int(self.x)
    
    def get_local_best(self):
        return self.local_best

class Pelajaran:
    def __init__(self, range_hari, range_jam, id_guru='', id_pel='', id_kelas='') -> None:
        self.hari = Particle(range_hari)
        self.jam = Particle(range_jam)
        self.id_guru = id_guru
        self.id_pel = id_pel
        # self.id_kelas = id_kelas
        self.id_kelas = str(int(id_kelas) + 1) # temp until string
        self.local_best = 0
    
    def __str__(self) -> str:
        info = '(guru-pel-kelas): {:>2s},{:>2s},{:>2s}'.format(self.id_guru, self.id_pel, self.id_kelas)
        waktu = '(hari-jam): {:>2d},{:>2d}'.format(self.hari.get_x(), self.jam.get_x())
        local_best = 'local_best: {:.2f}'.format(self.local_best)
        return ' '.join([waktu, info, local_best])
    
    def compare(self, other):
        if isinstance(other, self.__class__):
            collisions = 0
            if self.hari.get_x() == other.hari.get_x() and self.jam.get_x() == other.jam.get_x():
                if self.id_kelas != other.id_kelas and self.id_guru == other.id_guru:
                    collisions += 1 # bentrok waktu
                if self.id_kelas == other.id_kelas:
                    if self.id_guru != other.id_guru:
                        collisions += 1 # bentrok guru
                    if self.id_pel != other.id_pel:
                        collisions += 1 # bentrok pelajaran
            return collisions
        else:
            return 0

    def set_local_best(self, fitness):
        self.local_best = fitness
        self.hari.set_local_best(self.local_best)
        self.jam.set_local_best(self.local_best)

    def update_velocity(self, W, c1, c2, global_best):
        if self.local_best < 1.0:
            self.hari.update_velocity(W, c1, c2, global_best)
            self.jam.update_velocity(W, c1, c2, global_best)

    def get_id_guru(self):
        return self.id_guru

    def get_id_pel(self):
        return self.id_pel

    def get_id_kelas(self):
        return self.id_kelas

def display_jadwal(jadwal, kelas_total):
    hari_dict = {1:'SENIN', 2: 'SELASA', 3:'RABU', 4:'KAMIS', 5:'JUMAT'}
    # output = []
    # for pelajaran in jadwal:
    #     hari = pelajaran.hari.get_x()
    #     jam = pelajaran.jam.get_x()
    #     kelas = pelajaran.get_id_kelas()
    #     guru = pelajaran.get_id_guru()
    #     pel = pelajaran.get_id_pel()
    #     output.append([hari, jam, kelas, guru, pel])
        
    # output = pd.DataFrame(output, columns=['hari','jam','kelas','guru','pelajaran'])

    columns = ['hari', 'Jam'] + [str(x + 1) for x in range(kelas_total)]
    output = pd.DataFrame(columns=columns)
    for pelajaran in jadwal:
        hari = pelajaran.hari.get_x()
        jam = pelajaran.jam.get_x()
        kelas = pelajaran.get_id_kelas()
        guru_pel = ' '.join([pelajaran.get_id_guru(), pelajaran.get_id_pel()])
        row = pd.DataFrame({'hari':[hari], 'jam':[jam], kelas:[guru_pel]}, columns=columns)
        output = pd.concat([output, row])

    # output = output.sort_values(by=['hari', 'jam', 'kelas'])
    output = output.sort_values(by=['hari', 'jam'])
    output['hari'] = output['hari'].apply(lambda x: hari_dict[x])
    output = output.replace(np.nan, '{:^5s}'.format(''), regex=True)
    output['cleanme'] = 'cleanme'

    output = output.set_index(['hari', 'cleanme'])

    html = output.to_html(index_names=False)
    html = re.sub('<th></th>\n.*<th></th>', '<th></th>', html)  # notice your column name here
    html = re.sub('<th>cleanme</th>', '', html)

    with open('output/index.html', 'w') as fou:
        fou.write(html)

    # print(output)

def main():
    jumlah_jadwal = 48
    kelas = 4
    range_hari = {'min': 1, 'max': 5}
    range_jam = {'min': 1, 'max': 5}
    jadwal = [Pelajaran(range_hari, range_jam, id_guru=str(x), id_pel=str(x), id_kelas=str(x % kelas)) for x in range(jumlah_jadwal)] # TODO

    """calculate fitness"""
    W, c1, c2 = 0.5, 1.5, 1.5
    iteration = 1

    for z in range(iteration):
        global_best = 0
        collision = 0
        fitness = 0
        for x in jadwal:
            for y in jadwal:
                if jadwal.index(x) == jadwal.index(y):
                    continue
                collision += x.compare(y)
            fitness = 1 / (collision + 1)
            x.set_local_best(fitness)
            global_best = fitness if fitness > global_best else global_best
            x.update_velocity(W, c1, c2, global_best)

    # for x in jadwal:
    #     print(x)

    display_jadwal(jadwal, kelas)
    for x in jadwal:
        if x.local_best < 1.0:
            print('might have collisions')
            break

if __name__ == "__main__":
    main()