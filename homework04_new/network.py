from api import get_friends


def get_network(users_ids, as_edgelist=True):
    users_ids = get_friends(user_id)
    edges = []
    for user1 in range(len(users_ids)):
        response = get_friends(users_ids[user1])
        friends = response
        for user2 in range(user1 + 1, len(users_ids)):
            if users_ids[user2] in friends:
                edges.append((user1, user2))
        time.sleep(0.33333334)
    return edges



def plot_graph(graph):
    pass