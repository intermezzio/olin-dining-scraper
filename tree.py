from typing import Callable
from icecream import ic
from functools import reduce
from operator import or_
import json

all_days = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

all_days_lower = tuple(x.lower() for x in all_days)

class Tree:
    def __init__(self, data: str, parent = None, hier: int = 0):
        self.data = data
        self.children: list[Tree] = []
        self.parent: Tree | None = parent
        self.hier = hier
    
    def __repr__(self) -> str:
        self_str = "--" * self.hier + " " + self.data
        child_str = "".join(repr(c) for c in self.children)
        return self_str + "\n" + child_str

    def reveal(self) -> tuple[str,list["Tree"]]:
        return self.data, self.children

    def to_dict(self) -> dict | str:
        if len(self.children) == 0:
            return self.data
        else:
            child_data = [x.to_dict() for x in self.children]
            child_data_str = list(filter(lambda x: isinstance(x, str), child_data))
            child_data_dict = reduce(or_, filter(lambda x: isinstance(x, dict), child_data), dict())
            
            if child_data_dict and not child_data_str:
                return {self.data: child_data_dict}
            elif not child_data_dict and child_data_str:
                return {self.data: list(child_data_str)}
            else:
                return {self.data: [child_data_dict] + list(child_data_str)}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @staticmethod
    def from_list(data: list[str], hier: Callable[[str],int]) -> "Tree":
        base_tree = Tree("root")
        current_tree = base_tree
        for line in data:
            line_hier = hier(line)
            if line_hier == -1:
                continue
            elif line_hier == current_tree.hier + 1:
                # add current line as child
                new_tree = Tree(line, parent=current_tree, hier=line_hier)
                current_tree.children.append(new_tree)
                current_tree = new_tree
            elif line_hier == current_tree.hier:
                # current line is sibling of previous
                new_tree = Tree(line, parent=current_tree.parent, hier=line_hier)
                current_tree.parent.children.append(new_tree)
                current_tree = new_tree
            elif line_hier < current_tree.hier:
                # current line is a higher level
                while current_tree.hier > 0:
                    current_tree = current_tree.parent
                    assert current_tree is not None

                    if line_hier == current_tree.hier:
                        # current line is sibling of previous
                        new_tree = Tree(line, parent=current_tree.parent, hier=line_hier)
                        current_tree.parent.children.append(new_tree)
                        current_tree = new_tree
                        break
            else:
                raise ValueError(f"Invalid hier {line}:{line_hier} after hier {current_tree.data}:{current_tree.hier}.")

        return base_tree

if __name__ == "__main__":
    def hier_func(line: str) -> int:
        if line.lower() in all_days_lower:
            return 1
        if line.lower() in ("lunch", "dinner"):
            return 2
        elif line.lower() == "skip":
            return -1
        else:
            return 3

    test_str = """Monday
    Lunch
    Cauliflower
    Broccoli
    Dinner
    Shrimp
    Chicken
    Tuesday
    Lunch
    Cashews
    Fruit
    Dinner
    Barbecue
    Skip
    Wednesday
    Lunch
    Squid"""

    t = Tree.from_list([x.strip() for x in test_str.split("\n")], hier_func)