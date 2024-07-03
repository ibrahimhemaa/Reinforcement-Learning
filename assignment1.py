import math
class Environment:
    #equation of V(a)=max(reward,Discount_Factor*prev_state*(1-Gamma))
    def __init__(self,shape_array,position_one,position_neg_one,position_wall):
        self.shape_array=shape_array
        self.position_one=position_one
        self.position_neg_one=position_neg_one
        self.position_wall=position_wall
        self.grid=[[0 for j in range(self.shape_array[1])]for _ in range(self.shape_array[0])] # set all zeros
        self.direction=[(1, 0), (0, -1), (-1, 0), (0, 1)] # Down, Left, Up, Right
        self.noise,self.Discount_factor,self.num_of_iteration=.2,.9,100
        self.wall=math.nan
        self.grid[position_one[0]][position_one[1]] = 1
        self.grid[position_neg_one[0]][position_neg_one[1]] = -1
        self.grid[position_wall[0]][position_wall[1]]=self.wall
        self.dir = [["Down" for j in range(self.shape_array[1])] for i in range(self.shape_array[0])]# Initialize all dir down
        self.dir[self.position_one[0]][self.position_one[1]] = 1
        self.dir[self.position_neg_one[0]][self.position_neg_one[1]] = -1
        self.dir[self.position_wall[0]][self.position_wall[1]] = self.wall
        self.action=["Down","Left","Up","Right"] # all valid dir
        print("the initial of grid")
        [print(i) for i in self.grid]
        print("\n")
    def is_valid(self,x,y):
        return x>=0 and x<3 and y>=0 and y<4 and (x,y)!=(1,1)
    
    def rec(self,i,j,trans):
        x,y=self.direction[trans]
        dx=x+i
        dy=y+j
        if(self.is_valid(dx,dy)):
            return self.grid[dx][dy]
        else:
            return self.grid[i][j]

    def calc(self,i,j,trans):
        res=0
        res+=(self.noise/2)*self.Discount_factor*self.rec(i,j,(trans-1)%4)
        res+=(1-self.noise)*self.Discount_factor*self.rec(i,j,trans)
        res+=(self.noise/2)*self.Discount_factor*self.rec(i,j,(trans+1)%4)
        return res

    def build(self):
        print("During iteration\n")
        while(self.num_of_iteration>0):
            print(f"iteration number {100-self.num_of_iteration+1}\n")
            self.num_of_iteration-=1
            grid_edit = [[0 for i in range(self.shape_array[1])]for j in range(self.shape_array[0])]
            grid_edit[self.position_one[0]][self.position_one[1]],grid_edit[self.position_neg_one[0]][self.position_neg_one[1]],grid_edit[self.position_wall[0]][self.position_wall[1]]=self.grid[self.position_one[0]][self.position_one[1]],self.grid[self.position_neg_one[0]][self.position_neg_one[1]],self.grid[self.position_wall[0]][self.position_wall[1]]
            for i in range(self.shape_array[0]):
                for j in range(self.shape_array[1]):
                    if((i<=1 and j==3) or (i==j==1)):
                        continue
                    grid_edit[i][j] = max([self.calc(i, j, action) for action in range(len(self.dir))]) # Bellman update
            self.grid=grid_edit
            
            [print(i) for i in self.grid]
            print('\n')
    def get_path(self):
        for i in range(self.shape_array[0]):
            for j in range(self.shape_array[1]):
                if((i<=1 and j==3) or (i==j==1)):
                        continue
                mn_dis=0
                for k in range(len(self.direction)):
                    x,y=self.direction[k]
                    if(self.is_valid(i+x,j+y) and self.grid[i+x][j+y]>self.grid[i][j]):
                        mn=self.grid[i+x][j+y]-self.grid[i][j]
                        if(mn>mn_dis):
                            mn_dis=mn
                            self.dir[i][j]=self.action[k]
        [print(i) for i in self.dir]
print("enter shape of grid: ")
row,col=map(int, input().split())
print("enter position one in the grid :")
pos_x_one,pos_y_one=map(int, input().split())
print("enter position negative one in the grid :")
pos_x_neg_one,pos_y_neg_one=map(int, input().split())
print("enter position wall in the grid :")
pos_x_wall,pos_y_wall=map(int, input().split())
en=Environment([row,col],[pos_x_one,pos_y_one],[pos_x_neg_one,pos_y_neg_one],[pos_x_wall,pos_y_wall])
en.build()
en.get_path()
