from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.frames = frames                # number of frames in the physical memory
        self.debug = True                   # set default debug mode to true
        self.count_disk_reads = 0           # count number of disk reads action
        self.count_disk_writes = 0          # count number of disk writes action
        self.count_page_faults = 0          # count number of page faults
        self.page_frames =[]                # store page frames in current physical address

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug = True

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False
    
    def load_page(self, page_number):
        # TODO: Implement the method to load page
        if self.debug:
            print("RandMMU: load_page():  Start loading", page_number,"\n")
        # if there is empty slot for incoming page
        if len(self.page_frames) < self.frames:
            if self.debug:
                print("RandMMU: load_page():  Page replacement does not happen, load ", page_number,"\n")
            self.page_frames.append(page_number)
        # if there is no empty slot for incoming page
        else: 
            # randomly select a page to repalce
            frame_to_replace = random.choice(self.page_frames)
            if self.debug:
                print("RandMMU: load_page():  Page replacement happens, load ", page_number," replace ", frame_to_replace, "\n")
            self.page_frames.remove(frame_to_replace)
            self.page_frames.append(page_number)
        #
        if self.debug:
            print("RandMMU: load_page():  Finish loading", page_number,"\n")

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if self.debug:
            print("RandMMU: read_memory():  Start reading", page_number,"\n")
        # if page frame is loaded in memory
        if page_number in self.page_frames:
            if self.debug:
                print("RandMMU: read_memory():  ", page_number," is loaded in memory.\n")
        # if page frame is not loaded in memory
        else:
            if self.debug:
                print("RandMMU: read_memory():  ", page_number," is not loaded in memory.\n")
                # load the page & increase the page fault count and disk read count
                self.count_page_faults = self.count_page_faults + 1
                self.count_disk_reads = self.count_disk_reads + 1
                self.load_page(page_number)
        #
        if self.debug:
            print("RandMMU: read_memory():  Finish reading", page_number,"\n")

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if self.debug:
            print("RandMMU: write_memory():  Start writing", page_number,"\n")
        # if page frame is loaded in memory
        if page_number in self.page_frames:
            if self.debug:
                print("RandMMU: write_memory():  ", page_number," is loaded in memory.\n")
        # if page frame is not loaded in memory
        else:
            if self.debug:
                print("RandMMU: write_memory():  ", page_number," is not loaded in memory.\n")
                # load the page & increase the page fault counts
                self.count_page_faults = self.count_page_faults + 1
                self.count_disk_writes = self.count_disk_writes + 1
                self.load_page(page_number)
        #
        if self.debug:
            print("RandMMU: write_memory():  Finish writing", page_number,"\n")

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.count_disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.count_disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.count_page_faults
