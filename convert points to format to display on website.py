import matplotlib.pyplot as plt
import json

# Given list of points
points = [[-8.46183644,  1.85307666]]


# Scale the points by multiplying x and y coordinates by 100
scaled_points = [(x * 50, y * 50) for x, y in points]

# Shift the points by adding [-12.5, 12.5] to each x,y tuple
shifted_points = [(x + (500), y + 500) for x, y in scaled_points]


# Convert shifted points to the format required for Voronoi diagram
formatted_points = [coord for point in shifted_points for coord in point]

# Create the dictionary with the formatted points
voronoi_data = {
    "sites": formatted_points,
    "queries": []
}

# Convert the dictionary to JSON format without indentation and with minimal separators
json_data = json.dumps(voronoi_data, separators=(',', ':'))

# Print or use the JSON data
# print(json_data)


# List of top scores
top_scores = [
    2.5921853443077456, 4.083819661089976, 4.9515195021865495, 5.0699467259216835,
    5.838427898850929, 5.624556021134671, 5.828227851453698, 5.943659147401387,
    6.028195814585002, 6.146125117779489, 6.241029883572414, 6.356759289764241,
    6.458945048157735, 6.645411142934921, 6.721081584519678, 6.836766204444034,
    6.978138182384567, 7.074512605869889, 7.183325923553196, 7.344138296449883,
    7.42001651531965, 7.47751024512743, 7.5541231805505875, 7.6552550784882145,
    7.64485076676252, 7.741587553208293, 7.783422471021262, 7.842197404941647,
    7.915385537636973, 7.974210155052227, 8.037591283298644, 8.09097389505972,
    8.11051067210754, 8.16883973969253, 8.27756825624205, 8.281032388753042,
    8.371160084791805, 8.447325301283689, 8.573631488612724, 8.594137965431486,
    8.661880708348017, 8.731432945846445, 8.735996257787672, 8.777355186810539,
    8.802896466806018, 8.844177440230299, 8.844431243831766, 8.914718374011235,
    8.91022746255696, 8.984311007227612, 9.008959282911816, 9.042778880956373,
    9.120508200211388, 9.120087251871075, 9.14699986845212, 9.201131186640637,
    9.257583335206066, 9.251302871667942, 9.282775161605766, 9.33708704166408,
    9.360989068815995, 9.392247604627311, 9.472940122591648, 9.532774191600568,
    9.525868596895297, 9.553158368175643, 9.545309916100763, 9.581124826515854,
    9.567511671047065, 9.566359336496761, 9.571227191357709, 9.560681162654458,
    9.559731253624154, 9.563760921782348, 9.56775449809085, 9.583450086703996,
    9.578856214438042, 9.572197057315737, 9.573316966181585, 9.564649590811305,
    9.553125005672324, 9.57508785251311, 9.568902933026868, 9.562940786917785,
    9.580468157642297, 9.559687461061001, 9.563315437317069, 9.570587976112014,
    9.576391898054021, 9.567233246031625, 9.572321896639984, 9.56082953454357,
    9.579695388357012, 9.57629534078655, 9.573821396478154, 9.571898498615457,
    9.573243278951088, 9.580846077921828, 9.570456768065998, 9.566880163473986,
    9.591015298771874, 9.576202461491073, 9.555587696959087, 9.578945334035483,
    9.566722300132593, 9.583468147873385, 9.589065589779967, 9.57961387108802,
    9.578136852680595, 9.576257444025595, 9.582439159709686, 9.565851790268772,
    9.568510013997502, 9.56310586956209, 9.558611886149523, 9.575045764743415,
    9.577234282259639, 9.575077142713232, 9.577200593797864, 9.572175762849477,
    9.571883615946449, 9.58232408764704, 9.566276743926359, 9.572399491898038,
    9.578438380129418
]



# Create x values (positions)
x_values = list(range(1, len(top_scores) + 1))

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, top_scores, marker='o')

# Add labels and title
plt.xlabel('Position')
plt.ylabel('Top Score')
plt.title('Top Scores Line Graph')

# Show the plot
plt.tight_layout()
plt.show()
