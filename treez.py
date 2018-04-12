import random
from ete2 import Tree, TreeStyle, NodeStyle, faces, AttrFace, TreeFace

# Tree Style used to render small trees used as leaf faces
small_ts = TreeStyle()
small_ts.show_leaf_name = True
small_ts.scale = 10

def layout(node):
    if node.is_leaf():
        # Add node name to laef nodes
        N = AttrFace("name", fsize=14, fgcolor="black")
        faces.add_face_to_node(N, node, 0)

        t = Tree()
        t.populate(5)

        T = TreeFace(t, small_ts)
        # Let's make the sphere transparent 
        T.opacity = 0.8
        # And place as a float face over the tree
        T.show_leaf_name=False
        T.show_branch_length=False
        T.show_branch_support=False
        faces.add_face_to_node(T, node, 1, position="aligned")

def get_example_tree():
    # Random tree
    t = Tree("(((c1,c2,c3),(c1,c3),(c1,c2),(c1,c2,c5)),((b1,b4,b5)),((c1,c2),(b1,b3)));")

    # t.populate(10, random_branches=True)

    # Some random features in all nodes
    for n in t.traverse():
        n.add_features(weight=random.randint(0, 50))

    # Create an empty TreeStyle
    ts = TreeStyle()

    # Set our custom layout function
    ts.layout_fn = layout

    # Draw a tree 
    # ts.mode = "c"
    ts.rotation = 90

    # We will add node names manually
    ts.show_leaf_name = False
    # Show branch data
    ts.show_branch_length = False
    ts.show_branch_support = False
    return t, ts

if __name__ == "__main__":
    t, ts = get_example_tree()
    #t.render("tree_faces.png", w=600, dpi=300, tree_style=ts)
    t.show(tree_style=ts)
