from mcpi.minecraft import Minecraft as M
import mcpi.block as block
import time
import mcpi.block as blk

mc = M.create(address="127.0.0.1")
mc.postTochat("小坤坤吉林还")
x,y,z = mc.player.getTilePos()
while True:
    pos = mc.player.getTilePos()
    x,y,z = pos.x,pos.y,pos.z
    print(x,y,z)
    blockInfo = mc.getBlock(x,y-1,z)
    print(blockInfo)
    blockDataInfo = mc.getBlockWithData(x,y-1,z)
    print(blockDataInfo)
    blockNBTInfo = mc.getBlockWithNBT(x,y-1,z)
    print(blockNBTInfo)
    time.sleep(1)
    
# mc.player.setTilePos(x+200,y+10,z)
# def buildcube(x,y,z):
#     mc.setBlock(x,y,z,x+5,y+5,z+5,blk.STONE.id)
#     mc.setBlock(x+1,y+1,z+1,x+4,y+4,z+4,blk.AIR.id)
# n=1
# m=0
# mc.player.setTilePos(x+2,y+100,z)
# mc.postToChat("小坤坤季临海")
# import time
# while (n<=100):
    # time.sleep(1)
    # mc.player.setTilePos(x+200,y+100,z)
    # pos = mc.player.getPos()
    # buildcube(pos.x,pos.y,pos.z)
    # mc.postToChat(pos.x)
    # mc.postToChat(pos.y)
    # mc.postToChat(pos.z)
    # i=0
    # j=0
    # k=0
    # while(i<=100):
    #     while(j<=80):
    #         while(k<=20):
    #             mc.setBlock(x+j,y+i,z+k,blk.STONE.id)
    #             k+=1
    #         j+=1
    #     i+=1
    # n+=1
    
