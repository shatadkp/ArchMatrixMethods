
customer - agent in -> Flight
Customer - uses -> Aircraft
Flight - occupies temporal region -> Flight Temporal Interval
Flight Temporal Interval – subclass of -> temporal Interval
Flight - has process part -> flight segment
Flight Segment - occupies temporal region -> Flight Segment Temporal Interval
Flight Segment Temporal Interval – subclass of -> Temporal Interval
Aircraft - participates in -> Flight
Flight -> subclass of -> Process
Engine - continuant part of -> Aircraft
Engine - Participates in -> Engine Run
Engine Run - occupies temporal region -> Engine Run Temporal Interval
Flight Segment - has subclass -> Taxi Out Segment
Flight Segment - has subclass -> Takeoff Segment
Flight Segment - has subclass -> Climbing Segment
Flight Segment - has subclass -> Cruising Segment
Flight Segment - has subclass -> Descending Segment
Flight Segment - has subclass -> Landing Segment
Flight Segment - has subclass -> Reverse Thrust Segment
Flight Segment - has subclass -> Taxi In Segment
Flight - is measured by -> Flight Data
Engine Run - is measured by -> Engine Run Data
Engine Run – subclass of -> Process
Flight Data - subclass of -> Measurement Information Content Entity
Engine Run Data - subclass of -> Measurement Information Content Entity
Engine Run Design Assumptions -subclass of -> Prescriptive Information Content Entity
Act of Engine Compliance Assessment - has input -> Engine Run Data
Act of Engine Compliance Assessment - has input -> Engine Run Design Assumptions
Engine Run Design Assumptions - prescribes -> Engine Run
Act of Engine Compliance Assessment - has output -> Engine Compliance Result
Engine Compliance Result - subclass of -> Information Content Entity
Engine Compliance Result - is about -> Customer
Engine Component Durability - inheres in -> Engine Component
Engine Component – continuant part of -> Engine
Engine Component Durability - realized in -> Engine Run
Engine Component Durability - is affected by -> Degradation Process
Engine Component Durability – subclass of -> Durability
Durability - subclass of -> Disposition
Operational Condition - subclass of -> Quality
Flight Operational Condition - subclass of -> Operational Condition
Engine Operational Condition - subclass of -> Operational Condition
Flight Operational Condition – is measured by -> Flight Data
Engine Operational Condition – is measured by -> Engine Run Data
Act of Engine Compliance Assessment – has input -> Engine Operational Condition
Engine Run Design Assumptions – prescribes -> Engine Operational Condition
Customer – affects -> Engine Operational Condition
Engine Operational Condition - Affects -> Engine Component Durability
Engine Component Degradation Process – subclass of -> Degradation Process
Engine Component Degradation Process – affects -> Engine Component Durability
Engine Component Degradation Process – has participant -> Engine Component
Engine Component Degradation Process – occurs in -> Engine Run
Customer – subclass of -> Commercial Organization


Engine Operational Condition - inheres in -> Engine.
Full Climb Thrust Condition – subclass of -> Engine Operational Condition
Engine Operational Condition – realized in -> Engine Run

Flight Operational Procedure - subclass of -> Directive Information Content Entity.
Climb Profile - subclass of -> Flight Operational Procedure.
Direct Climb Profile - subclass of -> Climb Profile
Step Climb Profile - subclass of -> Climb Profile
Flight Operational Procedure – prescribes -> Flight 
Flight Operational Condition - inheres in -> Flight
Flight Operational Condition - realized in -> Flight
Climb Profile - prescribes -> Climbing Segment

Flight Operational Condition - is measured by -> Flight Data (I guess already defined)

Engine Thrust - is measured by -> Engine Run Data.

Thrust – subclass of – Force
Force  - subclass of -> Process Profile
Engine Thrust – subclass of -> Thrust

Aircraft Altitude – subclass of -> Altitude
Aircraft Altitude – inheres in -> Aircraft
Aircraft Altitude – is measured by -> Flight Data

Aircraft Speed – subclass of -> Speed
Aircraft Speed – is measured by -> Flight Data

Climb Profile – prescribes -> Flight Operational Condition
Flight Operational Condition - inheres in -> Flight

Full Climb Thrust Condition – subclass of -> Engine Operational Condition

Full Thrust Threshold – subclass of -> Measurement Unit of Engine Thrust
Measurement Unit of Engine Thrust - subclass of -> Measurement Unit of Force

Full Climb Thrust Condition – realized in -> Engine Run

Engine Thrust – caused by -> Engine Run
Aircraft Speed – caused by -> Engine Thrust

Engine Thrust – is measured by -> Engine Run Data
Flight Operational Procedure – prescribes -> Flight Operational Condition

Engine Operational Condition – realized in -> Engine Run
Flight Operational Condition - realized in -> Flight

Customer – affects -> Flight Operational Condition
Customer – affects -> Engine Operational Condition

Act of Accessing Climb Profiles – has input -> Climb Profile
Act of Accessing Climb Profiles – has output -> Climb Profile Assessment Result
Act of Accessing Climb Profiles – subclass of -> Planned Act
Act of Accessing Climb Profiles – has input -> Engine Run Data
Act of Accessing Climb Profiles – has input -> Flight Data

Act of Comparing Engine Thrust -> has input -> Full Thrust Threshold
Act of Comparing Engine Thrust -> has input -> Engine Thrust Data

Flight Operational Condition – is cause of -> Engine Operational Condition

Flight Data – has continuant part -> Aircraft Altitude Data
Flight Data – has continuant part -> Aircraft Speed Data

Engine Run Data – has continuant part -> Engine Thrust Data

Certified Flight Envelope – subclass of -> Prescriptive Information Content Entity
Certified Flight Envelope – prescribes -> Flight Operational Condition

Act of Flight Envelope Compliance Assessment -> has input -> Flight Data
Act of Flight Envelope Compliance Assessment -> has input -> Certified Flight Envelope
Act of Flight Envelope Compliance Assessment -> has output -> Flight Envelope Compliance Result
Act of Flight Envelope Compliance Assessment -> is about -> Flight

Takeoff Segment - occupies temporal region -> Takeoff Segment Temporal Interval
Certified Time in Take-off Limit – prescribes -> Takeoff Segment Temporal Interval
Certified Time in Take-off Limit – subclass of -> Prescriptive Information Content Entity

Flight Data - has continuant part -> Takeoff Duration Data
Act of Takeoff Time Compliance Assessment – has input -> Certified Time in Take-off Limit
Act of Takeoff Time Compliance Assessment – has input -> Takeoff Duration Data
Act of Takeoff Time Compliance Assessment – has output -> Takeoff Time Compliance Result
Takeoff Time Compliance Result – is about -> Customer



Takeoff Segment Temporal Interval – is measured by -> Takeoff Duration Data
Takeoff Segment Temporal Interval – temporal part of -> Flight Segment Temporal Interval

Engine Run Temporal Interval – interval during -> Takeoff Segment Temporal Interval
Engine Run Design Assumptions -has continuant part -> Maximum Rated Thrust Value
Engine Run Temporal Interval - is measured by -> Engine Run Data

Act of Accessing Derated Takeoff Operation- has input -> Engine Thrust Data
Act of Accessing Derated Takeoff Operation- has input -> Maximum Rated Thrust Value
Act of Accessing Derated Takeoff Operation – has input -> Engine Run Data
Act of Accessing Derated Takeoff Operation – has input -> Takeoff Duration Data

Act of Accessing Derated Takeoff Operation – has output -> Derated Takeoff Results
Act of Accessing Derated Takeoff Operation – is about -> Engine Run
Derated Takeoff Results – is about -> Customer


Engine Run Design Assumptions – prescribes -> Engine Run Temporal Interval 
Engine Run Data – has continuant part -> Engine Run Temporal Data
Engine Run Temporal Interval – is measured by - Engine Run Temporal Data
Act of Outlier Engine Run Assessment – has input -> Engine Run Temporal Data
Act of Outlier Engine Run Assessment – has input -> Engine Run Design Assumptions
Act of Outlier Engine Run Assessment – has output -> Outlier Engine Run Assessment Result
Engine Run Data - has continuant part -> Engine Operational Condition Data
Engine Operational Condition – is measured by -> Engine Operational Condition Data
Act of Engine Durability Impact Assessment – has input -> Outlier Engine Run Assessment Result
Act of Engine Durability Impact Assessment – has input -> Engine Operational Condition Data
Act of Engine Durability Impact Assessment – has output -> Engine Durability Impact Result
Engine Durability Impact Result – is about -> Engine
Engine Component Durability - inheres in -> Engine Component
Engine Component – continuant part of -> Engine
Engine Component Durability - realized in -> Engine Run
Engine Component Durability - is affected by -> Degradation Process
Engine Component Durability – subclass of -> Durability
Durability - subclass of -> Disposition
Operational Condition - subclass of -> Quality
Flight Operational Condition - subclass of -> Operational Condition
Engine Operational Condition - subclass of -> Operational Condition
Flight Operational Condition – is measured by -> Flight Data
Act of Engine Compliance Assessment – has input -> Engine Operational Condition
Engine Run Design Assumptions – prescribes -> Engine Operational Condition
Customer – affects -> Engine Operational Condition
Flight Operational Condition – is cause of -> Engine Operational Condition
Engine Operational Condition - Affects -> Engine Component Durability
Engine Component Degradation Process – subclass of -> Degradation Process
Engine Component Degradation Process – affects -> Engine Component Durability
Engine Component Degradation Process – has participant -> Engine Component
Engine Component Degradation Process – occurs in -> Engine Run
Customer – subclass of -> Commercial Organization
Engine Operational Condition - inheres in -> Engine.

