import numpy as np
import boundaryHelper as bh
import math 
import sys,getopt


def main(argv):
    Lx, Ly, Lz, gap, radius = None, None, None, None, None
    try:
        opts, args = getopt.getopt(argv, "x:y:z:g:r", ["Lx=","Ly=","Lz=","gap=", "radius="])
    except getopt.GetoptError:
        print ('boundryCreator.py --Lx <Lx> --Ly <Ly> --Lz <Lz> --gap <gap> --radius <radius>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('boundryCreator.py --Lx <Lx> --Ly <Ly> --Lz <Lz> --gap <gap> --radius <radius>')
            sys.exit()
        elif opt in ("-x","--Lx"):
            Lx = int(arg)
        elif opt in ("-y","--Ly"):
            Ly = int(arg)
        elif opt in ("-z","--Lz"):
            Lz = int(arg)
        elif opt in ("-g","--gap"):
            gap = int(arg)
        elif opt in ("-r","--radius"):
            radius=int(arg)

    if None in (Lx, Ly, Lz, gap, radius):
        print("Error: Missing required arguments.")
        print('Usage: boundaryCreator.py -x <Lx> -y <Ly> -z <Lz> -g <gap> -r <radius>')
        sys.exit()
    print(f"Debug Info: Lx={Lx}, Ly={Ly}, Lz={Lz}, gap={gap}, radius={radius}") 
    
    if radius*2+gap!=Lx or Lx!=Ly:
        print("Input error! Please check your data!")
        sys.exit()

    
    return Lx, Ly, Lz, gap, radius

Lx, Ly, Lz, gap, radius = main(sys.argv[1:])


interval = 10 #nm


Lx = Lx/interval
Ly = Ly/interval
Lz = Lz/interval
gap = gap / interval
radius = radius/interval
height =140/interval



period = Lx

[A,B,C,L,Ws,E]=[-0.172e6,-2.12e6,1.73e6,6e-12/(interval*1e-9)**2,1/(9*0.53**2)*1e-3/(interval*1e-9),5e6]#150V applied to 30um

A, B, C, L, Ws = [x / abs(A) for x in [A, B, C, L, Ws]]
# E=E*math.sqrt(8.854e-12/1.72e5)

# print("[A,B,C,L,Ws,E]"+[A,B,C,L,Ws])
# print("~E="+E)
sc = bh.Scene(Lx, Ly, Lz)
ac = bh.OrientedAnchoringCondition(strength=Ws, S0=1)

bo = bh.BoundaryObject(ac)

Cx, Cy = np.array([(Lx-1)/2, (Ly-1)/2]) # choose center of box as sphere center
Cz = (Lz-1)/2




# 创建圆柱的顶部
top_wall = bh.Wall(ac, normal="z", height=height)

# 修改顶部边界函数以仅在圆柱内部
def capped_cylinder_member_func(X, Y, Z):
    return (np.sqrt((X - ( period-1)/2)**2 + (Y - (period-1)/2)**2) < radius**2) & (Z == height+1)

def cylinderinfinite_member_func(X, Y, Z):
    return (np.sqrt((X - ( period-1)/2)**2 + (Y - ( period-1)/2)**2) < radius**2) & (Z <= height)
# 用新的成员函数替换顶部墙的成员函数
top_wall.wall_member_func = capped_cylinder_member_func
# cylindrical_capillary.member_func = cylinderinfinite_member_func


cylin = bh.CylindricalCapillary(ac,radius=radius,period=period,height=height)
lid = bh.Lid(ac,"z",radius=radius,height=height+1,Cx=Cx)
anch1= bh.OrientedAnchoringCondition(strength=Ws, S0=1)
anch2 = bh.DegeneratePlanarAnchoringCondition(strength=Ws, S0=0.53)

wall1 = bh.Wall(anch1, "z", 0) # normal to x, positioned at x=5
wall2 = bh.Wall(anch1,"z",Lz-1)

sc.boundary_objects = [cylin,wall1,lid]
# ,wall1,wall2,top_wall

sc.to_file(f'/gpfs/home/mc10709/ldg/boundryfiles/gap{gap:.0f}_radius{radius}.txt')
#sc.to_file(f'./gap{gap:.0f}_radius{radius:.0f}.txt')
