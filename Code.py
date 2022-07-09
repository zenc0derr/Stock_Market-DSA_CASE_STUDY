import requests
from bs4 import BeautifulSoup

class Stock:
    def __init__(self, comp, pri):
        self.company = comp
        self.price = pri
        self.left = None
        self.right = None
        self.height = 1

class AVL_Tree(object):
    def __init__(self):
        self.inArray = []

    def insert(self, root, key):
        if not root:
            return Stock(key.company, key.price)
        elif key.price < root.price:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        balance = self.getBalance(root)
        if balance > 1 and key.price < root.left.price:
            return self.rightRotate(root)
        if balance < -1 and key.price > root.right.price:
            return self.leftRotate(root)
        # Case 3 - Left Right
        if balance > 1 and key.price > root.left.price:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and key.price < root.right.price:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)


    def inOrder(self, root):
        if not root:
            return
        self.inOrder(root.left)
        # print(root.company, " - ", root.price)
        self.inArray.append([root.company, root.price])
        self.inOrder(root.right)

class Max_Heap:
    def __init__(self, arr=[]):
        self._heap = []

        if arr is not None:
            for root in arr:
                self.push(root)

    def push(self, value):
        self._heap.append(value)
        _bottom_up(self._heap, len(self) - 1)
    def pop(self):
        if len(self._heap) != 0:
            _swap(self._heap, len(self) - 1, 0)
            root = self._heap.pop()
            _top_down(self._heap, 0)

        else:
            root = "Heap is empty"
        return root
    def __len__(self):
        return len(self._heap)
    def peek(self):
        if len(self._heap) != 0:
            return (self._heap[0])
        else:
            return ("heap is empty")

def _swap(L, i, j):
    L[i], L[j] = L[j], L[i]

def _bottom_up(heap, index):
    root_index = (index - 1) // 2
    if root_index < 0:
        return


    if heap[index].price > heap[root_index].price:
        _swap(heap, index, root_index)
        _bottom_up(heap, root_index)

def _top_down(heap, index):
    child_index = 2 * index + 1
    if child_index >= len(heap):
        return

    if child_index + 1 < len(heap) and heap[child_index].price < heap[child_index + 1].price:
        child_index += 1

    if heap[child_index].price > heap[index].price:
        _swap(heap, child_index, index)
        _top_down(heap, child_index)

#Web Scraping
r = requests.get('https://economictimes.indiatimes.com/markets/indexsummary/indexid-2346,exchange-50.cms')
soup = BeautifulSoup(r.content, 'html.parser')
price = soup.find_all("span", class_="ltp")
company = soup.find_all("p", class_="flt w120")


stk = []
for i in range(0, len(price)):
    y = float(price[i].get_text())
    a = Stock(company[i].get_text(), y)
    stk.append(a)

class HashTable:
    def __init__(self):
        self.arr = [{} for i in range(0,10)]

    def get_hash(self, key):
        h = ord(key[0])
        h = h%10
        return h


    def add(self, key, val):
        h = self.get_hash(key)
        temp = self.arr[h]
        temp[key] = val

    def get(self, key):
        h = self.get_hash(key)
        if self.arr[h].keys():
            wtf = self.arr[h]
            return wtf[key]

    def exist(self,key):
        h = self.get_hash(key)
        d = self.arr[h]
        if key in d:
            return True




def main():
    t = HashTable()
    t.add("Susan", "2003")
    t.add("Kyle", "2002")
    t.add("Charolette", "2004")
    t.add("Rob", "1254")

    while (1):
        print("LOGIN")
        print("-----")
        usn = input("Username:")
        pwd = input("Password:")
        check = t.get(usn)
        e = t.exist(usn)
        if (check == pwd):
            print("\nHELLO THERE!!", usn)
            print("")
            print("Today's stock prices:")
            print("---------------------")
            for i in range(0, len(stk)):
                print(i + 1, ") ", stk[i].company, "- ₹", stk[i].price)

            print("\n\n")
            myTree = AVL_Tree()
            root = None

            col = []
            for i in range(0, len(stk)):
                col.append(stk[i])

            for i in range(0, len(col)):
                root = myTree.insert(root, col[i])
            temp = []

            print("Press \n1 - to sort the stock price in low-high\n2 - Today's low\n3 - Today's High\n4 - Prioritize stocks")
            choice = int(input())
            while(choice != 0):
                if (choice == 1):
                    print("Stocks sorted in low - high order: ")
                    print("----------------------------------\n")
                    myTree.inOrder(root)

                    for i in range(0, len(myTree.inArray)):
                        for j in range(0, len(myTree.inArray[i]) - 1):
                            print(myTree.inArray[i][j], " - ₹", myTree.inArray[i][j + 1])
                elif (choice == 2):
                    myTree.inOrder(root)
                    print("Today's Low: ", myTree.inArray[0][0], " - ₹", myTree.inArray[0][1])
                elif (choice == 3):
                    myTree.inOrder(root)
                    print("Today's High:", myTree.inArray[-1][-2], " - ₹", myTree.inArray[-1][-1])
                elif (choice == 4):
                    print("Add stocks to watchlist:")
                    id_set = []
                    stock_queue = []
                    while (1):

                        id = int(input())

                        if (id == 0):
                            break
                        id_set.append(id)

                        stock_queue.append(stk[id - 1])


                    maxHeap = Max_Heap(stock_queue)
                    print("Your Watchlist:")
                    print("----------")
                    for i in range(0, len(id_set)):
                        y = maxHeap.pop()
                        print(y.company, " - ₹", y.price)

                    break
                choice = int(input())

            break
        elif((check != pwd) and (e != True)):
            print("Create Account")
            user = input("Username:")
            pwd = input("Password:")
            t.add(user, pwd)
            print("Registration successful!")
            continue
        elif(check != pwd and e==True):
            print("Invalid password")
            continue


main()