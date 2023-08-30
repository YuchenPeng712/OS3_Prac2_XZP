from mmu import MMU


class ClockMMU(MMU):
    disk_reads = 0
    disk_writes = 0
    page_faults = 0
    page_table = []
    pointer = 0
    frames = 0
    def __init__(self, frames):
        # TODO: Constructor logic for EscMMU
        # initialize the page table with the number of frames
        for _ in range(frames):            
            self.page_table.append([None,0,0])
        self.frames = frames

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        pass

    def read_memory(self, page_number):
       
        for page in self.page_table:
            ## if page num is in page table, read and set ifread bit to 1
            if page[0] == page_number:
                page[1] = 1
                return
        # if page num not in page table,page fault and read from disk
        self.page_faults += 1
        self.disk_reads += 1
        # use the pointer to find the next page to replace
        while True:
            # if ifread bit is 0, replace the page
            if self.page_table[self.pointer][1] == 0:
                #if ifwrite bit is 1, write to disk first
                if self.page_table[self.pointer][2] == 1:
                    self.disk_writes += 1
                self.page_table[self.pointer] = [page_number,1,0]
                self.pointer = (self.pointer + 1) % self.frames
                return
            # if ifread bit is 1, set ifread bit to 0 and pointer ++
            else:
                self.page_table[self.pointer][1] = 0
                self.pointer = (self.pointer + 1) % self.frames           


    def write_memory(self, page_number):
        for page in self.page_table:
            ## if page num is in page table, read and set ifread bit to 1 and ifwrite bit to 1
            if page[0] == page_number:
                page[1] = 1
                page[2] = 1
                return
        # if page num not in page table,page fault and read from disk
        self.page_faults += 1
        self.disk_reads += 1

        # use the pointer to find the next page to replace
        while True:
            # if ifread bit is 0, replace the page
            if self.page_table[self.pointer][1] == 0:
                #if ifwrite bit is 1, write to disk first
                if self.page_table[self.pointer][2] == 1:
                    self.disk_writes += 1
                self.page_table[self.pointer] = [page_number,1,1]
                self.pointer = (self.pointer + 1) % self.frames
                return
            # if ifread bit is 1, set ifread bit to 0 and pointer ++
            else:
                self.page_table[self.pointer][1] = 0
                self.pointer = (self.pointer + 1) % self.frames
        

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults
    