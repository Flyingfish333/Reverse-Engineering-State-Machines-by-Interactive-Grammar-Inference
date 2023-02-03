import copy

class History:
    def __init__(self) -> None:
        self.next_history = {}
        self.back_history = {}
        self.__current_apta = None
        self.apta_idx_map = {}

    def set_current_apta(self, apta):
        if apta.apta_idx not in self.apta_idx_map:
            self.__current_apta = copy.deepcopy(apta)
            self.apta_idx_map[apta.apta_idx] = self.__current_apta
        else:
            self.__current_apta = self.apta_idx_map[apta.apta_idx]

    def get_current_apta(self):
        return self.__current_apta

    def clear(self):
        self.next_history = {}
        self.back_history = {}
        self.__current_apta = None
        self.apta_idx_map = {}
        
    # 返回apta的back历史节点
    # 返回的是一个apta对象
    def get_back_apta(self, k):
        if self.__current_apta not in self.back_history.keys():
            return None

        if k not in self.back_history[self.__current_apta]:
            return

        return self.back_history[self.__current_apta][k]
    
    # 返回当前apta的next选项
    # 返回的是一个apta对象列表, 如果是尾历史节点就返回空
    def show_next_apta_option(self, k):
        if self.__current_apta not in self.next_history.keys():
            return None

        if k not in self.next_history[self.__current_apta]:
            return

        return self.next_history[self.__current_apta][k]
    
    def add_back_apta(self, back_apta, k):
        if self.__current_apta not in self.back_history:
            self.back_history[self.__current_apta] = {}
        
        self.back_history[self.__current_apta][k] = back_apta

    def add_next_apta(self, apta, k):
        if apta not in self.next_history.keys():
            self.next_history[apta] = {}
            self.next_history[apta][k] = [self.__current_apta]
        elif k not in self.next_history[apta].keys():
            self.next_history[apta][k] = [self.__current_apta]
        else:
            self.next_history[apta][k].append(self.__current_apta)
        
    def empty(self):
        return self.__current_apta == None
    
    def clear_next_apta(self):
        if self.__current_apta:
            if self.__current_apta in self.next_history:
                del self.next_history[self.__current_apta]