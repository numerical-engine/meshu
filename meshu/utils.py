import numpy as np
from meshu import config
from meshu.core import Mesh

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