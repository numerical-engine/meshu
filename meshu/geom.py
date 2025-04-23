import numpy as np
from meshu import config
from meshu.core import Mesh

def get_centroid(element:dict, mesh:Mesh)->np.ndarray:
    """要素の重心を出力

    Args:
        element (dict): 要素情報
        mesh (Mesh): Meshオブジェクト
    Returns:
        np.ndarray: 重心座標。shapeは(D, )。
    """
    nodes = mesh.Nodes[element["node_tag"],]
    centroid = np.mean(nodes, axis = 0)

    return centroid

def get_volume(element:dict, mesh:Mesh)->float:
    """要素の体積を出力

    Args:
        element (dict): 要素
        mesh (Mesh): Mesh
    Returns:
        float: 体積
    """
    nodes = mesh.Nodes[element["node_tag"],:]
    if element["type"] == 2:
        return 0.5*np.abs(nodes[0,0]*(nodes[1,1]-nodes[2,1]) + nodes[1,0]*(nodes[2,1]-nodes[0,1]) + nodes[2,0]*(nodes[0,1]-nodes[1,1]))
    else:
        raise NotImplementedError


def get_facet_normal(element:dict, mesh:Mesh)->tuple[np.ndarray]:
    """各ファセットの外向き単位法線ベクトルを出力

    Args:
        element (dict): 要素
        mesh (Mesh): Mesh
    Returns:
        tuple[np.ndarray]: 各ファセットの外向き単位法線ベクトル(定義順)
    """
    if element["type"] == 2:
        node0, node1, node2 = mesh.Nodes[element["node_tag"],:]
        x1, y1 = node0; x2, y2 = node1; x3, y3 = node2
        l1 = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        l2 = np.sqrt((x2-x3)**2 + (y2-y3)**2)
        l3 = np.sqrt((x3-x1)**2 + (y3-y1)**2)

        n1 = np.array([y2-y1, x1-x2])/l1
        n2 = np.array([y3-y2, x2-x3])/l2
        n3 = np.array([y1-y3, x3-x1])/l3

        return n1, n2, n3
    else:
        raise NotImplementedError