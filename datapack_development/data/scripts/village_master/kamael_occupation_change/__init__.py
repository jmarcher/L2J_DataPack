# Created by DrLecter for the L2J Official Datapack Project
# Visit us at http://www.l2jdp.com/
# See readme-dp.txt and gpl.txt for license and distribution details
# Let us know if you did not receive a copy of such files.
import sys

from net.sf.l2j.gameserver.model.quest        import State
from net.sf.l2j.gameserver.model.quest        import QuestState
from net.sf.l2j.gameserver.model.quest.jython import QuestJython as JQuest

qn = "kamael_occupation_change"

GWAINS_RECOMMENTADION = 9753
ORKURUS_RECOMMENDATION = 9760
STEELRAZOR_EVALUATION = 9772
KAMAEL_INQUISITOR_MARK = 9782
#MAYNARD,KHADAVA,GERSHWIN,VALPOR,HOLST,CASCA,BROME,ZENYA,AETONIC,BARTA,
#MIYA,VITUS,LIANE,EDDY,FERDINAND,TAINE,RUPAUL,MELDINA,HAGEL,CECI,
#PIECHE,ZOLDART,NIZER,YENICHE
NPCS=[32145,32202,32196,32146,32199,32139,32221,32140,32205,32217,\
      32218,32213,32222,32210,32209,32225,32226,32214,32229,32230,\
      32206,32233,32234,32193]
#Filenames are made with the lowest npcId from the NPCs list. Some scripts
#contain generic dialogs for every npc to use, some others keep separate
#dialogs for different npcs.
preffix="32139"
#event:[newclass,req_class,req_race,low_ni,low_i,ok_ni,ok_i,[req_items]]
#low_ni : level too low, and you dont have quest item
#low_i: level too low, despite you have the item
#ok_ni: level ok, but you don't have quest item
#ok_i: level ok, you got quest item, class change takes place
CLASSES = {
    "DR":[125,123,5,20,"16","17","18","19",[GWAINS_RECOMMENTADION]],#m_kamael -> m_dragoon
    "WA":[126,124,5,20,"20","21","22","23",[STEELRAZOR_EVALUATION]], #f_kamael -> f_warder
    "BE":[127,125,5,40,"24","25","26","27",[ORKURUS_RECOMMENDATION]], #m_dragoon -> m_berserker
    "AR":[130,126,5,40,"28","29","30","31",[KAMAEL_INQUISITOR_MARK]], #f_warder -> f_arbalester
    }
#Messages
default = "No Quest"

def change(st,player,newclass,items) :
   for item in items :
      st.takeItems(item,1)
   st.playSound("ItemSound.quest_fanfare_2")
   player.setClassId(newclass)
   player.setBaseClass(newclass)
   player.broadcastUserInfo()
   return

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onAdvEvent (self,event,npc,player) :
   npcId    = npc.getNpcId()
   htmltext = default
   suffix = ''
   st = player.getQuestState(qn)
   if not st : return
   race     = player.getRace().ordinal()
   classid  = player.getClassId().getId()
   level    = player.getLevel()
   if npcId not in NPCS : return
   if not event in CLASSES.keys() :
     return event
   else :
     newclass,req_class,req_race,req_level,low_ni,low_i,ok_ni,ok_i,req_item=CLASSES[event]
     if race == req_race and classid == req_class :
        item = True
        for i in req_item :
            if not st.getQuestItemsCount(i):
               item = False
        if level < req_level :
           suffix = low_i
           if not item :
              suffix = low_ni
        else :
           if not item :
              suffix = ok_ni
           else :
              suffix = ok_i
              change(st,player,newclass,req_item)
     st.exitQuest(1)
     htmltext = preffix+"-"+suffix+".htm"
   return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   npcId = npc.getNpcId()
   race = player.getRace().ordinal()
   classId = player.getClassId()
   id = classId.getId()
   htmltext = default
   if player.isSubClassActive() :
      st.exitQuest(1)
      return htmltext
   # Kamaels only
   if npcId in NPCS :
     htmltext = preffix
     if race in [5] :
       if id == 123 :      # m_fighter
         return htmltext+"-01.htm"
       elif id == 124 :    # f_fighter
         return htmltext+"-05.htm"
       elif id == 125 :    # m_dragoon
         return htmltext+"-09.htm"
       elif id == 126 :    # f_warder
         return htmltext+"-13.htm"
       elif classId.level() >= 2 : # second/third occupation change already made
         htmltext += "-32.htm"
     else :
       htmltext += "-33.htm"  # other races
   st.exitQuest(1)
   return htmltext

QUEST   = Quest(99990,qn,"village_master")
CREATED = State('Start', QUEST)

QUEST.setInitialState(CREATED)

for npc in NPCS :
    QUEST.addStartNpc(npc)
    QUEST.addTalkId(npc)
