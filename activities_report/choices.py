project_choice = [
      ('Coastal road', 'Coastal road'),
      ('Sokoto road', 'Sokoto road'),
      ('Benin road', 'Benin road'),
      ('Abuja road', 'Abuja road'),

      
      ]
    
activities_category = [
    ('survey_and_design', 'Survey and Design'),
    ('clearing_grading', 'Clearing and Grading'),
    ('setting_out_points', 'Setting out points'),
    ('excavation_earthwork', 'Excavation and Earthwork'),
    ('drainage_channels', 'Channels, ducts and drainages works'),
    ('subbase_installation', 'Subbase Installation'),
    ('base_course_installation', 'Base Course Installation'),
    ('demolition', 'Demolition'),
    ('paving', 'Paving'),
    ('ducts', 'Ducts'),
    ('construction_drainage_channels', 'Construction of Drainage Channels'),
    ('sidewalks_shoulders', 'Sidewalks and Shoulders'),
    ('road_markings_signage', 'Road Markings and Signage'),
    ('vegetation_landscaping', 'Vegetation and Landscaping'),
    ('quality_control', 'Quality Control and Inspection'),
    ('trainings', 'Trainings'),
    ('soil_cement', 'Soil Cement'),
    ('construction', 'Construction'),
]


party = [
    ('HiTech Employees', 'HiTech Employees'),
    ('Sub-contactor', 'Sub-contactor'),
]
sources =  [
    ('HiTech Employees', 'HiTech Employees'),
    ('Sub-contactor', 'Sub-contactor'),
    ('Renting Third Party', "Renting Third Party")
]


supervisor = [
        ('Nabih', 'Nabih'),
        ('Tony', 'Tony'),
        ('Ahmad', 'Ahmad'),
        ('Boutros', 'Boutros'),
        ('Nadim', 'Nadim'),
        ('ziad', 'ziad'),
        ('Elie', 'Elie'),
        ('Dory', 'Dory'),
        ('Thens', 'Thens'),
        ('Antonios - Abou Nadim', 'Antonios - Abou Nadim')

]

engineers = [
    ('Believe', 'Believe'),
        ('TONY', 'TONY'),
        ('BUKOLA', 'BUKOLA'),
        ('ADERONKE', 'ADERONKE'),
        ('SODIQ', 'SODIQ'),
        ('Habib', 'Habib')

]


machines = [
        ('CRCP paver', 'CRCP paver'),
        ('Asphalt paver', 'Asphalt paver'),
        ('Dozer', 'Dozer'),
        ('Grader', 'Grader'),
        ('Excavator', 'Excavator'),
        ('Swamp buggy', 'Swamp buggy'),
        ('Smooth Roller', 'Smooth Roller'),
        ('Padfoot Roller', 'Padfoot Roller'),
        ('Water Tanker', 'Water Tanker'),
        ('Diesel Tanker', 'Diesel Tanker'),
        ('Hillux Pickup', 'Hillux Pickup'),
        ('Level Instruments', 'Level Instruments'),
        ('Total Stations', 'Total Stations'),
        ('GPS', 'GPS'),
        ('Batymetric survey machine', 'Batymetric survey machine'),
        ('Drone', 'Drone'),
        ('Canoe', 'Canoe'),
        ('Vehicules', 'Vehicules'),
        ('Containers', 'Containers'),
        ('Tipper', 'Tipper'),
        ('Payloader', 'Payloader'),
        ('Mechanical broom', 'Mechanical broom'),
        ('Mobile crane', 'Mobile crane'),
        ('Plate compactor', 'Plate compactor')

]

chanage = [(f'{x}+040', f'{x}+040') for x in range(49) ]

chanage2 = [(f'{x}+{y:03}', f'{x}+{y:03}') for x in range(11) for y in range(0, 1000, 20)]

activities = {
    "Construction": [
        "Barrier base",
        "Installation of jersey separation barrier",
        "Installation CRCP",
        "Installation stoneBase",
        "Installation subBase",
        "Installation soil cement",
        "Steel structure",
        "Concrete work",
        "Pipe factory",
        "Batching plant"
    ],
    "Survey and Design": [
        "Conduct a survey",
        "Create road design plans",
        "Cut elevations",
        "Fill elevations",
        "Dredging elevations",
        "Clearing elevations"
    ],
    "Trainings": [
        "Levelling and handling surveying instruments",
        "Hitech activity report"
    ],
    "Setting Out Points": [
        "Road requirements boundary",
        "Toe",
        "Top of stoneBase",
        "Top of subBase",
        "Top of CRCP",
        "Borehole",
        "Other"
    ],
    "Clearing and Grading": [
        "Clearing obstacles",
        "Grade prepare road",
        "Excavate road width",
        "Excavate unsuitable materials",
        "Compaction subgrade"
    ],
    "Excavation and Earthwork": [
        "Excavate for pipe 600mm",
        "Blinding for pipe 600mm",
        "Blinding for discharge 900mm",
        "Blinding for discharge 1200mm",
        "Excavate for discharge 900mm",
        "Excavate for discharge 1200mm",
        "Excavate for culvert 150*150",
        "Excavate for culvert 200*200",
        "Blinding culvert 150*150",
        "Blinding for culvert 200*200",
        "Base culvert 150*150",
        "Base for culvert 200*200"
    ],
    "Drainage Channels": [
        "Complete drainage",
        "Entrance slab",
        "Excavate drainage",
        "Line drainage",
        "Culvert cross drainage"
    ],
    "Ducts": [
        "Ducts for electrical cables",
        "Ducts for telecom cable",
        "Ducts for drinking water pipe"
    ],
    "Subbase Installation": [
        "Lay layer subbase",
        "Compact subbase"
    ],
    "Soil Cement": [
        "Soil cement stabilization"
    ],
    "Base Course Installation": [
        "Lay layer basecourse",
        "Compact basecourse"
    ],
    "Demolition": [
        "Building",
        "Other (fans, walls, etc.)"
    ],
    "Paving": [
        "Apply asphalt concrete",
        "Compact asphalt concrete"
    ],
    "Sidewalks and Shoulders": [
        "Construct sidewalks and shoulders"
    ],
    "Road Markings and Signage": [
        "Paint road marks",
        "Install traffic signs and signals"
    ],
    "Vegetation Landscaping": [
        "Plant grass or vegetation to prevent erosion",
        "Implement landscaping elements to beautify"
    ],
    "Quality Control": [
        "Ensure compliance with design specifications and safety standards",
        "Quality control test materials"
    ]
}

activitiess = [(f'{y}', f'{y}') for x in activities.values() for y in x]