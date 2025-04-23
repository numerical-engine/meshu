import numpy as np
from meshu import config
from meshu.core import Mesh
import sys

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
    """要素の体積(2次元の場合は面積)を出力

    Args:
        element (dict): 要素情報
        mesh (Mesh): Meshオブジェクト
    Returns:
        float: 体積(もしくは面積)
    Note:
        * 2次元の場合、要素は自己交差無しの多角形であること、並びに節点が反時計回りの順に定義されていることを仮定
    """
    if mesh.dim == 2:
        nodes = mesh.Nodes[element["node_tag"],:]
        nodes_ex = np.concatenate((nodes, nodes[0].reshape((1,2))), axis = 0)
        V = 0.
        for i in range(len(nodes)):
            V += (nodes_ex[i,0] - nodes_ex[i+1,0])*(nodes_ex[i,1] + nodes_ex[i+1,1])
        V *= 0.5
        return V
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