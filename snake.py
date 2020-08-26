import consts


class Snake:
    dx = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
    dy = {'UP': -1, 'DOWN': 1, 'LEFT': 0, 'RIGHT': 0}

    def __init__(self, keys, game, pos, color, direction):
        self.keys = keys
        self.cells = [pos]
        self.game = game
        self.game.add_snake(self)
        self.color = color
        self.direction = direction
        self.pre_direction = ''

        game.get_cell(pos).set_color(color)

    def get_head(self):
        return self.cells[-1]

    def val(self, x):
        if x < 0:
            x += self.game.size

        if x >= self.game.size:
            x -= self.game.size

        return x

    def next_move(self):
        new_direction = self.direction

        if new_direction == 'DOWN':
            self.move_down()
        elif new_direction == 'UP':
            self.move_up()
        elif new_direction == 'LEFT':
            self.move_left()
        elif new_direction == 'RIGHT':
            self.move_right()

    def move_right(self):

        head = self.get_head()
        new_cell = (head[0] + 1, head[1])

        if new_cell[0] >= consts.table_size:
            new_cell = (0, head[1])

        self.check_kill(new_cell)

        if not self.check_fruit(new_cell):
            self.game.get_cell(self.cells[0]).set_color(consts.back_color)
            self.cells.remove(self.cells[0])

        self.cells.append(new_cell)
        self.game.get_cell(new_cell).set_color(self.color)

    def move_left(self):
        head = self.get_head()
        new_cell = (head[0] - 1, head[1])

        if new_cell[0] == -1:
            new_cell = (consts.table_size - 1, head[1])

        self.check_kill(new_cell)

        if not self.check_fruit(new_cell):
            self.game.get_cell(self.cells[0]).set_color(consts.back_color)
            self.cells.remove(self.cells[0])

        self.cells.append(new_cell)
        self.game.get_cell(new_cell).set_color(self.color)

    def move_up(self):
        head = self.get_head()
        new_cell = (head[0], head[1] - 1)

        if new_cell[1] == -1:
            new_cell = (head[0], consts.table_size - 1)

        self.check_kill(new_cell)

        if not self.check_fruit(new_cell):
            self.game.get_cell(self.cells[0]).set_color(consts.back_color)
            self.cells.remove(self.cells[0])

        self.cells.append(new_cell)
        self.game.get_cell(new_cell).set_color(self.color)

    def move_down(self):

        head = self.get_head()
        new_cell = (head[0], head[1] + 1)

        if new_cell[1] >= consts.table_size:
            new_cell = (head[0], 1)

        self.check_kill(new_cell)

        if not self.check_fruit(new_cell):
            self.game.get_cell(self.cells[0]).set_color(consts.back_color)
            self.cells.remove(self.cells[0])

        self.cells.append(new_cell)
        self.game.get_cell(new_cell).set_color(self.color)

    def check_kill(self, new_cell):
        if [new_cell[0], new_cell[1]] in consts.block_cells:
            self.game.kill(self)
        elif new_cell in self.cells:
            self.game.kill(self)

        for snake in self.game.snakes:
            if new_cell in snake.cells:
                self.game.kill(self)

    def check_fruit(self, new_cell):
        if self.game.get_cell(new_cell).color == consts.fruit_color:
            return True
        else:
            return False

    def handle(self, keys):
        for key in keys:
            if key in self.keys:
                new_direction = self.keys[key]
                pre_direction = self.pre_direction

                if new_direction == 'UP' and pre_direction != 'DOWN':
                    self.change_direction(key)
                elif new_direction == 'DOWN' and pre_direction != 'UP':
                    self.change_direction(key)
                elif new_direction == 'LEFT' and pre_direction != 'RIGHT':
                    self.change_direction(key)
                elif new_direction == 'RIGHT' and pre_direction != "LEFT":
                    self.change_direction(key)

    def change_direction(self, key):
        self.pre_direction = self.keys[key]
        self.direction = self.keys[key]
