from mmu import MMU


class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        self.frames = frames
        # initialize static variables:
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0
        self.order_queue = []
        self.page_frames = []
        self.write = []
        self.debug = False   # initialize debug mode

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        # enable debug mode
        self.debug = True

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        # disable debug mode
        self.debug = False

    def load_page(self, page_number):
        if self.debug:
            print("LRU_MMU: load_page(): ", page_number)
        
        # if no more empty space 
        if len(self.page_frames) >= self.frames:
            # if memory is full, replace the least recently used page
            replace_page = self.order_queue[0]
            if self.debug:
                print("LRU_MMU: load_page(): Page frame is full, remove: ", replace_page)
            # remove previous page
            if replace_page in self.write:
                self.total_disk_writes += 1
                self.write.remove(replace_page)
            self.page_frames.remove(replace_page)
            self.page_frames.append(page_number)
            self.order_queue.remove(replace_page)
            self.order_queue.append(page_number)
        else:
            if self.debug:
                print("LRU_MMU: load_page(): Page frame is available: ", page_number)
            self.order_queue.append(page_number)
            self.page_frames.append(page_number)
        
        if self.debug:
            print("LRU_MMU: Finish loading.")

    def queue_update(self, page_number):
        self.order_queue.remove(page_number)
        self.order_queue.append(page_number)

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if self.debug:
            print("LRU_MMU: read_memory(): ", page_number)

        # if current page not in the page table, will cause page fault
        if page_number not in self.page_frames:
            if self.debug:
                print("LRU_MMU: read_memory(): page is not found in memory: ", page_number)
            self.total_page_faults += 1
            # read in a new page
            self.total_disk_reads += 1
            # load current page
            self.load_page(page_number)
        else:
            if self.debug:
                print("LRU_MMU: read_memory(): page is found in memory: ", page_number, " Updating the order queue")
            # update
            self.queue_update(page_number)
        if self.debug:
            print("LRU_MMU: read_memory(): Finish reading.")
            self.debug_statement()

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if self.debug:
            print("LRU_MMU: write_memory(): write memory: ", page_number)

        # if current page not in the page table, will cause page fault
        if page_number not in self.page_frames:
            if self.debug:
                print("LRU_MMU: write_memory(): page is not found in memory: ", page_number)
            self.total_page_faults += 1
            # write page into memory
            # self.total_disk_writes += 1
            self.total_disk_reads += 1
            self.load_page(page_number)
            if page_number not in self.write:
                self.write.append(page_number)
        else:
            if self.debug:
                print("LRU_MMU: write_memory(): page is found in memory: ", page_number)
            self.queue_update(page_number)
            if page_number not in self.write:
                self.write.append(page_number)
        if self.debug:
            print("LRU_MMU: write_memory(): Finish writing.")
            self.debug_statement()

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.total_disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.total_disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.total_page_faults

    def debug_statement(self):
        print("Current order_queue: ", self.order_queue)
        print("Current page_frames: ", self.page_frames)
        print("Current write: ", self.write)
        print("total_disk_reads: ", self.total_disk_reads)
        print("total_disk_writes: ", self.total_disk_writes)
        print("total_page_faults: ", self.total_page_faults)
        print("\n")