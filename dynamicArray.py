import sys

class Node:
    __slots__ = ("left", "right", "value") # alla får dessa tre,
    def __init__(self, left=0, right=0, value=0):
        self.left = left #pekare till vänsta barnet
        self.right = right #perkare högra barnet
        self.value = value #värde (i blad)

class PersistentArray:
    H = 31  # index upp till 2^31-1

    def __init__(self):
        self.all_nodes = [Node()]  # 0 = nollnod

    def new_node(self, left, right, value): #skapar ny nod
        self.all_nodes.append(Node(left, right, value))
        return len(self.all_nodes) - 1

    def newarray(self) -> int: #Roten är nollnoden
        return 0

    def get(self, root: int, i: int) -> int: #hämtar värdet på plats i i arrayen som börjar vid root
        index = root 
        for bit in range(self.H - 1, -1, -1): #går från bit 30 till 0
            if index == 0:
                return 0 #om tom gren
            b = (i >> bit) & 1 #Väljer ut en bit, 0 vänster 1 höger
            index = self.all_nodes[index].right if b else self.all_nodes[index].left #Flyttar trädet till rätt barn
        return 0 if index == 0 else self.all_nodes[index].value #returnerar value på bladet

    #Bygger en ny gren från roten till bladet, alla andra grenar består samma
    def set(self, root: int, i: int, value: int) -> int: #Sätter värdet på index i
        def set_rec(current_index: int, bit: int) -> int: #rekursiv hjälp
            if bit < 0:
                return self.new_node(0, 0, value) #nytt blad
            # Om vi inte är på nollnoden, hämta höger vänster barn
            left_id  = self.all_nodes[current_index].left  if current_index != 0 else 0 
            right_id = self.all_nodes[current_index].right if current_index != 0 else 0

            if ((i >> bit) & 1) == 0:
                new_left = set_rec(left_id, bit - 1)
                return self.new_node(new_left, right_id, 0)
            else:
                new_right = set_rec(right_id, bit - 1)
                return self.new_node(left_id, new_right, 0)

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

    current_ver = vs.new()

    #data = sys.stdin.read().strip().split()
    #if not data:
    #    v0 = vs.new()                      # tom array → v0
    #    v1 = vs.set(v0, 1, 8)              # b[1]=8     → v1
    #    v2 = vs.set(v1, 3, 1)              # b[3]=1     → v2
    #    v3 = vs.set(v2, 4, 13)             # b[4]=13    → v3
    #    v4 = vs.set(v3, 5, 12)             # b[5]=12    → v4
    #    v5 = vs.set(v4, 8, 24)             # b[8]=24    → v5
    #    # Läsningar
    #    print(v0, v1, v2, v3, v4, v5)      # versions-id
    #    print(vs.get(v5, 4))               # 13
    #    print(vs.get(v5, 10))              # 0
    #    print(vs.get(v3, 8))               # 0
    #    return
#
    #it = iter(data)
    out_lines = []
    for line in sys.stdin:
        parts = line.strip().split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "set":
            i = int(parts[1])
            val = int(parts[2])
            current_ver = vs.set(current_ver, i, val)
        elif cmd == "get":
            i = int(parts[1])
            out_lines.append(str(vs.get(current_ver, i)))
        elif cmd == "unset":
            # Ta bort senaste versionen
            if len(vs.roots) > 1:
                vs.roots.pop()
                current_ver = len(vs.roots) - 1  #indexet till senaste versionen


    sys.stdout.write("\n".join(out_lines) + "\n")

if __name__ == "__main__":
    main()

