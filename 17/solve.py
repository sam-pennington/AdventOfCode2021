class Velocity():

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def drag(self):
        x = self.x - 1 if self.x > 0 else self.x + 1 if self.x < 0 else 0
        y = self.y - 1
        return Velocity(x, y)


class Position():

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def step(self, velocity: Velocity):
        x = self.x + velocity.x
        y = self.y + velocity.y
        return Position(x, y)


class Target():

    def __init__(self, x_min, x_max, y_min, y_max) -> None:
        self.x_extents = (x_min, x_max)
        self.y_extents = (y_min, y_max)

    def intercept(self, position: Position):
        pos_x = position.x
        pos_y = position.y
        good_x = (pos_x >= self.x_extents[0] and pos_x <= self.x_extents[1])
        good_y = (pos_y >= self.y_extents[0] and pos_y <= self.y_extents[1])
        return good_x and good_y

    def intercept_possible(self, position: Position, velocity: Velocity):
        pos_x = position.x
        pos_y = position.y
        bad_x = (pos_x > self.x_extents[1])
        bad_y = (pos_y < self.y_extents[0])
        return not (bad_x or bad_y)


class Projectile():

    def __init__(self, starting_position: Position, starting_velocity: Velocity) -> None:
        self.starting_velocity = starting_velocity
        self.starting_position = starting_position
        self.position = starting_position
        self.velocity = starting_velocity
        self.maximum_y = starting_position.y

    def step(self):
        self.position = self.position.step(self.velocity)
        self.velocity = self.velocity.drag()
        self.maximum_y = max(self.maximum_y, self.position.y)
        return self

    def intercept(self, t: Target):
        return t.intercept(self.position)

    def intercept_possible(self, t: Target):
        return t.intercept_possible(self.position, self.velocity)


def run():
    #target: Target = Target(20, 30, -10, -5)
    # x=282..314, y=-80..-45
    target: Target = Target(282, 314, -80, -45)

    hits = []
    current_max_y = None

    for x in range(0, 1000):
        for y in range(-1000, 1000):
            projectile: Projectile = Projectile(Position(0, 0), Velocity(x, y))
            intercept = False
            missed = False
            while not (intercept or missed):
                projectile = projectile.step()
                intercept = projectile.intercept(target)
                missed = not projectile.intercept_possible(target)
            if intercept:
                hits.append((x, y))
                if current_max_y is None:
                    current_max_y = (projectile.maximum_y, x, y)
                else:
                    if current_max_y[0] < projectile.maximum_y:
                        current_max_y = (projectile.maximum_y, x, y)

    print(f"hits: {hits};")
    print(f"max_y: {current_max_y};")
    print(f"distinct: {len(hits)}")


def main():
    run()


if __name__ == "__main__":
    main()
