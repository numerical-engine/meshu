import numpy as np
from meshu import config, utils
from meshu.core import Mesh
import sys
from scipy.sparse import dok_matrix, triu

def get_adjacency_matrix(mesh:Mesh, include_selfloop:bool = False, double_direction:bool = False)->np.ndarray:
    """メッシュ構造の隣接行列(COO形式)を出力

    Args:
        mesh (Mesh): MSHオブジェクト
        include_selfroop (bool, optional): 自己ループを加えるか否か。
        double_direction (bool, optional): Trueの場合、(i,j), (j, i)両方がCOOに含む冗長な表現を出力
    Returns:
        np.ndarray: 隣接行列。shapeは(2, E)でEはエッジ数。
    Note:
        * 無向グラフを出力。
        * 隣接行列の要素値は節点タグ。
    """
    element_tags = utils.pickup_elementtag(mesh, mesh.dim)
    elements = [mesh.Elements[et] for et in element_tags]
    num_node = len(mesh.Nodes)
    
    A = dok_matrix((num_node, num_node), dtype = int)
    for element in elements:
        node_tag = element["node_tag"]
        for i in range(len(node_tag)-1):
            A[node_tag[i], node_tag[i+1]] = 1; A[node_tag[i+1], node_tag[i]] = 1
        A[node_tag[0], node_tag[-1]] = 1; A[node_tag[-1], node_tag[0]] = 1
    if include_selfloop:
        for i in range(num_node):
            A[i,i] = 1

    A = A.tocoo()
    if double_direction:
        A = triu(A)
    A = np.stack(A.coords, axis = 0)

    return A