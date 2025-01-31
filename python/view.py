import common.db as db
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore
import math

st.title('Brain Beaver 🦫')

networks = db.read_tb_networks_all()
concepts = db.read_tb_concepts_all()
references = db.read_tb_references_all()
print(f"networks: {len(networks)}, concepts: {len(concepts)}, references: {len(references)}")

nodes = []
edges = []

node_default_size = 10
node_multiple = 5
node_source_many = '#A3C9A8'
node_neutral = '#69A297'
node_target_many = '#50808E'

#node_type = 'circularImage'
#node_image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTxEQr3SSOrrhOXpbVP0B_4T2OysRy7cGnqA&s'

for concept in concepts:
    if concept.source_num * concept.target_num <= 0:
        node_size = node_default_size
    else:
        node_size = node_default_size * math.log(concept.source_num * concept.target_num,5)
    #node_size = max(node_default_size, 
    #                node_default_size*(concept.source_num//node_multiple), 
    #                node_default_size*(concept.target_num//node_multiple))
    #node_size = max(node_default_size,
    #                node_default_size * (concept.source_num + concept.target_num) // node_multiple)

    node_color = node_neutral
    if concept.source_num > concept.target_num * 2:
        node_color = node_source_many
    elif concept.target_num > concept.source_num * 2:
        node_color = node_target_many
    
    nodes.append(Node(
                        id=f"C{concept.id}",              
                        title=f"{concept.id} - {concept.title} | \n{concept.summary.replace('.', '.\n')}\n* {concept.filepath}",
                        label=concept.id,  
                        color=node_color,
                        shape='circularImage', # image, circularImage, diamond, dot, star, triangle, triangleDown, hexagon, square and icon
                        image='',
                        size=node_size
                    ))
    
for reference in references:
    nodes.append(Node(
                        id=f"R{reference.id}",              
                        title=f"{reference.concept_id} : {reference.description[:200].replace('.','.\n')}",
                        label=reference.id,  
                        color='#FF0000',
                        shape='dot', # image, circularImage, diamond, dot, star, triangle, dot, hexagon, square and icon
                        image='',
                        size=node_default_size*1.3
                    ))
    edges.append(Edge(
                        source=f"R{reference.id}",      
                        label='',  
                        target=f"C{reference.concept_id}",
                        color='#ced4da',      
                    ))

for network in networks:
    edges.append(Edge(
                        source=f"C{network.source_concept_id}",      
                        label='',                   
                        target=f"C{network.target_concept_id}",
                        color='#ced4da',      
                    ))

config = Config(
                    width=750,
                    height=950,
                    directed=True, 
                    physics=True, 
                    maxVelocity=60,
                    hierarchical=False
                )

rtnmsg = agraph(nodes=nodes, edges=edges, config=config)
#print(rtnmsg)