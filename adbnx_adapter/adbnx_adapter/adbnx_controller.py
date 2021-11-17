from .abc import ADBNX_Controller

from arango.graph import Graph as ArangoDBGraph
from networkx.classes.graph import Graph as NetworkXGraph


class Base_ADBNX_Controller(ADBNX_Controller):
    def __init__(self):
        self.nx_graph: NetworkXGraph = None
        self.nx_map = dict()  # Maps ArangoDB vertex IDs to NetworkX node IDs

        self.adb_graph: ArangoDBGraph = None

        self.adb_map = dict()  # Maps NetworkX node IDs to ArangoDB vertex IDs

    def _prepare_adb_vertex(self, vertex: dict, collection: str):
        """
        Given an ArangoDB vertex, you can modify it before it gets inserted
        into the NetworkX graph, and/or derive a custom node id for networkx to use.

        In most cases, it is only required to return the ArangoDB _id of the vertex.
        """
        return vertex["_id"]

    def _prepare_adb_edge(self, edge: dict, collection: str):
        """
        Given an ArangoDB edge, you can modify it before it gets inserted
        into the NetworkX graph.

        In most cases, no action is needed.
        """
        pass

    def _identify_nx_node(self, id, node: dict, overwrite: bool) -> str:
        """
        Given a NetworkX node, identify what ArangoDB collection should it belong to.

        NOTE: If your NetworkX graph does not comply to ArangoDB standards
        (i.e a node's ID is not "collection/key"), then you must override this function.
        """
        # In this case, id is already a valid ArangoDB _id
        adb_id: str = id
        return adb_id.split("/")[0] + ("" if overwrite else "_nx")

    def _identify_nx_edge(
        self, edge: dict, from_node: dict, to_node: dict, overwrite: bool
    ) -> str:
        """
        Given a NetworkX edge, its pair of nodes, and the overwrite boolean,
        identify what ArangoDB collection should it belong to.

        NOTE: If your NetworkX graph does not comply to ArangoDB standards
        (i.e a node's ID is not "collection/key"), then you must override this function.
        """
        # In this case, edge["_id"] is already a valid ArangoDB _id
        edge_id: str = edge["_id"]
        return edge_id.split("/")[0] + ("" if overwrite else "_nx")

    def _keyify_nx_node(self, id, node: dict, collection: str, overwrite: bool) -> str:
        """
        Given a NetworkX node, derive its valid ArangoDB key.

        NOTE: If your NetworkX graph does not comply to ArangoDB standards
        (i.e a node's ID is not "collection/key"), then you must override this function.
        """
        # In this case, id is already a valid ArangoDB _id
        adb_id: str = id
        return adb_id.split("/")[1]

    def _keyify_nx_edge(
        self,
        edge: dict,
        from_node: dict,
        to_node: dict,
        collection: str,
        overwrite: bool,
    ):
        """
        Given a NetworkX edge, its collection, its pair of nodes, and the overwrite boolean,
        derive its valid ArangoDB key.

        NOTE: If your NetworkX graph does not comply to ArangoDB standards
        (i.e a node's ID is not "collection/key"), then you must override this function.
        """
        # In this case, edge["_id"] is already a valid ArangoDB _id
        edge_id: str = edge["_id"]
        return edge_id.split("/")[1]

    def _string_to_arangodb_key_helper(self, string: str) -> str:
        """
        Given a string, derive a valid ArangoDB _key string.
        """
        res = ""
        for s in string:
            if s.isalnum() or s in self.VALID_KEY_CHARS:
                res += s

        return res

    def _tuple_to_arangodb_key_helper(self, tup: tuple) -> str:
        """
        Given a tuple, derive a valid ArangoDB _key string.
        """
        string = "".join(map(str, tup))
        return self._string_to_arangodb_key_helper(string)
