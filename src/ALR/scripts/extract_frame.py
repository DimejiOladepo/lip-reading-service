import os
from torch.utils.data import DataLoader, Dataset
import config
import time


class MyDataset(Dataset):
    def __init__(self):

        dataset = config.dataset

        self.IN = f'{dataset}/video/'
        self.OUT = f'{dataset}_imgs/'

        with open(f'{dataset}_files.txt', 'r') as f:
            files = [line.strip() for line in f.readlines()]
            self.files = []
            for file in files:  
                _, ext = os.path.splitext(file)
                self.files.append(file)

    def __len__(self):
        return len(self.files)
        
    def __getitem__(self, idx):
        file = self.files[idx]
        _, ext = os.path.splitext(file)
        dst = file.replace(self.IN, self.OUT).replace(ext, '')
        if(not os.path.exists(dst)): 
            os.makedirs(dst)
        cmd = 'ffmpeg -i \'{}\' -qscale:v 2 -r 25 \'{}/%d.jpg\' -hide_banner'.format(file, dst)
        os.system(cmd)
        return dst

if(__name__ == '__main__'):   
    dataset = MyDataset()
    loader = DataLoader(dataset, num_workers=32, batch_size=128, shuffle=False, drop_last=False)
    tic = time.time()
    for (i, batch) in enumerate(loader):
        eta = (1.0*time.time()-tic)/(i+1) * (len(loader)-i)
        print('eta:{}'.format(eta/3600.0))