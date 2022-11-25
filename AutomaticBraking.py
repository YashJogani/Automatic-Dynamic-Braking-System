class AutomaticDynamicBraking:
    def __init__(self):
        self.velocity = 0
        self.relative_velocity = 0
        self.relative_acceleration = 0
        self.relative_distance = 0
        self.safe_distance = 0
        self.time_to_collision = 30
        self.time_to_collision_prev = self.time_to_collision
        self.brake = False
        self.braking_power = 0
        self.braking_power_prev = 0
        self.braking_power_extra = 0
        self.braking_power_points = [self.braking_power]
        self.time_to_collision_points = [self.time_to_collision]
    
    def autobrake(self, velocity, relative_velocity, relative_acceleration, relative_distance):
        self.velocity = 1000 / 3600 * velocity
        self.relative_velocity = 1000 / 3600 * relative_velocity
        self.relative_acceleration = relative_acceleration
        self.relative_distance = relative_distance
        self.safe_distance = (self.velocity * self.velocity) / (2 * 7 * 2)

        self.time_to_collision = self.calculate_ttc()

        # Partial Braking for time to collision between 2.5 and 5 sec
        if self.time_to_collision < 5 and self.time_to_collision > 2.5:
            self.brake = True
            if self.time_to_collision < self.time_to_collision_prev:
                self.braking_power = min(100, self.braking_power + 2)
            else:
                self.braking_power = self.braking_power
            self.braking_power_prev = self.braking_power
            self.braking_power_extra = 0
        
        # Full Braking for time to collision less than 2.5 sec
        elif self.time_to_collision <= 2.5 and self.time_to_collision > 0:
            self.brake = True
            self.braking_power = 100
            self.braking_power_prev = self.braking_power
            self.braking_power_extra = 0
        
        # Once Automated Braking Activated and time to collision greater than 5 sec
        # Need to make Relative Acceleration 0,
        # Relative Velocity 0 and
        # Relative Distance greater than safe distance
        # Release Brake
        elif self.brake:
            if self.relative_acceleration > 0 and self.relative_distance < self.safe_distance * 2:
                self.braking_power_extra = 0
                self.braking_power = min(100, self.braking_power + 1)
                self.braking_power_prev = self.braking_power
            elif self.relative_velocity > 0:
                self.braking_power_extra = min(15, self.braking_power_extra + 1)
                self.braking_power = min(100, self.braking_power_prev + self.braking_power_extra)
            elif self.relative_distance < self.safe_distance / 2:
                self.braking_power_extra = 0
                self.braking_power = self.braking_power
                self.braking_power_prev = self.braking_power
            else:
                self.braking_power_extra = 0
                self.braking_power = max(0, self.braking_power - 2)
                self.braking_power_prev = self.braking_power
        
        if not self.braking_power:
            self.brake = False
            self.braking_power_prev = 0
            self.braking_power_extra = 0
        
        self.time_to_collision_prev = self.time_to_collision
        self.braking_power_points.append(self.braking_power)
        self.time_to_collision_points.append(self.time_to_collision)
    
    def calculate_ttc(self):
        # For a ≠ 0
        # d = ut + 1/2at²
        if self.relative_acceleration:
            a = self.relative_acceleration
            b = self.relative_velocity
            c = -self.relative_distance

            d = b * b - 2 * a * c

            time = (-b + d ** 0.5) / a

            if isinstance(time, complex):
                return 30
            if time < 0:
                return 30
            return round(time, 2)

        elif not self.relative_acceleration:
            # For a = 0
            # Time = Distance / Velocity
            if not self.relative_velocity:
                return 30
            
            time = round(self.relative_distance / self.relative_velocity, 2)
            if time < 0:
                return 30
            return time