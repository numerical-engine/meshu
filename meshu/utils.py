import numpy as np
from meshu import config
from meshu.core import Mesh
import pivtk
import sys

def pickup_elementtag(mesh:Mesh, dim:int)->tuple[int]:
    """次元数がdimの要素タグを出力

    Args:
        mesh (Mesh): Meshオブジェクト 
        dim (int): 次元
    Returns:
        tuple[int]: 該当要素のタグのリスト (ゼロ始まり)
    """
    element_tag = []

    for tag, element in enumerate(mesh.Elements):
        e_type = element["type"]
        if e_type in config.element_types[dim]:
            element_tag.append(tag)
    return tuple(element_tag)


def get_elements(mesh:Mesh, dim:int)->tuple[dict]:
    """次元がdimの要素のタプルを出力

    Args:
        mesh (Mesh): Meshオブジェクト
        dim (int): 次元
    Returns:
        tuple[dict]: 要素情報のタプル
    """
    tags = pickup_elementtag(mesh, dim)
    elements = tuple([mesh.Elements[t] for t in tags])

    return elements


def get_physical_names(mesh:Mesh, dim:int = None)->tuple[str]:
    """次元がdimのPhysicalGroupの名前を出力

    Args:
        mesh (Mesh): Meshオブジェクト
        dim (int, optional): PhysicalGroupの次元。Noneの場合すべてのPhysicalGroupの名前を出力
    Returns:
        tuple[str]: 名前のタプル
    """
    names = []
    for phys_g in mesh.PhysicalGroups:
        if dim is None:
            names.append(phys_g["name"])
        else:
            if phys_g["dim"] == dim:
                names.append(phys_g["name"])
    
    return tuple(names)


def Graph2UnstructuredGrid(V:np.ndarray, E:np.ndarray)->pivtk.geom.unstructured_grid:
    """ノード座標値と隣接行列(COO形式)からVTKジオメトリを出力

    Args:
        V (np.ndarray): ノード座標値。
        E (np.ndarray): 隣接行列。
    Returns:
        geom.unstructured_grid: unstructured gridジオメトリ
    """
    cells = [{"type" : 3, "indice" : np.array([e_st,e_fn])} for e_st, e_fn in zip(E[0], E[1])]
    return pivtk.geom.unstructured_grid(points = V, cells = tuple(cells))


def get_phystag_node(mesh:Mesh)->np.ndarray:
    """境界にあるノードに対し、属している境界のPhysical Tagを出力。

    境界上でないノードには、-1のTagを与える。
    Args:
        mesh (Mesh): Meshオブジェクト。
    Returns:
        np.ndarray: 境界ノードのPhysical Tag情報。
    """
    phys_tag = -np.ones(len(mesh.Nodes))
    element1d = get_elements(mesh, mesh.dim-1)
    for e1d in element1d:
        for n in e1d["node_tag"]:
            phys_tag[n] = e1d["phys_tag"]
    
    return phys_tag

def get_edge(mesh:Mesh, i:int, j:int)->dict:
    """e = (i,j)のエッジ情報を出力

    Args:
        mesh (Mesh): Meshオブジェクト。
        i (int): 開始点ノードtag。
        j (int): 終了点ノードtag。
    Returns:
        dict: エッジ情報。(i,j)なるエッジがない場合はNoneを返す。
    """
    edges = get_elements(mesh, 1)

    for edge in edges:
        if (i == edge["node_tag"][0]) & (j == edge["node_tag"][1]):
            return edge
    return None

def get_phystag_between_nodes(mesh:Mesh, i:int, j:int, except_val:int = -1)->int:
    """エッジ(i,j)のphysical tagを出力

    Args:
        mesh (Mesh): Meshオブジェクト。
        i (int): 開始点ノードtag。
        j (int): 終了点ノードtag。
        except_val (int): (i, j)がない場合に返す値。
    Returns:
        int: physical tag。
    """
    element = get_edge(mesh, i, j)
    if element is None:
        element = get_edge(mesh, j, i)
        if element is None:
            return except_val
        else:
            return element["phys_tag"]
    else:
        return element["phys_tag"]