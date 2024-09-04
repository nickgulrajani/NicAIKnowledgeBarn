#Author: Nicholas Gulrajani
import random
from datetime import datetime, timedelta
from py2neo import Graph, Node, Relationship
import networkx as nx
import matplotlib.pyplot as plt

# Connect to Neo4j (update with your credentials)
graph = Graph("bolt://localhost:7687", auth=("neo4j", ""))

# Clear existing data
graph.delete_all()

# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Generate sample data
patients = [f"Patient_{i}" for i in range(1, 11)]
doctors = [f"Doctor_{i}" for i in range(1, 6)]
nurses = [f"Nurse_{i}" for i in range(1, 11)]
facilities = ["Emergency Room", "Inpatient Ward", "Outpatient Clinic", "Radiology", "Laboratory"]
procedures = ["Blood Test", "X-Ray", "MRI", "CT Scan", "Ultrasound", "Surgery"]
medications = ["Antibiotic", "Pain Reliever", "Anti-inflammatory", "Antihypertensive", "Antidepressant"]

# Create nodes
node_dict = {}
for entity in patients + doctors + nurses + facilities + procedures + medications:
    node_type = entity.split('_')[0] if '_' in entity else entity.split()[0]
    node = Node(node_type, name=entity)
    graph.create(node)
    node_dict[entity] = node

print("All nodes created successfully.")

# Create episode of care for each patient
for patient in patients:
    episode_start = random_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
    episode_end = episode_start + timedelta(days=random.randint(1, 30))
    
    episode = Node("EpisodeOfCare", 
                   start_date=episode_start.strftime("%Y-%m-%d"),
                   end_date=episode_end.strftime("%Y-%m-%d"))
    graph.create(episode)
    
    patient_node = node_dict.get(patient)
    if patient_node:
        graph.create(Relationship(patient_node, "HAS_EPISODE", episode))
    else:
        print(f"Warning: Patient {patient} not found in the node dictionary.")
    
    # Generate random interactions within the episode
    current_date = episode_start
    while current_date <= episode_end:
        # Visit a facility
        facility = random.choice(facilities)
        visit = Node("Visit", date=current_date.strftime("%Y-%m-%d"), facility=facility)
        graph.create(visit)
        graph.create(Relationship(episode, "INCLUDES", visit))
        
        if patient_node:
            graph.create(Relationship(patient_node, "VISITS", visit))
        
        # Interact with healthcare professionals
        doctor = random.choice(doctors)
        nurse = random.choice(nurses)
        doctor_node = node_dict.get(doctor)
        nurse_node = node_dict.get(nurse)
        
        if doctor_node:
            graph.create(Relationship(doctor_node, "ATTENDS", visit))
        else:
            print(f"Warning: Doctor {doctor} not found in the node dictionary.")
        
        if nurse_node:
            graph.create(Relationship(nurse_node, "ASSISTS", visit))
        else:
            print(f"Warning: Nurse {nurse} not found in the node dictionary.")
        
        # Undergo procedures
        if random.random() < 0.7:  # 70% chance of procedure
            procedure = random.choice(procedures)
            procedure_node = node_dict.get(procedure)
            if procedure_node:
                graph.create(Relationship(visit, "INCLUDES", procedure_node))
            else:
                print(f"Warning: Procedure {procedure} not found in the node dictionary.")
        
        # Receive medications
        if random.random() < 0.8:  # 80% chance of medication
            medication = random.choice(medications)
            medication_node = node_dict.get(medication)
            if medication_node:
                graph.create(Relationship(visit, "PRESCRIBES", medication_node))
            else:
                print(f"Warning: Medication {medication} not found in the node dictionary.")
        
        current_date += timedelta(days=random.randint(1, 5))

print("Healthcare episode of care knowledge graph created successfully!")

# Query to analyze a patient's episode of care
query = """
MATCH (p:Patient)-[:HAS_EPISODE]->(e:EpisodeOfCare)-[:INCLUDES]->(v:Visit)
OPTIONAL MATCH (v)-[:INCLUDES]->(proc:Procedure)
OPTIONAL MATCH (v)-[:PRESCRIBES]->(med:Medication)
OPTIONAL MATCH (d:Doctor)-[:ATTENDS]->(v)
OPTIONAL MATCH (n:Nurse)-[:ASSISTS]->(v)
WITH p, e, v, 
     collect(DISTINCT proc.name) AS procedures,
     collect(DISTINCT med.name) AS medications,
     collect(DISTINCT d.name) AS doctors,
     collect(DISTINCT n.name) AS nurses
RETURN p.name AS patient, e.start_date, e.end_date, 
       count(v) AS visit_count,
       collect({date: v.date, facility: v.facility, 
                procedures: procedures, 
                medications: medications,
                doctors: doctors,
                nurses: nurses}) AS visits
ORDER BY visit_count DESC
LIMIT 1
"""

results = graph.run(query)

# Create a NetworkX graph for visualization
G = nx.Graph()

for record in results:
    patient = record['patient']
    G.add_node(patient, node_type='Patient')
    
    for visit in record['visits']:
        visit_id = f"{visit['date']}_{visit['facility']}"
        G.add_node(visit_id, node_type='Visit')
        G.add_edge(patient, visit_id)
        
        for procedure in visit['procedures']:
            G.add_node(procedure, node_type='Procedure')
            G.add_edge(visit_id, procedure)
        
        for medication in visit['medications']:
            G.add_node(medication, node_type='Medication')
            G.add_edge(visit_id, medication)
        
        for doctor in visit['doctors']:
            G.add_node(doctor, node_type='Doctor')
            G.add_edge(visit_id, doctor)
        
        for nurse in visit['nurses']:
            G.add_node(nurse, node_type='Nurse')
            G.add_edge(visit_id, nurse)

# Set up colors for different node types
color_map = {'Patient': 'lightblue', 'Visit': 'lightgreen', 'Procedure': 'lightcoral',
             'Medication': 'yellow', 'Doctor': 'orange', 'Nurse': 'pink'}
node_colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes()]

# Draw the graph
plt.figure(figsize=(20, 15))
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=3000, font_size=8, font_weight='bold')

# Add a legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=node_type,
                              markerfacecolor=color, markersize=15)
                   for node_type, color in color_map.items()]
plt.legend(handles=legend_elements, loc='upper right')

plt.title("Healthcare Episode of Care Analysis")
plt.axis('off')
plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('healthcare_episode_of_care.png', dpi=300, bbox_inches='tight')
print("Graph visualization saved as 'healthcare_episode_of_care.png'")

# Close the plot to free up memory
plt.close()

print("Healthcare Episode of Care Analysis:")
for record in results:
    print(f"Patient: {record['patient']}")
    print(f"Episode Start: {record['e.start_date']}, End: {record['e.end_date']}")
    print(f"Total Visits: {record['visit_count']}")
    print("\nDetailed Visit Information:")
    for visit in record['visits']:
        print(f"  Date: {visit['date']}, Facility: {visit['facility']}")
        print(f"  Procedures: {', '.join(visit['procedures'])}")
        print(f"  Medications: {', '.join(visit['medications'])}")
        print(f"  Doctors: {', '.join(visit['doctors'])}")
        print(f"  Nurses: {', '.join(visit['nurses'])}")
        print()



