from mmu import MMU


class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        self.frames = frames
        # initialize static variables:
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0
        # initialize page table and order list
        self.page_table = {}
        self.order_list = []
        # initialize debug mode
        self.debug = False

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
            print("LRU_MMU: load_page: ", page_number, "\n")
        if len(self.page_table >= self.frames):
            # if memory is full, replace the least recently used page
            replace_page = self.page_table.pop(0)
            if self.debug:
                print("LRU_MMU: Page frame is full, remove: ", replace_page, "\n")
            # remove previous page
            del replace_page
            # load the current page into memory
            self.page_table[page_number] = True
            self.order_list.append(page_number)
        else:
            print("LRU_MMU: Page frame is available: ", replace_page, "\n")
            # load the current page into memory
            self.page_table[page_number] = True
            self.order_list.append(page_number)
        if self.debug:
            print("LRU_MMU: Stop loading.", "\n")

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if self.debug:
            print("LRU_MMU: read memory: ", page_number, "\n")
        # if current page not in the page table, will cause page fault
        if page_number not in self.page_table:
            if self.debug:
                print("LRU_MMU: page is not found in memory: ", page_number, "\n")
            self.total_page_faults += 1
            # read in a new page
            self.total_page_reads += 1
            # load current page
            self.load_page(page_number)
        else:
            if self.debug:
                print("LRU_MMU: page is found in memory: ", page_number, "\n")
        if self.debug:
            print("LRU_MMU: stop reading.", "\n")

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if self.debug:
            print("LRU_MMU: write memory: ", page_number, "\n")
        # if current page not in the page table, will cause page fault
        if page_number not in self.page_table:
            if self.debug:
                print("LRU_MMU: page is not found in memory: ", page_number, "\n")
            self.total_page_faults += 1
            self.total_disk_writes += 1
            # write page into memory
            self.load_page(page_number)
        else:
            if self.debug:
                print("LRU_MMU: page is found in memory: ", page_number, "\n")
        if self.debug:
            print("LRU_MMU: stop writing.", "\n")

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.total_disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.total_disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.total_page_faults
