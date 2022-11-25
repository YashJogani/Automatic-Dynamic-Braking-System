# Automatic Dynamic Braking System

The Automatic Dynamic braking system is an effective intelligent vehicle safety system for avoiding rear-end types of collisions by automatically applying the brakes of the vehicles.

- It can identify when a possible collision is about to occur and responds by autonomously activating the brakes to slow a vehicle prior to impact or bring it to a stop to avoid a collision.
- Dynamically adjust braking power for ride comfort and safety of the passengers.

## Results

### Scenario 1:

Following Vehicle Velocity: 100kmph.<br />
Preceding Vehicle Velocity: 70kmph.<br />
Relative Distance: 50m.<br />

Preceding car has constant velocity of 70kmph. But following car has 100kmph so, relative distance decreases. As TTC decreases, braking system applies braking power of just 20% as risk of collision is very low. Velocity of following car is decreased to 69kmph and brakes are released.<br />

![1](https://user-images.githubusercontent.com/68644741/203930342-ea331e59-a8ec-4bdd-bb48-29ce118c746a.png)

### Scenario 2:

Following Vehicle Velocity: 120kmph.<br />
Preceding Vehicle Velocity: 120kmph.<br />
Relative Distance: 50m.<br />

Preceding car brakes lightly and velocity decreases to 65kmph in 7sec. As the relative distance decreases. Braking System gradually applies braking power to 45% to avoid collision which makes the velocity of following car 60kmph over 5 sec.<br />

![2](https://user-images.githubusercontent.com/68644741/203930360-a22bdff8-7cf2-4cb1-a1c2-116f4bf0c909.png)

### Scenario 3:

Following Vehicle Velocity: 120kmph.<br />
Preceding Vehicle Velocity: 120kmph.<br />
Relative Distance: 20m.<br />

Preceding car suddenly brakes and velocity decreases to 60kmph in just 3sec. As the relative distance decreases rapidly, TTC also decreases. Once it reaches below 5sec Dynamic Emergency Braking System is activated and gradually applies braking power to 80% to avoid collision. Velocity of following car is decreased to 40kmph in 6 sec. Once satisfying all the criteria, it releases brakes gradually.<br />

![3](https://user-images.githubusercontent.com/68644741/203930384-aa072d8b-d810-40a5-a161-3e783857ea39.png)
