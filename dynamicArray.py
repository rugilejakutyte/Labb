import sys

class Node:
    __slots__ = ("left", "right", "value")
    def __init__(self, left=0, right=0, value=0):
        self.left = left
        self.right = right
        self.value = value

class PersistentArray:
    H = 31  # index upp till 2^31-1

    def __init__(self):
        self.pool = [Node()]  # 0 = nollnod

    def _new_node(self, left, right, value):
        self.pool.append(Node(left, right, value))
        return len(self.pool) - 1

    def newarray(self) -> int:
        return 0

    def get(self, root: int, i: int) -> int:
        index = root
        for bit in range(self.H - 1, -1, -1):
            if index == 0:
                return 0
            b = (i >> bit) & 1
            index = self.pool[index].right if b else self.pool[index].left
        return 0 if index == 0 else self.pool[index].value

    def set(self, root: int, i: int, value: int) -> int:
        def set_rec(node_id: int, bit: int) -> int:
            if bit < 0:
                return self._new_node(0, 0, value)

            left_id  = self.pool[node_id].left  if node_id != 0 else 0
            right_id = self.pool[node_id].right if node_id != 0 else 0

            if ((i >> bit) & 1) == 0:
                new_left = set_rec(left_id, bit - 1)
                return self._new_node(new_left, right_id, 0)
            else:
                new_right = set_rec(right_id, bit - 1)
                return self._new_node(left_id, new_right, 0)

        return set_rec(root, self.H - 1)

class Versions:
    def __init__(self, pa: PersistentArray):
        self.pa = pa
        self.roots = []

    def new(self) -> int:
        r = self.pa.newarray()
        self.roots.append(r)
        return len(self.roots) - 1

    def set(self, ver: int, i: int, val: int) -> int:
        r_new = self.pa.set(self.roots[ver], i, val)
        self.roots.append(r_new)
        return len(self.roots) - 1

    def get(self, ver: int, i: int) -> int:
        return self.pa.get(self.roots[ver], i)

def main():
    pa = PersistentArray()
    vs = Versions(pa)

    data = sys.stdin.read().strip().split()
    if not data:
        # Liten demo om man kör utan input
        v0 = vs.new()                      # tom array → v0
        v1 = vs.set(v0, 1, 8)              # b[1]=8     → v1
        v2 = vs.set(v1, 3, 1)              # b[3]=1     → v2
        v3 = vs.set(v2, 4, 13)             # b[4]=13    → v3
        v4 = vs.set(v3, 5, 12)             # b[5]=12    → v4
        v5 = vs.set(v4, 8, 24)             # b[8]=24    → v5
        # Läsningar
        print(v0, v1, v2, v3, v4, v5)      # versions-id
        print(vs.get(v5, 4))               # 13
        print(vs.get(v5, 10))              # 0
        print(vs.get(v3, 8))               # 0
        return

    it = iter(data)
    out_lines = []
    for token in it:
        if token == "new":
            out_lines.append(str(vs.new()))
        elif token == "set":
            A = int(next(it)); i = int(next(it)); val = int(next(it))
            out_lines.append(str(vs.set(A, i, val)))
        elif token == "get":
            A = int(next(it)); i = int(next(it))
            out_lines.append(str(vs.get(A, i)))
        else:
            # Ignorera/hantera okända kommandon
            pass
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
