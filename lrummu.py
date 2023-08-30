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
        self.debug_mode = "quiet"

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        # enable debug mode
        self.debug_mode = "debug"

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        # disable debug mode
        self.debug_mode = "quiet"

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        # if current page not in the page table, will cause page fault
        if page_number not in self.page_table:
            self.total_page_faults += 1
            # read in a new page
            self.total_page_reads += 1

        # if memory is full, replace the least recently used page
        if len(self.page_table) >= self.frames:
            replace_page = self.page_table.pop(0)
            # if the page is modified, write count + 1
            if self.page_table[replace_page]:
                self.total_disk_writes += 1
            # delete previous page
            del self.page_table[replace_page]
        # load the current page into memory
        self.page_table[page_number] = True
        self.order_list.append(page_number)

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        # if current page not in the page table, will cause page fault
        if page_number not in self.page_table:
            self.total_page_faults += 1
            self.total_disk_writes += 1
         # if memory is full, replace the least recently used page
        if len(self.page_table) >= self.frames:
            replace_page = self.page_table.pop(0)
            # if the page is modified, write count + 1
            if self.page_table[replace_page]:
                self.total_disk_writes += 1
            # delete previous page
            del self.page_table[replace_page]
            # load the current page into memory
        self.page_table[page_number] = True
        self.order_list.append(page_number)

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.total_disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.total_disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.total_page_faults
